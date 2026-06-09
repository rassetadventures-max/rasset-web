# Replace invalid replacement char (�) with en-dash (–) across HTML files
# Creates a .bak backup for each modified file

$root = Get-Location
$changed = 0
$encList = @(
    [System.Text.Encoding]::Default,
    [System.Text.Encoding]::UTF8,
    [System.Text.Encoding]::Unicode,
    [System.Text.Encoding]::ASCII
)
Get-ChildItem -Path $root -Filter *.html -Recurse -File | ForEach-Object {
    $path = $_.FullName
    foreach ($enc in $encList) {
        try {
            $content = [System.IO.File]::ReadAllText($path, $enc)
        } catch {
            continue
        }
        if ($content.Contains([char]0xFFFD)) {
            $new = $content.Replace([char]0xFFFD, [char]0x2013)
            Copy-Item -Path $path -Destination ($path + '.bak') -Force
            [System.IO.File]::WriteAllText($path, $new, $enc)
            Write-Output "Updated (char) : $path"
            $changed++
            break
        }
    }
}
Write-Output "Total files updated: $changed"
