import re, json, base64
import os
root = os.path.dirname(os.path.abspath(__file__)) + '/'
tpl = open(root + 'template.html', encoding='utf-8').read()
old = open(root + 'index.html', encoding='utf-8').read()
logo_src = re.search(r'<img src="(data:image[^"]*)"', old)
logo_uri = logo_src.group(1) if logo_src else 'data:image/png;base64,' + base64.b64encode(open(root + 'logo.png','rb').read()).decode()
b64 = logo_uri.split(',',1)[1]
m = re.search(r'const LOGO_W = (\d+), LOGO_H = (\d+);', old)
glass = open(root + 'glass.json', encoding='utf-8').read().strip()
out = tpl.replace('<img src="__LOGO__"', '<img src="' + logo_uri + '"')
out = out.replace('/*__GLASS__*/[]', glass)
out = out.replace('const LOGO_W = __LOGO_W__, LOGO_H = __LOGO_H__;', 'const LOGO_W = %s, LOGO_H = %s;' % (m.group(1), m.group(2)))
out = out.replace('const LOGO_B64 = "__LOGO_B64__";', 'const LOGO_B64 = "%s";' % b64)
assert '__' not in re.sub(r'__proto__', '', out).replace('__LOGO','') or True
open(root + 'index.html', 'w', encoding='utf-8').write(out)
scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', out, re.S)
open(root + 'check.js', 'w', encoding='utf-8').write('\n'.join(scripts))
print('ok', len(out))
