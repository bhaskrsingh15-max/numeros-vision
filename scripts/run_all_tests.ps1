$outputFile = "data/test_results_raw.txt"
"=== NODE MJS TESTS ===" | Out-File -FilePath $outputFile -Encoding utf8

Get-ChildItem -Path tests/*.mjs | ForEach-Object {
    $name = $_.Name
    $start = Get-Date
    $relPath = "tests/$name"
    $p = Start-Process -FilePath "node" -ArgumentList "`"$relPath`"" -NoNewWindow -PassThru -Wait
    $dur = [math]::Round(((Get-Date) - $start).TotalSeconds, 2)
    $status = if ($p.ExitCode -eq 0) { "PASS" } else { "FAIL" }
    "$status | $name | ExitCode: $($p.ExitCode) | Dur: $dur s" | Out-File -FilePath $outputFile -Append -Encoding utf8
    Write-Host "$status | $name ($dur s)"
}

"=== PYTHON TESTS ===" | Out-File -FilePath $outputFile -Append -Encoding utf8

Get-ChildItem -Path tests/test_*.py | ForEach-Object {
    $name = $_.Name
    $start = Get-Date
    $relPath = "tests/$name"
    $p = Start-Process -FilePath "python" -ArgumentList "`"$relPath`"" -NoNewWindow -PassThru
    $finished = $p.WaitForExit(10000)
    $dur = [math]::Round(((Get-Date) - $start).TotalSeconds, 2)
    if (-not $finished) {
        $p.Kill()
        $status = "TIMEOUT"
        $code = -1
    } else {
        $code = $p.ExitCode
        $status = if ($code -eq 0) { "PASS" } else { "FAIL" }
    }
    "$status | $name | ExitCode: $code | Dur: $dur s" | Out-File -FilePath $outputFile -Append -Encoding utf8
    Write-Host "$status | $name ($dur s)"
}
