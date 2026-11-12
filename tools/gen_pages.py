#!/usr/bin/env python3
"""Builds About us, Our services and Contact us pages into public/<slug>/index.html.
Style, header and footer are copied from public/index.html. Re-run after design changes:
  python3 tools/gen_pages.py"""
import re, os, html, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(f"{ROOT}/public/index.html", encoding="utf-8").read()
style = re.search(r"<style>.*?</style>", src, re.S).group(0)
header = re.search(r"<header>.*?</header>", src, re.S).group(0).replace("<header>", '<header data-v="9">', 1)
m2 = re.search(r'(<span class="lg1">.*?</span> <span class="lg2">.*?</span>)', header, re.S)
header = header.replace(m2.group(1), '<a href="/" style="color:inherit;text-decoration:none">' + m2.group(1) + '</a>', 1)
footer = re.search(r"<footer>.*?</footer>", src, re.S).group(0)
fonts = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;600;800&display=swap" rel="stylesheet">'
m = re.search(r"<!-- Cloudflare Web Analytics -->.*?</script>", src, re.S)
beacon = m.group(0) if m else ""
SITE = "https://exoticearthworks.com.au"
FB = "https://www.facebook.com/p/Exotic-Earthworks-61579664133200/"
IG = "https://www.instagram.com/exoticearthworks/"
MSG = "https://m.me/61579664133200"
e = html.escape
EXTRA = """<style>.lp .hero{display:block;padding:28px 0 4px}.lp ul.tick{list-style:none;padding:0;margin:12px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}.lp ul.tick li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}.lp .two{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));margin-top:14px}.lp .two .card{margin:0}.lp .cta{margin-top:16px;display:flex;gap:10px;flex-wrap:wrap}.lp .sv{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));margin-top:14px}.lp .sv .card{margin:0;padding:0;overflow:hidden}.lp .sv img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}.lp .sv .t{padding:12px 14px}.lp .sv .t b{display:block}.lp .sv .noimg{padding:16px 14px}.lp .sv .noimg b{display:block}.lp form label{display:block;margin-top:12px;font-weight:600;font-size:14px}.lp form input,.lp form textarea{width:100%}.lp #cmsg{margin-top:12px}.lp main a:not(.btn){color:var(--accent-light);text-underline-offset:3px}</style>"""


def shell(slug, title, desc, body, script=""):
    url = f"{SITE}/{slug}/"
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="color-scheme" content="dark">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Exotic Earthworks">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.jpg">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
{fonts}
{style}
{EXTRA}
</head>
<body class="lp">
{header}
<main class="wrap">
{body}
</main>

{footer}
{script}
{beacon}
</body>
</html>
"""


BOOK = '<div class="cta"><a class="btn" href="/#choose">Check dates &amp; book</a><a class="btn alt" href="/contact/">Contact us</a></div>'

about = f"""<div class="hero"><div>
<h1>About Exotic Earthworks</h1>
<p class="muted">Excavator hire, landscaping, plumbing support and construction services across Sydney and the Central Coast.</p>
</div></div>
<section>
<h2>Who we are</h2>
<p>Exotic Earthworks is a local earthworks and excavator hire business based in Londonderry, servicing Sydney and the Central Coast. We hire out a 1.8 tonne mini excavator with trailer, and we also take on jobs with an experienced operator.</p>
<p>Whether you want to do the digging yourself or have someone do it for you, we aim to make it simple: pick your dates, choose your attachments, pay your deposit online and we deliver the machine to your site.</p>
</section>
<section>
<h2>What we do</h2>
<ul class="tick"><li><b>Excavator hire</b><br><span class="muted">Dry hire from $100 per day, or wet hire with an operator.</span></li>
<li><b>Landscaping</b><br><span class="muted">Garden beds, levelling, turf removal and soil moving.</span></li>
<li><b>Plumbing support</b><br><span class="muted">Digging for pipe, water and sewer lines.</span></li>
<li><b>Construction services</b><br><span class="muted">Site prep, footings, retaining wall and slab prep.</span></li></ul>
</section>
<section>
<h2>Why a mini excavator</h2>
<p>Our UHI UME18 is only 990 mm wide with the tracks retracted, so it fits through most side gates and narrow access points where a bigger machine can&rsquo;t go. It has a Kubota diesel engine, expandable tracks for stability, and eight attachments available.</p>
</section>
<section>
<h2>Where we work</h2>
<p class="muted">We service Sydney and the Central Coast. Drop off is $50 within Sydney metro and $75 outside Sydney metro. Not sure if we cover your suburb? <a href="/contact/">Ask us</a>.</p>
{BOOK}
</section>"""

SVC = [
    ("Trenching & drainage", "Stormwater, ag drains, pipe and cable trenches.", None),
    ("Pool & spa digs", "Small plunge pools, spas and tight-access excavation.", "svc-pool-spa-digs.jpg"),
    ("Tree stump & hedge removal", "Dig out and clear tree stumps, hedges and roots.", "svc-tree-stump-hedge-removal.jpg"),
    ("Levelling & site prep", "Shape yards and prepare for slabs, sheds and paving.", "svc-levelling-site-prep.jpg"),
    ("Post holes & footings", "Fences, decks, pergolas and posts.", "svc-post-holes-footings.jpg"),
    ("Garden beds & landscaping", "Shaping, turf removal and moving soil.", None),
    ("Retaining wall & slab prep", "Dig-outs and base preparation.", "svc-retaining-wall-slab-prep.jpg"),
    ("Soil, rubble & spoil moving", "Shift and load material around your site.", "svc-soil-rubble-spoil-moving.jpg"),
    ("Plumbing support", "Digging for pipe, water and sewer lines.", "svc-plumbing-support.jpg"),
]
cards = ""
for t, d, im in SVC:
    if im:
        cards += f'<div class="card"><img src="/img/{im}" alt="{e(t)}" width="800" height="600" ><div class="t"><b>{e(t)}</b><span class="muted">{e(d)}</span></div></div>'
    else:
        cards += f'<div class="card"><div class="noimg"><b>{e(t)}</b><span class="muted">{e(d)}</span></div></div>'

services = f"""<div class="hero"><div>
<h1>Our services</h1>
<p class="muted">Hire the excavator yourself, or have our experienced operator do the job for you. Wet hire is quoted per job and quotes are free.</p>
{BOOK}
</div></div>
<section>
<h2>Wet hire: with an operator</h2>
<div class="sv">{cards}</div>
<p class="muted" style="margin-top:14px">Something else? Tell us about the job and we&rsquo;ll let you know if we can help.</p>
<div class="cta"><a class="btn" href="/#choose">Request a free quote</a></div>
</section>
<section>
<h2>Dry hire: you operate</h2>
<div class="two">
<div class="card"><h3 style="margin:0 0 6px">1.8 tonne mini excavator with trailer</h3><p class="muted" style="margin:0">From <b>$100 per day</b> (2 day minimum) plus a $250 deposit that comes off your total hire cost. Drop off is $50 within Sydney metro or $75 outside Sydney metro.</p></div>
<div class="card"><h3 style="margin:0 0 6px">Eight attachments available</h3><p class="muted" style="margin:0">200, 400 and 600 mm digging buckets, a 1000 mm mud bucket, thumb grab, ripper, rake and quick hitch.</p></div>
</div>
<div class="cta"><a class="btn" href="/#choose">Check dates &amp; book</a></div>
</section>"""

contact = f"""<div class="hero"><div>
<h1>Contact us</h1>
<p class="muted">Questions about hire, delivery or a quote? Send us a message and we&rsquo;ll get back to you as soon as we can.</p>
</div></div>
<section>
<h2>Message us</h2>
<div class="two">
<div class="card"><h3 style="margin:0 0 6px">Facebook Messenger</h3><p class="muted" style="margin:0 0 12px">The quickest way to reach us.</p><a class="btn" href="{MSG}" target="_blank" rel="noopener">Open Messenger</a></div>
<div class="card"><h3 style="margin:0 0 6px">Social</h3><p class="muted" style="margin:0"><a href="{FB}" target="_blank" rel="noopener">Facebook</a> &middot; <a href="{IG}" target="_blank" rel="noopener">Instagram</a></p><p class="muted" style="margin:10px 0 0">Service area: Sydney &amp; Central Coast</p></div>
</div>
</section>
<section>
<h2>Send an enquiry</h2>
<div class="card"><form id="cf" novalidate>
<label for="cname">Name</label><input type="text" id="cname" autocomplete="name">
<label for="cphone">Mobile (optional)</label><input type="tel" id="cphone" autocomplete="tel" inputmode="tel" placeholder="04XX XXX XXX">
<label for="cemail">Email</label><input type="email" id="cemail" autocomplete="email">
<label for="cmsgtxt">Message</label><textarea id="cmsgtxt" rows="5" maxlength="2000" placeholder="e.g. Do you deliver to Terrigal next weekend?"></textarea>
<p style="margin-top:16px"><button class="btn" type="submit" id="csend">Send enquiry</button></p>
<div id="cmsg" role="status"></div>
</form></div>
<p class="muted" style="margin-top:16px">Ready to hire? <a href="/#choose">Check dates &amp; book online</a>.</p>
</section>"""

cscript = """<script>
(function(){var f=document.getElementById("cf"),m=document.getElementById("cmsg"),b=document.getElementById("csend");
var fail="Sorry, that didn\\u2019t send. Please message us on <a href=\\"https://m.me/61579664133200\\" target=\\"_blank\\" rel=\\"noopener\\">Facebook Messenger</a> instead.";
f.addEventListener("submit",function(ev){ev.preventDefault();
var n=document.getElementById("cname").value.trim(),p=document.getElementById("cphone").value.trim(),em=document.getElementById("cemail").value.trim(),t=document.getElementById("cmsgtxt").value.trim();
if(!n||!t||(!em&&!p)){m.textContent="Please add your name, a message, and an email or mobile so we can reply.";return}
if(em&&!/^[^\\s@<>]+@[^\\s@<>]+\\.[^\\s@<>]+$/.test(em)){m.textContent="Please check your email address.";return}
b.disabled=true;m.textContent="Sending\\u2026";
var body="Website enquiry\\n\\nName: "+n+"\\nMobile: "+(p||"-")+"\\nEmail: "+(em||"-")+"\\n\\nMessage:\\n"+t;
fetch("/api/send",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({subject:"Website enquiry from "+n,message:body,replyTo:em,auto:""})}).then(function(r){return r.json()}).then(function(j){
if(j&&j.success){m.textContent="Thanks "+n+", your message has been sent. We\\u2019ll get back to you as soon as we can.";f.reset()}else{m.innerHTML=fail}b.disabled=false}).catch(function(){m.innerHTML=fail;b.disabled=false})});})();
</script>"""

PAGES = [
    ("about", "About Us | Exotic Earthworks",
     "About Exotic Earthworks: excavator hire, landscaping and construction services across Sydney and the Central Coast, based in Londonderry.", about, ""),
    ("services", "Our Services | Excavator Hire, Trenching, Pool Digs | Exotic Earthworks",
     "Wet hire with an experienced operator and dry hire of a 1.8 tonne mini excavator: trenching, pool digs, stump removal, levelling, post holes and more across Sydney and the Central Coast.", services, ""),
    ("contact", "Contact Us | Exotic Earthworks",
     "Contact Exotic Earthworks for mini excavator hire and quotes across Sydney and the Central Coast. Message us on Facebook Messenger or send an enquiry.", contact, cscript),
]
for slug, title, desc, body, sc in PAGES:
    os.makedirs(f"{ROOT}/public/{slug}", exist_ok=True)
    open(f"{ROOT}/public/{slug}/index.html", "w", encoding="utf-8").write(shell(slug, title, desc, body, sc))
    print("wrote", slug)
urls = [SITE + "/"] + [f"{SITE}/{p[0]}/" for p in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-11-12</lastmod>\n  </url>\n" for u in urls) + "</urlset>\n"
open(f"{ROOT}/public/sitemap.xml", "w", encoding="utf-8").write(sm)
