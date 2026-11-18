import sys; sys.path.insert(0,'/tmp'); from hv_common import *
with sync_playwright() as p:
    b,pg,E,errs=open_page(p)
    pg.click('#lstart'); run(pg,500)
    E("game.points.f0=900; 1")
    # city panel
    E("selCity=game.cities.find(c=>c.owner==='f0'); refreshUI(); 1"); run(pg,300)
    click_all(pg,'#camp button'); run(pg,200)
    E("selCity=game.cities.find(c=>c.owner==='f0'); refreshUI(); 1"); run(pg,200); click_all(pg,'#camp button')
    # army panel
    E("selCity=null; selUnit=units.find(u=>u.team==='f0'&&u.troops); refreshUI(); 1"); run(pg,300); click_all(pg,'#camp button'); run(pg,200)
    E("selUnit=units.find(u=>u.team==='f0'&&u.troops); refreshUI(); 1"); run(pg,200); click_all(pg,'#camp button'); run(pg,200)
    # free land / other city
    E("selUnit=null; selCity=game.cities.find(c=>!c.owner); refreshUI(); 1"); run(pg,200)
    E("selCity=game.cities.find(c=>c.owner&&c.owner!=='f0'); refreshUI(); 1"); run(pg,200)
    E("selCity=null; refreshUI(); 1"); run(pg,200)
    # menus
    for sid in ['#bmenu','#btouch','#btap2','#btest']:
        try: pg.click(sid); run(pg,300); click_all(pg,'#modal button'); run(pg,200)
        except Exception as e: print('x',sid)
    try:
        pg.click('#thelp'); run(pg,300); click_all(pg,'#modal button'); click_all(pg,'#touchbar button'); run(pg,200)
    except Exception: print('no thelp')
    try: pg.click('#btouch'); run(pg,200)
    except Exception: pass
    save(E,'camp_ui')
    # a few turns with drawing on
    E("__ff.draw=true; game.opts.aiSpeed=8; game.opts.campSpeed=8; 1")
    for t in range(6):
        try: pg.click('#endturn', timeout=2000)
        except Exception: pass
        pg.evaluate("__ff.run(120000, () => __T.ev(\"game.turn==='f0' || game.view!=='campaign'\"), 6000)")
        if pg.is_visible('#modal button'):
            click_all(pg,'#modal button')
    save(E,'camp_turns'); print(errs[:2]); b.close()
