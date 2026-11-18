# Turkish translation — work in progress (not live)

`tr-entries.json`: new/changed entries for the `I18N.tr` dictionary in `next/index.html`
(prepend them after `const I18N = { tr: {`). Written on top of v3.61.

Tools (run against a local server on 8767 serving the 3D test copy):
- `extract.py` pulls every UI string out of the game source -> /tmp/segs.json
- `chk.py segs.json out.json` lists the strings `tr()` leaves untranslated
- `hv_*.py` play through lobby / campaign / battle / god mode in Turkish and log runtime misses
  (needs test_tr.html = test.html with a `window.__miss` hook at the end of trCore)
- `scan.py` reads the visible page text in Turkish and flags English words

Status: entries written; not yet done: final on-screen scan, screenshots, publishing.
Left in English on purpose: the bilingual phone guide (it has its own Turkish), developer connection-log lines.
