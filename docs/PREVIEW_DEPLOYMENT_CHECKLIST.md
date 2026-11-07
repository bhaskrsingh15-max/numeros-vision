# NUMEROS VISION — PREVIEW DEPLOYMENT CHECKLIST & RUNBOOK
**Document Version**: 2.3.0  
**Target Environment**: Preview (`release/monetisation-fix` branch on Cloudflare Pages + Google Cloud Run)  
**Security Standard**: Non-negotiable Zero-PII, HMAC-SHA256 Service Auth, AES-GCM 64-Hex Encryption, Isolated Microservice Deploy.

---

> [!IMPORTANT]
> **Single PowerShell Session Requirement**:
> Steps 1 through 4 MUST be executed in the **same PowerShell window / session** so that persistent environment variables (such as `$PDF_SERVICE_SECRET`, `$PDF_SERVICE_URL`, and `$GCP_PROJECT`) are retained across command invocations.

> [!NOTE]
> **Environment Variables & Secrets Single-Source Rule**:
> `ENVIRONMENT` and `ALLOWED_ORIGINS` are managed **strictly** in `wrangler.toml` (`[vars]` for production, `[env.preview.vars]` for preview). They must **NEVER** be created as Cloudflare encrypted secrets to eliminate configuration drift.

---

## Pre-Flight Verification: Real D1 & R2 Names
Verify that all resource identifiers match `wrangler.toml` exactly:
- **Cloudflare D1 Databases**:
  - Production: `numeros-vision-db`
  - Preview: `numeros-vision-db-preview`
- **Cloudflare R2 Private Storage Buckets**:
  - Production: `numeros-reports-private`
  - Preview: `numeros-reports-private-preview`

---

## Step 1: Deploy Dedicated Python PDF Generator to Google Cloud Run

> [!CAUTION]
> Never deploy from the repository root. Deploy **strictly** from the isolated `pdf_service/` directory after synchronizing modules.

In your PowerShell session:
```powershell
# 1. Sync isolated pdf_service repository files before deployment and assert module parity
cd "C:\Users\Bhaskr Singh\Downloads\AI Numrology"
python scripts/sync_pdf_service.py

# Assert pdf_service modules match app/ modules bit-for-bit
$hash1 = (Get-FileHash "app\services\pdf_report_generator.py" -Algorithm SHA256).Hash
$hash2 = (Get-FileHash "pdf_service\app\services\pdf_report_generator.py" -Algorithm SHA256).Hash
if ($hash1 -ne $hash2) { throw "SYNC ERROR: pdf_service does not match app/services/pdf_report_generator.py!" }
Write-Host "PASS: pdf_service verified in parity with app/ modules (SHA256: $hash1)"

# 2. Navigate to isolated pdf_service directory
cd "pdf_service"

# 3. Set GCP Project from active gcloud config and obtain default compute service account
$GCP_PROJECT = (gcloud config get-value project).Trim()
$GCP_REGION = "asia-south1"
$PROJECT_NUMBER = (gcloud projects describe $GCP_PROJECT --format="value(projectNumber)").Trim()
$SERVICE_ACCOUNT = "${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
Write-Host "Deploying to GCP Project: $GCP_PROJECT with Service Account: $SERVICE_ACCOUNT"

# 4. Generate a 64-hex PDF_SERVICE_SECRET securely (using Node crypto)
$PDF_SERVICE_SECRET = node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Documented verification step: Assert PDF_SERVICE_SECRET is exactly 64 hex characters with zero newlines
$secretBytes = [System.Text.Encoding]::UTF8.GetBytes($PDF_SERVICE_SECRET)
if ($secretBytes.Length -ne 64) { throw "PDF_SERVICE_SECRET must be exactly 64 bytes (got $($secretBytes.Length))." }
if ($PDF_SERVICE_SECRET -match "[\r\n]") { throw "PDF_SERVICE_SECRET contains invalid newline characters." }
Write-Host "PASS: PDF_SERVICE_SECRET verified identical and newline-free (Length: 64 bytes)."

# 5. Store PDF_SERVICE_SECRET in Google Secret Manager without trailing newlines
[System.IO.File]::WriteAllText("$env:TEMP\pdf_secret.txt", $PDF_SERVICE_SECRET, [System.Text.Encoding]::ASCII)
gcloud secrets create nv-pdf-service-secret-preview --data-file="$env:TEMP\pdf_secret.txt" --project=$GCP_PROJECT
Remove-Item "$env:TEMP\pdf_secret.txt" -Force

# 6. Grant Cloud Run Service Account Secret Accessor permission
gcloud secrets add-iam-policy-binding nv-pdf-service-secret-preview `
  --member="serviceAccount:${SERVICE_ACCOUNT}" `
  --role="roles/secretmanager.secretAccessor" `
  --project=$GCP_PROJECT

# 7. Deploy container to Cloud Run with 64KB body protection and memory limit
# Authentication is enforced at the application layer via timestamped HMAC-SHA256 signatures (X-NV-Signature); concurrency 4 and max-instances 2 prevent memory exhaustion under concurrent ReportLab rendering (1Gi RAM per instance).
gcloud run deploy pdf-service `
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

# 8. Obtain the deployed service URL
$CLOUD_RUN_URL = (gcloud run services describe pdf-service --region=$GCP_REGION --project=$GCP_PROJECT --format="value(status.url)").Trim()
Write-Host "Cloud Run Base URL: $CLOUD_RUN_URL"

# The Worker expects either the base URL or the full endpoint URL; normalize:
$PDF_SERVICE_URL = "$CLOUD_RUN_URL/internal/v1/render-pdf"
Write-Host "Configured PDF_SERVICE_URL: $PDF_SERVICE_URL"

# Return to repo root
cd ..
```

---

## Step 2: Create Cloudflare D1 Databases, Apply Migrations & Create R2 Buckets

In the **same** PowerShell session:
```powershell
# 1. Create Production and Preview D1 Databases
wrangler d1 create numeros-vision-db
wrangler d1 create numeros-vision-db-preview

# 2. Update wrangler.toml with the returned real UUIDs:
# [d1_databases] database_id = "<REAL_PROD_UUID>"
# [[env.preview.d1_databases]] database_id = "<REAL_PREVIEW_UUID>"

# 3. Create Production and Preview R2 Private Buckets
wrangler r2 bucket create numeros-reports-private
wrangler r2 bucket create numeros-reports-private-preview

# 4. Apply real migration files to BOTH preview and production D1 databases
# Canonical command:
wrangler d1 migrations apply numeros-vision-db-preview --remote
wrangler d1 migrations apply numeros-vision-db --remote

# Fallback command if executing individual SQL migration files directly:
wrangler d1 execute numeros-vision-db-preview --remote --file=migrations/0001_initial_schema.sql
wrangler d1 execute numeros-vision-db-preview --remote --file=migrations/0002_invoices_refunds_audit.sql
wrangler d1 execute numeros-vision-db-preview --remote --file=migrations/0003_report_jobs_lifecycle.sql
wrangler d1 execute numeros-vision-db-preview --remote --file=migrations/0004_cookie_consents.sql
wrangler d1 execute numeros-vision-db-preview --remote --file=migrations/0005_enquiries.sql
wrangler d1 execute numeros-vision-db-preview --remote --file=migrations/0006_events.sql

wrangler d1 execute numeros-vision-db --remote --file=migrations/0001_initial_schema.sql
wrangler d1 execute numeros-vision-db --remote --file=migrations/0002_invoices_refunds_audit.sql
wrangler d1 execute numeros-vision-db --remote --file=migrations/0003_report_jobs_lifecycle.sql
wrangler d1 execute numeros-vision-db --remote --file=migrations/0004_cookie_consents.sql
wrangler d1 execute numeros-vision-db --remote --file=migrations/0005_enquiries.sql
wrangler d1 execute numeros-vision-db --remote --file=migrations/0006_events.sql
```

### Pre-Flight Verification: Production D1 Migration Alignment Check
Before deploying or modifying production, verify applied migrations against the repository and abort if any differ:
```powershell
# 5. Production D1 Pre-Flight Check: Compare remote migrations against repo
$prodMigrations = (npx wrangler d1 migrations list numeros-vision-db --remote --json | ConvertFrom-Json)
$repoMigrations = (Get-ChildItem migrations/*.sql | Select-Object -ExpandProperty Name)
$unapplied = $repoMigrations | Where-Object { $_ -notin $prodMigrations.name }
if ($unapplied) {
    Write-Error "STOP: Production D1 does not match repository! Unapplied migrations: $($unapplied -join ', ')"
    throw "Production D1 migration alignment check failed. Aborting."
}
Write-Host "PASS: Production D1 migrations match repository (0 unapplied)."
```

---

## Step 3: Generate & Store Cryptographic Secrets in Cloudflare Pages

> [!WARNING]
> Back up the 64-hex `DATA_ENCRYPTION_KEY` in your team password manager before storing. If lost, existing encrypted fields cannot be decrypted.

In the **same** PowerShell session:
```powershell
$PAGES_PROJECT = "numeros-vision"

# Generate 64-hex cryptographically secure keys (32 bytes):
$DATA_ENCRYPTION_KEY   = node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
$SESSION_SECRET        = node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
$OTP_HMAC_SECRET       = node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
$IP_HASH_SALT          = node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
$DOWNLOAD_TOKEN_SECRET = node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Restored ProcessStartInfo helper: exact UTF-8 bytes, zero trailing newline
function Set-PagesSecret([string]$Name, [string]$Value, [string]$Env = "preview") {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "npx.cmd"
    $psi.Arguments = "wrangler pages secret put $Name --project-name $PAGES_PROJECT --env $Env"
    $psi.RedirectStandardInput = $true
    $psi.UseShellExecute = $false
    $proc = [System.Diagnostics.Process]::Start($psi)
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $writer = New-Object System.IO.StreamWriter($proc.StandardInput.BaseStream, $utf8NoBom)
    $writer.Write($Value) # Exact bytes, zero trailing \r or \n
    $writer.Close()
    $proc.WaitForExit()
}

# Prompt for Third-Party Secrets (do not hardcode in terminal):
$RAZORPAY_KEY_ID          = Read-Host "Enter RAZORPAY_KEY_ID (rzp_test_...)"
$RAZORPAY_KEY_SECRET      = Read-Host "Enter RAZORPAY_KEY_SECRET"
$RAZORPAY_WEBHOOK_SECRET  = Read-Host "Enter RAZORPAY_WEBHOOK_SECRET"
$FAST2SMS_API_KEY         = Read-Host "Enter FAST2SMS_API_KEY"
$WEB3FORMS_ACCESS_KEY     = Read-Host "Enter WEB3FORMS_ACCESS_KEY"

# Set all required Cloudflare secrets for preview environment (--env preview):
Set-PagesSecret "DATA_ENCRYPTION_KEY"    $DATA_ENCRYPTION_KEY    "preview"
Set-PagesSecret "SESSION_SECRET"         $SESSION_SECRET         "preview"
Set-PagesSecret "OTP_HMAC_SECRET"        $OTP_HMAC_SECRET        "preview"
Set-PagesSecret "IP_HASH_SALT"           $IP_HASH_SALT           "preview"
Set-PagesSecret "TELEMETRY_SALT"         $TELEMETRY_SALT         "preview"
Set-PagesSecret "DOWNLOAD_TOKEN_SECRET"  $DOWNLOAD_TOKEN_SECRET  "preview"
Set-PagesSecret "PDF_SERVICE_SECRET"     $PDF_SERVICE_SECRET     "preview"
Set-PagesSecret "PDF_SERVICE_URL"        $PDF_SERVICE_URL        "preview"
Set-PagesSecret "RAZORPAY_KEY_ID"         $RAZORPAY_KEY_ID          "preview"
Set-PagesSecret "RAZORPAY_KEY_SECRET"     $RAZORPAY_KEY_SECRET      "preview"
Set-PagesSecret "RAZORPAY_WEBHOOK_SECRET" $RAZORPAY_WEBHOOK_SECRET  "preview"
Set-PagesSecret "FAST2SMS_API_KEY"        $FAST2SMS_API_KEY         "preview"
Set-PagesSecret "WEB3FORMS_ACCESS_KEY"    $WEB3FORMS_ACCESS_KEY     "preview"

# Documented verification step: Assert PDF_SERVICE_SECRET in Secret Manager and Pages are identical & newline-free
$smSecret = (gcloud secrets versions access latest --secret=nv-pdf-service-secret-preview --project=$GCP_PROJECT).Trim()
if ($smSecret -ne $PDF_SERVICE_SECRET) { throw "Secret mismatch: Cloud Run secret does not match Pages PDF_SERVICE_SECRET!" }
if ($smSecret.Length -ne 64) { throw "Secret length error: expected 64 hex characters, got $($smSecret.Length)." }
Write-Host "PASS: Verified Cloud Run and Cloudflare Pages PDF_SERVICE_SECRET bytes are identical and newline-free."
```

---

## Step 4: Build Site & Verify Deployment Guards

In the **same** PowerShell session:
```powershell
# 1. Run Python and Node verification test suites before deployment:
python -m unittest tests/test_pdf_tier_gating.py
python -m unittest tests/test_commit6b_python_generator.py
python tests/test_checklist_routes.py
node tests/test_payments_commit4.mjs
node tests/test_commit6b_pdf_pipeline.mjs

# 2. Run canonical single-path build (synchronizes pdf_service and populates dist_cloudflare_pages)
python build_bulletproof_dist.py

# 2. Verify that wrangler.toml contains real database IDs (rejects placeholders)
python build_bulletproof_dist.py --verify-deploy

# 3. Verify single build path, pack price/page consistency, and sample PDF safety
python tests/test_build_dist_integrity.py

# 4. Deploy build to Cloudflare Pages (Preview branch)
wrangler pages deploy dist_cloudflare_pages --project-name $PAGES_PROJECT --branch preview
```

---

## Step 5: Configure Razorpay Test Webhook
In the Razorpay Dashboard (Test Mode):
1. Navigate to **Settings → Webhooks → Add New Webhook**.
2. **Webhook URL**:
   `https://preview.numeros-vision.pages.dev/api/v1/payments/webhook`
3. **Secret**: Use the value set for `RAZORPAY_WEBHOOK_SECRET`.
4. **Active Events**:
   - `order.paid`
   - `payment.captured`
   - `payment.failed`
   - `refund.processed`

---

## Step 6: Verify Preview Isolation vs Production (Before & After Row Counts)

1. Verify bindings in Cloudflare Dashboard:
   - Preview environment uses D1 binding `DB` pointing to `numeros-vision-db-preview`.
   - Preview environment uses R2 binding `REPORTS_BUCKET` pointing to `numeros-reports-private-preview`.

2. Record table row counts in BOTH databases BEFORE running smoke tests:
```powershell
$tables = @("users", "subjects", "orders", "payments", "entitlements", "report_jobs")

Write-Host "--- BEFORE SMOKE TESTS: ROW COUNTS ---"
foreach ($tbl in $tables) {
    $cPrev = (wrangler d1 execute numeros-vision-db-preview --remote --command="SELECT COUNT(*) as c FROM $tbl;" --json | ConvertFrom-Json)[0].results[0].c
    $cProd = (wrangler d1 execute numeros-vision-db --remote --command="SELECT COUNT(*) as c FROM $tbl;" --json | ConvertFrom-Json)[0].results[0].c
    Write-Host "$tbl - Preview: $cPrev | Production: $cProd"
}
```

3. Re-verify table row counts AFTER executing Step 7 smoke tests:
```powershell
Write-Host "--- AFTER SMOKE TESTS: ROW COUNTS ---"
foreach ($tbl in $tables) {
    $cPrev = (wrangler d1 execute numeros-vision-db-preview --remote --command="SELECT COUNT(*) as c FROM $tbl;" --json | ConvertFrom-Json)[0].results[0].c
    $cProd = (wrangler d1 execute numeros-vision-db --remote --command="SELECT COUNT(*) as c FROM $tbl;" --json | ConvertFrom-Json)[0].results[0].c
    Write-Host "$tbl - Preview: $cPrev | Production: $cProd"
}
# Assert: Preview row counts increment; Production row counts remain strictly UNCHANGED.
```

---

## Step 7: End-to-End Positive Smoke Test Flow

Follow this exact endpoint flow in the browser or via automated smoke test:

1. **Send OTP**:
   `POST /api/v1/auth/otp/send`
   Payload: `{"phone": "9876543210"}`
   Response: `{"success": true, "message": "OTP sent successfully"}`

2. **Verify OTP & Create Session**:
   `POST /api/v1/auth/otp/verify`
   Payload: `{"phone": "9876543210", "otp": "..."}`
   Response: Sets HttpOnly `__Host-nv_session` cookie; returns user profile and subject array.

3. **Create Order (Pre-Payment DOB Confirmation)**:
   `POST /api/v1/payments/create-order`
   Payload: `{"packId": "report_advanced", "subjectId": "<SUBJECT_ID>"}`
   Response: `{"orderId": "nv_ord_...", "rzpOrderId": "order_...", "amount": 51000, "currency": "INR", "status": "CREATED"}`

4. **Razorpay Webhook Dispatch (Asynchronous ctx.waitUntil)**:
   `POST /api/v1/payments/webhook`
   Headers: `X-Razorpay-Signature: <HMAC_SHA256>`
   Payload: `{"event": "payment.captured", "payload": { ... }}`
   Response: Immediate HTTP 200 acknowledgment `{"status": "ok"}`; report job queued in background.

5. **Poll Payment & Report Generation Status**:
   `GET /api/v1/payments/status?orderId=nv_ord_...`
   Expected Response:
   ```json
   {
     "orderId": "nv_ord_...",
     "rzpOrderId": "order_...",
     "status": "paid",
     "packId": "report_advanced",
     "subjectId": "subj_...",
     "jobId": "job_...",
     "jobStatus": "COMPLETED",
     "reportStatus": "completed",
     "message": "Your personalized report is being prepared. It will be available shortly."
   }
   ```

6. **Acquire Session-Bound Download Token**:
   `POST /api/v1/reports/download-token`
   Cookie: `__Host-nv_session=<SESSION_COOKIE>`
   Payload: `{"subjectId": "subj_...", "packId": "report_advanced"}`
   Response: `{"token": "<TOKEN>", "downloadUrl": "/api/v1/reports/download?token=<TOKEN>", "jobStatus": "COMPLETED"}`

7. **Download PDF Report from Private R2 Storage**:
   `GET /api/v1/reports/download?token=<TOKEN>`
   Response: HTTP 200 `Content-Type: application/pdf`, `Content-Disposition: attachment; filename="Numeros_Vision_Advanced_Master_Dossier_...pdf"`.

---

## Step 8: Negative Security Smoke Tests

Execute these verification checks to assert fail-closed security:

1. **Bad Webhook Signature**:
   `POST /api/v1/payments/webhook` with invalid `X-Razorpay-Signature`.
   **Expected Result**: HTTP 400 `{"error": "Invalid webhook signature."}`.

2. **Idempotent Webhook Replay**:
   Send the identical `payment.captured` webhook payload twice.
   **Expected Result**: Both return HTTP 200; database contains exactly 1 order record and 1 report job (zero duplicate jobs).

3. **Tenant Subject Isolation**:
   `POST /api/v1/payments/create-order` with a `subjectId` belonging to another user.
   **Expected Result**: HTTP 403 `{"error": "Subject not found or does not belong to user."}`.

4. **Tampered or Expired Download Token**:
   `GET /api/v1/reports/download?token=tampered_or_expired`
   **Expected Result**: HTTP 401 `{"error": "Invalid or expired download token."}`.

5. **Post-Generation DOB Correction Refusal**:
   `POST /api/v1/subjects/correct-dob` on a subject whose report job has `jobStatus = "COMPLETED"` or `"READY"`.
   **Expected Result**: HTTP 400 `{"error": "DOB cannot be modified once report processing has completed."}`.

6. **Refund Access Revocation**:
   Dispatch `POST /api/v1/payments/webhook` with event `refund.processed`.
   **Expected Result**: Entitlement is revoked; subsequent calls to `POST /api/v1/reports/download-token` return HTTP 403.
