import json, sys, time
from playwright.sync_api import sync_playwright
def open_page(p, god=False):
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1300,'height':900}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('https://unpkg.com/**', lambda r: r.fulfill(body='', content_type='text/javascript'))
    pg.goto('http://localhost:8767/test_tr.html?ff=1'); pg.evaluate("localStorage.clear(); localStorage.setItem('mc-lang','tr')"); pg.reload(); pg.wait_for_selector('#load', state='detached'); pg.wait_for_timeout(300)
    E=lambda c: pg.evaluate(f"__T.ev({json.dumps(c)})")
    E("window.__miss=new Set(); setLang('tr'); 1")
    return b,pg,E,errs
def save(E,name):
    m=E("[...window.__miss]"); json.dump(m,open(f'/tmp/miss/{name}.json','w'),ensure_ascii=False,indent=0); print(name,len(m))
def run(pg,ms): pg.evaluate(f"__ff.run({ms})")
def click_all(pg, sel, skip=()):
    n=pg.locator(sel).count(); done=0
    for i in range(n):
        try:
            el=pg.locator(sel).nth(i)
            if not el.is_visible() or el.is_disabled(): continue
            idv=el.get_attribute('id') or ''
            if idv in skip: continue
            if not (el.inner_text() or '').strip(): continue
            el.click(timeout=800); pg.evaluate("__ff.run(150)"); done+=1
        except Exception as e: pass
    return done
