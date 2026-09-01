$files = Get-ChildItem -Recurse -Filter *.html
foreach ($f in $files) {
  $text = Get-Content -Raw -Encoding UTF8 $f.FullName -ErrorAction SilentlyContinue
  if ($null -eq $text) { $text = (Get-Content -Encoding UTF8 $f.FullName) -join "`n" }
  $new = $text -replace ' loading="lazy"','' -replace " loading='lazy",''
  if ($new -ne $text) {
    Set-Content -Value $new -Encoding UTF8 -Path $f.FullName
    Write-Output "Updated: $($f.FullName)"
  }
}
