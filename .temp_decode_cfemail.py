import re
from pathlib import Path
root = Path('.')
pattern = re.compile(r'data-cfemail="([0-9a-fA-F]+)"')
uniq = {}
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    for m in pattern.finditer(text):
        uniq.setdefault(m.group(1), []).append(str(path))
for code, paths in uniq.items():
    data = bytes.fromhex(code)
    key = data[0]
    email = ''.join(chr(x ^ key) for x in data[1:])
    print(code, email, len(paths), paths[:10])
