#!/usr/bin/env python3
"""Builds the local landing pages in public/<slug>/index.html.
Re-run after design changes to index.html: python3 tools/gen_local_pages.py
Style, header and footer are copied from public/index.html so the pages always match."""
import re, json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(f"{ROOT}/public/index.html", encoding="utf-8").read()
style = re.search(r"<style>.*?</style>", src, re.S).group(0)
header = re.search(r"<header>.*?</header>", src, re.S).group(0).replace("<header>", '<header data-v="9">', 1)
header = header.replace('<div class="logo">', '<a class="logo" href="/" style="color:inherit;text-decoration:none">', 1)
header = header.replace('</div>\n<div class="brandbox">', '</a>\n<div class="brandbox">', 1)
footer = re.search(r"<footer>.*?</footer>", src, re.S).group(0)
fonts = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;600;800&display=swap" rel="stylesheet">'
beacon = re.search(r"<!-- Cloudflare Web Analytics -->.*", src, re.S)
beacon = beacon.group(0).split("</body>")[0].strip() if beacon else ""
SITE = "https://exoticearthworks.com.au"
PAGES = [
 dict(slug="mini-excavator-hire-central-coast", area="Central Coast",
  title="Mini Excavator Hire Central Coast NSW | Exotic Earthworks",
  desc="1.8 tonne mini excavator hire on the Central Coast. Dry hire from $100/day or wet hire with an operator. Delivery to Gosford, Wyong, Terrigal, The Entrance and more.",
  h1="Mini Excavator Hire on the Central Coast",
  lead="Hire a 1.8 tonne mini excavator with trailer, delivered anywhere on the Central Coast. Do the job yourself with dry hire from $100 per day, or have an experienced operator do it for you with wet hire.",
  intro=["The Central Coast is full of sloping blocks, tight side access and sandy or clay soil, which is exactly what a compact machine suits. Our UHI UME18 is only 990 mm wide with the tracks retracted, so it fits through most side gates and narrow access points, then extends to 1,240 mm for stability once it is in the yard.",
         "We deliver the excavator and trailer to your site and collect it when you are done. Pick your dates on the calendar, pay your deposit online and we confirm your booking."],
  places=["Gosford","Erina","Terrigal","Avoca Beach","Kincumber","Woy Woy","Umina Beach","Ettalong","Narara","Lisarow","Wyong","Tuggerah","The Entrance","Wyoming","Toukley","Budgewoi"],
  placenote="Not on the list? Ask us. If you are on the Central Coast we will almost certainly be able to deliver.",
  delivery="Central Coast is outside Sydney metro, so drop off is $75.",
  jobs=["Pool and spa digs","Drainage and trenching","Retaining wall and slab prep","Levelling and site prep","Post holes and footings","Tree stump and hedge removal","Garden beds and landscaping","Soil and rubble moving"],
  faq=[("How much is mini excavator hire on the Central Coast?","Dry hire (machine only, you operate it) is $100 per day with a 2 day minimum, plus a $250 deposit that comes off your total hire cost. Drop off to the Central Coast is $75. Wet hire with an operator is quoted per job, and quotes are free."),
       ("Will it fit through my side gate?","The machine is 990 mm wide with the tracks retracted, so it fits through most standard side gates and narrow access points. Measure your narrowest gap and message us if you are unsure."),
       ("Do you deliver to Gosford, Wyong and The Entrance?","Yes. We deliver across the Central Coast, including Gosford, Erina, Terrigal, Woy Woy, Wyong, Tuggerah and The Entrance."),
       ("Can I hire an operator?","Yes. Wet hire means we bring the machine and an experienced operator. Tell us about the job and we will send a free quote.")]),
 dict(slug="mini-excavator-hire-sydney", area="Sydney",
  title="Mini Excavator Hire Sydney | Dry or Wet Hire | Exotic Earthworks",
  desc="1.8 tonne mini excavator hire across Sydney. Dry hire from $100/day or wet hire with an experienced operator. Delivery included in the booking. Book online.",
  h1="Mini Excavator Hire in Sydney",
  lead="A 1.8 tonne mini excavator with trailer, delivered across Sydney. Dry hire from $100 per day, or wet hire with an experienced operator. Book online in a couple of minutes.",
  intro=["Sydney backyards are tight, and a full-size machine often will not get in. Our UHI UME18 is 990 mm wide with the tracks retracted, so it goes through standard side gates and narrow access, then extends to 1,240 mm for stability while it works.",
         "Choose dry hire if you are happy to operate it yourself, or wet hire if you would like us to bring an operator. Either way the machine and trailer come to you."],
  places=["Sydney metro (postcodes 2000 to 2234)","Inner West","Eastern suburbs","North Shore","Northern Beaches","Sutherland Shire","St George","Parramatta and Hills District","Penrith and Blacktown","Hawkesbury"],
  placenote="If your suburb is not listed, ask us. We service Sydney and the Central Coast.",
  delivery="Drop off is $50 within Sydney metro (postcodes 2000 to 2234) and $75 outside Sydney metro.",
  jobs=["Pool and spa digs","Drainage and trenching","Retaining wall and slab prep","Levelling and site prep","Post holes and footings","Tree stump and hedge removal","Garden beds and landscaping","Soil and rubble moving"],
  faq=[("How much does it cost to hire a mini excavator in Sydney?","Dry hire is $100 per day with a 2 day minimum, plus a $250 deposit that comes off your total hire cost. Drop off is $50 within Sydney metro or $75 outside it. Wet hire with an operator is quoted per job, and quotes are free."),
       ("What is the difference between dry hire and wet hire?","Dry hire is the machine only and you operate it. Wet hire means we bring the machine and an experienced operator, so you do not need to operate it yourself."),
       ("What attachments are available?","Eight attachments: 200, 400 and 600 mm digging buckets, a 1000 mm mud bucket, thumb grab, ripper, rake and quick hitch."),
       ("How do I pay?","The $250 deposit is paid online when you confirm your booking, by card or Afterpay through Square, or with PayPal. The rest of your hire is due 24 hours before delivery.")]),
 dict(slug="excavator-hire-western-sydney", area="Western Sydney",
  title="Excavator Hire Western Sydney | Penrith & Hawkesbury | Exotic Earthworks",
  desc="Mini excavator hire in Western Sydney, based in Londonderry. Dry hire from $100/day or wet hire with an operator. Delivery to Penrith, Richmond, Windsor, Blacktown and more.",
  h1="Excavator Hire in Western Sydney",
  lead="We are based in Londonderry, so the 1.8 tonne mini excavator is close to Penrith, Richmond, Windsor, Blacktown and the Hawkesbury. Dry hire from $100 per day, or wet hire with an experienced operator.",
  intro=["Acreage blocks, new builds and backyard renovations across Western Sydney all call for a machine that is easy to move and easy to get into. The UHI UME18 mini excavator fits through 990 mm gaps, and the expandable tracks give it a wide, stable stance when you are digging.",
         "Delivery and pick-up on the trailer are part of the booking. Choose your dates, pay the deposit online and we confirm."],
  places=["Penrith","Londonderry","Richmond","Windsor","St Marys","Blacktown","Castle Hill","Parramatta","Kellyville","Camden","Hawkesbury"],
  placenote="Not on the list? Ask us. We service Sydney and the Central Coast.",
  delivery="Drop off is $50 within Sydney metro (postcodes 2000 to 2234) and $75 outside Sydney metro, so your price depends on your postcode.",
  jobs=["Pool and spa digs","Drainage and trenching","Post holes and footings","Levelling and site prep","Retaining wall and slab prep","Tree stump and hedge removal","Garden beds and landscaping","Soil and rubble moving"],
  faq=[("Where are you based?","We are based in Londonderry in Western Sydney and deliver across Sydney and the Central Coast."),
       ("How much is excavator hire in Western Sydney?","Dry hire is $100 per day with a 2 day minimum, plus a $250 deposit that comes off your total hire cost. Drop off is $50 within Sydney metro or $75 outside it, depending on your postcode. Wet hire with an operator is quoted per job, and quotes are free."),
       ("Can you deliver to Penrith, Richmond and Windsor?","Yes. Delivery covers Western Sydney and the Hawkesbury, along with the rest of Sydney and the Central Coast."),
       ("Can I hire an operator?","Yes. Wet hire means we bring the machine and an experienced operator. Tell us about the job and we will send a free quote.")]),
]
e = html.escape
def page(p):
    others = [q for q in PAGES if q is not p]
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"HomeAndConstructionBusiness","name":"Exotic Earthworks","url":SITE+"/","logo":SITE+"/img/logo.jpg","image":SITE+"/og.jpg",
       "areaServed":[{"@type":"Place","name":p["area"]}],"priceRange":"$$",
       "sameAs":["https://www.facebook.com/p/Exotic-Earthworks-61579664133200/","https://www.instagram.com/exoticearthworks/"]},
      {"@type":"Service","name":p["h1"],"provider":{"@type":"HomeAndConstructionBusiness","name":"Exotic Earthworks","url":SITE+"/"},
       "areaServed":p["area"],"offers":{"@type":"Offer","price":"100","priceCurrency":"AUD","unitText":"day","description":"Dry hire of a 1.8 tonne mini excavator with trailer"}},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]}]}
    url = f"{SITE}/{p['slug']}/"
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="dark">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Exotic Earthworks">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.jpg">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{fonts}
{style}
<style>.lp .hero{{padding:28px 0 8px}}.lp ul.tick{{list-style:none;padding:0;margin:12px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:8px}}.lp ul.tick li{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}}.lp .two{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));margin-top:14px}}.lp .two .card{{margin:0}}.lp details{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-top:10px}}.lp summary{{cursor:pointer;font-weight:700}}.lp details p{{margin:8px 0 0}}.lp .links a{{margin-right:14px}}.lp .cta{{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap}}</style>
</head>
<body class="lp">
{header}
<main class="wrap">
<div class="hero">
<div>
<h1>{e(p['h1'])}</h1>
<p class="muted">{e(p['lead'])}</p>
<div class="cta"><a class="btn" href="/#choose">Check dates &amp; book</a><a class="btn alt" href="/#choose">Free wet hire quote</a></div>
</div>
<div class="photo"><img src="/img/photo-09.jpg" fetchpriority="high" alt="1.8 tonne mini excavator available for hire in {e(p['area'])}" width="700" height="875" style="width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;background:var(--card);border-radius:10px;display:block"></div>
</div>

<section>
<h2>Mini excavator hire in {e(p['area'])}</h2>
{''.join(f'<p>{e(t)}</p>' for t in p['intro'])}
</section>

<section>
<h2>Dry hire or wet hire</h2>
<div class="two">
<div class="card"><h3 style="margin:0 0 6px">Dry hire</h3><p class="muted" style="margin:0">Machine and trailer, you operate it. From <b>$100 per day</b> (2 day minimum) plus a $250 deposit that comes off your total. {e(p['delivery'])}</p></div>
<div class="card"><h3 style="margin:0 0 6px">Wet hire</h3><p class="muted" style="margin:0">We bring the machine and an experienced operator. Priced per job, and quotes are free.</p></div>
</div>
<div class="cta"><a class="btn" href="/#choose">Book now</a></div>
</section>

<section>
<h2>Great for</h2>
<ul class="tick">{''.join(f'<li>{e(j)}</li>' for j in p['jobs'])}</ul>
</section>

<section>
<h2>The machine</h2>
<p class="muted">UHI UME18 1.8 tonne mini excavator with a Kubota diesel engine and expandable tracks. Eight attachments are available: 200, 400 and 600 mm digging buckets, a 1000 mm mud bucket, thumb grab, ripper, rake and quick hitch.</p>
<div class="specs">
<div class="spec"><b>Operating weight</b>1,800 kg</div>
<div class="spec"><b>Width, tracks retracted</b>990 mm</div>
<div class="spec"><b>Width, tracks extended</b>1,240 mm</div>
<div class="spec"><b>Max dig depth</b>2,150 mm</div>
</div>
</section>

<section>
<h2>Where we deliver in {e(p['area'])}</h2>
<p class="muted">{', '.join(e(x) for x in p['places'])}.</p>
<p class="muted">{e(p['placenote'])}</p>
</section>

<section>
<h2>Questions</h2>
{''.join(f'<details><summary>{e(q)}</summary><p class="muted">{e(a)}</p></details>' for q,a in p['faq'])}
</section>

<section>
<h2>Ready to book?</h2>
<p class="muted">Pick your dates, choose dry or wet hire and pay your deposit online. We confirm your booking and arrange delivery.</p>
<div class="cta"><a class="btn" href="/#choose">Check dates &amp; book</a></div>
<p class="links muted" style="margin-top:18px">Also see: {''.join(f'<a href="/{q["slug"]}/">{e(q["area"])}</a>' for q in others)}<a href="/">Home</a></p>
</section>
</main>

{footer}
{beacon}
</body>
</html>
"""
for p in PAGES:
    d = f"{ROOT}/public/{p['slug']}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w", encoding="utf-8").write(page(p))
    print("wrote", p["slug"])
# sitemap
urls = [SITE + "/"] + [f"{SITE}/{p['slug']}/" for p in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-11-12</lastmod>\n  </url>\n" for u in urls) + "</urlset>\n"
open(f"{ROOT}/public/sitemap.xml", "w", encoding="utf-8").write(sm)
