// Inject minimal CSS for the welcome page and provide interactive behavior.
// This file is intentionally self-contained: it adds styles that used to be in
// an external stylesheet (as noted in templates/home.html) and wires up the
// buttons with accessible focus/keyboard behavior and a small animation.

(function () {
  'use strict';

  // CSS to inject. Keep selectors specific to avoid colliding with other pages.
  var css = "\
  :root { --bg:#0f1724; --card:#0b1220; --muted:rgba(255,255,255,0.65); --accent:#FF9168; }\
  html,body{height:100%;margin:0;font-family:Poppins,system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial;background:linear-gradient(180deg,#071025 0%, #081428 100%);color:#fff;-webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale;}\
  main.card{width:min(920px,94vw);margin:6vh auto;display:grid;grid-template-columns:1fr 220px;gap:28px;align-items:center;background:linear-gradient(180deg,rgba(255,255,255,0.03),rgba(255,255,255,0.02));padding:28px;border-radius:14px;box-shadow:0 8px 30px rgba(2,6,23,0.6);backdrop-filter: blur(6px);}\
  .brand{grid-column:1/-1;font-weight:700;font-size:22px;color:var(--accent);background:linear-gradient(90deg,rgba(255,255,255,0.06),transparent);padding:6px 10px;border-radius:8px;width:max-content} \
  .content h1{font-size:38px;margin:6px 0 6px 0} \
  .content .lead{color:var(--muted);margin-bottom:18px;max-width:62ch;line-height:1.45} \
  .actions{display:flex;gap:12px;margin-bottom:12px} \
  .btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 14px;border-radius:10px;font-weight:600;border:0;cursor:pointer;text-decoration:none;color:inherit} \
  .btn:focus{outline:3px solid rgba(255,145,104,0.18);outline-offset:3px} \
  .btn-primary{background:linear-gradient(180deg,var(--accent),#ff7b4f);color:#0b1220} \
  .btn-outline{background:transparent;border:1px solid rgba(255,255,255,0.06);color:var(--muted)} \
  .small{color:rgba(255,255,255,0.45);font-size:13px} \
  .illustration{justify-self:end;opacity:0.98} \
  @media (max-width:760px){main.card{grid-template-columns:1fr;gap:18px;padding:20px} .illustration{justify-self:center}}\
  ";

  function injectStyles() {
    var style = document.createElement('style');
    style.type = 'text/css';
    style.appendChild(document.createTextNode(css));
    document.head.appendChild(style);
  }

  function onStartClick(e) {
    e.preventDefault();
    // simple focus/announce animation: temporarily change brand text
    var brand = document.querySelector('.brand');
    if (!brand) return;
    var orig = brand.textContent;
    brand.textContent = 'Hai să începem — Pregătim totul...';
    brand.setAttribute('aria-live', 'polite');
    brand.style.transform = 'translateY(-2px)';
    setTimeout(function () {
      brand.textContent = orig;
      brand.style.transform = '';
    }, 1200);
  }

  function onMenuClick(e) {
    e.preventDefault();
    // Smoothly scroll to a #menu element if present; otherwise show a toast
    var target = document.getElementById('menu') || document.querySelector('[role="main"]');
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function wireButtons() {
    var start = document.querySelector('.btn-primary');
    var menu = document.querySelector('.btn-outline');
    if (start) start.addEventListener('click', onStartClick);
    if (menu) menu.addEventListener('click', onMenuClick);

    // allow Enter/Space activation for keyboard users when focused as it's an <a>
    [start, menu].forEach(function (el) {
      if (!el) return;
      el.setAttribute('role', 'button');
      el.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' || ev.key === ' ') {
          ev.preventDefault();
          el.click();
        }
      });
    });
  }

  // Quick, tiny runtime check for older browsers: requestAnimationFrame optional poly
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    try {
      injectStyles();
      wireButtons();
    } catch (err) {
      // fail silently but log to console for developer
      if (window.console && console.error) console.error('home.js init error:', err);
    }
  });

})();
