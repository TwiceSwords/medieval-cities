import sys, re, json; sys.path.insert(0,'/tmp'); from hv_common import *
EN=re.compile(r"\b(the|and|of|to|your|you|can|turn|turns|battle|army|city|cities|realm|realms|wins?|with|alliance|ally|allies|dead|undead|stand|alone|offer|waiting|frozen|free|land|limit|pause|resume|camera|next|guide|exit|box|all|team|start|how|many|living|betray|accept|decline|keep|faith|round|dark|closes|wave|strong)\b", re.I)
def scan(pg, tag):
    t=pg.evaluate("document.body.innerText")
    hits=sorted(set(l.strip() for l in t.split('\n') if EN.search(l) and not re.search(r'[çğıöşüÇĞİÖŞÜ]', l)))
    print(f'== {tag}: {len(hits)}'); print('\n'.join(hits[:60]))
with sync_playwright() as p:
    b,pg,E,errs=open_page(p)
    pg.click('#llvd'); run(pg,300); scan(pg,'lobby'); pg.screenshot(path='/tmp/tr_lobby.png', full_page=True)
    pg.click('#lstart'); run(pg,800)
    E("game.factions.find(f=>f.id==='f1').ai=false; 1"); run(pg,300); scan(pg,'campaign'); pg.screenshot(path='/tmp/tr_camp.png')
    pg.click('button[data-lvd="betray"]'); run(pg,300); scan(pg,'betray modal'); pg.screenshot(path='/tmp/tr_betray.png')
    pg.click('button[data-lvdbetray]'); run(pg,300); E("lvdBetrayOp('f1', null); 1"); run(pg,300); scan(pg,'after betray')
    pg.click('button[data-lvdally="f1"]'); run(pg,300); E("game.turn='f1'; 1"); run(pg,600); scan(pg,'ask'); pg.screenshot(path='/tmp/tr_ask.png')
    print(errs[:2]); b.close()
