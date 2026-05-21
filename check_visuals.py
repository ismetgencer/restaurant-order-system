import urllib.request
import time

urls = ['http://127.0.0.1:5000/', 'http://127.0.0.1:5000/admin']

for url in urls:
    ok = False
    html = ''
    for _ in range(10):
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                html = r.read().decode('utf-8', errors='ignore')
            ok = True
            break
        except Exception as e:
            time.sleep(0.5)
    print('\nURL:', url)
    if not ok:
        print('  ERROR: sayfa yüklenemedi')
        continue
    lower = html.lower()
    has_bs = 'bootstrap' in lower
    has_css = 'style.css' in lower or 'static/style.css' in lower
    print('  length:', len(html))
    print('  bootstrap link found:', has_bs)
    print('  style.css found:', has_css)
    # save snapshot
    fname = url.replace('http://127.0.0.1:5000','').strip('/') or 'index'
    fname = f"snapshot_{fname}.html"
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  snapshot saved to', fname)

print('\nDone')
