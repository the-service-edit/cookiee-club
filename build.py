#!/usr/bin/env python3
"""Builds The Cookiee Club v2 concept as static HTML pages.
Run: python3 build.py   (writes into this folder)"""
import json, os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'assets/data.js')).read()
SHIP = 16.20
# read the catalogue from data.js so the pages and the cart agree
js = src[src.index('{'):src.rindex('}') + 1]
js = re.sub(r'/\*.*?\*/', '', js, flags=re.S)
js = re.sub(r'//[^\n]*', '', js)
js = re.sub(r"([{,]\s*)([a-zA-Z_]+)\s*:", r'\1"\2":', js)
js = js.replace("\\u2019", "’")
js = re.sub(r"'((?:[^'\\]|\\.)*)'", lambda m: json.dumps(m.group(1).replace("\\'", "'")), js)
js = re.sub(r',(\s*[}\]])', r'\1', js)
D = json.loads(js)
P = {p['id']: p for p in D['products']}
F = {f['id']: f for f in D['flavours'] + D['extraFlavours']}
e = html.escape

def money(n):
    s = f'${n:,.2f}'
    return s[:-3] if s.endswith('.00') else s

def per(p):
    return (p['price'] + SHIP) / p['cookies']

ICON = {
 'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 'truck': '<path d="M3 7h11v9H3z"/><path d="M14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
 'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 'card': '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>',
 'check': '<path d="M5 12l5 5L20 7"/>',
 'bag': '<path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
 'tiktok': '<path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.5 2.6 2.4 4.4 5 4.6"/>',
}
def icon(n, s=24, sw=1.9):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>'

NAV = [('shop.html', 'Shop'), ('build-a-box.html', 'Build a box'), ('our-kitchen.html', 'Our kitchen'), ('drops.html', 'Drops'), ('faq.html', 'Help')]

def page(path, title, body, desc, active='', extra_head=''):
    depth = path.count('/')
    B = '../' * depth
    nav = ''.join(f'<a href="{B}{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    band = ('<span>Baked to order</span><span>Posted in 2 to 4 business days</span><span>Nut &amp; egg free</span>'
            '<span>$16.20 express, Australia wide</span><span>Mum’s recipe</span>')
    doc = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#F7A8A0">
<link rel="icon" href="{B}img/logo_old.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@600;800;900&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{B}assets/site.css">
{extra_head}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="logo" href="{B}index.html" aria-label="The Cookiee Club home"><img src="{B}img/logo_old.png" alt="The Cookiee Club" width="84" height="84"></a>
    <nav class="nav" id="main-nav" aria-label="Main">{nav}</nav>
    <div class="hdr-actions">
      <a class="icon-btn" href="{B}cart.html" data-open-cart aria-label="Open cart">{icon('bag', 20, 2)}<span class="cart-count" data-n="0">0</span></a>
      <button class="icon-btn menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav"><span class="mt-label">Menu</span></button>
    </div>
  </div>
</header>
<div class="band red" role="note" aria-label="Baked to order, posted in 2 to 4 business days, nut and egg free, $16.20 express Australia wide">
  <div class="track" aria-hidden="true">{band}{band}</div>
</div>
<main id="main">
{body}
</main>
<footer class="site">
  <div class="wrap fcols">
    <div class="fbrand"><img src="{B}img/logo_old.png" alt="The Cookiee Club" width="96" height="96"><p>Nut and egg free cookies, baked to order from Mum’s recipe by sisters Ruby and Rachel. Posted Australia wide.</p>
      <a class="icon-btn" style="align-self:flex-start;border-color:#fff;color:#fff" href="https://www.tiktok.com/@rubyrosedemiroski" aria-label="Ruby on TikTok">{icon('tiktok', 22, 2)}</a></div>
    <div><h3>Shop</h3><ul><li><a href="{B}build-a-box.html?size=12">Box of 12</a></li><li><a href="{B}build-a-box.html?size=6">Box of 6</a></li><li><a href="{B}products/the-haunted-batch.html">The Haunted Batch</a></li><li><a href="{B}products/gluten-free-range.html">Gluten Free Range</a></li><li><a href="{B}products/the-little-cookiee-club.html">Little Cookiee Club</a></li><li><a href="{B}products/the-imperfect-box.html">Imperfect Box</a></li></ul></div>
    <div><h3>Help</h3><ul><li><a href="{B}delivery.html">Delivery &amp; shipping</a></li><li><a href="{B}refunds.html">Refunds &amp; damaged orders</a></li><li><a href="{B}faq.html">FAQ</a></li><li><a href="{B}contact.html">Contact us</a></li></ul></div>
    <div><h3>The club</h3><ul><li><a href="{B}our-kitchen.html">Our kitchen &amp; allergens</a></li><li><a href="{B}drops.html">Drops &amp; calendar</a></li><li><a href="{B}corporate.html">Corporate &amp; events</a></li><li><span class="fill">[hello@thecookieeclub.com]</span></li></ul></div>
  </div>
  <div class="wrap legal"><span>© 2026 The Cookiee Club</span><span>ABN <span class="fill">[ABN]</span></span><span>Prices in AUD</span><a href="{B}privacy.html">Privacy</a><a href="{B}refunds.html">Refunds</a><a href="{B}delivery.html">Shipping</a><a href="{B}terms.html">Terms</a></div>
</footer>
<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-label="Your cart" aria-hidden="true">
  <div class="dr-head"><h2>Your box</h2><button class="icon-btn dr-close" type="button" data-close-cart aria-label="Close cart">✕</button></div>
  <div class="dr-body"></div>
  <div class="dr-foot" hidden></div>
</aside>
<nav class="vswitch" aria-label="Concept versions"><a href="{B}v1/">View v1</a><span>v2</span><a href="{B}notes.html">What changed</a></nav>
<script>window.TCC_BASE='{B}';</script>
<script src="{B}assets/data.js"></script>
<script src="{B}assets/site.js"></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)

def rel(depth): return '../' * depth

# ---------- shared blocks ----------
def card(p, B, two=False):
    url = f'{B}products/{p["handle"]}.html'
    tag = ''
    if p.get('badge'):
        tag = f'<span class="tag{" dark" if p.get("badgeDark") else ""}">{e(p["badge"])}</span>'
    out = '<span class="tag out">Sold out</span>' if p['stock'] != 'in' else ''
    price = (f'<s>{money(p["compare"])}</s>' if p.get('compare') else '') + money(p['price'])
    perl = ''
    return (f'<a class="card" href="{url}" data-groups="{" ".join(p["group"])}"><div class="ph">'
            f'<img src="{B}img/p/{p["imgs"][0]}.jpg" alt="{e(p["alt"][0])}" loading="lazy" width="1000" height="1250">{tag}{out}</div>'
            f'<div class="row"><span class="name">{e(p["name"])}</span><span class="price">{price}</span></div>'
            f'<span class="sub">{e(p["short"])}</span>{perl}</a>')

def best_tag(f):
    return '<span class="ftag best">Best seller</span>' if f.get('best') else ''

def flav_img(f, B, cls='', studio=False):
    if studio and os.path.exists(os.path.join(ROOT, 'img/m', f['id'] + '.jpg')):
        return f'<img src="{B}img/m/{f["id"]}.jpg" alt="{e(f["name"])} cookie" loading="lazy" width="1000" height="1250">'
    if f.get('img'):
        return f'<img src="{B}img/f/{f["img"]}.jpg" alt="{e(f["name"])} cookie" loading="lazy" width="700" height="700">'
    return f'<div class="noimg {cls}" role="img" aria-label="{e(f["name"])}: photo to come"><strong>{e(f["name"])}</strong><small>Photo from Ruby</small></div>'

def reviews_block():
    return '''<section class="sec" id="reviews">
  <div class="wrap">
    <div class="sec-head"><h2>In their words.</h2><p>Copied word for word from customers’ own TikToks. Tap any review to watch the original.</p></div>
    <figure class="rv-feature">
      <blockquote>“All I have to say is, these were DELICIOUS! 😍 Obviously, there was a wait to receive them 😂 Yes, the girls are going through drama, yes, they went viral, but YES, the cookies are delicious! … 10/10, will be returning to order more!”</blockquote>
      <figcaption><b>Sade Sitaloto</b> · TikTok caption · 30 Sep 2026 · <a href="https://www.tiktok.com/@sade.sitaloto/video/7691478128849440021">Watch</a></figcaption>
    </figure>
    <div class="rv-grid">
      <article class="rv"><p class="rv-q">“Her cookie dough is amazing. My favourite is the cinnamon, hands down. … She’s definitely worth the hype.”</p><div class="rv-by"><b>ALAÍA MUSE</b><span>TikTok video · 3 Sep 2026 · <a href="https://www.tiktok.com/@alaiamuse_/video/7681237616687172872">Watch</a></span></div></article>
      <article class="rv"><p class="rv-q">“It is super soft. Like it’s low key breaking in my hands. … That one is by far the best one.”</p><div class="rv-by"><b>jordan.and.zara</b><span>TikTok video, on the Cinnamon Roll · 2 Oct 2026 · <a href="https://www.tiktok.com/@jordan.and.zara/video/7692187335189941524">Watch</a></span></div></article>
      <article class="rv loud"><p class="rv-q">“GUYS WHAT THE HECK THESE TASTE INSANEEE OMGGG AHH”</p><div class="rv-by"><b>Katie Hennessey</b><span>TikTok caption · 7 Aug 2026 · <a href="https://www.tiktok.com/@katie_hennessey_official/video/7671174224802745608">Watch</a></span></div></article>
      <article class="rv"><p class="rv-q">“I need to eat the cinnamon one 24:7 😩❤️ Ps. These are the gluten free ones!!”</p><div class="rv-by"><b>Hannah Jayde</b><span>TikTok caption · 24 Sep 2026 · <a href="https://www.tiktok.com/@hannahhjayde/video/7689046787625274625">Watch</a></span></div></article>
      <article class="rv"><p class="rv-q">“Oh, look at how soft they are.”</p><div class="rv-by"><b>Georgia Reilly</b><span>TikTok video · 30 Sep 2026 · <a href="https://www.tiktok.com/@georgia_reilly77/video/7691193500661976338">Watch</a></span></div></article>
    </div>
  </div>
</section>'''

CAL = [
    # (start, end, title, short date, description, kind, cta label, cta href)
    ('2026-10-11', '2026-10-25', 'The Haunted Batch', '11 to 25 Oct', 'Four Halloween flavours. Gone on the 25th.', 'drop', 'Shop the batch', 'products/the-haunted-batch.html'),
    ('2026-10-26', '2026-11-04', 'Christmas, early', '26 Oct to 4 Nov', 'New Chrissy flavours, a week before anyone else.', 'drop', 'Build a box', 'build-a-box.html'),
    ('2026-11-12', '2026-11-15', 'Perth pop-up', '12 to 15 Nov', 'Our first interstate pop-up. Come say hi. <span class="fill">[Venue]</span>', 'event', 'Get the details', 'drops.html'),
    ('2026-11-16', '2026-11-16', 'Advent calendars', '16 Nov', '50 boxes only. The club gets the link first.', 'drop', 'Get the link first', 'index.html#join'),
    ('2026-11-16', '2026-12-05', 'Shop closed', '16 Nov to 6 Dec', 'Resting up before Christmas.', 'closed', '', ''),
    ('2026-12-06', '2026-12-31', 'Christmas, in full', 'From 6 Dec', 'Every Christmas flavour, back for the season.', 'drop', 'Join for the reminder', 'index.html#join'),
]
import datetime as _dt
BUILD_DAY = _dt.date(2026, 10, 26)

def _status(st, en, today=BUILD_DAY):
    s, e = _dt.date.fromisoformat(st), _dt.date.fromisoformat(en)
    return 'done' if e < today else 'now' if s <= today else 'next'

def calendar_block(B, head=True):
    sts = [_status(c[0], c[1]) for c in CAL]
    cur = sts.index('now') if 'now' in sts else None
    upnext = next((i for i, x in enumerate(sts) if x == 'next'), None)
    def label(i, st):
        return 'Done' if st == 'done' else 'On now' if st == 'now' else ('Up next' if i == upnext else 'Coming up')
    def item(i, c):
        st = sts[i]
        cls = st + (' up' if i == upnext else '') + (' closed' if c[5] == 'closed' else '')
        return (f'<li class="tl-item {cls}" data-start="{c[0]}" data-end="{c[1]}"><span class="tl-dot" aria-hidden="true"></span>'
                f'<span class="tl-when">{c[3]}</span><span class="tl-chip">{label(i, st)}</span>'
                f'<b class="tl-title">{c[2]}</b><span class="tl-desc">{c[4]}</span></li>')
    feat = ''
    if cur is not None:
        c = CAL[cur]
        days = (_dt.date.fromisoformat(c[1]) - BUILD_DAY).days + 1
        feat = (f'<div class="cal-now" data-end="{c[1]}"><div class="cn-l"><span class="cn-tag"><i></i>On now</span>'
                f'<h3>{c[2]}</h3><p>{c[4]}</p>'
                f'<a class="btn" href="{B}{c[7]}">{c[6]}</a></div>'
                f'<div class="cn-r"><span class="cn-n" data-countdown>{days}</span><span class="cn-u">days left</span><span class="cn-d">{c[3]}</span></div></div>')
    h = (f'<div class="sec-head"><h2>The cookie calendar</h2><div class="side"><p>Stick it on the fridge. '
         f'We email the club before each one opens.</p><a class="btn light" href="{B}index.html#join">Get reminders</a></div></div>') if head else ''
    items = ''.join(item(i, c) for i, c in enumerate(CAL))
    return f'<section class="sec red cal2" id="calendar"><div class="wrap">{h}{feat}<ol class="tl">{items}</ol></div></section>'

def join_block():
    return '''<section class="sec pink join" id="join"><div class="inner wrap">
  <h2>Join the club.</h2>
  <p>Restock alerts, new flavours and first go at the 50 advent calendars. Straight to your inbox, not buried in a feed.</p>
  <form class="inline-form" data-form="join" novalidate><label class="sr" for="join-email">Email address</label><input id="join-email" type="email" placeholder="Your email" autocomplete="email" required><button class="btn" type="submit">Sign me up</button><p class="form-msg" aria-live="polite" style="flex-basis:100%;margin-top:12px"></p></form>
  <p class="consent">One email per drop or restock, plus order emails. Unsubscribe any time.</p>
</div></section>'''

FAQS = [
 ('How long until my cookies arrive?', '<p>Every order is baked to order. We bake and post within 2 to 4 business days, then express post usually takes 1 to 3 business days depending on where you are. Tracking is emailed when your parcel is posted.</p>'),
 ('Are your cookies nut and egg free?', '<p>Yes. We don’t handle nuts or eggs in our kitchen, and none of our recipes use eggs. Some chocolates we use (Cadbury and Nestlé) carry a “may contain” statement from the manufacturer. <a class="link" href="our-kitchen.html#allergens">Read the full allergen guide</a>.</p>'),
 ('How much is shipping?', '<p>Express post is a flat $16.20 anywhere in Australia, whatever the size of your order.</p>'),
 ('Can I choose my own flavours?', '<p>Yes. Build a box of 6 or 12 from any flavours on the menu. <a class="link" href="build-a-box.html">Build a box</a>.</p>'),
 ('Does express shipping mean you bake it faster?', '<p>No. Every order joins the same baking queue. Express applies once your cookies are baked, packed and with Australia Post.</p>'),
 ('How long do the cookies keep?', '<p>Best within <span class="fill">[X]</span> days in an airtight container. <span class="fill">[Ruby’s storage and warming tip]</span></p>'),
 ('Can I change my order or address?', '<p>We can’t change an order once it’s placed. If you’ve made a mistake, like a typo in your address, message us straight away and we’ll do our best to fix it before it’s posted.</p>'),
 ('What if my cookies arrive damaged?', '<p>Send us your order number and a photo within 48 hours and we’ll replace or refund the damaged cookies. <a class="link" href="refunds.html">Refunds and damaged orders</a>.</p>'),
 ('Do you do corporate gifts or events?', '<p>Sometimes, depending on our baking calendar. <a class="link" href="corporate.html">Send an enquiry</a> with your date and numbers and we’ll tell you honestly what’s possible.</p>'),
 ('How do I contact you?', '<p>Use our <a class="link" href="contact.html">contact form</a> or email <span class="fill">[hello@thecookieeclub.com]</span>. We reply within <span class="fill">[X]</span> business days.</p>'),
]
def faq_html(items, B):
    return '<div class="acc">' + ''.join(f'<details><summary>{e(q)}</summary><div class="body">{a.replace("href=\"", "href=\"" + B) if B else a}</div></details>' for q, a in items) + '</div>'

# ---------- HOME ----------
B = ''
order = ['byo12', 'byo6', 'haunted', 'gf', 'little', 'imperfect']
home = f'''
<section class="hero" id="home">
  <picture><source media="(max-width:700px)" srcset="img/s_hero_mobile2.jpg"><source media="(max-width:900px)" srcset="img/s_hero_mobile.jpg"><img class="hero-bg" src="img/s_hero_wide_icing.jpg" alt="A hand holding a stack of Caramello Koala, Mini M&amp;M and Cinnamon Scroll cookies" width="2600" height="1050" fetchpriority="high"></picture>
  <div class="hero-inner"><div class="hero-txt">
    <span class="kick desk-only">Nut &amp; egg free cookies, baked to order</span>
    <h1>What you see <span>is what arrives.</span></h1>
    <p class="desk-only">Mum’s recipe, baked fresh in small batches by two sisters. Nut and egg free, and out the door in 2 to 4 days, Australia wide.</p>
    <div class="hero-ctas desk-only"><a class="btn" href="build-a-box.html">Build your box</a><a class="btn line" href="shop.html">Shop the menu</a></div>
  </div></div>
  <div class="hero-after"><p>Mum’s recipe, baked fresh in small batches by two sisters. Nut and egg free, out the door in 2 to 4 days.</p><a class="btn" href="build-a-box.html">Build your box</a></div>
</section>

<section class="proof" aria-label="Why the Cookiee Club"><div class="wrap">
  <div class="pi">{icon('heart', 30)}<div><b>Nut &amp; egg free kitchen</b><span>No nuts in the house, no eggs in the recipes</span></div></div>
  <div class="pi">{icon('clock', 30)}<div><b>Posted in 2 to 4 days</b><span>Baked to order, then express post</span></div></div>
  <div class="pi">{icon('truck', 30)}<div><b>$16.20 express, Australia wide</b><span>One flat price, any size order</span></div></div>
  <div class="pi">{icon('card', 30)}<div><b>Afterpay available</b><span>Four payments, no interest</span></div></div>
</div></section>

<section class="sec paper" id="shop"><div class="wrap">
  <div class="sec-head"><h2>The menu</h2><p>Baked to order, posted Australia wide in 2 to 4 business days.</p></div>
  <div class="grid cards-2 three">{''.join(card(P[i], B) for i in order)}</div>
</div></section>

<div class="band pink" aria-hidden="true"><div class="track">{''.join(f'<span>{e(f["name"])}</span>' for f in D['flavours'])*2}</div></div>

<section class="sec cream" id="flavours"><div class="wrap">
  <div class="sec-head"><h2>Pick your flavours</h2><div class="side"><p>Eleven on the menu right now, including two Halloween specials until 25 October. Studio shots made from Ruby’s own photos of each cookie.</p><a class="btn" href="build-a-box.html">Build a box</a></div></div>
  <div class="rail">{''.join(f'<a class="fl" href="build-a-box.html" style="text-decoration:none;position:relative">{flav_img(f, B, studio=True)}{best_tag(f)}<div class="t"><b>{e(f["name"])}</b><span>{e(f["desc"])}</span></div></a>' for f in D['flavours'])}</div>
</div></section>

<section class="sec" id="story"><div class="wrap">
  <div class="split">
    <img src="img/s_ruby_koala.jpg" alt="A tray of freshly baked Caramello Koala cookies in Ruby’s kitchen" loading="lazy" width="1536" height="1536">
    <div class="txt">
      <span class="eyebrow">From Ruby &amp; Rachel · in their words, for them to approve</span>
      <h2>We’re so, so sorry.</h2>
      <p>We went from a few orders a day to hundreds overnight, and some of you waited way too long for your cookies. To everyone who stuck with us, we can’t thank you enough.</p>
      <p>So we’ve changed a few things. We’ve got a bigger team now, more hands in the kitchen and more hands packing, and we’re back to how the Cookiee Club used to be: 2 to 4 days.</p>
      <span class="sig">Ruby &amp; Rachel x</span>
    </div>
  </div>
  <div class="facts" id="kitchen">
    <div class="fact"><b>Nut free, egg free</b><span>No nuts in our house, ever, and none of our recipes use eggs. Some chocolates carry a “may contain”.</span></div>
    <div class="fact"><b>Gluten free, kept separate</b><span>GF cookies are baked in their own space, approved by our allergen specialist.</span></div>
    <div class="fact"><b>Registered to bake all week</b><span>Our health inspector checks in every year, sometimes unannounced. <span class="fill">[Council reg. no.]</span></span></div>
  </div>
  <p style="margin-top:22px"><a class="link" href="our-kitchen.html">Our kitchen and full allergen guide →</a></p>
</div></section>

<section class="sec ink" id="how"><div class="wrap">
  <div class="sec-head"><h2 style="color:var(--pink)">How ordering works now</h2></div>
  <div class="steps-grid">
    <ol class="steps">
      <li><b>You order.</b><span>Pick a box, choose your flavours, pay with card, Apple Pay, Shop Pay or Afterpay.</span></li>
      <li><b>We bake it for you.</b><span>Your cookies are baked to order and posted within 2 to 4 business days.</span></li>
      <li><b>Express post.</b><span>Usually 1 to 3 business days across Australia. One flat $16.20, whatever you order.</span></li>
      <li><b>We keep you posted.</b><span>An email when your order’s confirmed, when it’s in the oven and when it’s on its way.</span></li>
    </ol>
    <figure class="arrive"><img src="img/real_packbox.jpg" alt="A real Cookiee Club mailer opened to show hot pink tissue and a thank-you sticker" loading="lazy" width="1000" height="1000"><figcaption>Real box. Real photo.</figcaption></figure>
  </div>
</div></section>

{reviews_block()}

{calendar_block(B)}

{join_block()}

<section class="sec paper" id="faq"><div class="wrap">
  <div class="two-col" style="padding-bottom:0">
    <div><div class="sec-head" style="margin-bottom:24px"><h2>Good questions</h2></div>{faq_html(FAQS[:5], B)}</div>
    <aside class="aside"><b>Still wondering?</b><p>Everything about delivery, allergens, refunds and changing an order lives in Help.</p><a class="btn line" href="faq.html">All questions</a><a class="btn line" href="contact.html">Contact us</a></aside>
  </div>
</div></section>
'''
page('index.html', 'The Cookiee Club · Nut and egg free cookies, baked to order', home,
     'Nut and egg free cookies baked to order by sisters Ruby and Rachel. Build a box of 6 or 12, posted Australia wide in 2 to 4 days.')

# ---------- SHOP ----------
shop = f'''
<section class="page-head wrap"><h1>The menu.</h1><p>Six boxes and one extra. $16.20 express post, Australia wide.</p></section>
<section class="wrap" style="padding-bottom:88px">
  <div class="chips" role="group" aria-label="Filter the menu">
    <button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>
    <button class="chip" type="button" data-filter="build" aria-pressed="false">Build your own</button>
    <button class="chip" type="button" data-filter="seasonal" aria-pressed="false">Halloween</button>
    <button class="chip" type="button" data-filter="gf" aria-pressed="false">Gluten free</button>
    <button class="chip" type="button" data-filter="kids" aria-pressed="false">For kids</button>
    <button class="chip" type="button" data-filter="extras" aria-pressed="false">Extras</button>
  </div>
  <div class="grid cards-2">{''.join(card(P[i], B) for i in order + ['moulds'])}</div>
</section>
'''
page('shop.html', 'Shop the menu · The Cookiee Club', shop, 'Build your own box of 6 or 12, the Haunted Batch, gluten free cookies and more. Nut and egg free, posted Australia wide.', 'shop.html')

# ---------- PRODUCT PAGES ----------
for p in D['products']:
    B = '../'
    gal = ''.join(f'<img src="{B}img/p/{im}.jpg" alt="{e(p["alt"][i])}" {"fetchpriority=\"high\"" if i == 0 else "loading=\"lazy\""} width="1000" height="1000">' for i, im in enumerate(p['imgs']))
    gal += f'<img src="{B}img/real_packbox.jpg" alt="How it arrives: a mailer box with hot pink tissue and a thank-you sticker" loading="lazy" width="1000" height="1000">' if p['cookies'] else ''
    gal += '<p class="gal-note">Gallery photos are our real cookies.</p>'
    badge = f'<span class="tag static{" dark" if p.get("badgeDark") else ""}">{e(p["badge"])}</span>' if p.get('badge') else ''
    compare = f'<s>{money(p["compare"])}</s>' if p.get('compare') else ''
    count = f'{p["cookies"]} cookies · ' if p['cookies'] else ''
    pricebits = f'<div class="pr"><b id="pr-main">{money(p["price"])}</b>{compare}<span>{count}or 4 payments with Afterpay</span></div>'
    delivered = ''
    flist = ''
    if p.get('fixed'):
        flist = '<div><h2 style="font-size:22px;margin-bottom:12px">What’s in the box</h2><div class="flist">' + ''.join(
            f'<div class="fi"><span class="th">{flav_img(F[i], B, studio=True)}</span><div><b>{e(F[i]["name"])}{' <em class="bs">Best seller</em>' if F[i].get("best") else ''}</b><span>{e(F[i]["desc"])}</span></div></div>' for i in p['fixed']) + '</div></div>'
    variants = ''
    if p.get('variants'):
        variants = '<fieldset style="border:0;padding:0;margin:0"><legend style="font-weight:700;margin-bottom:8px">Choose</legend><div class="variants">' + ''.join(
            f'<label><input type="radio" name="variant" value="{v["id"]}"{" checked" if j == 0 else ""}><span>{e(v["name"])} · {money(v["price"])}</span></label>' for j, v in enumerate(p['variants'])) + '</div></fieldset>'
    if p.get('builder'):
        buy = (f'<a class="btn red block" id="choose-btn" href="{B}build-a-box.html?size={p["builder"]}">Choose your {p["builder"]} flavours</a>'
               f'<p class="muted" style="font-size:14px">Pick from {len(D["flavours"])} flavours. You’ll see your box fill up as you go.</p>')
        sticky = f'<div class="sticky-buy"><div><b>{e(p["name"])}</b><span>{money(p["price"])}</span></div><a class="btn red" href="{B}build-a-box.html?size={p["builder"]}">Choose flavours</a></div>'
    elif p['stock'] == 'in':
        lim = f'<p class="muted" style="font-size:14px">Limited to {p["limit"]} per customer.</p>' if p.get('limit') else ''
        buy = (f'{variants}<div class="buy"><div class="qty"><button type="button" id="q-minus" aria-label="Decrease quantity">−</button><output id="q-val" aria-live="polite">1</output>'
               f'<button type="button" id="q-plus" aria-label="Increase quantity">+</button></div><button class="btn red" type="button" id="add-btn">Add to cart</button></div>{lim}')
        sticky = f'<div class="sticky-buy"><div><b>{e(p["name"])}</b><span>{money(p["price"])}</span></div><button class="btn red" type="button" id="sticky-add">Add</button></div>'
    else:
        buy = (f'{variants}<div class="alert-box"><b>Sold out this week.</b><p>Next bake opens <span class="fill">[day] 7pm AEST</span>. Leave your email and we’ll tell you the moment it’s back.</p>'
               f'<form class="inline-form" data-form="alert" novalidate><label class="sr" for="al-email">Email address</label><input id="al-email" type="email" placeholder="Your email" autocomplete="email" required><button class="btn red" type="submit">Tell me</button></form><p class="form-msg" aria-live="polite"></p></div>')
        sticky = ''
    ship = (f'<div class="ship-line">{icon("clock", 22)}<span><b>Baked to order, posted within 2 to 4 business days.</b> Express post usually takes 1 to 3 more. Need it by a date? <a class="link" href="{B}contact.html">Ask before you order</a>.</span></div>') if p['cookies'] else (
            f'<div class="ship-line">{icon("clock", 22)}<span><b>Pre-order.</b> Dispatched within 5 to 7 days, then express post.</span></div>')
    acc_items = []
    if p['cookies']:
        acc_items.append(('What arrives', f'<p>{"Twelve" if p["cookies"]==12 else "Six" if p["cookies"]==6 else "Four"} flat, chewy cookies about <span class="fill">[size] cm</span> across, each sealed in its own bag, packed in hot pink tissue inside a mailer box.</p><p>Best within <span class="fill">[X]</span> days in an airtight container. <span class="fill">[Ruby’s warming tip]</span></p>'))
        gf = ' Our gluten-free cookies are baked in their own space, approved by our allergen specialist.' if 'gf' in p['group'] or p.get('variants') else ''
        acc_items.append(('Allergens', f'<p>Made in our nut and egg free kitchen: no nuts in the house, no eggs in our recipes.{gf}</p><p>Contains <span class="fill">[wheat, milk, soy: Ruby to confirm per flavour]</span>. Our chocolate (Cadbury and Nestlé) carries the manufacturer’s “may contain traces of nuts” statement.</p><p><a class="link" href="{B}our-kitchen.html#allergens">Full allergen guide</a></p>'))
    acc_items.append(('Delivery', '<p>Express post, $16.20 flat anywhere in Australia, whatever you order. Tracking is emailed when your parcel is posted. In hot weather, choose an address where someone can bring it inside.</p>'))
    acc_items.append(('Refunds and damage', f'<p>Cookies are made to order, so we can’t refund a change of mind. If anything arrives damaged, send a photo within 48 hours and we’ll replace or refund the damaged cookies. <a class="link" href="{B}refunds.html">Full policy</a>.</p>'))
    acc = '<div class="acc">' + ''.join(f'<details{" open" if j == 0 else ""}><summary>{t}</summary><div class="body">{b}</div></details>' for j, (t, b) in enumerate(acc_items)) + '</div>'
    others = [P[i] for i in order if i != p['id'] and P[i]['stock'] == 'in'][:3]
    more = f'<section class="sec paper"><div class="wrap"><div class="sec-head"><h2>Add one of these</h2><p>Same parcel, one shipping price.</p></div><div class="grid cards-2">{"".join(card(o, B) for o in others)}</div></div></section>'
    body = f'''
<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{B}index.html">Home</a> / <a href="{B}shop.html">Shop</a> / <span>{e(p["name"])}</span></nav>
<div class="pdp" data-pdp="{p["id"]}">
  <div class="gal">{gal}</div>
  <div class="info">
    {badge}
    <h1>{e(p["name"])}</h1>
    {pricebits}
    <p style="font-size:17px">{e(p["intro"])}</p>
    {delivered}
    {flist}
    {buy}
    {ship}
    {acc}
  </div>
</div></div>
{more}
{sticky}
'''
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p['name'], "description": p['intro'],
                     "brand": {"@type": "Brand", "name": "The Cookiee Club"},
                     "offers": {"@type": "Offer", "priceCurrency": "AUD", "price": f'{p["price"]:.2f}',
                                "availability": "https://schema.org/InStock" if p['stock'] == 'in' else "https://schema.org/OutOfStock"}})
    page(f'products/{p["handle"]}.html', f'{p["name"]} · The Cookiee Club', body, f'{p["name"]}: {p["short"]}. {p["intro"]}', 'shop.html',
         f'<script type="application/ld+json">{ld}</script>\n')

# ---------- BUILDER ----------
B = ''
fcards = ''.join(f'''<article class="fcard" data-card="{f["id"]}"><div class="pic">{flav_img(f, B, studio=True)}<span class="cnt" hidden>0</span>{f'<span class="ftag">{e(f["tag"])}</span>' if f.get("tag") else ''}{'<span class="ftag best">Best seller</span>' if f.get("best") else ''}</div>
<div class="t"><b>{e(f["name"])}</b><span>{e(f["desc"])}</span></div>
<div class="step-ctl"><button type="button" data-f="{f["id"]}" data-d="-1" aria-label="Remove one {e(f["name"])}">−</button><output aria-live="polite">0</output><button type="button" data-f="{f["id"]}" data-d="1" aria-label="Add one {e(f["name"])}">+</button></div></article>''' for f in D['flavours'])
b6, b12 = P['byo6'], P['byo12']
builder = f'''
<section class="wrap bld-head">
  <span class="eyebrow">Build your own</span>
  <h1 id="bld-title">Build your box of 6.</h1>
  <fieldset style="border:0;padding:0;margin:0"><legend class="sr">Box size</legend><div class="sizes">
    <label class="size"><input type="radio" name="size" value="6"><span><b>6 cookies · {money(b6["price"])}</b><small>Six of your favourites</small></span></label>
    <label class="size"><input type="radio" name="size" value="12"><span><b>12 cookies · {money(b12["price"])}</b><small>Twelve of your favourites</small></span></label>
  </div></fieldset>
</section>
<section class="wrap bld" id="builder">
  <div>
    <div class="tools"><button class="btn line" type="button" id="surprise">Surprise me</button><button class="btn line" type="button" id="clear">Start again</button></div>
    <div class="fgrid">{fcards}</div>
  </div>
  <aside class="summary" aria-label="Your box">
    <h2>Your box</h2>
    <div class="prog"><div class="lbl"><span class="prog-n">0 of 6</span><span>chosen</span></div><div class="bar"><i></i></div></div>
    <ul class="picked" id="picked"></ul>
    <div class="sum-price"><span>Box price</span><b id="sum-price">$39.95</b></div>
    <p class="sum-note">Plus $16.20 express post. Baked to order, posted within 2 to 4 business days.</p>
    <button class="btn red block bld-add" type="button" disabled>Pick 6 more</button>
  </aside>
</section>
<div class="bar-m" aria-hidden="false"><div class="c"><b class="prog-n">0 of 6</b><div class="bar"><i></i></div></div><button class="btn red bld-add" type="button" disabled>Pick 6 more</button></div>
'''
page('build-a-box.html', 'Build a box · The Cookiee Club', builder, 'Build your own box of 6 or 12 nut and egg free cookies. Pick from 11 flavours, posted Australia wide.', 'build-a-box.html')

# ---------- KITCHEN ----------
kitchen = f'''
<section class="page-head wrap"><span class="eyebrow">Our kitchen</span><h1>Made so more people can have one.</h1>
<p>The Cookiee Club was started by sisters Ruby and Rachel, from their mum’s recipe. Rachel lives with severe food allergies, so from day one the rule has been simple: nobody gets left out of the cookie box.</p></section>
<section class="wrap"><div class="split" style="padding-bottom:72px">
  <img src="img/s_ruby_koala.jpg" alt="Caramello Koala cookies cooling on a tray in Ruby’s kitchen" width="1536" height="1536" loading="lazy">
  <div class="txt"><h2>Two sisters, Mum’s recipe, a bigger team.</h2>
  <p>We went from a few orders a day to hundreds overnight. We’ve since grown the team, so more hands bake and more hands pack, and we’re back to posting within 2 to 4 business days.</p>
  <p class="muted"><span class="fill">[Ruby to add: where you bake, how the team works, a line from Mum]</span></p><span class="sig">Ruby &amp; Rachel x</span></div>
</div></section>
<section class="sec paper" id="allergens"><div class="wrap">
  <div class="sec-head"><h2>Allergen guide</h2><p>Straight answers, in plain words. If you have a severe allergy, <a class="link" href="contact.html">message us before you order</a>.</p></div>
  <div class="prose" style="padding-bottom:0;max-width:900px">
    <table><thead><tr><th>Allergen</th><th>In our kitchen?</th><th>Detail</th></tr></thead><tbody>
      <tr><td>Peanuts and tree nuts</td><td>No</td><td>We don’t handle nuts. Our chocolate (Cadbury Dairy Milk, Cadbury baking chips, Nestlé) carries the manufacturer’s “may contain traces of nuts” statement.</td></tr>
      <tr><td>Egg</td><td>No</td><td>None of our recipes use eggs.</td></tr>
      <tr><td>Gluten (wheat)</td><td>Yes</td><td>Most cookies contain wheat. The Gluten Free Range is baked in its own space, approved by our allergen specialist.</td></tr>
      <tr><td>Milk</td><td><span class="fill">[Ruby to confirm]</span></td><td>Milk chocolate and toppings contain milk.</td></tr>
      <tr><td>Soy</td><td><span class="fill">[Ruby to confirm]</span></td><td>Chocolate commonly contains soy lecithin.</td></tr>
    </tbody></table>
  </div>
  <div class="facts">
    <div class="fact"><b>Registered to bake all week</b><span>Our health inspector checks in every year, sometimes unannounced. <span class="fill">[Council reg. no.]</span></span></div>
    <div class="fact"><b>Gluten free, kept separate</b><span>Baked in their own space, approved by our allergen specialist.</span></div>
    <div class="fact"><b>Every flavour listed</b><span>Ingredients per flavour live on each product page. <span class="fill">[Ruby to supply]</span></span></div>
  </div>
</div></section>
'''
page('our-kitchen.html', 'Our kitchen and allergen guide · The Cookiee Club', kitchen, 'Nut and egg free kitchen, gluten free baked separately. The Cookiee Club allergen guide.', 'our-kitchen.html')

# ---------- DROPS ----------
drops = f'''
<section class="page-head wrap"><span class="eyebrow">Drops</span><h1>What’s baking next.</h1><p>Seasonal flavours, the Perth pop-up and 50 advent calendars. Join the club and we’ll email you before each one opens.</p></section>
{calendar_block('', head=False)}
<section class="sec paper"><div class="wrap two-col" style="padding-bottom:0">
  <div class="prose" style="padding-bottom:0"><h2>Advent calendars, 16 November</h2><p>We’re making 50. The club gets the link first, then whatever is left goes on Instagram and TikTok.</p>
  <h2>Perth pop-up, 12 to 15 November</h2><p>Our first interstate pop-up. <span class="fill">[Venue, times, what’s on the table]</span></p>
  <h2>The shop closes 16 November to 6 December</h2><p>We’re resting up before Christmas. We’re back on 6 December with every Christmas flavour.</p></div>
  <aside class="aside"><b>Get the drop emails</b><p>One email before each drop. Unsubscribe any time.</p><form class="inline-form" data-form="join" novalidate><label class="sr" for="dj">Email address</label><input id="dj" type="email" placeholder="Your email" required><button class="btn" type="submit">Sign up</button><p class="form-msg" aria-live="polite" style="flex-basis:100%;margin-top:10px"></p></form></aside>
</div></section>
'''
page('drops.html', 'Drops and calendar · The Cookiee Club', drops, 'Halloween, Christmas early release, the Perth pop-up and 50 advent calendars.', 'drops.html')

# ---------- HELP PAGES ----------
DRAFT = '<div class="draft">Draft policy for Ruby and Rachel to check and approve. Have the refund wording checked against the Australian Consumer Law before it goes live.</div>'
page('faq.html', 'Help and FAQ · The Cookiee Club', f'''
<section class="page-head wrap"><span class="eyebrow">Help</span><h1>Questions, answered.</h1><p>Can’t find it here? <a class="link" href="contact.html">Message us</a>.</p></section>
<section class="wrap two-col">{faq_html(FAQS, '')}<aside class="aside"><b>Quick links</b><a class="link" href="delivery.html">Delivery &amp; shipping</a><a class="link" href="refunds.html">Refunds &amp; damaged orders</a><a class="link" href="our-kitchen.html#allergens">Allergen guide</a><a class="link" href="contact.html">Contact us</a></aside></section>''',
     'Delivery times, allergens, shipping costs, refunds and more.', 'faq.html')

page('delivery.html', 'Delivery and shipping · The Cookiee Club', f'''
<section class="page-head wrap"><span class="eyebrow">Help</span><h1>Delivery &amp; shipping.</h1></section>
<section class="wrap prose">{DRAFT}
<table><tbody><tr><th>Where</th><td>Anywhere in Australia. We don’t ship overseas.</td></tr>
<tr><th>Cost</th><td>$16.20 express post, flat, whatever you order.</td></tr>
<tr><th>Baking</th><td>Every order is baked to order and posted within 2 to 4 business days.</td></tr>
<tr><th>Express post</th><td>Usually 1 to 3 business days after posting, depending on your location.</td></tr>
<tr><th>Tracking</th><td>Emailed when your parcel is posted. “Label created” means it hasn’t reached Australia Post yet.</td></tr></tbody></table>
<h2>Does express mean you bake it faster?</h2><p>No. Every order joins the same baking queue. Express applies once your cookies are with Australia Post.</p>
<h2>Need it by a date?</h2><p><a class="link" href="contact.html">Message us before you order</a> and we’ll tell you honestly if we can make it.</p>
<h2>Hot weather</h2><p>Choose an address where someone can bring the parcel inside. Missed deliveries go to your local post office; collect them as soon as you can.</p>
<h2>Wrong address?</h2><p>Message us straight away. We can usually fix a typo before your order is posted, but not after.</p></section>''',
     'Express post Australia wide for $16.20 flat. Baked to order and posted in 2 to 4 business days.')

page('refunds.html', 'Refunds and damaged orders · The Cookiee Club', f'''
<section class="page-head wrap"><span class="eyebrow">Help</span><h1>Refunds &amp; damaged orders.</h1></section>
<section class="wrap prose">{DRAFT}
<h2>Change of mind</h2><p>Every cookie is baked for your order, so we don’t offer refunds if you simply change your mind.</p>
<h2>Damaged, wrong or missing cookies</h2><p>If something isn’t right, send us your order number and a photo within 48 hours of delivery. We’ll replace or refund the affected cookies. You don’t need half the box to be broken.</p>
<h2>Lost parcels</h2><p>If tracking stops moving for <span class="fill">[X]</span> business days, contact us and we’ll chase it with Australia Post.</p>
<h2>Your rights</h2><p>Our goods come with guarantees that cannot be excluded under the Australian Consumer Law. Nothing in this policy limits those rights.</p>
<p><a class="btn" href="contact.html">Report a problem</a></p></section>''',
     'Change-of-mind, damaged cookies and lost parcels: how we put it right.')

page('contact.html', 'Contact us · The Cookiee Club', f'''
<section class="page-head wrap"><span class="eyebrow">Help</span><h1>Get in touch.</h1><p>The fastest way to reach us about an order. We reply within <span class="fill">[X]</span> business days.</p></section>
<section class="wrap two-col">
<form class="form" data-form="contact" novalidate>
  <label>Your name<input name="name" autocomplete="name" required></label>
  <label>Email<input type="email" name="email" autocomplete="email" required></label>
  <label>Order number (if you have one)<input name="order" placeholder="#1234"></label>
  <label>What’s it about?<select name="topic"><option>An order</option><option>Damaged or missing cookies</option><option>Allergens</option><option>A date I need it by</option><option>Something else</option></select></label>
  <label class="full">Message<textarea name="msg" required></textarea></label>
  <div class="full"><button class="btn red" type="submit">Send message</button><p class="form-msg" aria-live="polite" style="margin-top:12px"></p></div>
</form>
<aside class="aside"><b>Email</b><p><span class="fill">[hello@thecookieeclub.com]</span></p><b>Corporate and events</b><p><a class="link" href="corporate.html">Send an enquiry</a></p><b>Quick answers</b><p><a class="link" href="faq.html">Help and FAQ</a></p></aside>
</section>''', 'Contact The Cookiee Club about an order, allergens or a delivery date.')

page('corporate.html', 'Corporate and events · The Cookiee Club', f'''
<section class="page-head wrap"><span class="eyebrow">Corporate &amp; events</span><h1>Cookies for a crowd.</h1><p>Team thank-yous, client gifts and events. We bake in small batches, so tell us your date and numbers and we’ll reply honestly with what’s possible.</p></section>
<section class="wrap two-col">
<form class="form" data-form="corporate" novalidate>
  <label>Your name<input name="name" autocomplete="name" required></label>
  <label>Email<input type="email" name="email" autocomplete="email" required></label>
  <label>Company<input name="company" autocomplete="organization"></label>
  <label>Date needed<input type="date" name="date"></label>
  <label>How many boxes or cookies?<input name="qty" inputmode="numeric"></label>
  <label>Budget (optional)<input name="budget"></label>
  <label class="full">Any allergies we should know about?<input name="allergies"></label>
  <label class="full">Anything else<textarea name="msg"></textarea></label>
  <div class="full"><button class="btn red" type="submit">Send enquiry</button><p class="form-msg" aria-live="polite" style="margin-top:12px"></p></div>
</form>
<aside class="aside"><b>Good to know</b><p>Nut and egg free, so they’re safe for more of the office.</p><p>The shop closes 16 November to 6 December. Ask early for Christmas.</p></aside>
</section>''', 'Corporate gifts and event orders from The Cookiee Club.')

page('privacy.html', 'Privacy · The Cookiee Club', f'''<section class="page-head wrap"><h1>Privacy.</h1></section><section class="wrap prose"><div class="draft">Placeholder. The live site uses Ruby’s existing Shopify privacy policy.</div><p>We collect what we need to bake and post your order and, if you join the club, to email you about drops and restocks. We never sell your details.</p></section>''', 'Privacy policy.')
page('terms.html', 'Terms · The Cookiee Club', f'''<section class="page-head wrap"><h1>Terms.</h1></section><section class="wrap prose"><div class="draft">Placeholder for Shopify’s terms of service, to be written and approved by Ruby and Rachel.</div></section>''', 'Terms of service.')

# ---------- CART / CHECKOUT / 404 / NOTES ----------
page('cart.html', 'Your cart · The Cookiee Club', '<section class="page-head wrap"><h1>Your box.</h1></section><section class="wrap" id="cart-page" style="padding-bottom:88px"></section>', 'Your cart.')
page('checkout.html', 'Checkout · The Cookiee Club', '''<section class="page-head wrap"><span class="eyebrow">Concept</span><h1>Shopify checkout goes here.</h1><p>On the live store this button opens Shopify’s checkout: Shop Pay, Apple Pay, Google Pay, PayPal, Afterpay and cards. Nothing is charged in this concept.</p></section>
<section class="wrap two-col"><div class="aside" id="checkout-summary"></div><aside class="aside"><b>What happens next</b><p>1. Order confirmation email.</p><p>2. “In the oven” email when we start baking.</p><p>3. Tracking email when it’s posted.</p><a class="btn line" href="cart.html">Back to cart</a></aside></section>''', 'Checkout.')
page('404.html', 'Page not found · The Cookiee Club', '<section class="page-head wrap"><h1>This one crumbled.</h1><p>The page you wanted isn’t here.</p><p style="margin-top:24px"><a class="btn" href="/index.html">Back to the menu</a></p></section>', 'Not found.')
print('built', len(D['products']), 'products')

# ---------- CONCEPT NOTES ----------
notes = '''
<section class="page-head wrap"><span class="eyebrow">Concept notes · The Service Edit</span><h1>What’s new in v2.</h1><p>Same look as v1. Underneath, it’s now a full store you can click through: every product, a working box builder, a cart and every help page.</p></section>
<section class="wrap prose">
<h2>Changed from v1</h2>
<ul>
<li>Removed the made-up “boxes left” count and the example bake dates. Delivery is stated as a rule: baked and posted within 2 to 4 business days, then express post.</li>
<li>Added the Build Your Own (12) and The Little Cookiee Club, both live on Ruby’s store since 11 October. Imperfect Gluten Free is now an option on the Imperfect Box.</li>
<li>One layout for every screen. v1 had a separate phone version that dropped the kitchen facts and the calendar; both now show on phones.</li>
<li>A real box builder: photo cards, + and − per flavour, “4 of 6” progress, Surprise me, and “Edit flavours” from the cart.</li>
<li>The cart offers one upgrade: a 6-box to a 12-box, keeping the flavours already picked.</li>
<li>Sold-out products swap the buy button for a restock alert form (the Imperfect Box shows this in the demo).</li>
<li>Product pages: real photos only, what’s in the box, allergens, delivery and refunds, and a sticky add-to-cart bar on phones.</li>
<li>New pages: Our kitchen and allergen guide, Drops, Delivery, Refunds, FAQ, Contact, Corporate, Cart.</li>
<li>Removed the unverified “Most ordered” label. Badges now state facts only.</li>
<li>The AI hero image is kept as it was.</li>
<li>Flavour images in “Pick your flavours” and the box builder are studio shots in v1’s menu style, made with Higgsfield (Nano Banana Pro) from Ruby’s real photo of each cookie. Product page galleries still use her untouched photos; the “What’s in the box” thumbnails use the studio shots.</li>
</ul>
<h2>Still needed from Ruby</h2>
<ul>
<li>Restock day and time, cookie size, shelf life and her warming tip.</li>
<li>Allergens per flavour (milk, soy, wheat) and the council registration number.</li>
<li>Confirm the flavour shots for Cinnamon Scroll, Biscoff White Choco, Oreo Milkshake and Plain Vanilla. They were made from her photos, but I matched which cookie is which by eye.</li>
<li>Confirm which Halloween photo is which flavour (matched from her product photos).</li>
<li>Contact email, ABN, Perth pop-up venue, reply time, and whether shipping is flat $16.20 or weight-based.</li>
<li>Sign-off on the delivery and refund drafts, and whether Afterpay is switched on.</li>
</ul>
<h2>Demo only</h2>
<ul><li>Stock states are set by hand. Forms show a thank-you but send nothing. Checkout stops at a placeholder page. In Shopify all of this comes from the platform.</li></ul>
</section>'''
page('notes.html', 'Concept notes · The Cookiee Club v2', notes, 'What changed in v2 of the concept.')
print('notes built')
