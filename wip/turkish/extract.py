import re, json
s=open('/home/claude/mc3d/index.html').read()
i=s.index('<script'); js=max(re.findall(r'<script[^>]*>(.*?)</script>',s,re.S),key=len)
# skip the I18N dictionary line
js='\n'.join(l for l in js.split('\n') if 'const I18N = { tr:' not in l)
out=[]; n=len(js); k=0
def read_template(k):
    # returns (text_with_placeholders, end_index)
    buf=''; k+=1
    while k<n:
        c=js[k]
        if c=='\\': buf+=js[k:k+2]; k+=2; continue
        if c=='`': return buf,k+1
        if c=='$' and js[k+1]=='{':
            # skip balanced braces, but collect nested strings
            depth=1; k+=2; inner_start=k
            while k<n and depth:
                ch=js[k]
                if ch in '\'"':
                    q=ch; k+=1; st=k
                    while js[k]!=q:
                        if js[k]=='\\': k+=1
                        k+=1
                    out.append(js[st:k]); k+=1; continue
                if ch=='`':
                    t,k=read_template(k); out.append(t); continue
                if ch=='{': depth+=1
                elif ch=='}': depth-=1
                k+=1
            buf+='${}'; continue
        buf+=c; k+=1
    return buf,k
prev=''
while k<n:
    c=js[k]
    if c=='/' and js[k+1]=='/': k=js.find('\n',k); k = n if k<0 else k; continue
    if c=='/' and js[k+1]=='*': k=js.find('*/',k)+2; continue
    if c in '\'"':
        q=c; k+=1; st=k
        while k<n and js[k]!=q and js[k]!='\n':
            if js[k]=='\\': k+=1
            k+=1
        out.append(js[st:k]); k+=1; continue
    if c=='`':
        t,k=read_template(k); out.append(t); continue
    # crude regex literal skip: / after ( , = : [ ! & | ? { } ; or start
    if c=='/' and re.match(r'[(,=:\[!&|?{};]\s*$', js[max(0,k-3):k]+' ') :
        m=re.match(r'/(?:\\.|\[(?:\\.|[^\]])*\]|[^/\n\\])+/[gimsuy]*', js[k:])
        if m: k+=m.end(); continue
    k+=1
segs=set()
for t in out:
    t=t.replace('\\n','\n')
    for part in re.split(r'<[^>]*>', t):
        part=part.strip()
        if not part: continue
        chk=part.replace('${}','QQ')
        if not re.search(r'[A-Za-z]{3}', chk.replace('QQ','')): continue
        if not re.search(r'[A-Za-z]{2,}[^A-Za-z]+[A-Za-z]{2,}', chk) and not re.match(r'^[A-Z][a-z]+', chk): continue
        if re.search(r'[{};]|=>|\bconst\b|function|\.\w+\(|^[\w-]+:\s*[\w#(]|px\b|rgba?\(|^#|https?:|\bvar\(|^[a-z]+[A-Z]\w*$', chk): continue
        if re.match(r'^[a-z0-9_.\-#\[\]=: ,>*]+$', part) and ' ' not in part: continue
        segs.add(part)
json.dump(sorted(segs),open('/tmp/segs.json','w'),ensure_ascii=False,indent=0)
print(len(out), len(segs))
