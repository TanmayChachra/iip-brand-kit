// Home page behaviour. Everything works without it: the size list is plain links, the drawing shows every plot, the hours are text.
(function () {
  var q = function (s) { return document.querySelector(s); };
  // 1. Open now (Asia/Kolkata). Hours: 8 am to 8 pm every day except Tuesday.
  var el = q('[data-open-now]');
  if (el) {
    try {
      var parts = {};
      new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Kolkata', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date()).forEach(function (p) { parts[p.type] = p.value; });
      var mins = (+parts.hour) * 60 + (+parts.minute), day = parts.weekday, open = day !== 'Tue' && mins >= 480 && mins < 1200, msg;
      if (open) msg = 'Open now, until 8 pm';
      else if (day === 'Tue') msg = 'Closed today, opens Wednesday at 8 am';
      else if (mins < 480) msg = 'Closed now, opens today at 8 am';
      else msg = day === 'Mon' ? 'Closed now, opens Wednesday at 8 am' : 'Closed now, opens tomorrow at 8 am';
      el.textContent = msg;
      el.parentNode.classList.toggle('is-closed', !open);
    } catch (e) { /* keep the static text */ }
  }
  // 2. Plot size finder: chips light up the plots of that size band on the layout drawing.
  var lay = q('.lay'), out = q('#find-out'), ask = q('#find-ask'), chips = [].slice.call(document.querySelectorAll('[data-band]')), cur = '';
  if (!lay || !out || !chips.length) return;
  var base = out.innerHTML;
  function pick(c) {
    var b = c && c.getAttribute('data-band') !== cur ? c.getAttribute('data-band') : '';
    cur = b;
    chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c && b ? 'true' : 'false'); });
    if (b) {
      lay.setAttribute('data-sel', b);
      out.innerHTML = '<b>' + c.getAttribute('data-n') + ' plots</b> in this size in the layout<small>Sizes from the architect drawing. This is not a list of what is available.</small>';
      ask.href = c.getAttribute('data-wa'); ask.hidden = false;
    } else {
      lay.removeAttribute('data-sel'); out.innerHTML = base; ask.hidden = true;
    }
  }
  chips.forEach(function (c) {
    c.setAttribute('role', 'button'); c.setAttribute('aria-pressed', 'false');
    c.addEventListener('click', function (e) { e.preventDefault(); pick(c); });
    c.addEventListener('keydown', function (e) { if (e.key === ' ') { e.preventDefault(); pick(c); } });
  });
})();
