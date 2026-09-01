import re
from pathlib import Path

root = Path('.').resolve()
pat = re.compile(r"\s+loading\s*=\s*(?:\"|\')lazy(?:\"|\')", flags=re.I)
updated = []
for p in root.rglob('*.html'):
    try:
        text = p.read_text(encoding='utf-8')
    except Exception:
        try:
            text = p.read_text(encoding='latin-1')
        except Exception:
            continue
    new = pat.sub('', text)
    if new != text:
        p.write_text(new, encoding='utf-8')
        updated.append(str(p))
        print('Updated', p)
print('Total files updated:', len(updated))
