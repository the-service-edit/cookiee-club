/* The Cookiee Club v2 concept: cart, drawer, product pages, box builder, forms.
   Prototype only: in Shopify the cart, stock and checkout come from the platform. */
(function () {
  'use strict';
  var D = window.TCC, BASE = window.TCC_BASE || '';
  var KEY = 'tcc_cart_v2';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var money = function (n) { return '$' + n.toFixed(2); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var prod = function (id) { return D.products.filter(function (p) { return p.id === id; })[0]; };
  var allFlav = D.flavours.concat(D.extraFlavours);
  var flav = function (id) { return allFlav.filter(function (f) { return f.id === id; })[0]; };
  var perCookie = function (price, n) { return (price + D.shipping) / n; };

  /* ---------- storage (works without it) ---------- */
  var mem = [];
  function load() { var v; try { v = JSON.parse(localStorage.getItem(KEY) || '[]'); if (!Array.isArray(v)) v = []; } catch (e) { v = mem; } return v.filter(function (l) { return prod(l.pid) && (!l.flavours || Object.keys(l.flavours).every(function (k) { return flav(k); })); }); }
  function save(c) { mem = c; try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} render(); }

  function lineKey(pid, variant, fl) {
    var sig = fl ? Object.keys(fl).sort().map(function (k) { return k + fl[k]; }).join('.') : '';
    return pid + '|' + (variant || '') + '|' + sig;
  }
  function linePrice(l) {
    var p = prod(l.pid);
    if (p.variants && l.variant) { var v = p.variants.filter(function (x) { return x.id === l.variant; })[0]; if (v) return v.price; }
    return p.price;
  }
  function limitLeft(pid, cart, exceptKey) {
    var p = prod(pid); if (!p.limit) return Infinity;
    var used = cart.filter(function (l) { return l.pid === pid && l.key !== exceptKey; }).reduce(function (s, l) { return s + l.qty; }, 0);
    return p.limit - used;
  }
  function add(pid, qty, variant, fl, replaceKey) {
    var cart = load(), p = prod(pid);
    if (p.stock !== 'in') return toast(p.name + ' is sold out right now.');
    if (replaceKey) cart = cart.filter(function (l) { return l.key !== replaceKey; });
    var key = lineKey(pid, variant, fl);
    var ex = cart.filter(function (l) { return l.key === key; })[0];
    var room = limitLeft(pid, cart, null);
    if (room <= 0) return toast('The ' + p.name + ' is limited to one per customer.');
    qty = Math.min(qty, room);
    if (ex) ex.qty += qty; else cart.push({ key: key, pid: pid, variant: variant || null, qty: qty, flavours: fl || null });
    save(cart); openDrawer();
  }
  function setQty(key, q) {
    var cart = load();
    cart.forEach(function (l) { if (l.key === key) { var room = limitLeft(l.pid, cart, key); l.qty = Math.max(0, Math.min(q, room)); } });
    save(cart.filter(function (l) { return l.qty > 0; }));
  }
  function totals(cart) {
    var sub = cart.reduce(function (s, l) { return s + linePrice(l) * l.qty; }, 0);
    var cookies = cart.reduce(function (s, l) { return s + prod(l.pid).cookies * l.qty; }, 0);
    var ship = cart.length ? D.shipping : 0;
    return { sub: sub, ship: ship, total: sub + ship, cookies: cookies, items: cart.reduce(function (s, l) { return s + l.qty; }, 0) };
  }
  function flavText(l) {
    if (!l.flavours) {
      var p = prod(l.pid), bits = [];
      if (p.variants && l.variant) bits.push(p.variants.filter(function (v) { return v.id === l.variant; })[0].name);
      if (p.fixed) bits.push(p.fixed.map(function (id) { return flav(id).name; }).join(', '));
      return bits.join(' · ');
    }
    return Object.keys(l.flavours).map(function (id) { return l.flavours[id] + '× ' + flav(id).name; }).join(', ');
  }

  /* ---------- toast ---------- */
  var tEl, tTimer;
  function toast(msg) {
    if (!tEl) { tEl = document.createElement('div'); tEl.className = 'toast'; tEl.setAttribute('role', 'status'); document.body.appendChild(tEl); }
    tEl.textContent = msg; tEl.classList.add('show'); clearTimeout(tTimer);
    tTimer = setTimeout(function () { tEl.classList.remove('show'); }, 2600);
  }

  /* ---------- drawer ---------- */
  var drawer = $('#drawer'), scrim = $('#scrim'), lastFocus;
  function openDrawer() {
    if (!drawer) return; lastFocus = document.activeElement;
    drawer.classList.add('show'); scrim.classList.add('show'); drawer.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; setTimeout(function () { $('.dr-close', drawer).focus(); }, 50);
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('show'); scrim.classList.remove('show'); drawer.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = ''; if (lastFocus) lastFocus.focus();
  }
  function lineHTML(l, editable) {
    var p = prod(l.pid), price = linePrice(l), room = limitLeft(l.pid, load(), l.key);
    var edit = p.builder ? '<a href="' + BASE + 'build-a-box.html?size=' + p.builder + '&edit=' + encodeURIComponent(l.key) + '">Edit flavours</a>' : '';
    return '<div class="cline"><img src="' + BASE + 'img/p/' + p.imgs[0] + '.jpg" alt="" width="76" height="76">' +
      '<div><div class="nm">' + esc(p.name) + '<span>' + money(price * l.qty) + '</span></div>' +
      '<div class="fls">' + esc(flavText(l)) + '</div>' +
      (editable ? '<div class="ctl"><div class="mini-qty"><button type="button" data-q="-1" data-k="' + esc(l.key) + '" aria-label="One less ' + esc(p.name) + '">−</button><output>' + l.qty + '</output>' +
        '<button type="button" data-q="1" data-k="' + esc(l.key) + '" aria-label="One more ' + esc(p.name) + '"' + (room <= l.qty ? ' disabled' : '') + '>+</button></div>' +
        edit + '<button type="button" class="rm" data-rm="' + esc(l.key) + '">Remove</button>' +
        (p.limit ? '<span class="lim">One per customer</span>' : '') + '</div>' : '<div class="fls">Qty ' + l.qty + '</div>') +
      '</div></div>';
  }
  function upsellHTML(cart) {
    var has = function (id) { return cart.some(function (l) { return l.pid === id; }); };
    var six = cart.filter(function (l) { return l.pid === 'byo6'; })[0];
    if (six && !has('byo12')) {
      var p6 = prod('byo6'), p12 = prod('byo12');
      return '<div class="upsell"><p><b>Make it a 12?</b>Twice the cookies, one shipping fee. Your six picks come with you.</p>' +
        '<a class="btn red" href="' + BASE + 'build-a-box.html?size=12&from=' + encodeURIComponent(six.key) + '">Upgrade</a></div>';
    }
    var imp = prod('imperfect');
    if (!has('imperfect') && imp.stock === 'in') {
      return '<div class="upsell"><p><b>Add the Imperfect Box</b>4 wonky cookies for ' + money(imp.price) + '. Same parcel, no extra shipping.</p><button class="btn red" type="button" data-add="imperfect" data-variant="reg">Add</button></div>';
    }
    return '';
  }
  function totalsHTML(t) {
    return '<div class="totals"><div><span>Subtotal (' + t.cookies + ' cookies)</span><span>' + money(t.sub) + '</span></div>' +
      '<div><span>Express post, Australia wide</span><span>' + money(t.ship) + '</span></div>' +
      '<div class="grand"><span>Total</span><span>' + money(t.total) + '</span></div>' +
      (t.cookies ? '<small>Baked and posted within ' + D.turnaround + '. Or 4 payments of ' + money(t.total / 4) + ' with Afterpay.</small>' : '') + '</div>';
  }
  function render() {
    var cart = load(), t = totals(cart);
    $$('.cart-count').forEach(function (el) { el.textContent = t.items; el.setAttribute('data-n', t.items); });
    if (drawer) {
      var body = $('.dr-body', drawer), foot = $('.dr-foot', drawer);
      if (!cart.length) {
        body.innerHTML = '<div class="empty-cart"><b>Your box is empty.</b><p>Start with six of your favourites, or go big with twelve.</p><a class="btn" href="' + BASE + 'build-a-box.html">Build a box</a></div>';
        foot.hidden = true;
      } else {
        body.innerHTML = cart.map(function (l) { return lineHTML(l, true); }).join('') + upsellHTML(cart);
        foot.hidden = false;
        foot.innerHTML = totalsHTML(t) + '<a class="btn red block" href="' + BASE + 'checkout.html">Checkout</a><a class="btn line block" href="' + BASE + 'cart.html">View cart</a>';
      }
    }
    var cp = $('#cart-page');
    if (cp) {
      if (!cart.length) { cp.innerHTML = '<div class="empty-cart"><b>Your box is empty.</b><a class="btn" href="' + BASE + 'shop.html">Shop the menu</a></div>'; }
      else {
        cp.innerHTML = '<div class="cart-page"><div class="lines">' + cart.map(function (l) { return lineHTML(l, true); }).join('') + upsellHTML(cart) + '</div>' +
          '<aside class="side">' + totalsHTML(t) + '<a class="btn red block" href="' + BASE + 'checkout.html">Checkout</a>' +
          '<p class="sum-note">Shop Pay, Apple Pay, Google Pay, PayPal and Afterpay at checkout. Need it by a date? <a class="link" href="' + BASE + 'contact.html">Ask before you order</a>.</p></aside></div>';
      }
    }
    var co = $('#checkout-summary');
    if (co) {
      co.innerHTML = cart.length ? cart.map(function (l) { return lineHTML(l, false); }).join('') + totalsHTML(t) : '<p>Your cart is empty.</p>';
    }
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-open-cart],[data-close-cart],[data-q],[data-rm],[data-add],.menu-toggle');
    if (!t) return;
    if (t.hasAttribute('data-open-cart')) { e.preventDefault(); openDrawer(); }
    else if (t.hasAttribute('data-close-cart')) closeDrawer();
    else if (t.hasAttribute('data-q')) { var l = load().filter(function (x) { return x.key === t.getAttribute('data-k'); })[0]; if (l) setQty(l.key, l.qty + (+t.getAttribute('data-q'))); }
    else if (t.hasAttribute('data-rm')) setQty(t.getAttribute('data-rm'), 0);
    else if (t.hasAttribute('data-add')) add(t.getAttribute('data-add'), 1, t.getAttribute('data-variant'));
    else if (t.classList.contains('menu-toggle')) {
      var h = t.closest('.top'), o = h.classList.toggle('open');
      t.setAttribute('aria-expanded', o); $('.mt-label', t).textContent = o ? 'Close' : 'Menu';
    }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && drawer && drawer.classList.contains('show')) closeDrawer(); });
  if (scrim) scrim.addEventListener('click', closeDrawer);

  /* ---------- email / contact forms (not wired: concept) ---------- */
  $$('form[data-form]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = $('.form-msg', f) || $('.form-msg', f.parentNode), em = $('input[type=email]', f);
      if (em && !/.+@.+\..+/.test(em.value.trim())) { msg.textContent = 'Pop in a valid email address.'; em.focus(); return; }
      var kind = f.getAttribute('data-form');
      msg.textContent = kind === 'alert' ? 'Done. We’ll email you the moment it’s back.' :
        kind === 'join' ? 'You’re in. We’ll email you before the next restock.' :
        kind === 'corporate' ? 'Thanks. Ruby or Rachel will reply with what’s possible for your date.' :
        'Thanks, we’ve got your message. We reply within [X] business days.';
      f.reset();
    });
  });

  /* ---------- shop filters ---------- */
  var chips = $$('.chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var g = c.getAttribute('data-filter');
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      $$('[data-groups]').forEach(function (card) { card.hidden = g !== 'all' && card.getAttribute('data-groups').split(' ').indexOf(g) < 0; });
    });
  });

  /* ---------- product page ---------- */
  var pdp = $('[data-pdp]');
  if (pdp) {
    var p = prod(pdp.getAttribute('data-pdp')), q = 1, out = $('#q-val'), btn = $('#add-btn'), sbtn = $('#sticky-add');
    var variant = function () { var r = $('input[name=variant]:checked'); return r ? r.value : null; };
    var price = function () { if (!p.variants) return p.price; var v = variant(); return p.variants.filter(function (x) { return x.id === v; })[0].price; };
    var upd = function () {
      if (out) out.textContent = q;
      var lbl = 'Add to cart · ' + money(price() * q);
      if (btn) btn.textContent = lbl;
      if (sbtn) sbtn.textContent = 'Add · ' + money(price() * q);
      var pr = $('#pr-main'); if (pr) pr.textContent = money(price()).replace('.00', '');
    };
    $$('input[name=variant]').forEach(function (r) { r.addEventListener('change', upd); });
    var mx = p.limit || 9;
    if ($('#q-minus')) $('#q-minus').addEventListener('click', function () { q = Math.max(1, q - 1); upd(); });
    if ($('#q-plus')) $('#q-plus').addEventListener('click', function () { q = Math.min(mx, q + 1); upd(); });
    [btn, sbtn].forEach(function (b) { if (b) b.addEventListener('click', function () { add(p.id, q, variant()); }); });
    var sticky = $('.sticky-buy'), anchor = $('.buy') || $('.alert-box') || $('#choose-btn');
    if (sticky && anchor) {
      var tick = false, check = function () { tick = false; sticky.classList.toggle('show', anchor.getBoundingClientRect().bottom < 0); };
      window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(check); } }, { passive: true });
      check();
    }
    upd();
  }

  /* ---------- box builder ---------- */
  var bld = $('#builder');
  if (bld) {
    var params = new URLSearchParams(location.search), size = params.get('size') === '12' ? 12 : 6;
    var editKey = params.get('edit'), fromKey = params.get('from'), counts = {};
    var cart0 = load(), seed = cart0.filter(function (l) { return l.key === (editKey || fromKey); })[0];
    if (seed && seed.flavours) Object.keys(seed.flavours).forEach(function (k) { counts[k] = seed.flavours[k]; });
    var total = function () { return Object.keys(counts).reduce(function (s, k) { return s + counts[k]; }, 0); };
    var pid = function () { return size === 12 ? 'byo12' : 'byo6'; };

    $$('input[name=size]').forEach(function (r) {
      r.checked = +r.value === size;
      r.addEventListener('change', function () {
        size = +r.value;
        while (total() > size) { var ks = Object.keys(counts).filter(function (k) { return counts[k] > 0; }); var last = ks[ks.length - 1]; counts[last]--; if (!counts[last]) delete counts[last]; }
        history.replaceState(null, '', '?size=' + size + (editKey ? '&edit=' + encodeURIComponent(editKey) : ''));
        draw();
      });
    });
    bld.addEventListener('click', function (e) {
      var b = e.target.closest('[data-f]'); if (!b) return;
      var id = b.getAttribute('data-f'), d = +b.getAttribute('data-d');
      if (d > 0 && total() >= size) return toast('Your box is full. Take one out to swap.');
      counts[id] = Math.max(0, (counts[id] || 0) + d); if (!counts[id]) delete counts[id];
      draw();
    });
    $('#surprise').addEventListener('click', function () {
      var ids = D.flavours.map(function (f) { return f.id; });
      while (total() < size) { var id = ids[Math.floor(Math.random() * ids.length)]; counts[id] = (counts[id] || 0) + 1; }
      draw(); toast('Filled with a random mix. Swap any you like.');
    });
    $('#clear').addEventListener('click', function () { counts = {}; draw(); });
    $$('.bld-add').forEach(function (b) {
      b.addEventListener('click', function () {
        if (total() !== size) return;
        var fl = {}; Object.keys(counts).forEach(function (k) { if (counts[k]) fl[k] = counts[k]; });
        add(pid(), 1, null, fl, editKey || (seed && fromKey ? fromKey : null));
        if (editKey) { editKey = null; history.replaceState(null, '', '?size=' + size); }
        counts = {}; draw();
      });
    });
    function draw() {
      var n = total(), pp = prod(pid()), full = n === size, pct = Math.round(n / size * 100) + '%';
      D.flavours.forEach(function (f) {
        var c = counts[f.id] || 0, card = $('[data-card="' + f.id + '"]');
        card.classList.toggle('on', c > 0);
        $('.cnt', card).hidden = !c; $('.cnt', card).textContent = c;
        $('output', card).textContent = c;
        $('[data-d="-1"]', card).disabled = !c;
        $('[data-d="1"]', card).disabled = full;
      });
      $$('.prog-n').forEach(function (el) { el.textContent = n + ' of ' + size; });
      $$('.prog .bar i, .bar-m .bar i').forEach(function (el) { el.style.width = pct; });
      var ks = Object.keys(counts);
      $('#picked').innerHTML = ks.length ? ks.map(function (k) {
        return '<li><span>' + counts[k] + '× ' + esc(flav(k).name) + '</span><button type="button" data-f="' + k + '" data-d="-1" aria-label="Remove one ' + esc(flav(k).name) + '">−</button></li>';
      }).join('') : '<li class="empty">Nothing picked yet. Tap + on any flavour.</li>';
      $('#sum-price').textContent = money(pp.price);
      $$('.bld-add').forEach(function (b) {
        b.disabled = !full;
        b.textContent = full ? (editKey ? 'Update box' : 'Add box · ' + money(pp.price)) : 'Pick ' + (size - n) + ' more';
      });
      $('#bld-title').textContent = editKey ? 'Edit your box of ' + size + '.' : 'Build your box of ' + size + '.';
    }
    draw();
  }


  /* ---------- calendar: status from today's date (Perth) ---------- */
  (function () {
    var tl = $('.tl'); if (!tl) return;
    var t = new Date(new Date().toLocaleString('en-US', { timeZone: 'Australia/Perth' }));
    var today = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');
    var items = $$('.tl-item', tl), nextSet = false;
    items.forEach(function (li) {
      var s = li.getAttribute('data-start'), e = li.getAttribute('data-end');
      var st = e < today ? 'done' : s <= today ? 'now' : 'next';
      li.classList.remove('done', 'now', 'next', 'up'); li.classList.add(st);
      var chip = $('.tl-chip', li);
      if (st === 'next' && !nextSet) { li.classList.add('up'); nextSet = true; chip.textContent = 'Up next'; }
      else chip.textContent = st === 'done' ? 'Done' : st === 'now' ? 'On now' : 'Coming up';
    });
    var cn = $('.cal-now');
    if (cn) {
      var end = cn.getAttribute('data-end');
      var days = Math.round((new Date(end + 'T00:00:00') - new Date(today + 'T00:00:00')) / 864e5) + 1;
      if (days < 1) cn.hidden = true; else { $('[data-countdown]', cn).textContent = days; $('.cn-u', cn).textContent = days === 1 ? 'last day' : 'days left'; }
    }
  })();

  render();
})();
