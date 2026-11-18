import json, sys
from playwright.sync_api import sync_playwright
segs=json.load(open(sys.argv[1])); out=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.route('https://unpkg.com/**', lambda r: r.fulfill(body='', content_type='text/javascript'))
    pg.goto('http://localhost:8767/test.html?ff=1'); pg.wait_for_selector('#load', state='detached')
    res=pg.evaluate("""segs => __T.ev(`(()=>{ setLang('tr'); const out=[]; for (const s of ${JSON.stringify(segs)}) { const t=tr(s); if (t===s) out.push(s); } setLang('en'); return out; })()`)""", segs)
    json.dump(res,open(out,'w'),ensure_ascii=False,indent=0); print(len(res))
    b.close()
