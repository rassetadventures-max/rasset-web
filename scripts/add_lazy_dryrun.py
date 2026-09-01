import re
from pathlib import Path

root = Path('..') if Path('.').name == 'scripts' else Path('.')
img_re = re.compile(r'<img\b([^>]*)>', re.I)
loading_re = re.compile(r'\bloading\s*=')
class_hero_re = re.compile(r'class\s*=\s*["\'][^"\']*(hero|banner|slider|slide|carousel)[^"\']*["\']', re.I)
src_re = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.I)
skip_tokens = ['hero-', '/slider/', 'home05', 'elephant', 'slider', 'carousel', 'banner']

proposed = []
for path in sorted(root.rglob('*.html')):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        try:
            text = path.read_text(encoding='latin-1')
        except Exception:
            continue
    changes = []
    for m in img_re.finditer(text):
        attrs = m.group(1)
        if loading_re.search(attrs):
            continue
        if class_hero_re.search(attrs):
            continue
        msrc = src_re.search(attrs)
        if msrc:
            src = msrc.group(1).lower()
            if any(tok in src for tok in skip_tokens):
                continue
        start = max(0, m.start()-60)
        end = min(len(text), m.end()+60)
        old = text[start:end]
        new_tag = m.group(0)[:-1] + ' loading="lazy">'
        new = old.replace(m.group(0), new_tag)
        changes.append((m.start(), old, new))
    if changes:
        proposed.append((path, changes))

print(f'Files with proposed changes: {len(proposed)}')
total = sum(len(c) for _,c in proposed)
print(f'Total <img> tags to update: {total}\n')
for path, changes in proposed[:50]:
    print('---')
    print(path)
    print(f'  img tags to update: {len(changes)}')
    for i,(pos,old,new) in enumerate(changes[:3]):
        print('\n  Sample old:')
        print(old)
        print('\n  Sample new:')
        print(new)
        print('\n')

if len(proposed) > 50:
    print('\n...more files not shown...')
