# [DEPRECATED - 2026-11-10]: GCP Cloud Run hosting is deprecated due to closed GCP billing account.
# PDF/Charm generation is transitioned to Render (see render.yaml). Kept for reference only.
# Single-session Cloud Run deployment & Pages secret provisioning
$ErrorActionPreference = "Stop"

$GCLOUD = "C:\Users\Bhaskr Singh\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
$GCP_PROJECT = "project-b73607a3-4c7a-4120-bbb"
$GCP_REGION = "asia-south1"
$SERVICE_NAME = "pdf-service"

Write-Host "=== 1. Syncing pdf_service modules ==="
python scripts/sync_pdf_service.py

Write-Host "=== 2. Setting GCP project configuration ==="
& $GCLOUD config set project $GCP_PROJECT

$PROJECT_NUMBER = (& $GCLOUD projects describe $GCP_PROJECT --format="value(projectNumber)").Trim()
$SERVICE_ACCOUNT = "${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
Write-Host "Target GCP Project: $GCP_PROJECT (Number: $PROJECT_NUMBER)"
Write-Host "Compute Service Account: $SERVICE_ACCOUNT"

Write-Host "=== 3. Granting Required Cloud Build & Storage Roles to Compute SA ==="
& $GCLOUD projects add-iam-policy-binding $GCP_PROJECT `
  --member="serviceAccount:${SERVICE_ACCOUNT}" `
  --role="roles/storage.objectViewer"

& $GCLOUD projects add-iam-policy-binding $GCP_PROJECT `
  --member="serviceAccount:${SERVICE_ACCOUNT}" `
  --role="roles/cloudbuild.builds.builder"

Write-Host "=== 4. Generating / Verifying 64-hex PDF_SERVICE_SECRET ==="
$PDF_SERVICE_SECRET = node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
if ($PDF_SERVICE_SECRET.Length -ne 64) { throw "PDF_SERVICE_SECRET must be 64 characters." }

Write-Host "=== 5. Storing secret in Google Secret Manager ==="
$secretFile = "$env:TEMP\pdf_secret.txt"
[System.IO.File]::WriteAllText($secretFile, $PDF_SERVICE_SECRET, [System.Text.Encoding]::ASCII)

$secretExists = & $GCLOUD secrets list --filter="name:nv-pdf-service-secret-preview" --project=$GCP_PROJECT --format="value(name)"
if ($secretExists) {
    Write-Host "Secret nv-pdf-service-secret-preview exists; adding new version..."
    & $GCLOUD secrets versions add nv-pdf-service-secret-preview --data-file=$secretFile --project=$GCP_PROJECT
} else {
    Write-Host "Creating secret nv-pdf-service-secret-preview..."
    & $GCLOUD secrets create nv-pdf-service-secret-preview --data-file=$secretFile --project=$GCP_PROJECT
}
Remove-Item $secretFile -Force

Write-Host "=== 6. Granting Secret Accessor role to Compute Service Account ==="
& $GCLOUD secrets add-iam-policy-binding nv-pdf-service-secret-preview `
  --member="serviceAccount:${SERVICE_ACCOUNT}" `
  --role="roles/secretmanager.secretAccessor" `
  --project=$GCP_PROJECT

Write-Host "=== 7. Deploying Cloud Run service [$SERVICE_NAME] from pdf_service/ ==="
Push-Location "pdf_service"
try {
    & $GCLOUD run deploy $SERVICE_NAME `
      --source="." `
      --region=$GCP_REGION `
      --platform=managed `
      --service-account=$SERVICE_ACCOUNT `
      --set-secrets="PDF_SERVICE_SECRET=nv-pdf-service-secret-preview:latest" `
      --memory=1Gi `
      --cpu=1 `
      --min-instances=0 `
      --max-instances=2 `
      --concurrency=4 `
      --timeout=60s `
      --allow-unauthenticated `
      --project=$GCP_PROJECT
} finally {
    Pop-Location
}

Write-Host "=== 8. Resolving Cloud Run Service URL ==="
$CLOUD_RUN_URL = (& $GCLOUD run services describe $SERVICE_NAME --region=$GCP_REGION --project=$GCP_PROJECT --format="value(status.url)").Trim()
$PDF_SERVICE_URL = "$CLOUD_RUN_URL/internal/v1/render-pdf"
Write-Host "Cloud Run Base URL: $CLOUD_RUN_URL"
Write-Host "Configured PDF_SERVICE_URL: $PDF_SERVICE_URL"

Write-Host "=== 9. Updating Cloudflare Pages Secrets for preview ==="
function Set-PagesSecret([string]$Name, [string]$Value, [string]$Env = "preview") {
    Write-Host "Setting Pages secret: $Name for env: $Env..."
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "cmd.exe"
    $psi.Arguments = "/c npx wrangler pages secret put $Name --project-name numeros-vision --env $Env"
    $psi.RedirectStandardInput = $true
    $psi.UseShellExecute = $false
    $proc = [System.Diagnostics.Process]::Start($psi)
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $writer = New-Object System.IO.StreamWriter($proc.StandardInput.BaseStream, $utf8NoBom)
    $writer.Write($Value)
    $writer.Close()
    $proc.WaitForExit()
    if ($proc.ExitCode -ne 0) { throw "Failed to set Pages secret: $Name" }
    Write-Host "PASS: Set Pages secret $Name."
}

Set-PagesSecret "PDF_SERVICE_SECRET" $PDF_SERVICE_SECRET "preview"
Set-PagesSecret "PDF_SERVICE_URL" $PDF_SERVICE_URL "preview"

Write-Host "=== 10. Testing Health Endpoints on Cloud Run ==="
Write-Host "Testing curl.exe -s $CLOUD_RUN_URL/healthz :"
$healthOutput1 = curl.exe -s "$CLOUD_RUN_URL/healthz"
Write-Host "Healthz output: $healthOutput1"

Write-Host "Testing curl.exe -s $CLOUD_RUN_URL/internal/v1/health :"
$healthOutput2 = curl.exe -s "$CLOUD_RUN_URL/internal/v1/health"
Write-Host "Internal health output: $healthOutput2"

Write-Host "`n=== CLOUD RUN & PAGES PROVISIONING COMPLETE ==="
