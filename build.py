import base64, fitz
from pathlib import Path

def img_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

def pdf_preview_b64(pdf_path, dpi=150):
    doc = fitz.open(str(pdf_path))
    page = doc[0]
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    data = pix.tobytes("png")
    doc.close()
    return 'data:image/png;base64,' + base64.b64encode(data).decode()

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

previews = {
    'cash':  pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutCash',     'JStoutCash_*.pdf')),
    'horse': pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutHorse',    'JStoutHorse_Report_*.pdf')),
    'mlb':   pdf_preview_b64(latest_pdf(r'C:\Users\frost\MLBNewsletter',  'newsletter_*.pdf')),
    'odds':  pdf_preview_b64(latest_pdf(r'C:\Users\frost\OddsNewsletter', 'newsletter_*.pdf')),
    'house': pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutHouse',    'JStoutHouse_*.pdf')),
}
print("PDFs rendered.")

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>JStout Inc</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{--red:#c8102e;--red2:#9e0c24;--cream:#f0eadb;--dark:#111;}
html,body{height:100vh;overflow:hidden;display:flex;flex-direction:column;background:var(--cream);}
body{font-family:"Segoe UI",system-ui,sans-serif;}

/* ── BANNER ── */
.banner{
  flex:0 0 auto;
  background:linear-gradient(90deg,var(--red) 0%,var(--red2) 100%);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 24px;height:68px;overflow:hidden;
}
.banner-brand{display:flex;align-items:center;gap:14px;}
.banner-logo{height:52px;width:auto;flex-shrink:0;filter:brightness(0) invert(1);opacity:.9;}
.banner-left{display:flex;flex-direction:column;justify-content:center;}
.banner-title{
  font-family:'Playfair Display',serif;
  font-size:26px;font-weight:900;color:#fff;
  letter-spacing:-.5px;line-height:1;
}
.banner-sub{
  font-family:'Cinzel',serif;font-size:7.5px;font-weight:700;
  letter-spacing:3px;text-transform:uppercase;
  color:rgba(255,255,255,.5);margin-top:4px;
}
.banner-nav{display:flex;gap:22px;align-items:center;}
.banner-nav a{
  font-family:'Cinzel',serif;font-size:8.5px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  color:rgba(255,255,255,.65);text-decoration:none;transition:color .2s;
}
.banner-nav a:hover{color:#fff;}

/* ── CONTENT ROWS ── */
.rows{flex:1;display:flex;flex-direction:column;gap:0;min-height:0;overflow:hidden;}
.row-wrap{flex:1;display:flex;flex-direction:column;min-height:0;border-bottom:1px solid rgba(0,0,0,.07);}
.row-label{
  flex:0 0 auto;padding:8px 20px 0;
  font-family:'Cinzel',serif;font-size:7px;font-weight:700;
  letter-spacing:3.5px;text-transform:uppercase;color:rgba(40,20,0,.28);
}
.row-cards{flex:1;display:flex;gap:10px;padding:8px 20px 10px;min-height:0;overflow:hidden;}

/* ── NEWSLETTER CARDS ── */
.nl-card{
  flex:1;background:#fff;border-radius:10px;
  border:1px solid rgba(0,0,0,.07);
  overflow:hidden;display:flex;
  box-shadow:0 2px 12px rgba(0,0,0,.07);
  transition:transform .18s,box-shadow .18s;
  position:relative;min-width:0;
}
.nl-card:hover:not(.nl-soon){transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.12);}
.nl-thumb{width:55px;flex-shrink:0;overflow:hidden;}
.nl-thumb img{width:100%;height:100%;object-fit:cover;object-position:top;transition:transform .5s;}
.nl-card:hover .nl-thumb img{transform:scale(1.06);}
.nl-body{flex:1;padding:10px 12px 8px;display:flex;flex-direction:column;justify-content:space-between;min-width:0;}
.nl-name{font-family:'Cinzel',serif;font-size:9px;font-weight:800;color:var(--red);margin-bottom:3px;}
.nl-desc{font-size:8.5px;color:#777;line-height:1.4;flex:1;}
.nl-foot{display:flex;align-items:center;justify-content:space-between;margin-top:6px;}
.nl-price{font-family:'Playfair Display',serif;font-size:15px;font-weight:900;color:var(--red);}
.nl-price span{font-size:8px;color:#999;font-weight:400;}
.nl-btn{background:linear-gradient(135deg,var(--red),var(--red2));color:#fff;padding:4px 10px;border-radius:5px;font-size:7.5px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.nl-live{position:absolute;top:5px;left:5px;font-size:6px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:2px 5px;border-radius:999px;color:#fff;background:#16a34a;}
.nl-soon{opacity:.45;pointer-events:none;}
.nl-soon-tag{position:absolute;top:5px;right:5px;font-size:6px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:2px 5px;border-radius:999px;color:#fff;background:#bbb;}
.nl-soon-btn{background:#ddd;color:#bbb;padding:4px 10px;border-radius:5px;font-size:7.5px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;}

/* ── SERVICES ROW ── */
.row-wrap-dark{background:var(--dark);}
.row-label-light{color:rgba(255,255,255,.25);}
.svc-card{
  flex:1;background:rgba(255,255,255,.04);border-radius:10px;
  border:1px solid rgba(255,255,255,.07);
  padding:14px 16px;display:flex;flex-direction:column;
  position:relative;overflow:hidden;min-width:0;
  transition:transform .18s,background .18s;
}
.svc-card:hover{transform:translateY(-2px);background:rgba(255,255,255,.07);}
.svc-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--red),var(--red2));}
.svc-icon{font-size:22px;margin-bottom:7px;}
.svc-name{font-family:'Playfair Display',serif;font-size:15px;font-weight:900;color:#fff;margin-bottom:4px;}
.svc-desc{font-size:9px;color:rgba(255,255,255,.4);line-height:1.5;flex:1;}
.svc-cta{display:inline-block;margin-top:10px;background:linear-gradient(135deg,var(--red),var(--red2));color:#fff;padding:5px 12px;border-radius:5px;font-family:'Cinzel',serif;font-size:7px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;}

/* B Day featured in services row */
.bday-card{
  flex:1.5;background:rgba(200,16,46,.06);border-radius:10px;
  border:2px solid rgba(200,16,46,.3);
  padding:14px 16px;display:flex;flex-direction:column;
  position:relative;min-width:0;
  transition:transform .18s,box-shadow .18s;
  box-shadow:0 4px 20px rgba(200,16,46,.12);
}
.bday-card:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(200,16,46,.2);}
.bday-new{position:absolute;top:6px;right:6px;font-size:6px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;padding:2px 6px;border-radius:999px;color:#fff;background:var(--red);}
.bday-hook{font-family:'Playfair Display',serif;font-size:13px;font-weight:700;font-style:italic;color:rgba(200,16,46,.8);margin-bottom:2px;}
.bday-name{font-family:'Cinzel',serif;font-size:9px;font-weight:900;color:var(--red);letter-spacing:.5px;margin-bottom:6px;}
.bday-desc{font-size:9px;color:rgba(255,255,255,.45);line-height:1.5;flex:1;}
.bday-foot{display:flex;align-items:center;justify-content:space-between;margin-top:10px;}
.bday-price{font-family:'Playfair Display',serif;font-size:20px;font-weight:900;color:#fff;}
.bday-price span{font-size:9px;color:rgba(255,255,255,.4);font-weight:400;}
.bday-btn{background:linear-gradient(135deg,var(--red),var(--red2));color:#fff;padding:7px 14px;border-radius:6px;font-family:'Cinzel',serif;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;box-shadow:0 3px 12px rgba(200,16,46,.4);}

/* ── MARKETPLACE ROW ── */
.shop-card{
  flex:1;background:#fff;border-radius:10px;
  border:1px solid rgba(0,0,0,.07);
  overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 2px 12px rgba(0,0,0,.07);
  transition:transform .18s,box-shadow .18s;
  position:relative;min-width:0;
}
.shop-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.12);}
.shop-img{flex:1;min-height:0;overflow:hidden;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px;}
.shop-img-dark{background:linear-gradient(145deg,#0d0d0b,#1c1508);}
.shop-img-ph{background:#f5f2ec;}
.cj-lbl{font-family:'Cinzel',serif;font-size:9px;letter-spacing:4px;color:#c8941e;}
.cj-yr{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;color:#fff;letter-spacing:-1px;}
.cj-type{font-family:'Cinzel',serif;font-size:6.5px;letter-spacing:3px;color:rgba(200,148,30,.5);}
.ph-lbl{font-family:'Cinzel',serif;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(0,0,0,.18);}
.shop-foot{flex:0 0 auto;padding:8px 12px 10px;border-top:1px solid rgba(0,0,0,.05);}
.shop-name{font-family:'Playfair Display',serif;font-size:11px;font-weight:700;color:#111;margin-bottom:1px;}
.shop-sub{font-size:8px;color:#999;margin-bottom:7px;}
.shop-price{font-family:'Playfair Display',serif;font-size:17px;font-weight:900;color:var(--red);margin-bottom:7px;}
.shop-btns{display:flex;gap:6px;}
.btn-paypal{flex:1;text-align:center;background:#0070ba;color:#fff;padding:6px;border-radius:5px;font-size:7px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.btn-stripe{flex:1;text-align:center;background:linear-gradient(135deg,var(--red),var(--red2));color:#fff;padding:6px;border-radius:5px;font-size:7px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.btn-notify{display:inline-block;background:rgba(0,0,0,.07);color:#888;padding:6px 14px;border-radius:5px;font-size:7px;font-weight:800;letter-spacing:.8px;text-transform:uppercase;text-decoration:none;}
.avail{position:absolute;top:6px;right:6px;font-size:6px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:2px 6px;border-radius:999px;color:#fff;background:#16a34a;}
</style>
</head>
<body>

<!-- BANNER -->
<div class="banner">
  <div class="banner-brand">
    <img src="LOGO" class="banner-logo" alt="JStout Inc">
    <div class="banner-left">
      <div class="banner-title">Your Edge in Every Market</div>
      <div class="banner-sub">Newsletters &nbsp;&middot;&nbsp; AI Agents &nbsp;&middot;&nbsp; Websites &nbsp;&middot;&nbsp; Shop</div>
    </div>
  </div>
  <div class="banner-nav">
    <a href="#newsletters">Newsletters</a>
    <a href="#services">Services</a>
    <a href="#shop">Shop</a>
    <a href="mailto:frostbytehero@gmail.com">Contact</a>
  </div>
</div>

<!-- ROWS -->
<div class="rows">

  <!-- ROW 1: NEWSLETTERS -->
  <div class="row-wrap" id="newsletters">
    <div class="row-label">Newsletters</div>
    <div class="row-cards">

      <div class="nl-card">
        <span class="nl-live">&#9679; Live</span>
        <div class="nl-thumb"><img src="PREVIEW_CASH" alt="JStoutCash"></div>
        <div class="nl-body">
          <div>
            <div class="nl-name">&#128176; JStoutCash</div>
            <div class="nl-desc">52-wk lows, dividends &amp; options flow before the bell.</div>
          </div>
          <div class="nl-foot">
            <div class="nl-price">$2<span>/mo</span></div>
            <a href="https://buy.stripe.com/4gM4gsfrn4Ar5T19lr5Rm00" target="_blank" class="nl-btn">Subscribe</a>
          </div>
        </div>
      </div>

      <div class="nl-card nl-soon">
        <span class="nl-soon-tag">Coming Soon</span>
        <div class="nl-thumb"><img src="PREVIEW_HORSE" alt="JStoutHorse"></div>
        <div class="nl-body">
          <div>
            <div class="nl-name">&#127939; JStoutHorse</div>
            <div class="nl-desc">Pace analysis &amp; value overlays every race day.</div>
          </div>
          <div class="nl-foot">
            <div class="nl-price">$8<span>/mo</span></div>
            <span class="nl-soon-btn">Coming Soon</span>
          </div>
        </div>
      </div>

      <div class="nl-card nl-soon">
        <span class="nl-soon-tag">Coming Soon</span>
        <div class="nl-thumb"><img src="PREVIEW_MLB" alt="MLB"></div>
        <div class="nl-body">
          <div>
            <div class="nl-name">&#9918; MLB Newsletter</div>
            <div class="nl-desc">Hot bats, matchups &amp; value picks daily.</div>
          </div>
          <div class="nl-foot">
            <div class="nl-price">$2<span>/mo</span></div>
            <span class="nl-soon-btn">Coming Soon</span>
          </div>
        </div>
      </div>

      <div class="nl-card nl-soon">
        <span class="nl-soon-tag">Coming Soon</span>
        <div class="nl-thumb"><img src="PREVIEW_ODDS" alt="Odds"></div>
        <div class="nl-body">
          <div>
            <div class="nl-name">&#127922; Odds Report</div>
            <div class="nl-desc">Sharp line movement &amp; value plays across all leagues.</div>
          </div>
          <div class="nl-foot">
            <div class="nl-price">$2<span>/mo</span></div>
            <span class="nl-soon-btn">Coming Soon</span>
          </div>
        </div>
      </div>

      <div class="nl-card nl-soon">
        <span class="nl-soon-tag">Coming Soon</span>
        <div class="nl-thumb"><img src="PREVIEW_HOUSE" alt="JStoutHouse"></div>
        <div class="nl-body">
          <div>
            <div class="nl-name">&#127968; JStoutHouse</div>
            <div class="nl-desc">Market trends &amp; deal alerts for investors.</div>
          </div>
          <div class="nl-foot">
            <div class="nl-price">$5<span>/mo</span></div>
            <span class="nl-soon-btn">Coming Soon</span>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- ROW 2: SERVICES -->
  <div class="row-wrap row-wrap-dark" id="services">
    <div class="row-label row-label-light">Services &amp; AI</div>
    <div class="row-cards">

      <div class="bday-card">
        <span class="bday-new">&#9733; New</span>
        <div class="bday-hook">When's your next birthday?</div>
        <div class="bday-name">&#127874; B Day Execution</div>
        <div class="bday-desc">We search Walmart, buy the best gift in budget, get it wrapped &amp; ship it 3 days before the birthday. Set it once, done forever.</div>
        <div class="bday-foot">
          <div class="bday-price">$30<span>/mo</span></div>
          <a href="bday.html" class="bday-btn">Get Started</a>
        </div>
      </div>

      <div class="svc-card">
        <div class="svc-icon">&#127760;</div>
        <div class="svc-name">Websites</div>
        <div class="svc-desc">Fast, sharp, built to convert. Landing pages to full builds.</div>
        <a href="mailto:frostbytehero@gmail.com?subject=Website Inquiry" class="svc-cta">Get a Quote</a>
      </div>

      <div class="svc-card">
        <div class="svc-icon">&#129302;</div>
        <div class="svc-name">AI Agents</div>
        <div class="svc-desc">Custom automation. Set it once, runs itself.</div>
        <a href="mailto:frostbytehero@gmail.com?subject=AI Agent Inquiry" class="svc-cta">Get a Quote</a>
      </div>

      <div class="svc-card">
        <div class="svc-icon">&#9889;</div>
        <div class="svc-name">Performance</div>
        <div class="svc-desc">Speed audits &amp; Core Web Vitals. Make it fast enough to rank.</div>
        <a href="mailto:frostbytehero@gmail.com?subject=Performance Inquiry" class="svc-cta">Get a Quote</a>
      </div>

      <div class="svc-card">
        <div class="svc-icon">&#128200;</div>
        <div class="svc-name">SEO</div>
        <div class="svc-desc">Technical SEO &amp; local search domination.</div>
        <a href="mailto:frostbytehero@gmail.com?subject=SEO Inquiry" class="svc-cta">Get a Quote</a>
      </div>

    </div>
  </div>

  <!-- ROW 3: MARKETPLACE -->
  <div class="row-wrap" id="shop">
    <div class="row-label">Marketplace</div>
    <div class="row-cards">

      <!-- Cactus Jack -->
      <div class="shop-card">
        <span class="avail">In Stock</span>
        <div class="shop-img shop-img-dark">
          <div class="cj-lbl">Cactus Jack</div>
          <div class="cj-yr">2025</div>
          <div class="cj-type">NBA Hobby Box &middot; Factory Sealed</div>
        </div>
        <div class="shop-foot">
          <div class="shop-name">Cactus Jack 2025 NBA Hobby Box</div>
          <div class="shop-sub">Factory Sealed &middot; Travis Scott x NBA &middot; Ships Insured</div>
          <div class="shop-price">$1,000</div>
          <div class="shop-btns">
            <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business=frostbytehero%40gmail.com&item_name=Cactus+Jack+2025+NBA+Hobby+Box&amount=1000.00&currency_code=USD&no_shipping=0" target="_blank" class="btn-paypal">PayPal</a>
            <a href="mailto:frostbytehero@gmail.com?subject=Cactus Jack - Pay by Stripe" class="btn-stripe">Stripe</a>
          </div>
        </div>
      </div>

      <div class="shop-card">
        <div class="shop-img shop-img-ph"><div class="ph-lbl">Next Drop</div></div>
        <div class="shop-foot">
          <div class="shop-name" style="color:#ccc">Coming Soon</div>
          <div class="shop-sub">More inventory loading</div>
          <a href="mailto:frostbytehero@gmail.com?subject=Notify Me" class="btn-notify">Notify Me</a>
        </div>
      </div>

      <div class="shop-card">
        <div class="shop-img shop-img-ph"><div class="ph-lbl">Next Drop</div></div>
        <div class="shop-foot">
          <div class="shop-name" style="color:#ccc">Coming Soon</div>
          <div class="shop-sub">More inventory loading</div>
          <a href="mailto:frostbytehero@gmail.com?subject=Notify Me" class="btn-notify">Notify Me</a>
        </div>
      </div>

      <div class="shop-card">
        <div class="shop-img shop-img-ph"><div class="ph-lbl">Next Drop</div></div>
        <div class="shop-foot">
          <div class="shop-name" style="color:#ccc">Coming Soon</div>
          <div class="shop-sub">More inventory loading</div>
          <a href="mailto:frostbytehero@gmail.com?subject=Notify Me" class="btn-notify">Notify Me</a>
        </div>
      </div>

    </div>
  </div>

</div>
</body>
</html>"""

html = (html
    .replace("LOGO",          logo)
    .replace("PREVIEW_CASH",  previews['cash'])
    .replace("PREVIEW_HORSE", previews['horse'])
    .replace("PREVIEW_MLB",   previews['mlb'])
    .replace("PREVIEW_ODDS",  previews['odds'])
    .replace("PREVIEW_HOUSE", previews['house'])
)

with open(r'C:\Users\frost\JStoutInc\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Done. {len(html):,} chars written.")
