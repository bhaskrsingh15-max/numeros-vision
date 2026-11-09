<#
.SYNOPSIS
  Securely sets preview secrets for Cloudflare Pages without writing or logging values.
#>

$ErrorActionPreference = "Stop"

function Generate-Secret32 {
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    $charsLen = $chars.Length
    $sb = New-Object System.Text.StringBuilder(32)
    for ($i = 0; $i -lt 32; $i++) {
        [void]$sb.Append($chars[$bytes[$i] % $charsLen])
    }
    return $sb.ToString()
}

function Put-PagesSecret {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,
        [Parameter(Mandatory=$true)]
        [string]$SecretValue
    )

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "cmd.exe"
    $psi.Arguments = "/c npx wrangler pages secret put $Name --project-name numeros-vision --env preview"
    $psi.UseShellExecute = $false
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true

    $proc = [System.Diagnostics.Process]::Start($psi)
    $proc.StandardInput.WriteLine($SecretValue)
    $proc.StandardInput.Close()

    $stdout = $proc.StandardOutput.ReadToEnd()
    $stderr = $proc.StandardError.ReadToEnd()
    $proc.WaitForExit()

    if ($proc.ExitCode -eq 0) {
        Write-Host "OK $Name" -ForegroundColor Green
    } else {
        $errClean = "Exit code $($proc.ExitCode)"
        foreach ($line in ($stderr + "`n" + $stdout) -split "`r?`n") {
            $trimmed = $line.Trim()
            if ($trimmed -match "Error:" -or $trimmed -match "failed") {
                $errClean = $trimmed
                break
            }
        }
        Write-Host "FAILED ${Name}: $errClean" -ForegroundColor Red
    }
}

$secretNames = @(
    "ADMIN_TOKEN",
    "EMAIL_PROVIDER",
    "EMAIL_API_KEY",
    "EMAIL_FROM",
    "TURNSTILE_SITE_KEY",
    "TURNSTILE_SECRET_KEY",
    "RAZORPAY_WEBHOOK_SECRET"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Numeros Vision - Preview Secrets Configuration" -ForegroundColor Cyan
Write-Host " Project: numeros-vision | Environment: preview" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

foreach ($name in $secretNames) {
    $canGenerate = ($name -eq "ADMIN_TOKEN" -or $name -eq "RAZORPAY_WEBHOOK_SECRET")

    if ($canGenerate) {
        Write-Host "`n[$name] Enter value (hidden), or 'G' to generate a 32-char secret, or Enter to skip:" -ForegroundColor Yellow
    } else {
        Write-Host "`n[$name] Enter value (hidden), or Enter to skip:" -ForegroundColor Yellow
    }

    $secInput = Read-Host -Prompt "$name" -AsSecureString
    if ($null -eq $secInput) {
        Write-Host "SKIPPED $name" -ForegroundColor DarkGray
        continue
    }

    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secInput)
    $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

    if ([string]::IsNullOrWhiteSpace($plain)) {
        Write-Host "SKIPPED $name" -ForegroundColor DarkGray
        continue
    }

    if ($canGenerate -and ($plain.Trim() -eq "G" -or $plain.Trim() -eq "g")) {
        $plain = Generate-Secret32
        try {
            Set-Clipboard -Value $plain
            Write-Host "  -> Generated 32-char secret copied to clipboard! (Please save it in your password manager now)" -ForegroundColor Cyan
        } catch {
            Write-Host "  -> Generated 32-char secret (Clipboard unavailable; ensure value is saved)" -ForegroundColor Yellow
        }
    }

    Put-PagesSecret -Name $name -SecretValue $plain
    $plain = $null
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Current Preview Secrets in Cloudflare Pages:" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
cmd.exe /c npx wrangler pages secret list --project-name numeros-vision --env preview
