import re
from pathlib import Path

root = Path('.')
img_re = re.compile(r'<img\b([^>]*)>', re.I)
loading_re = re.compile(r'\bloading\s*=')
class_hero_re = re.compile(r'class\s*=\s*["\'][^"\']*(hero|banner|slider|slide|carousel)[^"\']*["\']', re.I)
src_re = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.I)
skip_tokens = ['hero-', '/slider/', 'home05', 'elephant', 'slider', 'carousel', 'banner']

total_imgs = 0
already = 0
skipped_class = 0
skipped_src = 0
updated = 0
files_with_imgs = 0

for path in root.rglob('*.html'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        try:
            text = path.read_text(encoding='latin-1')
        except Exception:
            continue
    matches = list(img_re.finditer(text))
    if matches:
        files_with_imgs += 1
    for m in matches:
        total_imgs += 1
        attrs = m.group(1)
        if loading_re.search(attrs):
            already += 1
            continue
        if class_hero_re.search(attrs):
            skipped_class += 1
            continue
        msrc = src_re.search(attrs)
        if msrc:
            src = msrc.group(1).lower()
            if any(tok in src for tok in skip_tokens):
                skipped_src += 1
                continue
        updated += 1

print(f'Files scanned with img tags: {files_with_imgs}')
print(f'Total <img> tags: {total_imgs}')
print(f'Already have loading attribute: {already}')
print(f'Skipped due to class containing hero/banner/slider/slide/carousel: {skipped_class}')
print(f'Skipped due to src containing skip tokens: {skipped_src}')
print(f'Would update (no loading and not skipped): {updated}')
