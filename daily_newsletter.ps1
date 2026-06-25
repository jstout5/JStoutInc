# JStoutCash Daily Newsletter — generate PDF, rebuild hub preview, push to GitHub
$PYTHON    = "C:\Users\frost\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$LOG       = "C:\Users\frost\JStoutInc\daily_newsletter.log"
$NL_SCRIPT = "C:\Users\frost\JStoutCash\tools\generate_newsletter.py"
$BUILD     = "C:\Users\frost\JStoutInc\build.py"
$REPO      = "C:\Users\frost\JStoutInc"

function Log { param([string]$msg); $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"; Add-Content -Path $LOG -Value "$ts  $msg" -Encoding UTF8 }

Log "========================================="
Log "Starting daily newsletter update"
Log "Generating newsletter PDF..."
& $PYTHON $NL_SCRIPT
$code1 = $LASTEXITCODE
Log "Newsletter exit code: $code1"
if ($code1 -ne 0) { Log "ERROR: newsletter generation failed"; exit 1 }
Log "Rebuilding hub site..."
& $PYTHON $BUILD
$code2 = $LASTEXITCODE
Log "Build exit code: $code2"
if ($code2 -ne 0) { Log "ERROR: build.py failed"; exit 1 }
Log "Committing changes..."
Set-Location $REPO
& git add index.html preview_cash.html
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $d = Get-Date -Format "yyyy-MM-dd"
    & git commit -m "Daily update $d"
    & git push
    if ($LASTEXITCODE -eq 0) { Log "Pushed to GitHub." } else { Log "ERROR: git push failed."; exit 1 }
} else {
    Log "No changes — nothing to push."
}
Log "Done."
