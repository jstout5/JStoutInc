# JStoutCash Daily Newsletter — generates PDF, rebuilds hub preview, pushes to GitHub
# Scheduled daily at 9:00 AM

$LogFile = "C:\Users\frost\JStoutInc\daily_newsletter.log"

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$ts  $msg" | Out-File -Append -FilePath $LogFile -Encoding utf8
}

Log "========================================="
Log "Starting daily newsletter update"

# Step 1: Generate newsletter PDF
Log "Generating newsletter PDF..."
$out = & python "C:\Users\frost\JStoutCash\tools\generate_newsletter.py" 2>&1
Log $out
if ($LASTEXITCODE -ne 0) {
    Log "ERROR: newsletter generation failed (exit $LASTEXITCODE)"
    exit 1
}
Log "Newsletter PDF generated."

# Step 2: Rebuild hub site — picks up new PDF for index.html preview + preview_cash.html
Log "Rebuilding hub site..."
$out = & python "C:\Users\frost\JStoutInc\build.py" 2>&1
Log $out
if ($LASTEXITCODE -ne 0) {
    Log "ERROR: build.py failed (exit $LASTEXITCODE)"
    exit 1
}
Log "Hub site rebuilt."

# Step 3: Commit and push
Log "Committing and pushing..."
$date = Get-Date -Format "yyyy-MM-dd"
Set-Location "C:\Users\frost\JStoutInc"
git add index.html preview_cash.html
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "Daily update $date"
    git push
    if ($LASTEXITCODE -eq 0) {
        Log "Pushed to GitHub — Render will auto-deploy."
    } else {
        Log "ERROR: git push failed."
    }
} else {
    Log "No changes to commit."
}

Log "Done."
