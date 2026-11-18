import sys; sys.path.insert(0,'/tmp'); from hv_common import *
with sync_playwright() as p:
    b,pg,E,errs=open_page(p)
    pg.click('#lstart'); run(pg,500)
    E("game.points.f0=900; testOn=true; refreshUI(); 1"); run(pg,300)
    click_all(pg,'#tst button'); run(pg,300)
    for i in range(pg.locator('#tst select').count()):
        try:
            sl=pg.locator('#tst select').nth(i)
            for o in sl.locator('option').all()[:6]: sl.select_option(o.get_attribute('value')); run(pg,80)
        except Exception: pass
    click_all(pg,'#tst button'); E("testOn=false; refreshUI(); 1")
    if pg.is_visible('#modal button'): click_all(pg,'#modal button')
    save(E,'test_panel')
    # field battle with heroes
    E("""(()=>{ const A=units.find(u=>u.team==='f0'&&u.troops), B=units.find(u=>u.team==='f1'&&u.troops); const n=neighbors(A.col,A.row).find(h=>!impassable(h)&&!unitAt(h)&&!cityAt(h)); B.col=n[0]; B.row=n[1];
      A.troops=['knight','ranger','mage','assassin','warrior','swordsman','spearman','halberdier','archer','crossbow','horseman','lancer','horsearcher','trebuchet','ballista','swordmaster'].map(troop);
      B.troops=['knight','mage','swordsman','archer','horseman','ballista','trebuchet','spearman'].map(troop); game.turn='f0'; engage(A,B); return 1; })()""")
    for _ in range(10):
        run(pg,800)
        if pg.is_visible('#modal'): click_all(pg,'#modal button')
        if E("game.view")=='battle': break
    run(pg,800); click_all(pg,'#camp button'); run(pg,300)
    E("__ff.draw=true; 1")
    # auto place / ready
    for _ in range(3):
        click_all(pg,'#camp button'); click_all(pg,'#modal button'); run(pg,600)
    print('phase', E("game.bt && game.bt.phase")); save(E,'battle_place')
    E("requestOp({op:'ready', fid:'f0'}); 1"); run(pg,1500); print('phase2', E("game.bt && game.bt.phase"))
    # select each unit of mine to show labels and hero cards
    ids=E("units.filter(u=>u.team==='f0'&&u.dying===null).map(u=>u.id)")
    for uid in ids:
        E(f"selUnit=units.find(u=>u.id==='{uid}'); hover=selUnit?[selUnit.col+1,selUnit.row]:null; refreshUI(); 1"); run(pg,250)
        if E(f"T(units.find(u=>u.id==='{uid}')).hero"):
            try: E(f"openHero(units.find(u=>u.id==='{uid}'),0); 1"); run(pg,300); click_all(pg,'#modal button:not([data-act])'); run(pg,200)
            except Exception as e: print('hero',e)
            if pg.is_visible('#modal'): E("hideModal(); 1")
    # hover enemies
    for uid in E("units.filter(u=>u.team==='f1'&&u.dying===null).map(u=>u.id)"):
        E(f"const o=units.find(u=>u.id==='{uid}'); selUnit=units.find(u=>u.team==='f0'&&u.type==='archer')||selUnit; hover=[o.col,o.row]; 1"); run(pg,200)
    E("selUnit=units.find(u=>u.team==='f0'&&u.type==='trebuchet'); armed=null; refreshUI(); 1"); run(pg,200)
    save(E,'battle_ui')
    # let the battle run with auto-fight for my side
    E("game.opts.aiSpeed=8; 1")
    try: click_all(pg,'#camp button')
    except Exception: pass
    E("for (const f of game.factions) if(f.id==='f0') f.ai=true; 1")
    for _ in range(6):
        pg.evaluate("__ff.run(240000, () => __T.ev(\"game.view!=='battle'\"), 8000)")
        if E("game.view")!='battle': break
    print('after battle view', E("game.view"))
    run(pg,3000); click_all(pg,'#modal button'); run(pg,1000)
    save(E,'battle_run')
    # siege as human: f0 attacks an AI city with walls
    E("""(()=>{ for (const f of game.factions) if(f.id==='f0') f.ai=false; const c=game.cities.find(c=>c.owner==='f2'); c.buildings=['tradepost','walls','tower','garrison','archer']; const A=units.find(u=>u.team==='f0'&&u.troops) || runtimeUnit({id:'army-f0-x',type:'army',team:'f0',col:0,row:0,hp:1,maxHp:1,face:0,moved:false,attacked:false,troops:[]});
       if(!units.includes(A)) units.push(A); const n=neighbors(c.col,c.row).find(h=>!impassable(h)&&!unitAt(h)&&!cityAt(h)); A.col=n[0]; A.row=n[1]; A.moved=false; A.attacked=false; A.troops=['swordsman','swordsman','archer','trebuchet','knight','spearman'].map(troop); game.turn='f0'; game.view='campaign'; engage(A,c); return 1; })()""")
    for _ in range(10):
        run(pg,800)
        if pg.is_visible('#modal'): click_all(pg,'#modal button')
        if E("game.view")=='battle': break
    for _ in range(3): click_all(pg,'#camp button'); click_all(pg,'#modal button'); run(pg,600)
    try:
        E("""(()=>{ const s2=sg(); const w=Object.entries(s2.pieces).find(([k,p])=>p.kind==='wall'); const h=w[0].split(',').map(Number); const u=units.find(x=>x.team==='f0'&&x.type==='swordsman'&&x.dying===null); selUnit=u; window.__wh=h; return 1; })()""")
        E("rightClickAt && rightClickAt(window.__wh); 1"); run(pg,500); click_all(pg,'#modal button'); run(pg,300)
    except Exception as e: print('wall', e)
    save(E,'siege_ui'); print(errs[:3]); b.close()
