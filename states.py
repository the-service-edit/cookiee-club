# Sold out and closed states. Run from build.py (shares its helpers).
# On Shopify these switch on automatically: sold out when every box is out of stock,
# closed between the break dates set in the theme settings.

def ring(text, days, label='days'):
    t = e(text)
    return f'''<div class="st-badge" aria-hidden="true">
  <svg viewBox="0 0 200 200" class="st-ring"><defs><path id="st-c" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
    <circle cx="100" cy="100" r="96" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="1.6" stroke-dasharray="4 5"/>
    <text><textPath href="#st-c" textLength="488" lengthAdjust="spacing">{t} • {t} •</textPath></text></svg>
  <div class="st-badge-in"><b data-st-days>{days}</b><span>{label}</span><small data-st-clock>00:00:00</small></div>
</div>'''

def st_hero(kind, word1, word2, img, alt, title, body, pill, target, form_btn, form_note, ring_text, ring_days, tag='', kick=''):
    return f'''
<section class="st-hero st-{kind}" data-st-target="{target}">
  <div class="wrap st-grid">
    <div class="st-copy">
      <h1 class="st-big">{f'<span class="st-kick">{kick}</span>' if kick else ''}<span class="r">{word1}</span><span>{word2}</span></h1>
      <div class="st-card">
        {ring(ring_text, ring_days)}
        <h2>{title}</h2>
        <p>{body}</p>
        <p class="st-pill" data-st-pill>{pill}</p>
        <form class="inline-form" data-form="alert" novalidate><label class="sr" for="st-email">Email address</label><input id="st-email" type="email" placeholder="Your email" autocomplete="email" required><button class="btn" type="submit">{form_btn}</button></form>
        <p class="form-msg" aria-live="polite"></p>
        <p class="st-note">{form_note}</p>
      </div>
    </div>
    <div class="st-pic">{tag}<img src="img/{img}" alt="{e(alt)}" width="1600" height="2000" fetchpriority="high"></div>
  </div>
</section>'''

# ---------- SOLD OUT ----------
back = [F[i] for i in ['caramello-koala', 'mini-mm', 'fairy-bread', 'cinnamon-scroll', 'biscoff-white-choco', 'oreo-milkshake']]
back_cards = ''.join(f'<a class="st-fl" href="shop.html">{flav_img(f, "", studio=True)}{"<span class=\"tag\">Best seller</span>" if f.get("best") else ""}<b>{e(f["name"])}</b></a>' for f in back)
sold = st_hero('sold', 'Sold', 'out.', 's_soldout.jpg', 'A hand holding a bitten Caramello Koala cookie, crumbs falling',
               'That’s tonight’s cookies <em>all gone.</em>',
               'Thank you so, so much. The next restock opens Sunday at 7pm Sydney time.',
               'Counting down to the next restock…', 'sunday', 'Tell me first',
               'One email when the shop opens. Nothing else unless you join the club.',
               'Next restock · Sunday 7pm', 5, kick='The Cookiee Club is') + f'''
<section class="st-ordered"><div class="wrap">
  <span class="st-tick" aria-hidden="true">{icon('check', 22, 2.4)}</span>
  <div><b>Ordered tonight? You’re all set.</b><p>Your order confirmation is in your inbox now, and tracking comes as soon as your box is posted. Can’t see it? Check your junk folder, then flick us a message.</p></div>
  <a class="btn pinkbtn" href="contact.html">Check my order</a>
</div></section>
<section class="sec cream"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Back on Sunday</span><h2>What’s coming back</h2></div><div class="side"><p>Pick your flavours now, so you’re in and out fast at 7pm.</p><a class="btn line" href="shop.html">See the full menu</a></div></div>
  <div class="st-flgrid">{back_cards}</div>
</div></section>
'''
page('sold-out.html', 'Sold out tonight · The Cookiee Club', sold,
     'Tonight’s cookies are gone. The next restock opens Sunday at 7pm Sydney time.', '',
     band_items=['Sold out tonight', 'Next restock Sunday 7pm Sydney time', 'Get the email, don’t miss out', 'Baked to order', 'Nut &amp; egg free'])

# ---------- CLOSED ----------
fav = [F[i] for i in ['caramello-koala', 'mini-mm', 'fairy-bread', 'cinnamon-scroll']]
come = ''.join(f'<a class="st-fl" href="shop.html">{flav_img(f, "", studio=True)}<span class="tag">Back 6 Dec</span><b>{e(f["name"])}</b></a>' for f in fav)
come += ''.join(f'<a class="st-fl st-myst" href="#st-email"><span class="ph">{flav_img(F[i], "", studio=True)}<i aria-hidden="true">?</i></span><span class="tag">New for Christmas</span><b>Top secret</b></a>' for i in ['gingerbread-white-choc', 'santas-mix'])
closed = st_hero('closed', 'On a', 'break.', 's_closed.jpg', 'An open Cookiee Club mailer box with hot pink tissue and a thank you sticker',
                 'Back Sunday 6 December, <em>7pm.</em>',
                 'We’re closed from 16 November to rest up and get the kitchen ready for Christmas. Thank you so, so much for an incredible few months.',
                 'Counting down to Christmas…', '2026-12-06T19:00', 'Get the reopening email',
                 'The list sees the Christmas flavours first.', 'Back 6 Dec · 7pm Sydney', 40,
                 tag='<span class="st-tag">Back 6 Dec</span>', kick='The Cookiee Club is') + f'''
<section class="st-ordered"><div class="wrap">
  <span class="st-tick" aria-hidden="true">{icon('check', 22, 2.4)}</span>
  <div><b>Ordered before 16 November? It’s on its way.</b><p>Every order placed before the break is baked and posted as normal, and tracking comes as soon as your box is posted. Messages are a little slower while we’re away.</p></div>
  <a class="btn pinkbtn" href="contact.html">Check my order</a>
</div></section>
<section class="sec cream"><div class="wrap">
  <div class="sec-head"><div><span class="eyebrow">Back on 6 December</span><h2>What’s coming back</h2></div><div class="side"><p>All your favourites, plus brand new Christmas flavours. The list sees them first.</p><a class="btn" href="#st-email">Get the reopening email</a></div></div>
  <div class="st-flgrid">{come}</div>
</div></section>
'''
page('closed.html', 'On a break until 6 December · The Cookiee Club', closed,
     'We’re closed from 16 November and back on 6 December at 7pm Sydney time with Christmas.', '',
     band_items=['On a break until 6 December', 'Christmas reopening 6 Dec, 7pm Sydney time', 'Get the reopening email', 'Mum’s recipe', 'Nut &amp; egg free'])
print('state pages built')
