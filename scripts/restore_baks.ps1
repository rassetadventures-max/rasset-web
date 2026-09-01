$log = Join-Path -Path (Resolve-Path .).Path -ChildPath "scripts\restore_baks_log.txt"
Remove-Item -Path $log -ErrorAction SilentlyContinue -Force
Get-ChildItem -Path . -Recurse -Filter *.bak | ForEach-Object {
    try {
        $bak = $_.FullName
        $orig = $bak -replace '\.bak$',''
        if (Test-Path $orig) {
            Copy-Item -Path $orig -Destination "$orig.postapply.bak" -Force
            Write-Output "Created safety backup: $orig.postapply.bak" | Out-File -FilePath $log -Append -Encoding UTF8
        }
        Copy-Item -Path $bak -Destination $orig -Force
        Write-Output "Restored: $orig from $bak" | Out-File -FilePath $log -Append -Encoding UTF8
    } catch {
        Write-Output "ERROR restoring $bak : $_" | Out-File -FilePath $log -Append -Encoding UTF8
    }
}
Write-Output "Done. Log: $log"
