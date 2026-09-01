import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
img_re = re.compile(r'<img\b([^>]*)>', re.I)
loading_re = re.compile(r'\bloading\s*=')
src_re = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.I)
hero_tokens = ['hero','banner','slider','slide','carousel','main-banner','banner-bg','banner-bg11']

results = []
for path in sorted(root.rglob('*.html')):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        try:
            text = path.read_text(encoding='latin-1')
        except Exception:
            continue
    tags = []
    for m in img_re.finditer(text):
        attrs = m.group(1)
        if loading_re.search(attrs):
            continue
        srcm = src_re.search(attrs)
        src = srcm.group(1).lower() if srcm else ''
        skip = False
        for t in hero_tokens:
            if t in attrs.lower() or (src and t in src):
                skip = True
                break
        if skip:
            continue
        snippet = text[max(0,m.start()-40):m.end()+40]
        tags.append(snippet.strip())
    if tags:
        results.append((path, len(tags), tags[:5]))

report = Path(__file__).resolve().parent / 'scan_missing_loading_report.txt'
with report.open('w', encoding='utf-8') as f:
    f.write(f'Files with missing loading: {len(results)}\n')
    total = sum(r[1] for r in results)
    f.write(f'Total <img> tags missing loading: {total}\n\n')
    for p,count,samples in results:
        f.write(f'{p} : {count}\n')
        for s in samples:
            f.write('\nSNIPPET:\n')
            f.write(s.replace('\n','\n') + '\n')
        f.write('\n---\n')

print('Scan complete.')
print(f'Report: {report}')
