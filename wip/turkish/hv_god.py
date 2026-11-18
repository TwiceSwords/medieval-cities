import sys; sys.path.insert(0,'/tmp'); from hv_common import *
with sync_playwright() as p:
    b,pg,E,errs=open_page(p)
    pg.click('#lgod'); run(pg,200); pg.click('#llvd'); run(pg,200); pg.select_option('#llvdwin','2'); run(pg,200)
    pg.click('#lstart'); run(pg,500)
    E("__ff.draw=true; game.opts.aiSpeed=8; game.opts.campSpeed=8; game.opts.arTrig=0; 1")
    try: pg.click('#bgcam'); run(pg,300); pg.click('#bgcam'); run(pg,300); pg.click('#bgpause'); run(pg,300); pg.click('#bgpause'); run(pg,300)
    except Exception as e: print('godbar', e)
    t0=time.time(); last=0; forced=False
    while time.time()-t0<330:
        pg.evaluate("__ff.run(600000, () => __T.ev('game.round > %d || !!game.cwinner'), 6000)"%last)
        if E("game.view")=='campaign':
            r=E("game.round")
            if r!=last: last=r
            if r>=8 and not forced: E("undeadWave(FINAL_WAVE); 1"); forced=True
        if pg.is_visible('#modal button'): click_all(pg,'#modal button')
        if E("!!game.cwinner"): break
    run(pg,3000)
    print('round', last, E("game.view"), E("game.cwinner"))
    save(E,'god_lvd'); print(errs[:2]); b.close()
