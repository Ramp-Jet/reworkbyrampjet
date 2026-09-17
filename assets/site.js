/* Ramp/Jet shared script.
   Email addresses are assembled at runtime so they never appear as a
   harvestable string in the HTML source. Markup carries the parts:
     <a class="mail" data-u="joseph" data-d="rampjet.ai" href="/#book">email us</a>
   Without JS the link still goes somewhere useful; with JS it becomes a
   real mailto and shows the address. */
(function () {
  function decode() {
    var links = document.querySelectorAll('a.mail');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var u = a.getAttribute('data-u'), d = a.getAttribute('data-d');
      if (!u || !d) continue;
      var addr = u + String.fromCharCode(64) + d;
      a.setAttribute('href', 'mai' + 'lto:' + addr);
      if (a.getAttribute('data-show') !== 'no') a.textContent = addr;
      a.removeAttribute('data-u');
      a.removeAttribute('data-d');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', decode);
  } else {
    decode();
  }
})();
