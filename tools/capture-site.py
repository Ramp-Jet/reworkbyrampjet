#!/usr/bin/env python3
"""Capture a full-page screenshot of a website, for the before/after panes.

Drives headless Chrome over the DevTools Protocol and stitches viewport-sized
tiles together. Tiles rather than one tall capture, because Chrome's
`captureBeyondViewport` does not composite video or fixed backgrounds — a
hero video comes out as a blank rectangle, and a `100vh` hero stretches to
fill the whole page height.

Requires Chrome and Pillow. Everything else is stdlib; the script only talks
to Chrome on localhost, so it needs no TLS support of its own.

    python3 tools/capture-site.py https://www.flextram.com/ \
        --out img/after-flextram-full --video-time 35.6 --hide .calc-toast

For an archived page, use the Wayback `if_` suffix so the archive's own
toolbar and donation banner are not baked into the screenshot:

    .../web/20240907221802if_/https://www.flextram.com/
"""

import argparse
import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]


def find_chrome():
    for path in CHROME_CANDIDATES:
        if path and os.path.exists(path):
            return path
    sys.exit("Could not find Chrome. Set --chrome to its path.")


class WS:
    """Minimal WebSocket client — just enough to speak CDP."""

    def __init__(self, url):
        rest = url[len("ws://"):]
        hostport, _, path = rest.partition("/")
        host, _, port = hostport.partition(":")
        self.sock = socket.create_connection((host, int(port or 80)))
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall(
            f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\n"
            f"Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
            .encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.sock.recv(4096)
        if b"101" not in buf.split(b"\r\n")[0]:
            raise RuntimeError(f"WebSocket upgrade refused: {buf[:120]!r}")
        self.buf = buf.split(b"\r\n\r\n", 1)[1]
        self.next_id = 0

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(1 << 20)
            if not chunk:
                raise EOFError("Chrome closed the connection")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def call(self, method, params=None, timeout=120):
        self.next_id += 1
        mid = self.next_id
        payload = json.dumps(
            {"id": mid, "method": method, "params": params or {}}).encode()
        n = len(payload)
        header = b"\x81"
        if n < 126:
            header += struct.pack("!B", 0x80 | n)
        elif n < 65536:
            header += struct.pack("!BH", 0x80 | 126, n)
        else:
            header += struct.pack("!BQ", 0x80 | 127, n)
        mask = os.urandom(4)
        self.sock.sendall(header + mask + bytes(
            b ^ mask[i % 4] for i, b in enumerate(payload)))

        deadline = time.time() + timeout
        while time.time() < deadline:
            _, b1 = self._read(2)
            size = b1 & 0x7F
            if size == 126:
                size = struct.unpack("!H", self._read(2))[0]
            elif size == 127:
                size = struct.unpack("!Q", self._read(8))[0]
            msg = json.loads(self._read(size))
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
        raise TimeoutError(method)

    def eval(self, expression, await_promise=False, timeout=120):
        result = self.call("Runtime.evaluate", {
            "expression": expression, "returnByValue": True,
            "awaitPromise": await_promise}, timeout=timeout)
        return result.get("result", {}).get("value")


# Wait for images that are actually on screen, so a tile is never shot
# half-loaded. Capped, because a stalled request should not hang the run.
SETTLE_IMAGES = """
(async()=>{
  const inView=[...document.images].filter(i=>{
    const r=i.getBoundingClientRect();
    return r.bottom>-200 && r.top<innerHeight+200;
  });
  await Promise.race([
    Promise.all(inView.map(i=>i.complete?0:new Promise(r=>{i.onload=r;i.onerror=r}))),
    new Promise(r=>setTimeout(r,4000))
  ]);
  await new Promise(r=>setTimeout(r,%d));
})()
"""

# Sticky and fixed chrome would otherwise repeat in every tile down the page.
HIDE_STICKY = """
(()=>{let n=0;document.querySelectorAll('body *').forEach(e=>{
  const p=getComputedStyle(e).position;
  if(p==='fixed'||p==='sticky'){e.style.setProperty('visibility','hidden','important');n++}
});return n})()
"""

# Hold a background video on a chosen frame. Paused-and-seeked composites
# correctly in a viewport capture; whatever frame playback happens to be on
# when the shutter falls usually does not read well at pane size.
SEEK_VIDEO = """
(async()=>{
  const v=document.querySelector('video');
  if(!v) return 'no video on page';
  v.pause();
  if(v.readyState<1){
    await new Promise(r=>{v.addEventListener('loadedmetadata',r,{once:true});
                          setTimeout(r,8000)});
  }
  v.currentTime=%f;
  await new Promise(r=>{v.addEventListener('seeked',r,{once:true});
                        setTimeout(r,8000)});
  v.pause();
  await new Promise(r=>setTimeout(r,600));
  return 'video held at '+v.currentTime.toFixed(2)+'s';
})()
"""


def launch(chrome, port, profile):
    proc = subprocess.Popen(
        [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--autoplay-policy=no-user-gesture-required", "--no-first-run",
         f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
         "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(80):
        try:
            targets = json.load(urllib.request.urlopen(
                f"http://127.0.0.1:{port}/json"))
            for t in targets:
                if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                    return proc, t["webSocketDebuggerUrl"]
        except Exception:
            pass
        time.sleep(0.4)
    proc.terminate()
    sys.exit("Chrome did not expose a debugging target.")


def capture(args):
    from PIL import Image

    chrome = args.chrome or find_chrome()
    width, height = (int(v) for v in args.viewport.lower().split("x"))
    profile = tempfile.mkdtemp(prefix="capture-site-")
    tiles_dir = tempfile.mkdtemp(prefix="capture-tiles-")
    proc, ws_url = launch(chrome, args.port, profile)

    try:
        ws = WS(ws_url)
        ws.call("Page.enable")
        ws.call("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height,
            "deviceScaleFactor": args.scale, "mobile": False})
        ws.call("Page.navigate", {"url": args.url})
        time.sleep(args.wait)

        for selector in args.hide:
            removed = ws.eval(
                f"(()=>{{const n=document.querySelectorAll({selector!r});"
                f"n.forEach(e=>e.remove());return n.length}})()")
            print(f"  removed {removed} x {selector}")

        if args.video_time is not None:
            print("  " + str(ws.eval(SEEK_VIDEO % args.video_time,
                                     await_promise=True)))

        page_h = ws.eval("document.documentElement.scrollHeight")
        print(f"  page height: {page_h}px")

        offsets, y = [], 0
        while y < page_h:
            offsets.append(min(y, max(0, page_h - height)))
            y += height
        offsets = sorted(set(offsets))

        shots = []
        for i, target_y in enumerate(offsets):
            ws.eval(f"window.scrollTo(0,{target_y})")
            time.sleep(0.4)
            ws.eval(SETTLE_IMAGES % args.settle, await_promise=True, timeout=60)
            # Only after the first tile: the top of the page is the one place
            # sticky chrome belongs, and scrolling at all can break a hero
            # video's compositing, so tile 0 is shot untouched.
            if i == 0:
                ws.eval(HIDE_STICKY)
            actual_y = ws.eval("window.scrollY")
            data = ws.call("Page.captureScreenshot", {"format": "png"},
                           timeout=90)["data"]
            path = os.path.join(tiles_dir, f"tile-{i:02d}.png")
            with open(path, "wb") as fh:
                fh.write(base64.b64decode(data))
            shots.append((path, actual_y))
            print(f"  tile {i + 1}/{len(offsets)} at y={actual_y}")

        canvas = Image.new(
            "RGB", (int(width * args.scale), int(page_h * args.scale)),
            (255, 255, 255))
        for path, y_at in shots:
            canvas.paste(Image.open(path).convert("RGB"),
                         (0, int(y_at * args.scale)))

        out_w = args.width
        out_h = round(canvas.height * out_w / canvas.width)
        final = canvas.resize((out_w, out_h), Image.LANCZOS)
        base = args.out
        os.makedirs(os.path.dirname(base) or ".", exist_ok=True)
        final.save(base + ".webp", quality=args.quality, method=6)
        final.save(base + ".jpg", quality=max(args.quality - 2, 1),
                   optimize=True, progressive=True)
        print(f"\nwrote {base}.webp and {base}.jpg  ({out_w}x{out_h})")
        print(f"remember to update width/height in the <img> tag: "
              f"width=\"{out_w}\" height=\"{out_h}\"")
    finally:
        proc.terminate()
        shutil.rmtree(profile, ignore_errors=True)
        shutil.rmtree(tiles_dir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(
        description="Full-page screenshot for the before/after panes.")
    ap.add_argument("url")
    ap.add_argument("--out", required=True,
                    help="output path without extension, e.g. img/after-site")
    ap.add_argument("--width", type=int, default=1200,
                    help="width of the written image (default 1200)")
    ap.add_argument("--viewport", default="1440x900",
                    help="browser viewport, WxH (default 1440x900)")
    ap.add_argument("--scale", type=float, default=2,
                    help="device pixel ratio to capture at (default 2)")
    ap.add_argument("--wait", type=float, default=20,
                    help="seconds to let the page settle after load")
    ap.add_argument("--settle", type=int, default=700,
                    help="extra ms to wait per tile after images load")
    ap.add_argument("--quality", type=int, default=80)
    ap.add_argument("--video-time", type=float, default=None,
                    help="hold the page's <video> at this timestamp, in seconds")
    ap.add_argument("--hide", action="append", default=[], metavar="SELECTOR",
                    help="remove matching elements before capture; repeatable")
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--port", type=int, default=9339)
    capture(ap.parse_args())


if __name__ == "__main__":
    main()
