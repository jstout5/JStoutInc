import base64, fitz
from pathlib import Path

def img_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

def pdf_preview_b64(pdf_path, dpi=72):
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    data = pix.tobytes("png")
    doc.close()
    return 'data:image/png;base64,' + base64.b64encode(data).decode()

def pdf_all_pages_b64(pdf_path, dpi=150):
    doc = fitz.open(str(pdf_path))
    mat = fitz.Matrix(dpi/72, dpi/72)
    pages = []
    for page in doc:
        pix = page.get_pixmap(matrix=mat)
        data = pix.tobytes("png")
        pages.append('data:image/png;base64,' + base64.b64encode(data).decode())
    doc.close()
    return pages

def latest_pdf(folder, pattern="*.pdf"):
    pdfs = sorted(Path(folder).glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    if not pdfs: raise FileNotFoundError(f"No PDFs in {folder}")
    print(f"  {pdfs[0].name}")
    return pdfs[0]

logo      = img_b64(r'C:\Users\frost\Downloads\myLogo_still.png')
bulldog   = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstoutCash.png')
horse     = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstouthorst.png')
mlb_img   = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstoutmlb.png')
house_img = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstouthouse.png')
nba_img   = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstoutnba.png')

cash_pdf = latest_pdf(r'C:\Users\frost\JStoutCash', 'JStoutCash_*.pdf')
cash_pages = pdf_all_pages_b64(cash_pdf)
previews = {
    'cash':  cash_pages[0],
    'horse': pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutHorse',    'JStoutHorse_Report_*.pdf')),
    'mlb':   pdf_preview_b64(latest_pdf(r'C:\Users\frost\MLBNewsletter',  'newsletter_*.pdf')),
    'odds':  pdf_preview_b64(latest_pdf(r'C:\Users\frost\OddsNewsletter', 'newsletter_*.pdf')),
    'house': pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutHouse',    'JStoutHouse_*.pdf')),
}
cash_full = cash_pages  # all pages already at 150 dpi
print("PDFs rendered.")

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>JStout Inc — Your Edge in Every Market</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{--red:#c8102e;--cream:#f5f0e8;--dark:#1a1a1a;}
body{font-family:'Inter',system-ui,sans-serif;background:var(--cream);color:var(--dark);max-width:100%;overflow-x:hidden;}

/* ── HEADER ── */
header{
  background:var(--cream);
  padding:0 60px;
  height:220px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  border-bottom:3px solid var(--red);
  position:relative;
  overflow:hidden;
}
#matrix-bg{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}
.header-left{display:flex;align-items:center;gap:30px;position:relative;z-index:1;}
.header-logo{height:180px;width:auto;}
.header-text{}
.header-brand{font-size:12px;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:var(--red);margin-bottom:6px;}
.header-tagline{font-family:'Playfair Display',serif;font-size:56px;font-weight:900;line-height:1;color:var(--dark);}
.header-tagline span{color:var(--red);}
.header-nav{display:flex;align-items:center;gap:24px;position:relative;z-index:1;}
.header-nav a{font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--dark);text-decoration:none;opacity:.6;transition:opacity .2s;white-space:nowrap;}
.header-nav a:hover{opacity:1;}
.header-cta{background:var(--red);color:#fff;padding:10px 22px;border-radius:4px;font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;text-decoration:none;}
.header-phone{display:inline-block;font-size:10px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--red) !important;opacity:1 !important;text-decoration:none;border:2px solid var(--red);padding:8px 16px;border-radius:4px;white-space:nowrap;transition:background .2s,color .2s !important;}
.header-phone:hover{background:var(--red) !important;color:#fff !important;}

/* ── STATS BAR ── */
.stats-bar{background:var(--red);padding:18px 40px;display:flex;justify-content:center;gap:80px;}
.stat{text-align:center;}
.stat-num{font-family:'Playfair Display',serif;font-size:26px;font-weight:900;color:#fff;line-height:1;}
.stat-lbl{font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,.6);margin-top:3px;}

/* ── SECTION WRAPPER ── */
.section{padding:64px 40px;}
.section-dark{background:#111;}
.section-label{font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--red);text-align:center;margin-bottom:10px;}
.section-title{font-family:'Playfair Display',serif;font-size:38px;font-weight:900;text-align:center;margin-bottom:8px;}
.section-title-light{color:#fff;}
.section-sub{font-size:14px;color:#888;text-align:center;margin-bottom:40px;}
.section-sub-light{color:rgba(255,255,255,.4);}

/* ── NEWSLETTER CARDS ── */
.cards-row{display:flex;gap:20px;justify-content:center;}
.nl-card{
  background:#fff;border-radius:14px;
  border:1px solid rgba(0,0,0,.07);
  box-shadow:0 4px 20px rgba(0,0,0,.08);
  width:240px;flex-shrink:0;
  overflow:hidden;
  transition:transform .2s,box-shadow .2s;
  position:relative;
}
.nl-card:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(0,0,0,.14);}
.nl-card-soon{opacity:.5;pointer-events:none;}
.nl-badge{position:absolute;top:12px;right:12px;font-size:7px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;padding:3px 8px;border-radius:999px;color:#fff;}
.badge-live{background:#16a34a;}
.badge-soon{background:#999;}
.badge-hot{background:var(--red);}
.nl-head{padding:20px 20px 12px;display:flex;align-items:center;gap:12px;}
.nl-avatar{width:52px;height:52px;border-radius:50%;object-fit:cover;border:2px solid var(--cream);}
.nl-name{font-weight:800;font-size:15px;color:var(--dark);}
.nl-freq{font-size:10px;color:#aaa;margin-top:2px;}
.nl-body{padding:0 20px 16px;}
.nl-desc{font-size:12px;color:#777;line-height:1.6;}
.nl-footer{padding:14px 20px;border-top:1px solid rgba(0,0,0,.06);display:flex;align-items:center;justify-content:space-between;}
.nl-price{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;color:var(--red);}
.nl-price span{font-size:11px;color:#aaa;font-weight:400;}
.nl-btn{background:var(--red);color:#fff;padding:7px 14px;border-radius:6px;font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.nl-btn-soon{background:#e5e5e5;color:#aaa;padding:7px 14px;border-radius:6px;font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;}
.nl-preview{width:100%;height:120px;object-fit:cover;object-position:top;border-top:1px solid rgba(0,0,0,.06);}

/* ── SERVICES ── */
.services-grid{display:grid;grid-template-columns:repeat(4,300px);gap:20px;justify-content:center;}
.svc-preview-img{width:100%;height:150px;object-fit:cover;object-position:top;border-radius:6px;display:block;margin-bottom:8px;}
.bday-card{
  background:rgba(200,16,46,.08);
  border:2px solid rgba(200,16,46,.35);
  border-radius:14px;padding:28px;
  width:320px;position:relative;
  box-shadow:0 8px 32px rgba(200,16,46,.15);
  transition:transform .2s;
}
.bday-card:hover{transform:translateY(-4px);}
.bday-new{position:absolute;top:14px;right:14px;background:var(--red);color:#fff;font-size:7px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;padding:3px 8px;border-radius:999px;}
.bday-emoji{font-size:36px;margin-bottom:12px;}
.bday-name{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;color:#fff;margin-bottom:6px;}
.bday-tagline{font-size:13px;color:rgba(255,255,255,.5);font-style:italic;margin-bottom:14px;}
.bday-desc{font-size:12px;color:rgba(255,255,255,.4);line-height:1.7;margin-bottom:20px;}
.bday-footer{display:flex;align-items:center;justify-content:space-between;}
.bday-price{font-family:'Playfair Display',serif;font-size:28px;font-weight:900;color:#fff;}
.bday-price span{font-size:12px;color:rgba(255,255,255,.4);font-weight:400;}
.bday-btn{background:var(--red);color:#fff;padding:10px 20px;border-radius:7px;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;box-shadow:0 4px 14px rgba(200,16,46,.4);}
.svc-card{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);
  border-radius:14px;padding:24px;
  width:300px;
  transition:transform .2s,background .2s;
  position:relative;overflow:hidden;
}
.svc-card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--red);}
.svc-card:hover{transform:translateY(-4px);background:rgba(255,255,255,.07);}
.svc-icon{font-size:28px;margin-bottom:12px;}
.svc-name{font-family:'Playfair Display',serif;font-size:18px;font-weight:900;color:#fff;margin-bottom:8px;}
.svc-desc{font-size:11px;color:rgba(255,255,255,.4);line-height:1.6;margin-bottom:16px;}
.svc-btn{font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--red);text-decoration:none;}

/* ── MARKETPLACE ── */
.shop-row{display:flex;gap:20px;justify-content:center;}
.shop-card{
  background:#fff;border-radius:14px;
  border:1px solid rgba(0,0,0,.07);
  box-shadow:0 4px 20px rgba(0,0,0,.08);
  width:260px;overflow:hidden;
  transition:transform .2s,box-shadow .2s;
  position:relative;
}
.shop-card:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(0,0,0,.14);}
.shop-img{height:160px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;}
.shop-img-dark{background:linear-gradient(145deg,#0d0d0b,#1c1508);}
.shop-img-ph{background:#f0ece4;border-bottom:1px solid rgba(0,0,0,.06);}
.cj-label{font-family:'Playfair Display',serif;font-size:10px;letter-spacing:5px;color:#c8941e;text-transform:uppercase;}
.cj-year{font-family:'Playfair Display',serif;font-size:32px;font-weight:900;color:#fff;}
.cj-type{font-size:8px;letter-spacing:3px;color:rgba(200,148,30,.5);text-transform:uppercase;}
.ph-text{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(0,0,0,.2);}
.shop-body{padding:16px 18px;}
.shop-name{font-weight:800;font-size:14px;margin-bottom:3px;}
.shop-sub{font-size:11px;color:#999;margin-bottom:10px;}
.shop-price{font-family:'Playfair Display',serif;font-size:26px;font-weight:900;color:var(--red);margin-bottom:12px;}
.shop-btns{display:flex;gap:8px;}
.btn-pp{flex:1;text-align:center;background:#0070ba;color:#fff;padding:9px;border-radius:6px;font-size:9px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.btn-st{flex:1;text-align:center;background:var(--red);color:#fff;padding:9px;border-radius:6px;font-size:9px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.btn-notify{display:inline-block;width:100%;text-align:center;background:#f0ece4;color:#aaa;padding:9px;border-radius:6px;font-size:9px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.in-stock{position:absolute;top:10px;right:10px;background:#16a34a;color:#fff;font-size:7px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;border-radius:999px;}

/* ── MEDIUM (tablet 769–1199px) ── */
@media(min-width:769px) and (max-width:1199px){
  header{padding:0 32px;height:180px;}
  .header-logo{height:140px;}
  .header-tagline{font-size:40px;}
  .header-nav{gap:16px;}
  .header-phone{font-size:9px;padding:7px 12px;}
  .section{padding:52px 28px;}
  .section-title{font-size:32px;}
  .cards-row{overflow-x:auto;justify-content:flex-start;padding-bottom:12px;-webkit-overflow-scrolling:touch;scroll-snap-type:x mandatory;}
  .nl-card{flex-shrink:0;scroll-snap-align:start;}
  .services-grid{grid-template-columns:repeat(2,minmax(0,300px));max-width:680px;margin:0 auto;}
  .svc-card{width:100%;}
  .shop-row{overflow-x:auto;justify-content:flex-start;padding-bottom:12px;-webkit-overflow-scrolling:touch;scroll-snap-type:x mandatory;}
  .shop-card{flex-shrink:0;scroll-snap-align:start;}
}

/* ── SMALL (mobile ≤768px) ── */
@media(max-width:768px){
  *{box-sizing:border-box;}
  html,body{overflow-x:hidden;width:100%;}
  header{height:auto;padding:14px 16px;flex-direction:column;align-items:flex-start;gap:8px;}
  #matrix-bg{display:none;}
  .header-logo{height:68px;}
  .header-tagline{font-size:24px;}
  .header-brand{font-size:9px;}
  .header-nav{gap:8px;flex-wrap:wrap;}
  .header-nav>a[href="#newsletters"],
  .header-nav>a[href="#services"],
  .header-nav>a[href="#shop"]{display:none;}
  .header-phone{font-size:10px;padding:7px 13px;letter-spacing:1px;}
  .section{padding:32px 14px;overflow:hidden;}
  .section-dark{overflow:hidden;}
  .section-title{font-size:24px;}
  .section-sub{font-size:12px;margin-bottom:22px;}
  .section-label{font-size:9px;}
  .cards-row{overflow-x:auto;overflow-y:visible;justify-content:flex-start;padding-bottom:14px;-webkit-overflow-scrolling:touch;scroll-snap-type:x mandatory;gap:12px;width:100%;}
  .nl-card{width:210px;min-width:210px;flex-shrink:0;scroll-snap-align:start;}
  .services-grid{grid-template-columns:1fr;width:100%;max-width:100%;gap:12px;}
  .svc-card{width:100%;box-sizing:border-box;}
  .bday-card{width:100%;box-sizing:border-box;}
  .shop-row{overflow-x:auto;overflow-y:visible;justify-content:flex-start;padding-bottom:14px;-webkit-overflow-scrolling:touch;scroll-snap-type:x mandatory;gap:12px;width:100%;}
  .shop-card{width:220px;min-width:220px;flex-shrink:0;scroll-snap-align:start;}
  .cta-strip{padding:28px 16px !important;}
  .cta-strip a{font-size:16px !important;padding:12px 20px !important;}
  .cta-strip div:first-child{font-size:22px !important;}
}
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <canvas id="matrix-bg"></canvas>
  <div class="header-left">
    <img src="LOGO" class="header-logo" alt="JStout Inc">
    <div class="header-text">
      <div class="header-brand">JStout Inc</div>
      <div class="header-tagline">Your Edge in <span>Every Market</span></div>
    </div>
  </div>
  <nav class="header-nav">
    <a href="#newsletters">Newsletters</a>
    <a href="#services">Services</a>
    <a href="#shop">Marketplace</a>
    <a href="tel:8593965538" class="header-phone">&#128222;&nbsp;(859)&nbsp;396-5538</a>
    <a href="https://jstout-bday.onrender.com/admin/shop" target="_blank" style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:rgba(0,0,0,.3);text-decoration:none;border:1px solid rgba(0,0,0,.15);padding:8px 14px;border-radius:4px;">&#128274; Admin</a>
  </nav>
</header>

<!-- NEWSLETTERS -->
<div class="section" id="newsletters">
  <div class="section-label">Subscriptions</div>
  <h2 class="section-title">Premium Newsletters</h2>
  <p class="section-sub">Unlock the full report. Subscribe and get every issue delivered to your inbox.</p>
  <div class="cards-row">

    <div class="nl-card">
      <span class="nl-badge badge-live">&#9679; Live</span>
      <div class="nl-head">
        <img src="IMG_BULLDOG" class="nl-avatar" alt="JStoutCash">
        <div><div class="nl-name">Wall Street Edge</div><div class="nl-freq">Daily &middot; Stock Market</div></div>
      </div>
      <div class="nl-body"><div class="nl-desc">Daily stock market intelligence. 52-week lows, dividend plays, options flow &amp; top movers — before the bell.</div></div>
      <div class="nl-footer">
        <div class="nl-price">$2<span>/mo</span></div>
        <a href="preview_cash.html" target="_blank" class="nl-btn">Free Preview</a>
      </div>
      <img src="PREVIEW_CASH" class="nl-preview" alt="Preview">
    </div>

    <div class="nl-card nl-card-soon">
      <span class="nl-badge badge-soon">Coming Soon</span>
      <div class="nl-head">
        <img src="IMG_HORSE" class="nl-avatar" alt="JStoutHorse">
        <div><div class="nl-name">Jockey's Angle</div><div class="nl-freq">Race Days &middot; Handicapping</div></div>
      </div>
      <div class="nl-body"><div class="nl-desc">Horse racing picks &amp; handicapping. Track conditions, pace analysis, trainer stats &amp; value overlays for every major race.</div></div>
      <div class="nl-footer">
        <div class="nl-price">$8<span>/mo</span></div>
        <span class="nl-btn-soon">Coming Soon</span>
      </div>
      <img src="PREVIEW_HORSE" class="nl-preview" alt="Preview">
    </div>

    <div class="nl-card nl-card-soon">
      <span class="nl-badge badge-soon">Coming Soon</span>
      <div class="nl-head">
        <img src="IMG_MLB" class="nl-avatar" alt="MLB Newsletter">
        <div><div class="nl-name">MLB Edge</div><div class="nl-freq">Daily &middot; Baseball</div></div>
      </div>
      <div class="nl-body"><div class="nl-desc">Daily baseball intelligence. Standings, hot bats, pitcher matchups, and value picks for the serious fan.</div></div>
      <div class="nl-footer">
        <div class="nl-price">$2<span>/mo</span></div>
        <span class="nl-btn-soon">Coming Soon</span>
      </div>
      <img src="PREVIEW_MLB" class="nl-preview" alt="Preview">
    </div>

    <div class="nl-card nl-card-soon">
      <span class="nl-badge badge-soon">Coming Soon</span>
      <div class="nl-head">
        <img src="IMG_HOUSE" class="nl-avatar" alt="JStoutHouse">
        <div><div class="nl-name">Real Estate</div><div class="nl-freq">Weekly &middot; Real Estate</div></div>
      </div>
      <div class="nl-body"><div class="nl-desc">Market trends &amp; deal alerts for real estate investors. Find the edge before anyone else.</div></div>
      <div class="nl-footer">
        <div class="nl-price">$5<span>/mo</span></div>
        <span class="nl-btn-soon">Coming Soon</span>
      </div>
      <img src="PREVIEW_HOUSE" class="nl-preview" alt="Preview">
    </div>

    <div class="nl-card nl-card-soon">
      <span class="nl-badge badge-soon">Coming Soon</span>
      <div class="nl-head">
        <img src="IMG_BULLDOG" class="nl-avatar" alt="Odds">
        <div><div class="nl-name">Bet the NBA</div><div class="nl-freq">Daily &middot; Betting</div></div>
      </div>
      <div class="nl-body"><div class="nl-desc">Sharp line movement &amp; value plays across all major sports leagues. Know where the money's going.</div></div>
      <div class="nl-footer">
        <div class="nl-price">$2<span>/mo</span></div>
        <span class="nl-btn-soon">Coming Soon</span>
      </div>
      <img src="PREVIEW_ODDS" class="nl-preview" alt="Preview">
    </div>

  </div>
</div>

<!-- SERVICES -->
<div class="section section-dark" id="services">
  <div class="section-label">What We Do</div>
  <h2 class="section-title section-title-light">Services &amp; AI</h2>
  <p class="section-sub section-sub-light">Automation, websites, and intelligence tools built to make you money.</p>
  <div class="services-grid">

    <div class="svc-card">
      <div class="svc-icon">&#129302;</div>
      <div class="svc-name">AI Agents</div>
      <div class="svc-desc">Custom automation built to run itself. Set it once, done forever.</div>
      <div style="margin-top:14px;padding:12px;background:rgba(200,16,46,.1);border:1px solid rgba(200,16,46,.25);border-radius:8px;">
        <div style="font-size:9px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:var(--red);margin-bottom:6px;">&#9733; Available Now</div>
        <div style="font-size:13px;font-weight:700;color:#fff;margin-bottom:3px;">&#127874; Birthday Gift Agent</div>
        <div style="font-size:11px;color:rgba(255,255,255,.4);margin-bottom:10px;">We find, buy &amp; ship the perfect gift — 3 days before every birthday. $30/mo.</div>
        <a href="bday.html" class="svc-btn" style="display:inline-block;background:var(--red);color:#fff;padding:6px 14px;border-radius:5px;font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;text-decoration:none;">Get Started</a>
      </div>
      <a href="mailto:frostbytehero@gmail.com?subject=AI Agent Inquiry" class="svc-btn" style="display:inline-block;margin-top:14px;">Custom Agent &rarr;</a>
    </div>

    <div class="svc-card">
      <div class="svc-icon">&#127760;</div>
      <div class="svc-name">Websites</div>
      <div class="svc-desc">Fast, sharp, built to convert. Landing pages to full builds.</div>
      <div style="margin-top:14px;padding:12px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:8px;">
        <div style="font-size:9px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.4);margin-bottom:6px;">&#9733; Recent Work</div>
        <div style="font-size:13px;font-weight:700;color:#fff;margin-bottom:3px;">&#127968; ChristyStout.com</div>
        <div style="font-size:11px;color:rgba(255,255,255,.4);margin-bottom:10px;">Real estate site — clean, fast, built to generate leads.</div>
        <a href="https://christystout.com" target="_blank" class="svc-btn" style="display:inline-block;background:rgba(255,255,255,.1);color:#fff;padding:6px 14px;border-radius:5px;font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;text-decoration:none;">View Site &rarr;</a>
      </div>
      <a href="mailto:frostbytehero@gmail.com?subject=Website Inquiry" class="svc-btn" style="display:inline-block;margin-top:14px;">Get a Quote &rarr;</a>
    </div>

    <div class="svc-card">
      <div class="svc-icon">&#128241;</div>
      <div class="svc-name">Apps</div>
      <div class="svc-desc">Custom web &amp; mobile apps built to solve real problems.</div>
      <div style="margin-top:14px;padding:12px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:8px;">
        <div style="font-size:9px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.4);margin-bottom:6px;">&#9733; Recent Work</div>
        <div style="font-size:13px;font-weight:700;color:#fff;margin-bottom:3px;">&#9997; Bible Reading App</div>
        <div style="font-size:11px;color:rgba(255,255,255,.4);margin-bottom:10px;">Daily reading tracker &amp; verse journal.</div>
        <a href="bible_mock.html" target="_blank" style="display:inline-block;background:rgba(255,255,255,.1);color:#fff;padding:6px 14px;border-radius:5px;font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;text-decoration:none;">View App &rarr;</a>
      </div>
      <a href="mailto:frostbytehero@gmail.com?subject=App Inquiry" class="svc-btn" style="display:inline-block;margin-top:14px;">Get a Quote &rarr;</a>
    </div>

    <div class="svc-card">
      <div class="svc-icon">&#128293;</div>
      <div class="svc-name">Marketing Tools</div>
      <div class="svc-desc">Flyers, email campaigns, promos &amp; social content built to drive traffic.</div>
      <div style="margin-top:14px;padding:12px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:8px;">
        <div style="font-size:9px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.4);margin-bottom:6px;">&#9733; Recent Work</div>
        <div style="font-size:13px;font-weight:700;color:#fff;margin-bottom:3px;">&#127807; Brushy Creek Fall Hunt</div>
        <div style="font-size:11px;color:rgba(255,255,255,.4);margin-bottom:10px;">Promo flyer — designed, printed &amp; sold.</div>
        <a href="fall-hunt-2026.html" target="_blank" style="display:inline-block;background:rgba(255,255,255,.1);color:#fff;padding:6px 14px;border-radius:5px;font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;text-decoration:none;">View Flyer &rarr;</a>
      </div>
      <a href="mailto:frostbytehero@gmail.com?subject=Marketing Inquiry" class="svc-btn" style="display:inline-block;margin-top:14px;">Get a Quote &rarr;</a>
    </div>

  </div>
</div>

<!-- CTA STRIP -->
<div class="cta-strip" style="background:var(--red);padding:36px 40px;text-align:center;">
  <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:900;color:#fff;margin-bottom:8px;">Ready to work together?</div>
  <div style="font-size:13px;color:rgba(255,255,255,.7);margin-bottom:20px;letter-spacing:.5px;">Newsletters &middot; AI Agents &middot; Websites &middot; Apps &middot; Marketing &mdash; let&rsquo;s talk.</div>
  <a href="tel:8593965538" style="display:inline-block;background:#fff;color:var(--red);padding:14px 36px;border-radius:6px;font-family:'Playfair Display',serif;font-size:22px;font-weight:900;text-decoration:none;letter-spacing:1px;white-space:nowrap;max-width:100%;box-sizing:border-box;">Call JStout &mdash; (859) 396-5538</a>
</div>

<!-- MARKETPLACE -->
<div class="section" id="shop">
  <div class="section-label">Shop</div>
  <h2 class="section-title">Marketplace</h2>
  <p class="section-sub">Premium inventory. Ships insured. Real deals.</p>
  <div class="shop-row" id="shop-row">
    <div style="text-align:center;width:100%;color:#aaa;padding:40px;font-size:14px;">Loading products...</div>
  </div>
</div>

<!-- MATRIX -->
<script>
(function(){
  var c=document.getElementById('matrix-bg');
  if(!c)return;
  var ctx=c.getContext('2d');
  var chars='JSTOUT$$$';
  var fs=15,cols,drops;
  function init(){
    c.width=c.offsetWidth;c.height=c.offsetHeight;
    cols=Math.floor(c.width/fs);
    drops=[];
    for(var i=0;i<cols;i++)drops[i]=Math.random()*-(c.height/fs)|0;
  }
  init();
  window.addEventListener('resize',init);
  function draw(){
    ctx.fillStyle='rgba(245,240,232,0.15)';
    ctx.fillRect(0,0,c.width,c.height);
    ctx.font='bold '+fs+'px "Courier New",monospace';
    ctx.fillStyle='rgba(200,16,46,0.35)';
    for(var i=0;i<drops.length;i++){
      var ch=chars[Math.floor(Math.random()*chars.length)];
      ctx.fillText(ch,i*fs,drops[i]*fs);
      if(drops[i]*fs>c.height&&Math.random()>0.975)drops[i]=0;
      drops[i]++;
    }
  }
  setInterval(draw,80);
})();
</script>

<!-- FOOTER -->
<div style="background:#111;border-top:3px solid var(--red);padding:40px;text-align:center;">
  <div style="font-family:'Playfair Display',serif;font-size:20px;font-weight:900;color:#fff;margin-bottom:6px;">JStout Inc</div>
  <div style="font-size:11px;color:rgba(255,255,255,.3);letter-spacing:2px;text-transform:uppercase;margin-bottom:16px;">Kentucky Built &amp; Based</div>
  <a href="tel:8593965538" style="display:inline-block;font-size:18px;font-weight:800;color:var(--red);text-decoration:none;letter-spacing:1px;">(859) 396-5538</a>
  <div style="margin-top:6px;font-size:11px;color:rgba(255,255,255,.2);">Call or text anytime</div>
  <div style="margin-top:24px;font-size:10px;color:rgba(255,255,255,.15);letter-spacing:1px;">&copy; 2026 JStout Inc. All rights reserved.</div>
</div>

<script>
const API = "https://jstout-bday.onrender.com/api/products";
fetch(API)
  .then(r => r.json())
  .then(products => {
    const row = document.getElementById("shop-row");
    if (!products.length) {
      row.innerHTML = '<div style="text-align:center;width:100%;color:#aaa;padding:40px">No products listed yet.</div>';
      return;
    }
    row.innerHTML = products.map(p => {
      const img = p.image_b64
        ? `<img src="${p.image_b64}" style="width:100%;height:160px;object-fit:cover;">`
        : `<div class="shop-img shop-img-ph"><div class="ph-text">${p.name}</div></div>`;
      const badge = p.in_stock ? '<span class="in-stock">In Stock</span>' : '<span class="in-stock" style="background:#aaa">Out of Stock</span>';
      const btns = [
        p.paypal_link ? `<a href="${p.paypal_link}" target="_blank" class="btn-pp">PayPal</a>` : '',
        p.stripe_link ? `<a href="${p.stripe_link}" target="_blank" class="btn-st">Stripe</a>` : '',
        (!p.paypal_link && !p.stripe_link) ? `<a href="mailto:frostbytehero@gmail.com?subject=Purchase: ${encodeURIComponent(p.name)}" class="btn-st">Buy Now</a>` : ''
      ].join('');
      return `<div class="shop-card">
        ${badge}
        <div class="shop-img">${img}</div>
        <div class="shop-body">
          <div class="shop-name">${p.name}</div>
          <div class="shop-sub">${p.description || ''}</div>
          <div class="shop-price">$${Number(p.price).toLocaleString()}</div>
          <div class="shop-btns">${btns}</div>
        </div>
      </div>`;
    }).join('');
  })
  .catch(() => {
    document.getElementById("shop-row").innerHTML =
      '<div style="text-align:center;width:100%;color:#aaa;padding:40px">Shop loading... check back soon.</div>';
  });
</script>

</body>
</html>"""

html = (html
    .replace("LOGO",          logo)
    .replace("IMG_BULLDOG",   bulldog)
    .replace("IMG_HORSE",     horse)
    .replace("IMG_MLB",       mlb_img)
    .replace("IMG_HOUSE",     house_img)
    .replace("PREVIEW_CASH",  previews['cash'])
    .replace("PREVIEW_HORSE", previews['horse'])
    .replace("PREVIEW_MLB",   previews['mlb'])
    .replace("PREVIEW_ODDS",  previews['odds'])
    .replace("PREVIEW_HOUSE", previews['house'])
)

with open(r'C:\Users\frost\JStoutInc\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Done. {len(html):,} chars written.")

preview_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Wall Street Edge — Free Preview</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
:root{{--red:#c8102e;--cream:#f5f0e8;--dark:#1a1a1a;}}
body{{font-family:'Inter',system-ui,sans-serif;background:var(--cream);color:var(--dark);}}
nav{{background:#111;border-bottom:3px solid var(--red);padding:14px 28px;display:flex;align-items:center;justify-content:space-between;}}
.nav-logo{{font-family:'Playfair Display',serif;font-size:18px;font-weight:900;color:#fff;}}
.nav-logo span{{color:var(--red);}}
.nav-back{{font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.4);text-decoration:none;transition:color .2s;}}
.nav-back:hover{{color:#fff;}}
.wrap{{max-width:860px;margin:48px auto;padding:0 24px 80px;}}
.kicker{{font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--red);margin-bottom:10px;}}
h1{{font-family:'Playfair Display',serif;font-size:36px;font-weight:900;color:var(--dark);margin-bottom:6px;}}
.sub{{font-size:14px;color:#888;margin-bottom:28px;}}
.preview-img{{width:100%;border-radius:10px;box-shadow:0 8px 48px rgba(0,0,0,.18);border:1px solid rgba(0,0,0,.08);display:block;margin-bottom:16px;}}
.cta-box{{margin-top:40px;background:#111;border-radius:14px;padding:36px;text-align:center;}}
.cta-box h2{{font-family:'Playfair Display',serif;font-size:26px;font-weight:900;color:#fff;margin-bottom:8px;}}
.cta-box p{{font-size:13px;color:rgba(255,255,255,.45);margin-bottom:24px;}}
.cta-btn{{display:inline-block;background:var(--red);color:#fff;padding:14px 40px;border-radius:7px;font-size:12px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;box-shadow:0 4px 18px rgba(200,16,46,.35);}}
.cta-btn:hover{{background:#a50d25;}}
.price{{font-family:'Playfair Display',serif;font-size:48px;font-weight:900;color:#fff;}}
.price span{{font-size:16px;color:rgba(255,255,255,.35);font-weight:400;}}
@media(max-width:600px){{
  h1{{font-size:26px;}}
  .cta-box{{padding:24px 18px;}}
  .price{{font-size:36px;}}
}}
</style>
</head>
<body>
<nav>
  <div class="nav-logo">JStout <span>Inc</span></div>
  <a href="/" class="nav-back">&#8592; Back to Hub</a>
</nav>
<div class="wrap">
  <div class="kicker">Wall Street Edge &mdash; Sample Issue</div>
  <h1>Free Preview</h1>
  <p class="sub">Daily stock market intelligence. 52-week lows, dividend plays, options flow &amp; top movers &mdash; before the bell.</p>
  {''.join(f'<img src="{p}" class="preview-img" alt="Page {i+1}">' for i, p in enumerate(cash_full))}
  <div class="cta-box">
    <h2>Like what you see?</h2>
    <p>Get every issue delivered to your inbox every morning for just&nbsp;&mdash;</p>
    <div class="price">$2<span>/mo</span></div>
    <br><br>
    <a href="https://buy.stripe.com/4gM4gsfrn4Ar5T19lr5Rm00" target="_blank" class="cta-btn">Subscribe Now</a>
  </div>
</div>
</body>
</html>"""

with open(r'C:\Users\frost\JStoutInc\preview_cash.html', 'w', encoding='utf-8') as f:
    f.write(preview_page)
print("preview_cash.html written.")
