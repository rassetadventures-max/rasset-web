import re
from pathlib import Path

def is_hero(attrs, src):
    attrs_l = attrs.lower()
    tokens = ['hero', 'banner', 'slider', 'slide', 'carousel', 'main-banner', 'banner-bg', 'banner-bg11']
    for t in tokens:
        if t in attrs_l:
            return True
    if src and any(t in src for t in tokens):
        return True
    return False

img_re = re.compile(r'<img\b([^>]*)>', re.I)
loading_re = re.compile(r'\bloading\s*=')
src_re = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.I)

root = Path(__file__).resolve().parent.parent
modified = []
total_tags = 0

for path in sorted(root.rglob('*.html')):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        try:
            text = path.read_text(encoding='latin-1')
        except Exception:
            print(f"Skipping (read error): {path}")
            continue
    new_text = text
    changes = []
    for m in list(img_re.finditer(text)):
        tag = m.group(0)
        attrs = m.group(1)
        if loading_re.search(attrs):
            continue
        msrc = src_re.search(attrs)
        src = msrc.group(1).lower() if msrc else ''
        if is_hero(attrs, src):
            continue
        # prepare new tag
        if tag.endswith('/>'):
            new_tag = tag[:-2].rstrip() + ' loading="lazy" />'
        else:
            new_tag = tag[:-1].rstrip() + ' loading="lazy">'
        new_text = new_text.replace(tag, new_tag, 1)
        changes.append((tag, new_tag))
    if changes:
        # backup original
        bak = Path(str(path) + '.bak')
        i = 1
        while bak.exists():
            bak = Path(str(path) + f'.bak.{i}')
            i += 1
        bak.write_text(text, encoding='utf-8')
        path.write_text(new_text, encoding='utf-8')
        modified.append((path, len(changes), changes[:3]))
        total_tags += len(changes)

# write report
report = Path('scripts') / 'add_lazy_report.txt'
with report.open('w', encoding='utf-8') as f:
    f.write(f'Files modified: {len(modified)}\n')
    f.write(f'Total <img> tags updated: {total_tags}\n\n')
    for p,count,samples in modified:
        f.write(f'{p} : {count} tags updated\n')
        for old,new in samples:
            f.write('\nOLD: ' + old + '\n')
            f.write('\nNEW: ' + new + '\n')
        f.write('\n---\n')

print('Apply complete.')
print(f'Files modified: {len(modified)}')
print(f'Total <img> tags updated: {total_tags}')
print(f'Report: {report}')
