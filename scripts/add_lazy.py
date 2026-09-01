import re
from pathlib import Path

root = Path('.')
img_re = re.compile(r'<img\b([^>]*)>', re.I)
loading_re = re.compile(r'\bloading\s*=')
class_hero_re = re.compile(r'class\s*=\s*["\'][^"\']*(hero|banner|slider|slide|carousel)[^"\']*["\']', re.I)
src_re = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.I)
skip_tokens = ['hero-', '/slider/', 'home05', 'elephant', 'slider', 'carousel', 'banner']
modified_files = []
modified_count = 0

for path in root.rglob('*.html'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        try:
            text = path.read_text(encoding='latin-1')
        except Exception:
            continue
    changed = False
    def repl(m):
        nonlocal changed, modified_count
        full = m.group(0)
        attrs = m.group(1)
        if loading_re.search(attrs):
            return full
        if class_hero_re.search(attrs):
            return full
        msrc = src_re.search(attrs)
        if msrc:
            src = msrc.group(1).lower()
            for tok in skip_tokens:
                if tok in src:
                    return full
        new = full[:-1] + ' loading="lazy">'
        changed = True
        modified_count += 1
        return new
    new_text = img_re.sub(repl, text)
    if changed and new_text != text:
        path.write_text(new_text, encoding='utf-8')
        modified_files.append(str(path))

print(f'Files modified: {len(modified_files)}')
print(f'Image tags updated: {modified_count}')
for p in modified_files[:200]:
    print(p)
