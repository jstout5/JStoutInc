import base64

with open(r'C:\Users\frost\Downloads\myLogo_still.png', 'rb') as f:
    logo = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>JStout Inc — Digital Products &amp; Services</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{--red:#c8102e;--red2:#a00c24;--white:#fff;--light:#f9f9f9;--dark:#111;--gray:#555;--border:#e0e0e0;}
body{font-family:"Segoe UI",Arial,sans-serif;background:var(--light);color:var(--dark);}

nav{background:var(--dark);padding:0 40px;display:flex;align-items:center;justify-content:space-between;height:80px;position:sticky;top:0;z-index:100;box-shadow:0 2px 12px rgba(0,0,0,.4);}
.nav-logo{display:flex;align-items:center;gap:14px;}
.nav-logo img{height:62px;}
.nav-logo span{color:#fff;font-size:22px;font-weight:700;letter-spacing:1px;}
.nav-links{display:flex;gap:28px;}
.nav-links a{color:rgba(255,255,255,.65);text-decoration:none;font-size:13px;letter-spacing:.5px;text-transform:uppercase;transition:color .2s;}
.nav-links a:hover{color:#fff;}
.nav-cta{background:var(--red);color:#fff;padding:9px 22px;border-radius:6px;font-size:13px;font-weight:700;letter-spacing:1px;text-decoration:none;text-transform:uppercase;}
.nav-cta:hover{background:var(--red2);}

.hero{background:linear-gradient(135deg,#0f0f0f 55%,#200008);padding:48px 40px 44px;text-align:center;}
.hero-badge{display:inline-block;background:rgba(200,16,46,.15);border:1px solid rgba(200,16,46,.4);color:var(--red);font-size:11px;letter-spacing:3px;text-transform:uppercase;padding:6px 18px;border-radius:20px;margin-bottom:18px;}
.hero h1{font-size:40px;font-weight:900;color:#fff;line-height:1.1;margin-bottom:12px;}
.hero h1 span{color:var(--red);}
.hero p{font-size:15px;color:rgba(255,255,255,.55);line-height:1.7;max-width:540px;margin:0 auto 28px;}
.hero-btns{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;}
.btn-primary{background:var(--red);color:#fff;padding:14px 36px;border-radius:8px;font-size:14px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;transition:background .2s;}
.btn-primary:hover{background:var(--red2);}
.btn-ghost{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.3);padding:14px 36px;border-radius:8px;font-size:14px;font-weight:600;letter-spacing:1px;text-transform:uppercase;text-decoration:none;}
.btn-ghost:hover{border-color:#fff;}

.stats{background:var(--red);padding:22px 40px;display:flex;justify-content:center;gap:60px;flex-wrap:wrap;}
.stat{text-align:center;color:#fff;}
.stat-num{font-size:30px;font-weight:900;}
.stat-label{font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:.8;margin-top:2px;}

.section{padding:80px 40px;max-width:1200px;margin:0 auto;}
.section-header{text-align:center;margin-bottom:56px;}
.section-header h2{font-size:36px;font-weight:800;margin-bottom:12px;}
.section-header p{color:var(--gray);font-size:16px;max-width:520px;margin:0 auto;}
.tag{display:inline-block;background:rgba(200,16,46,.1);color:var(--red);font-size:10px;letter-spacing:3px;text-transform:uppercase;padding:4px 12px;border-radius:12px;margin-bottom:16px;}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:28px;}
.card{background:#fff;border-radius:14px;padding:32px;border:1px solid var(--border);transition:transform .2s,box-shadow .2s;position:relative;overflow:hidden;}
.card::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--red);}
.card:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(0,0,0,.1);}
.card-icon{font-size:38px;margin-bottom:16px;}
.card-title{font-size:21px;font-weight:700;margin-bottom:8px;}
.card-desc{color:var(--gray);font-size:14px;line-height:1.65;margin-bottom:20px;}
.card-price{display:flex;align-items:baseline;gap:4px;margin-bottom:20px;}
.price-num{font-size:34px;font-weight:900;color:var(--red);}
.price-period{font-size:13px;color:var(--gray);}
.price-free{font-size:22px;font-weight:800;color:#22a05a;}
.card-btn{display:block;text-align:center;background:var(--dark);color:#fff;padding:12px;border-radius:8px;font-size:13px;font-weight:600;letter-spacing:.5px;text-decoration:none;transition:background .2s;}
.card-btn:hover{background:var(--red);}
.badge{position:absolute;top:20px;right:20px;font-size:9px;font-weight:800;letter-spacing:2px;text-transform:uppercase;padding:4px 10px;border-radius:20px;color:#fff;}
.badge-hot{background:#ff6b00;}
.badge-new{background:var(--red);}
.badge-soon{background:#555;}

.services-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;}
.svc{background:#fff;border-radius:12px;padding:28px;border:1px solid var(--border);display:flex;gap:18px;align-items:flex-start;transition:box-shadow .2s;}
.svc:hover{box-shadow:0 8px 24px rgba(0,0,0,.08);}
.svc-icon{font-size:26px;flex-shrink:0;width:52px;height:52px;background:rgba(200,16,46,.08);border-radius:10px;display:flex;align-items:center;justify-content:center;}
.svc-title{font-size:16px;font-weight:700;margin-bottom:6px;}
.svc-desc{font-size:13px;color:var(--gray);line-height:1.6;}

.bg-white{background:#fff;}
.mkt-section{background:#fff;padding:80px 0;}

.cta-section{background:linear-gradient(135deg,#0f0f0f,#1a0006);padding:90px 40px;text-align:center;}
.cta-section h2{font-size:42px;font-weight:900;color:#fff;margin-bottom:16px;}
.cta-section p{color:rgba(255,255,255,.55);font-size:16px;margin-bottom:36px;max-width:500px;margin-left:auto;margin-right:auto;}

footer{background:#080808;padding:44px 40px;text-align:center;border-top:1px solid #1a1a1a;}
.footer-logo{display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:14px;}
.footer-logo img{height:34px;opacity:.75;}
.footer-logo span{color:rgba(255,255,255,.55);font-size:17px;font-weight:700;}
footer p{color:rgba(255,255,255,.25);font-size:12px;letter-spacing:.5px;}
</style>
</head>
<body>

<nav>
  <div class="nav-logo">
    <img src="LOGO_PLACEHOLDER" alt="JStout Inc">
    <span>JStout Inc</span>
  </div>
  <div class="nav-links">
    <a href="#products">Products</a>
    <a href="#services">Services</a>
    <a href="#marketplace">Marketplace</a>
  </div>
  <a href="#products" class="nav-cta">Get Started</a>
</nav>

<section class="hero">
  <div class="hero-badge">Intelligence &middot; Tools &middot; Results</div>
  <h1>Your Edge in<br><span>Every Market</span></h1>
  <p>Premium newsletters, AI-powered tools, and digital products built for serious investors, sports bettors, collectors, and believers.</p>
  <div class="hero-btns">
    <a href="#products" class="btn-primary">Browse Products</a>
    <a href="#services" class="btn-ghost">Our Services</a>
  </div>
</section>

<div class="stats">
  <div class="stat"><div class="stat-num">8+</div><div class="stat-label">Products</div></div>
  <div class="stat"><div class="stat-num">$2</div><div class="stat-label">Starting Price</div></div>
  <div class="stat"><div class="stat-num">Daily</div><div class="stat-label">Intelligence</div></div>
  <div class="stat"><div class="stat-num">KY</div><div class="stat-label">Built &amp; Based</div></div>
</div>

<section class="section" id="products">
  <div class="section-header">
    <div class="tag">Subscriptions</div>
    <h2>Premium Products</h2>
    <p>Data-driven newsletters and tools built to give you an edge &mdash; delivered daily.</p>
  </div>
  <div class="grid">

    <div class="card">
      <span class="badge badge-hot">Popular</span>
      <div class="card-icon">&#128200;</div>
      <div class="card-title">JStoutCash</div>
      <div class="card-desc">Daily stock market intelligence. 52-week lows, dividend plays, options flow, and top movers &mdash; curated every morning before the bell.</div>
      <div class="card-price"><span class="price-num">$2</span><span class="price-period">&nbsp;/month</span></div>
      <a href="#" class="card-btn">Subscribe</a>
    </div>

    <div class="card">
      <div class="card-icon">&#127936;</div>
      <div class="card-title">NBA Odds Report</div>
      <div class="card-desc">Sharp betting intelligence for NBA. Line movement, value plays, injury updates, and prop picks &mdash; sent before tip-off.</div>
      <div class="card-price"><span class="price-num">$2</span><span class="price-period">&nbsp;/month</span></div>
      <a href="#" class="card-btn">Subscribe</a>
    </div>

    <div class="card">
      <span class="badge badge-hot">Best Value</span>
      <div class="card-icon">&#127950;</div>
      <div class="card-title">JStoutHorse</div>
      <div class="card-desc">Horse racing picks and handicapping data. Track conditions, pace analysis, trainer stats, and value overlays for every major race.</div>
      <div class="card-price"><span class="price-num">$8</span><span class="price-period">&nbsp;/month</span></div>
      <a href="#" class="card-btn">Subscribe</a>
    </div>

    <div class="card">
      <span class="badge badge-new">New</span>
      <div class="card-icon">&#127968;</div>
      <div class="card-title">Real Estate Report</div>
      <div class="card-desc">Local market intelligence for buyers, sellers, and investors. Price trends, new listings, and deal alerts in your area.</div>
      <div class="card-price"><span class="price-num">$5</span><span class="price-period">&nbsp;/month</span></div>
      <a href="#" class="card-btn">Subscribe</a>
    </div>

    <div class="card">
      <div class="card-icon">&#128214;</div>
      <div class="card-title">Scripture &amp; Soul</div>
      <div class="card-desc">Daily scripture, devotionals, and spiritual reflection. Built with faith at the center &mdash; delivered to your inbox every morning.</div>
      <div class="card-price"><span class="price-free">Free</span></div>
      <a href="#" class="card-btn">Subscribe</a>
    </div>

    <div class="card">
      <span class="badge badge-soon">Coming Soon</span>
      <div class="card-icon">&#129302;</div>
      <div class="card-title">AI Agent Marketplace</div>
      <div class="card-desc">Custom-built AI agents for your business &mdash; lead gen, research, report writing, and automation. Buy or commission your own.</div>
      <div class="card-price"><span class="price-num">$25</span><span class="price-period">+ / agent</span></div>
      <a href="#" class="card-btn">Join Waitlist</a>
    </div>

  </div>
</section>

<section class="mkt-section" id="marketplace">
  <div class="section" style="padding-top:0;padding-bottom:0;">
    <div class="section-header">
      <div class="tag">Marketplace</div>
      <h2>Buy &amp; Sell Direct</h2>
      <p>Skip the eBay fees. List your collectables and gear directly to buyers with zero platform cuts.</p>
    </div>
    <div class="grid">
      <div class="card">
        <div class="card-icon">&#127183;</div>
        <div class="card-title">Pokemon Lookup</div>
        <div class="card-desc">Instant card value lookup, set data, and graded sales history. Know what you have before you buy or sell.</div>
        <div class="card-price"><span class="price-free">Free</span></div>
        <a href="#" class="card-btn">Use Tool</a>
      </div>
      <div class="card">
        <div class="card-icon">&#128721;</div>
        <div class="card-title">Collectables Market</div>
        <div class="card-desc">List and sell sports cards, Pokemon, memorabilia, and collectables directly to buyers. Zero platform fees &mdash; keep every dollar.</div>
        <div class="card-price"><span class="price-free">Free to List</span></div>
        <a href="#" class="card-btn">Start Selling</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="services">
  <div class="section-header">
    <div class="tag">Services</div>
    <h2>We Build Digital</h2>
    <p>Custom websites, newsletters, and automation &mdash; done right and delivered fast.</p>
  </div>
  <div class="services-grid">
    <div class="svc">
      <div class="svc-icon">&#127760;</div>
      <div>
        <div class="svc-title">Website Design</div>
        <div class="svc-desc">Custom, mobile-ready websites for small businesses, outfitters, and professionals. No templates &mdash; built for your brand.</div>
      </div>
    </div>
    <div class="svc">
      <div class="svc-icon">&#128231;</div>
      <div>
        <div class="svc-title">Newsletter Systems</div>
        <div class="svc-desc">Automated email newsletters with real data. Daily, weekly, or triggered &mdash; we build and run the whole pipeline.</div>
      </div>
    </div>
    <div class="svc">
      <div class="svc-icon">&#9889;</div>
      <div>
        <div class="svc-title">Automation &amp; AI</div>
        <div class="svc-desc">Cut hours of manual work to seconds with custom AI agents and business automation tools built for your workflow.</div>
      </div>
    </div>
    <div class="svc">
      <div class="svc-icon">&#128202;</div>
      <div>
        <div class="svc-title">Data &amp; Analytics</div>
        <div class="svc-desc">Custom dashboards and data pipelines. Stocks, sales, traffic, or betting lines &mdash; know your numbers in real time.</div>
      </div>
    </div>
  </div>
</section>

<section class="cta-section">
  <h2>Ready to Get Started?</h2>
  <p>Pick a plan, subscribe, and get your first briefing tomorrow morning.</p>
  <a href="#products" class="btn-primary">Browse All Products</a>
</section>

<footer>
  <div class="footer-logo">
    <img src="LOGO_PLACEHOLDER" alt="JStout Inc">
    <span>JStout Inc</span>
  </div>
  <p>&copy; 2026 JStout Inc &middot; Kentucky &middot; Built with purpose.</p>
</footer>

</body>
</html>"""

html = html.replace("LOGO_PLACEHOLDER", logo)

with open(r'C:\Users\frost\JStoutInc\index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
