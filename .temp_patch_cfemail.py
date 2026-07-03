import re
from pathlib import Path
root = Path('.')
script_pattern = re.compile(r'<script\s+data-cfasync="false"\s+src="\.\.\/\.\.\/\.\.\/cdn-cgi\/scripts\/5c5dd728\/cloudflare-static\/email-decode\.min\.js"><\/script>')
link_pattern = re.compile(
    r'<a\s+href="https://demo\.egenslab\.com/cdn-cgi/l/email-protection#[^"]+">\s*<span\s+class="__cf_email__"\s+data-cfemail="([0-9a-fA-F]+)">[^<]*<\/span>\s*<\/a>'
)

mapping = {
    '3950575f56795c41585449555c175a5654': 'info@example.com',
    '72010702021d000632170a131f021e175c111d1f': 'support@example.com',
}

changed_files = []
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    new_text = script_pattern.sub('', text)

    def repl(match):
        code = match.group(1)
        email = mapping.get(code, None)
        if email:
            return f'<a href="mailto:{email}">{email}</a>'
        return match.group(0)

    new_text = link_pattern.sub(repl, new_text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        changed_files.append(str(path))

print('changed', len(changed_files))
for f in changed_files[:50]:
    print(f)
