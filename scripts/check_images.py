import re
from pathlib import Path
import os

root = Path('.').resolve()
htmls = list(root.rglob('*.html'))
img_re = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)
report = []
seen = {}
missing = []

for h in htmls:
    try:
        text = h.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    for m in img_re.finditer(text):
        src = m.group(1).split('?')[0]
        # ignore data URIs
        if src.startswith('data:'):
            continue
        # resolve path
        src_path = (h.parent / src).resolve()
        # normalize to workspace-relative if inside root
        try:
            rel = src_path.relative_to(root)
        except Exception:
            rel = src
        if rel in seen:
            seen[rel]['count'] += 1
            seen[rel]['refs'].add(str(h))
        else:
            seen[rel] = {'path': src_path, 'count': 1, 'refs': set([str(h)])}

for rel, info in seen.items():
    p = info['path']
    exists = p.exists()
    size = p.stat().st_size if exists and p.is_file() else None
    entry = {'file': str(rel), 'exists': exists, 'size': size, 'count': info['count'], 'refs': list(info['refs'])}
    if not exists:
        missing.append(entry)
    report.append(entry)

# sort by size desc
existing = [r for r in report if r['exists']]
existing.sort(key=lambda x: x['size'] or 0, reverse=True)

out = []
out.append(f"Total unique images referenced: {len(report)}")
out.append(f"Missing images: {len(missing)}")
if missing:
    out.append("--- Missing files (sample 50) ---")
    for m in missing[:50]:
        out.append(f"{m['file']} referenced {m['count']} times in {len(m['refs'])} pages")

out.append('\n--- Top 30 largest existing images ---')
for e in existing[:30]:
    out.append(f"{e['file']} size={e['size']:,} bytes referenced {e['count']} times")

report_path = root / 'scripts' / 'check_images_report.txt'
report_path.write_text('\n'.join(out), encoding='utf-8')
print('\n'.join(out))
print('\nReport written to', report_path)
