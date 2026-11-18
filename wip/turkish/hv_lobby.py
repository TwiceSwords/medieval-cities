import sys; sys.path.insert(0,'/tmp'); from hv_common import *
with sync_playwright() as p:
    b,pg,E,errs=open_page(p)
    for _ in range(1): click_all(pg,'#lobby button',skip=('lstart',))
    for sid in ['#llvd','#lcoop','#lgod','#lbless']:
        try: pg.click(sid); run(pg,200)
        except Exception: pass
    for i in range(pg.locator('#lobby select').count()):
        try:
            sl=pg.locator('#lobby select').nth(i); opts=sl.locator('option').all_text_contents()
            for o in sl.locator('option').all()[:4]: sl.select_option(o.get_attribute('value')); run(pg,100)
        except Exception: pass
    pg.click('#llvd'); run(pg,300)
    save(E,'lobby'); print(errs[:2]); b.close()
