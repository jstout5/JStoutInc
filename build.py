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
    if not pdfs:
        raise FileNotFoundError(f"No PDFs found in {folder}")
    print(f"  {pdfs[0].name}")
    return pdfs[0]

logo      = img_b64(r'C:\Users\frost\Downloads\myLogo_still.png')
bulldog   = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstoutCash.png')
horse     = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstouthorst.png')
mlb_img   = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstoutmlb.png')
house_img = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstouthouse.png')
nba_img   = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstoutnba.png')
bible_img     = img_b64(r'C:\Users\frost\BrushyCreek\assets\images\jstoutBible.png')
bible_preview = img_b64(r'C:\Users\frost\JStoutInc\bible_preview.png')

previews = {
    'cash':    pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutCash', 'JStoutCash_*.pdf')),
    'horse':   pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutHorse', 'JStoutHorse_Report_*.pdf')),
    'mlb':     pdf_preview_b64(latest_pdf(r'C:\Users\frost\MLBNewsletter', 'newsletter_*.pdf')),
    'odds':    pdf_preview_b64(latest_pdf(r'C:\Users\frost\OddsNewsletter', 'newsletter_*.pdf')),
    'house':   pdf_preview_b64(latest_pdf(r'C:\Users\frost\JStoutHouse', 'JStoutHouse_*.pdf')),
    'pokemon': pdf_preview_b64(latest_pdf(r'C:\Users\frost\Pokemon\card_reports')),
}
print("PDFs rendered.")

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>JStout Inc — Your Edge in Every Market</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{--red:#c8102e;--red2:#9e0c24;--gray:#777;}
html,body{height:100vh;overflow:hidden;display:flex;flex-direction:column;}
body{font-family:"Segoe UI",system-ui,Arial,sans-serif;background:#f0eadb;color:#1a1a1a;}

/* ── NAV ── */
nav{
  flex:0 0 54px;background:#f0eadb;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 28px;
  border-bottom:1px solid rgba(0,0,0,.08);
  box-shadow:0 2px 14px rgba(0,0,0,.07);
  position:relative;z-index:10;
}
.nav-brand{
  font-family:'Playfair Display',serif;
  font-size:28px;font-weight:900;letter-spacing:-.5px;
  color:var(--red);text-shadow:0 2px 14px rgba(200,16,46,.18);
}
.nav-tagline{
  font-family:'Cinzel',serif;font-size:9.5px;font-weight:700;
  letter-spacing:3.5px;text-transform:uppercase;color:rgba(40,20,0,.32);
}
.nav-links{display:flex;gap:28px;}
.nav-links a{
  font-family:'Cinzel',serif;font-size:11px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;
  color:rgba(60,35,0,.4);text-decoration:none;transition:color .2s;
}
.nav-links a:hover{color:var(--red);}

/* ── HERO BANNER ── */
.hero{
  flex:0 0 88px;display:flex;align-items:center;gap:22px;
  padding:0 28px;
  border-bottom:2px solid rgba(200,16,46,.12);
  background:#f0eadb;
}
.hero-logo{
  height:68px;width:auto;flex-shrink:0;
  mix-blend-mode:multiply;
  -webkit-mask-image:radial-gradient(ellipse 90% 85% at 50% 44%,black 25%,rgba(0,0,0,.85) 44%,rgba(0,0,0,.35) 64%,transparent 85%);
  mask-image:radial-gradient(ellipse 90% 85% at 50% 44%,black 25%,rgba(0,0,0,.85) 44%,rgba(0,0,0,.35) 64%,transparent 85%);
}
.hero-divider{width:1px;height:50px;background:rgba(0,0,0,.09);flex-shrink:0;}
.hero-text{flex:1;}
.hub-brand{
  font-family:'Playfair Display',serif;
  font-size:28px;font-weight:900;letter-spacing:-1px;
  color:var(--red);text-shadow:0 3px 18px rgba(200,16,46,.2);
  line-height:1;
}
.hub-tagline{
  font-family:'Playfair Display',serif;
  font-size:13px;font-weight:700;font-style:italic;
  color:rgba(20,10,0,.5);line-height:1.4;margin-top:3px;
}
.hub-sub{
  font-family:'Cinzel',serif;font-size:8px;font-weight:700;
  letter-spacing:3px;text-transform:uppercase;
  color:rgba(40,20,0,.32);margin-top:4px;
}
.hub-cta{
  display:inline-block;
  background:linear-gradient(135deg,var(--red),var(--red2));
  color:#fff;padding:9px 22px;border-radius:7px;
  font-family:'Cinzel',serif;font-size:9px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;text-decoration:none;
  box-shadow:0 4px 18px rgba(200,16,46,.35);
  transition:transform .2s,box-shadow .2s;flex-shrink:0;
}
.hub-cta:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(200,16,46,.5);}

/* ── MAIN CONTENT ── */
.main-content{
  flex:1;display:flex;flex-direction:column;
  padding:8px 10px;gap:7px;min-height:0;overflow:hidden;
}
.content-section{flex:1;display:flex;flex-direction:column;min-height:0;}
.section-label{
  font-family:'Cinzel',serif;font-size:7.5px;font-weight:700;
  letter-spacing:3px;text-transform:uppercase;
  color:rgba(40,20,0,.3);margin-bottom:5px;flex:0 0 auto;
}
.card-row{flex:1;display:flex;gap:8px;min-height:0;}

/* ── CARDS ── */
.card{
  flex:1;background:#fff;border-radius:13px;
  border:1px solid rgba(0,0,0,.06);
  overflow:hidden;display:flex;flex-direction:column;
  box-shadow:0 3px 14px rgba(0,0,0,.08);
  transition:transform .2s,box-shadow .2s;
  position:relative;min-width:0;
}
.card:hover{transform:translateY(-3px);box-shadow:0 12px 36px rgba(0,0,0,.12);}
.card-top{padding:10px 13px 7px;flex-shrink:0;}
.card-img-icon{width:34px;height:34px;border-radius:7px;object-fit:cover;margin-bottom:5px;display:block;box-shadow:0 2px 7px rgba(0,0,0,.12);}
.card-icon{font-size:24px;margin-bottom:4px;}
.card-title{
  display:inline-block;font-size:9px;font-weight:800;
  font-family:'Cinzel',serif;letter-spacing:.5px;
  background:rgba(200,16,46,.08);color:var(--red);
  padding:3px 10px;border-radius:999px;
  border:1px solid rgba(200,16,46,.15);
  margin-bottom:4px;
}
.card-desc{color:var(--gray);font-size:9.5px;line-height:1.5;margin-bottom:5px;}
.card-price{font-size:18px;font-weight:900;color:var(--red);font-family:'Playfair Display',serif;letter-spacing:-.3px;}
.card-price span{font-size:10px;font-weight:400;color:var(--gray);font-family:"Segoe UI",sans-serif;}
.price-free{font-size:13px;font-weight:800;color:#16a34a;font-family:'Playfair Display',serif;}
.badge{position:absolute;top:7px;right:7px;font-size:6.5px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;padding:3px 6px;border-radius:999px;color:#fff;}
.badge-hot{background:linear-gradient(135deg,#f97316,#ea6000);}
.badge-new{background:linear-gradient(135deg,var(--red),var(--red2));}

/* ── PREVIEW ── */
.preview-wrap{flex:1;min-height:0;overflow:hidden;border-top:1px solid rgba(0,0,0,.05);cursor:pointer;position:relative;}
.preview-wrap img{width:100%;display:block;transition:transform .5s ease;}
.card:hover .preview-wrap img{transform:scale(1.04);}
.preview-fill{width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#f8f8f8;}
.preview-fade{position:absolute;bottom:0;left:0;right:0;height:80px;background:linear-gradient(transparent,rgba(255,255,255,.97));}
.preview-lock{position:absolute;bottom:0;left:0;right:0;padding:7px 11px;text-align:center;}
.lock-btn{
  display:inline-block;
  background:linear-gradient(135deg,var(--red),var(--red2));
  color:#fff;padding:5px 13px;border-radius:6px;
  font-size:8px;font-weight:800;letter-spacing:1px;text-transform:uppercase;
  text-decoration:none;
  box-shadow:0 3px 10px rgba(200,16,46,.3);
  transition:box-shadow .2s,transform .15s;
}
.lock-btn:hover{box-shadow:0 5px 16px rgba(200,16,46,.5);transform:translateY(-1px);}
.lock-note{font-size:8px;color:var(--gray);margin-top:2px;}

/* ── B DAY EXECUTION ACCENT ── */
.card-bday{
  border:1.5px solid rgba(200,16,46,.22);
  background:linear-gradient(155deg,#fff 70%,rgba(200,16,46,.04));
}
.bday-headline{
  font-family:'Playfair Display',serif;font-size:11px;font-weight:700;font-style:italic;
  color:rgba(20,10,0,.55);margin-bottom:3px;line-height:1.2;
}

/* ── SERVICES ── */
.services{
  flex:0 0 auto;display:flex;gap:10px;
  padding:0 10px 9px;height:98px;
}
.service-card{
  flex:1;background:#fff;border-radius:13px;
  border:1px solid rgba(0,0,0,.06);
  box-shadow:0 3px 14px rgba(0,0,0,.08);
  display:flex;align-items:center;gap:14px;
  padding:11px 17px;
  transition:transform .2s,box-shadow .2s;
}
.service-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.13);}
.service-icon{font-size:28px;flex-shrink:0;}
.service-name{
  font-family:'Playfair Display',serif;font-size:14px;font-weight:900;
  color:#1a1a1a;letter-spacing:-.3px;margin-bottom:2px;
}
.service-desc{font-size:9px;color:var(--gray);line-height:1.45;margin-bottom:6px;}
.service-cta{
  display:inline-block;
  background:linear-gradient(135deg,var(--red),var(--red2));
  color:#fff;padding:4px 12px;border-radius:5px;
  font-family:'Cinzel',serif;font-size:7.5px;font-weight:700;
  letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;
  box-shadow:0 2px 8px rgba(200,16,46,.3);
  transition:box-shadow .15s,transform .15s;
}
.service-cta:hover{box-shadow:0 4px 14px rgba(200,16,46,.5);transform:translateY(-1px);}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-brand">JStout Inc</div>
  <div class="nav-tagline">Your Edge in Every Market &nbsp;&middot;&nbsp; AI &middot; Analytics &middot; Sports &middot; Real Estate</div>
  <div class="nav-links">
    <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc Bundle Subscription">Subscribe</a>
    <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc Services Inquiry">Services</a>
    <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc Contact">Contact</a>
  </div>
</nav>

<!-- HERO BANNER -->
<div class="hero">
  <img src="LOGO" class="hero-logo" alt="JStout Inc">
  <div class="hero-divider"></div>
  <div class="hero-text">
    <div class="hub-brand">JStout Inc</div>
    <div class="hub-tagline">Your <em>Edge</em> in <em>Every</em> Market</div>
    <div class="hub-sub">AI &middot; Analytics &middot; Sports &middot; Real Estate</div>
  </div>
  <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc Bundle Subscription" class="hub-cta">Get the Bundle</a>
</div>

<!-- MAIN CONTENT -->
<div class="main-content">

  <!-- NEWSLETTERS & INTELLIGENCE -->
  <div class="content-section">
    <div class="section-label">Newsletters &amp; Intelligence</div>
    <div class="card-row">

      <!-- JStoutCash -->
      <div class="card">
        <span class="badge badge-hot">Popular</span>
        <div class="card-top">
          <img src="BULLDOG" class="card-img-icon" alt="JStoutCash">
          <div class="card-title">JStoutCash</div>
          <div class="card-desc">Daily stock intel. 52-week lows, dividend plays, options flow &amp; top movers before the bell.</div>
          <div class="card-price">$2 <span>/month</span></div>
        </div>
        <div class="preview-wrap">
          <img src="PREVIEW_CASH" alt="JStoutCash Preview">
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=Subscribe to JStoutCash" class="lock-btn">&#128274; Subscribe</a>
            <div class="lock-note">$2/month &middot; Cancel anytime</div>
          </div>
        </div>
      </div>

      <!-- JStoutHorse -->
      <div class="card">
        <span class="badge badge-hot">Best Value</span>
        <div class="card-top">
          <img src="HORSE" class="card-img-icon" alt="JStoutHorse">
          <div class="card-title">JStoutHorse</div>
          <div class="card-desc">Horse racing picks. Track conditions, pace analysis &amp; value overlays for every major race.</div>
          <div class="card-price">$8 <span>/month</span></div>
        </div>
        <div class="preview-wrap">
          <img src="PREVIEW_HORSE" alt="JStoutHorse Preview">
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=Subscribe to JStoutHorse" class="lock-btn">&#128274; Subscribe</a>
            <div class="lock-note">$8/month &middot; Cancel anytime</div>
          </div>
        </div>
      </div>

      <!-- MLB -->
      <div class="card">
        <div class="card-top">
          <img src="MLB_IMG" class="card-img-icon" alt="MLB Newsletter">
          <div class="card-title">MLB Newsletter</div>
          <div class="card-desc">Daily baseball. Hot bats, pitcher matchups &amp; value picks for the serious fan.</div>
          <div class="card-price">$2 <span>/month</span></div>
        </div>
        <div class="preview-wrap">
          <img src="PREVIEW_MLB" alt="MLB Preview">
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=Subscribe to MLB Newsletter" class="lock-btn">&#128274; Subscribe</a>
            <div class="lock-note">$2/month &middot; Cancel anytime</div>
          </div>
        </div>
      </div>

      <!-- JStoutHouse -->
      <div class="card">
        <span class="badge badge-new">New</span>
        <div class="card-top">
          <img src="HOUSE_IMG" class="card-img-icon" alt="JStoutHouse">
          <div class="card-title">JStoutHouse</div>
          <div class="card-desc">Real estate intel. Market trends, new listings &amp; deal alerts delivered daily.</div>
          <div class="card-price">$5 <span>/month</span></div>
        </div>
        <div class="preview-wrap">
          <img src="PREVIEW_HOUSE" alt="JStoutHouse Preview">
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=Subscribe to JStoutHouse" class="lock-btn">&#128274; Subscribe</a>
            <div class="lock-note">$5/month &middot; Cancel anytime</div>
          </div>
        </div>
      </div>

      <!-- Odds Report -->
      <div class="card">
        <div class="card-top">
          <img src="NBA_IMG" class="card-img-icon" alt="Odds Report">
          <div class="card-title">Odds Report</div>
          <div class="card-desc">Sharp betting intel. Line movement, value plays &amp; prop picks across all major leagues.</div>
          <div class="card-price">$2 <span>/month</span></div>
        </div>
        <div class="preview-wrap">
          <img src="PREVIEW_ODDS" alt="Odds Preview">
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=Subscribe to Odds Report" class="lock-btn">&#128274; Subscribe</a>
            <div class="lock-note">$2/month &middot; Cancel anytime</div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- MARKETPLACE & APPS -->
  <div class="content-section">
    <div class="section-label">Marketplace &amp; Apps</div>
    <div class="card-row">

      <!-- Scripture & Soul -->
      <div class="card">
        <div class="card-top">
          <img src="BIBLE_IMG" class="card-img-icon" alt="Scripture &amp; Soul">
          <div class="card-title">Scripture &amp; Soul</div>
          <div class="card-desc">Daily devotionals &amp; spiritual reflection. Built with faith at the center.</div>
          <div class="price-free">Free</div>
        </div>
        <div class="preview-wrap">
          <img src="BIBLE_PREVIEW" alt="Still Waters Bible App">
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="https://still-waters-scripture.onrender.com/read" target="_blank" class="lock-btn">Open App &rarr;</a>
            <div class="lock-note">Free &middot; No account needed</div>
          </div>
        </div>
      </div>

      <!-- Pokemon Lookup -->
      <div class="card">
        <div class="card-top">
          <div class="card-icon">&#127183;</div>
          <div class="card-title">Pokemon Lookup</div>
          <div class="card-desc">Card values, set data &amp; graded sales history. Know before you buy or sell.</div>
          <div class="price-free">Free</div>
        </div>
        <div class="preview-wrap">
          <img src="PREVIEW_POKEMON" alt="Pokemon Preview">
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc - Pokemon Lookup Access" class="lock-btn">Get Access &rarr;</a>
            <div class="lock-note">Free &middot; Email for access</div>
          </div>
        </div>
      </div>

      <!-- Collectables Market -->
      <div class="card">
        <div class="card-top">
          <div class="card-icon">&#128721;</div>
          <div class="card-title">Collectables Market</div>
          <div class="card-desc">List cards, Pokémon &amp; memorabilia. Zero eBay fees — keep every dollar.</div>
          <div class="price-free">Free to List</div>
        </div>
        <div class="preview-wrap">
          <div class="preview-fill">
            <div style="text-align:center;color:#bbb;padding:12px;">
              <div style="font-size:36px;margin-bottom:5px;">&#128721;</div>
              <div style="font-size:9px;letter-spacing:1.5px;text-transform:uppercase;">Coming Soon</div>
            </div>
          </div>
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=JStoutCollectables - Sell Item" class="lock-btn">Join Waitlist</a>
            <div class="lock-note">Free to list &middot; Keep 100%</div>
          </div>
        </div>
      </div>

      <!-- B Day Execution -->
      <div class="card card-bday">
        <span class="badge badge-new">New</span>
        <div class="card-top">
          <div class="card-icon">&#127874;</div>
          <div class="bday-headline">When's your next birthday?</div>
          <div class="card-title">B Day Execution</div>
          <div class="card-desc">Set it once &mdash; we find the perfect gift, buy it on Prime, gift wrap it &amp; ship to your door 3 days before the birthday. Fully automated.</div>
          <div class="card-price">$3 <span>/month</span></div>
        </div>
        <div class="preview-wrap">
          <div class="preview-fill">
            <div style="text-align:center;color:#ccc;padding:10px;">
              <div style="font-size:38px;margin-bottom:5px;">&#127874;</div>
              <div style="font-size:8.5px;letter-spacing:1.5px;text-transform:uppercase;color:#bbb;">AI Gift Agent</div>
            </div>
          </div>
          <div class="preview-fade"></div>
          <div class="preview-lock">
            <a href="mailto:frostbytehero@gmail.com?subject=B Day Execution - Sign Up" class="lock-btn">&#127873; Get Started &mdash; $3/mo</a>
            <div class="lock-note">Never miss a birthday again</div>
          </div>
        </div>
      </div>

    </div>
  </div>

</div>

<!-- SERVICES -->
<div class="services">

  <div class="service-card">
    <div class="service-icon">&#127760;</div>
    <div>
      <div class="service-name">Websites</div>
      <div class="service-desc">Custom-built sites that convert. Fast, sharp &amp; built to rank from day one.</div>
      <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc - Website Inquiry" class="service-cta">Get a Quote</a>
    </div>
  </div>

  <div class="service-card">
    <div class="service-icon">&#129302;</div>
    <div>
      <div class="service-name">AI Agents</div>
      <div class="service-desc">B Day Execution &amp; custom automation built around your workflow. We build it, it runs itself.</div>
      <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc - AI Agent Inquiry" class="service-cta">Get a Quote</a>
    </div>
  </div>

  <div class="service-card">
    <div class="service-icon">&#9889;</div>
    <div>
      <div class="service-name">Performance</div>
      <div class="service-desc">Speed tuning, Core Web Vitals &amp; load time optimization that users &amp; Google notice.</div>
      <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc - Performance Inquiry" class="service-cta">Get a Quote</a>
    </div>
  </div>

  <div class="service-card">
    <div class="service-icon">&#128200;</div>
    <div>
      <div class="service-name">SEO</div>
      <div class="service-desc">Rank higher. Technical SEO, content strategy &amp; local search domination.</div>
      <a href="mailto:frostbytehero@gmail.com?subject=JStout Inc - SEO Inquiry" class="service-cta">Get a Quote</a>
    </div>
  </div>

</div>

</body>
</html>"""

html = (html
    .replace("LOGO", logo)
    .replace("HORSE", horse)
    .replace("BULLDOG", bulldog)
    .replace("MLB_IMG", mlb_img)
    .replace("HOUSE_IMG", house_img)
    .replace("NBA_IMG", nba_img)
    .replace("BIBLE_IMG", bible_img)
    .replace("BIBLE_PREVIEW", bible_preview)
    .replace("PREVIEW_CASH", previews['cash'])
    .replace("PREVIEW_HORSE", previews['horse'])
    .replace("PREVIEW_MLB", previews['mlb'])
    .replace("PREVIEW_ODDS", previews['odds'])
    .replace("PREVIEW_HOUSE", previews['house'])
    .replace("PREVIEW_POKEMON", previews['pokemon'])
)

with open(r'C:\Users\frost\JStoutInc\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Done. {len(html):,} chars written.")
