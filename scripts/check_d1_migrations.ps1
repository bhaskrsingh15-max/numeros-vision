# scripts/check_d1_migrations.ps1
param(
    [string]$Database = "numeros-vision-db",
    [string]$Env = ""
)

$ErrorActionPreference = "Stop"

$envFlag = ""
if ($Env) {
    $envFlag = "--env $Env"
}

Write-Host "Checking D1 migrations for database: $Database $envFlag..."

$cmd = "npx wrangler d1 execute $Database --remote $envFlag --command=`"SELECT name FROM d1_migrations;`" --json"
$rawJson = Invoke-Expression $cmd

if (-not $rawJson) {
    throw "Failed to query d1_migrations from $Database. Raw response was empty."
}

$parsed = $rawJson | ConvertFrom-Json
if (-not $parsed -or -not $parsed[0] -or -not $parsed[0].success) {
    throw "D1 query did not return success for database $Database."
}

$appliedNames = @()
if ($parsed[0].results) {
    $appliedNames = @($parsed[0].results | ForEach-Object { $_.name })
}

$repoMigrations = @(Get-ChildItem -Path "migrations/*.sql" | Select-Object -ExpandProperty Name)
$unapplied = @($repoMigrations | Where-Object { $_ -notin $appliedNames })

Write-Host "Applied migrations in D1 ($($appliedNames.Count)): $($appliedNames -join ', ')"
Write-Host "Migrations in repository ($($repoMigrations.Count)): $($repoMigrations -join ', ')"

if ($unapplied.Count -gt 0) {
    Write-Error "STOP: D1 database $Database does not match repository! Unapplied migrations: $($unapplied -join ', ')"
    exit 1
}

Write-Host "PASS: D1 migrations match repository (0 unapplied)."
exit 0
