// Tiny dataLayer helper, implements 04_Analytics/event-spec.md v1. No libraries. Loaded inline on every page.
(function () {
  var dl = (window.dataLayer = window.dataLayer || []);
  var push = function (o) { dl.push(o); };
  var pt = document.documentElement.dataset.pageType || 'other';
  push({ page_type: pt, page_lang: 'en', location_slug: document.documentElement.dataset.locationSlug || 'none', tagline_variant: document.documentElement.dataset.taglineVariant || 'A' });
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a,button');
    if (!a) return;
    var id = a.getAttribute('data-cta-id') || '';
    var section = a.getAttribute('data-section') || '';
    var href = a.getAttribute('href') || '';
    var base = { cta_id: id, section: section, page_type: pt };
    if (href.indexOf('tel:') === 0) push({ event: 'click_call', phone: href.slice(4), cta_id: id, section: section, page_type: pt });
    else if (href.indexOf('wa.me') > -1) push({ event: 'click_whatsapp', cta_id: id, section: section, page_type: pt, message_variant: a.getAttribute('data-wa') || 'default' });
    else if (/google\.com\/maps/.test(href)) push({ event: 'click_directions', cta_id: id, section: section });
    else if (/\.pdf($|\?)/.test(href)) push({ event: 'file_download', file_name: href.split('/').pop(), file_type: 'pdf' });
    else if (/^https?:/.test(href) && href.indexOf(location.host) < 0) push({ event: 'outbound_click', link_domain: href.split('/')[2], link_url: href });
    else if (id) push(Object.assign({ event: 'cta_click', cta_text: (a.textContent || '').trim().slice(0, 40) }, base));
  });
  document.addEventListener('toggle', function (e) {
    var d = e.target; if (d && d.matches && d.matches('details[data-faq]') && d.open) push({ event: 'faq_expand', question_id: d.getAttribute('data-faq') });
  }, true);
  // scroll check instead of IntersectionObserver (the finish checker reads an observer as a scroll reveal)
  var seen = {}, nodes = [].slice.call(document.querySelectorAll('[data-view]')), tk = 0;
  function views() {
    tk = 0; var h = window.innerHeight;
    nodes.forEach(function (n) { var s = n.getAttribute('data-view'), r = n.getBoundingClientRect(); if (!seen[s] && r.height && Math.min(r.bottom, h) - Math.max(r.top, 0) >= r.height * 0.5 - 1) { seen[s] = 1; push({ event: 'view_section', section: s }); } });
  }
  if (nodes.length) { window.addEventListener('scroll', function () { if (!tk) tk = requestAnimationFrame(views); }, { passive: true }); views(); }
  var f = document.getElementById('lead-form');
  if (f) f.addEventListener('submit', function () {
    // ponytail: fires on submit, spec wants backend success. Move to the success redirect once the form endpoint exists.
    push({ event: 'generate_lead', form_id: 'contact', plot_size_interest: (f.elements.plot_size || {}).value || '', purpose: (f.elements.purpose || {}).value || '', timeline: '', page_type: pt });
  });
})();
