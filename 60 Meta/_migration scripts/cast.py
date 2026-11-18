import re, os, io, json, hashlib, sys
from common import *
DRY = '--dry' in sys.argv
LINK = registry(); LINK['Till']='Till'; LINK['Yueyla']='Yueyla'
NAMES = set(LINK)|set(LINK.values())
def rd(rel, base=SRC, moj=False):
    return fix_name_apos(read(rel, base, moj).replace('\u2018',"'").replace('&#10;','\n'), NAMES)
def keyname(h):
    h=h.strip().strip('*').strip()
    h=re.sub(r'^Recom ','',h)
    for k,(n,al) in SPECIAL.items():
        if h.startswith(k): return n
    return re.split(r' \(| — | - ', h)[0].strip()
def resolve(label):
    """label from a table/heading -> list of note names"""
    l=label.strip().strip('*').strip()
    if l.startswith('Chutaury'): return ['Chuchu']
    if re.match(r"M[ìi]yo & M[ìi]r[ìi]", l): return ['Mìyo','Mìrì']
    k=keyname(l)
    if k in LINK: return [LINK[k]]
    first=re.split(r'\s*/\s*| & ', k)[0].strip()
    if first in LINK: return [LINK[first]]
    return []
norm=lambda s: re.sub(r'\s+',' ',s.replace('*','').replace('\u2019',"'").replace('\u201c','"').replace('\u201d','"')).strip()

MASTER='Local_Only_Core/AITM_00_Master_List.md'
FILES=[(MASTER,BK),('Local_Only_Core/AITM_06_Other_Characters_and_Lore.md',BK),
 ('AITM_02_Samaya_Family_Profiles.md',SRC),('AITM_03_Haykxa_Family_Profiles.md',SRC),('AITM_04_Ngotxi_and_Korhe_Family_Profiles.md',SRC),
 ('AITM_05_Factions_Profiles.md',SRC),('AITM_07_The_Flying_Troupe.md',SRC),
 ('02_Character_Profiles_Samaya_Haykxa.md',SRC),('03_Character_Profiles_Ngotxi_Korhe.md',SRC),('04_Character_Profiles_Groups_and_Others.md',SRC)]
H2MAP=[('Samaya Family',('family','Samaya')),('Haykxa Family',('family','Haykxa')),('Ngotxì Family',('family','Ngotxì')),('Korhe Family',('family','Korhe')),
 ('The Lost Cohort',('group','The Lost Cohort')),('The Scattered Ashes',('group','The Scattered Ashes')),('The Resistance',('group','Earth House')),
 ('The ANAKT',('group','ANAKT Fireteam')),('The Flying Troupe',('group','The Flying Troupe')),('Other Characters',(None,None))]
def h2kind(h):
    h=h.strip('*').strip()
    for k,v in H2MAP:
        if h.startswith(k): return v
    return None
FIELD=re.compile(r"\*\*([A-Za-z' ]+?):?\*\*:?[ \t]*(.*?)(?=[ \t]+\*\*[A-Za-z' ]+?:?\*\*:?[ \t]|$)")
def split_fields(body):
    lines=body.split('\n'); f={}; i=0
    while i<len(lines):
        l=lines[i].strip()
        if not l: i+=1; continue
        if re.match(r'\*{1,2}Personality', l) or len(l)>160: break
        m=FIELD.findall(l)
        if not m or not l.startswith('**'): break
        for k,v in m: f[k.strip()]=v.strip().replace('\u2019',"'")
        i+=1
    return f, '\n'.join(lines[i:]).strip()

versions={}   # name -> list of dict(file, fields, prose, kind, heading)
groupintro={} # group -> dict(file-> (intro, outro))
order=[]
for f,b in FILES:
    t=rd(f,b)
    if f==MASTER: t=t[t.index('## Character Profiles'):]
    short=os.path.basename(f)[:-3]
    for h2,blk in sections(t,2):
        kind=h2kind(h2)
        if not kind: continue
        entries=[]
        if kind[1]=='ANAKT Fireteam':
            ms=list(re.finditer(r'^(?:### )?\*\*(Recom \w+ \(.+?\))\*\*\s*$', blk, re.M))
            intro=blk[:ms[0].start()].strip() if ms else ''
            for i,m in enumerate(ms):
                entries.append((m.group(1), blk[m.end(): ms[i+1].start() if i+1<len(ms) else len(blk)]))
        else:
            hs=sections('\n'+blk,3)
            first=re.search(r'^### ', blk, re.M)
            intro=blk[:first.start()].strip() if first else blk.strip()
            entries=hs
        intro=re.sub(r'\n-{3,}\s*$','',intro).strip()
        outro=''
        for h,body in entries:
            if h.strip('*').strip().endswith('Family'): continue
            parts=re.split(r'\n\s*-{3,}\s*(?:\n|$)', '\n'+body)
            body=parts[0]; rest='\n\n'.join(p.strip() for p in parts[1:] if p.strip())
            if rest: outro=(outro+'\n\n'+rest).strip()
            fields,prose=split_fields(body.strip('\n'))
            n=keyname(h)
            if n not in order: order.append(n)
            versions.setdefault(n,[]).append({'file':short,'fields':fields,'prose':prose,'kind':kind,'heading':h.strip('*').strip()})
        if kind[1] and (intro or outro):
            groupintro.setdefault(kind[1],[]).append((short,intro,outro))

# ---- side sources
dbt=rd('Astikasya_Character_Database.md',moj=True); db={}
def dbfields(b):
    b=b.split('\n---')[0]
    return dict((m.group(1).strip(), m.group(2).strip()) for m in re.finditer(r'^\*\*(.+?):\*\*[ \t]*(.*)$', b, re.M)), b
for lvl in (3,4):
    for h,b in sections(dbt,lvl):
        if h in ('Children','The Nine Spears of the Mists'): continue
        f,raw=dbfields(b)
        st=re.search(r' - ([A-Z/ ]+)$', h)
        if st: f['_status']=st.group(1).capitalize()
        ep=re.search(r'\((The [^)]+)\)', h)
        if h.startswith('Recom') and ep: f['_epithet']=ep.group(1)
        rs=resolve(h)
        if len(rs)==2:  # twins
            nn=[x.strip() for x in f.get("Na'vi Names",'').split(' & ')]; ik=[x.strip() for x in f.get('Ikrans','').split(' & ')]
            for i,n in enumerate(rs):
                g={"Na'vi Name":nn[i] if len(nn)==2 else None,'Ikran':ik[i] if len(ik)==2 else None,'Age':f.get('Ages'),'Role':f.get('Roles'),'Family':f.get('Family')}
                m=re.search(r'^- \*\*%s:\*\*\s*(.+)$'%re.escape(n), raw, re.M)
                if m: g['Key Traits']=m.group(1).strip()
                db[n]={k:v for k,v in g.items() if v}
        elif rs: db[rs[0]]=f
        else: print('DB unmatched:',h)
spears={}
i=dbt.index('### The Nine Spears of the Mists'); spear_db=dbt[i:dbt.index('\n## ',i)].split('\n',1)[1].strip()
for m in re.finditer(r'^\d+\. \*\*(.+?)\*\* - (The \w+) \(([^)-]+?)(?: -.*)?\)', spear_db, re.M): spears[m.group(1)]=(m.group(2),m.group(3).strip())
mbti_t=rd('AITM_MBTI_Reference.md'); mbti={}; mbti_extra={}
for line in mbti_t.splitlines():
    if line.startswith('|') and '---' not in line:
        c=[x.strip() for x in line.strip().strip('|').split('|')]
        if c[0]=='Character' or len(c)<3: continue
        rs=resolve(c[0])
        if c[0]=='Kerevi': mbti_extra['Tìmeyo']=('Kerevi',c)
        elif rs:
            for n in rs: mbti.setdefault(n,c)
        else: print('MBTI unmatched:',c[0])
case_t=rd('AITM_Navi_Name_Case_Forms.md'); case={}; case_hdr=[l for l in case_t.splitlines() if l.startswith('| Name |')][0]
for line in case_t.splitlines():
    if line.startswith('| **'):
        c=[x.strip() for x in line.strip().strip('|').split('|')]; rs=resolve(c[0])
        if rs: case.setdefault(rs[0],[]).append(line.strip())
        else: print('CASE unmatched:',c[0])
quick={}
for h,b in sections(rd('AITM_Relationships_QuickRef.md'),3):
    rs=resolve(h)
    if not rs: print('QUICK unmatched:',h)
    for n in rs: quick.setdefault(n,[]).append((h,b.strip()))
lore_t=rd('AITM_Relationships_Lore.md'); lore_heads=[h for h,_ in sections(lore_t,3)]
prov_heads=[h for h,_ in sections(rd('AITM_Navi_Proverbs.md'),2)]
acc_heads=[h for h,_ in sections(rd('AITM_Astikasya_Accent_Reference.md'),3)]
roster_t=rd('AITM_01_Clan_Overview_and_Groups.md'); roster={}
for m in re.finditer(r"\*\*([^*\n]+?)\*\*[ \t]*\n[ \t]+\*\*Na'vi Name:?\*\*:?[ \t]*(.+)(?:\n[ \t]+\*\*Age:?\*\*:?[ \t]*(.+))?", roster_t):
    rs=resolve(m.group(1))
    if rs: roster[rs[0]]={'navi':m.group(2).strip().strip('*').strip().replace('\u2019',"'"),'age':(m.group(3) or '').strip() or None,'label':m.group(1)}

S=lambda s,*n: {x:s for x in n}
SERIES={}
SERIES.update(S('Mobile Suit Gundam: The Witch from Mercury',"Tsu'ong",'Nika','Chuchu','Aliya','Martin Upmont','Till Nys','Nuno Kargan','Ojelo Gabel','Lilique Kadoka Lipati'))
SERIES.update(S('Chainsaw Man',"Tsa'rawm",'Rewon','Lamaytxa','Sänume','Kayan','Txolaw','Ketxe','Kobeni','Yueyla'))
SERIES.update(S('Bocchi the Rock!','Txewan',"'Eweyn",'Syulang','Mitsìyo',"Tse'hayu",'Tswesya','Katirì','Waynhì','Tìfyaw','Zìsaw'))
SERIES.update(S("BanG Dream! It's MyGO!!!!!",'Rängay','Pxayu','Apayì','Pamyaw'))
SERIES.update(S('BanG Dream! Ave Mujica','Syayvi','Tìmeyo',"Nì'syu",'Txafwe','Yawyay'))
SERIES.update(S('Jujutsu Kaisen',"Tsu'lan",'Tsyokanì','Yukeyo'))
SERIES.update(S('Soul Eater','Teysaw','Txokän','Layon','Sìltsyu','Seytu','Yezì','Pakì','Paysìn','Roneyu'))
SERIES.update(S('Alien Stage','Ivan','Sua','Mizi','Till','Hyuna','Luka'))
KIDS=['Anake','Kxayì','Mìyo','Mìrì','Netezu','Lawarey','Nìla','Mawpay','Oarä']; JETURK=['Tulìpey','Eantu']
for _n in ['Miri Sugo']+KIDS+JETURK: SERIES[_n]='Original character'
CREDIT={'Miri Sugo':'Millie'}; CREDIT.update({k:'Millie' for k in KIDS}); CREDIT.update({k:'@lindholm_lizzie (Twitter)' for k in JETURK})
ALIAS_OVR={'Tìmeyo':['Kerevi','Mutsumi Togawa','Mutsumi','Mortis'],"Nì'syu":["'Awll",'Uika Misumi','Uika','Hatsune Misumi','Hatsune'],
 'Txewan':['Txewì','Hitori Gotou','Hitori'],'Nika':['Nika Nanaura-Fardin','Silver Hand'],'Chuchu':['Chuatury Panlunch','Chuatury "Chuchu" Panlunch'],
 'Aliya':['Aliya Mahvash'],'Kobeni':['Kobeni Higashiyama','Cpl. Kobeni Higashiyama'],'Miri Sugo':['Cpl. Miri Sugo']}
PILOT=['Eyfuwen',"'Ipxerey",'Kaymi','Sänrri',"Lì'may",'Atanvi','Mìreya','Rawìl','Notä']
HUMAN=set(['Nika','Chuchu','Aliya','Kobeni','Miri Sugo','Martin Upmont','Till Nys','Nuno Kargan','Ojelo Gabel','Lilique Kadoka Lipati'])
ANAKT=['Ivan','Sua','Mizi','Till','Hyuna','Luka']
def srcname(n):
    h=versions[n][0]['heading']
    if n in ANAKT: return None
    if n in HUMAN: return None
    if n=='Tìmeyo': return 'Mutsumi Togawa (Kerevi: Mortis)'
    m=re.search(r'\((.+)\)\s*$', h); return m.group(1) if m else None
tokcount={}
for n in versions:
    s=srcname(n)
    if s:
        for part in s.split('/'):
            for tok in part.split(): tokcount[tok]=tokcount.get(tok,0)+1
def aliases_for(n, navi):
    if n in ALIAS_OVR: a=list(ALIAS_OVR[n])
    else:
        a=[]; s=srcname(n)
        if s:
            for part in s.split('/'):
                part=part.strip(); a.append(part); toks=part.split()
                if len(toks)==2:
                    for t in toks:
                        if tokcount.get(t)==1 and t not in LINK: a.append(t)
    if n in ANAKT: a += ['Recom '+n, db.get(n,{}).get('_epithet')]
    if n=='Syayvi': a.append("Tswa'avä")
    if navi: a.append(navi)
    out=[]
    for x in a:
        if x and x!=n and x not in out: out.append(x)
    return out

conflicts=[]; versnotes=[]; built=[]
def quote(text): return '\n'.join('> '+l if l.strip() else '>' for l in text.split('\n'))
def profile_block(n):
    vs=versions[n]; base=vs[0]; seen=norm(base['prose']); out=base['prose']+'\n'; kept=[]
    for v in vs[1:]:
        paras=[norm(p) for p in re.split(r'\n\s*\n', v['prose']) if len(norm(p))>40]
        if all(p in seen for p in paras): continue
        out += f"\n> [!quote]- Earlier version — {v['file']}\n"+quote(v['prose'])+'\n'
        seen += ' '+norm(v['prose']); kept.append(v['file'])
    if kept: versnotes.append((n, base['file'], kept))
    return out
SETTLED={('Tswesya','Ikran'):'Lokxtu',('Sänume','Ikran'):'Payarä',('Sänrri','Ikran'):'Towa',('Ketxe','Ikran'):'Kxäng'}
def fieldval(n, key, dbkey=None):
    if (n,key) in SETTLED: return SETTLED[(n,key)]
    vals=[]
    for v in versions[n]:
        x=v['fields'].get(key)
        if x and x not in [a for a,_ in vals]: vals.append((x,v['file']))
    d=db.get(n,{}).get(dbkey or key)
    if d: d=re.sub(r'\s*\(formerly .*?\)','',d)
    if d and d.startswith('(Not'): d=None
    if key=="Na'vi Name" and roster.get(n,{}).get('navi') and roster[n]['navi'] not in [a for a,_ in vals]: vals.append((roster[n]['navi'],'AITM_01 roster'))
    if d and d not in [a for a,_ in vals]: vals.append((d,'Astikasya_Character_Database'))
    if key=="Na'vi Name":
        for src,lab in ((None,''),(mbti[n][1] if n in mbti and len(mbti[n])>3 else None,'AITM_MBTI_Reference')):
            if src and src not in [a for a,_ in vals]: vals.append((src,lab))
    if len(vals)>1:
        conflicts.append(f"**[[{n}]] — {key.lower()}.** "+' · '.join(f"*{a}* ({s})" for a,s in vals)+f". The note uses *{vals[0][0]}*.")
    return vals[0][0] if vals else None
def rel_block(n):
    rel=[]
    for h,b in quick.get(n,[]):
        if len(quick[n])>1 or len(resolve(h))>1 or keyname(h)!=n: rel.append(f'*{h}*')
        rel.append(linkify(b,LINK,n)+'\n')
    keys=[k for k,v in LINK.items() if v==n]
    lh=[h for h in lore_heads if any(re.search(r"(?<![\w'])%s(?![\w]|'\w)"%re.escape(k), h) for k in keys)]
    if lh: rel.append('**The longer story:** '+' · '.join(f'[[Relationship Lore#{h}|{h}]]' for h in lh))
    return '\n'.join(rel).strip()

MAN_P=MANIFEST; MAN=json.load(open(MAN_P)) if os.path.exists(MAN_P) else {}
sha=lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
skipped=[]
def put(rel, content):
    content = content.rstrip('\n') + '\n'
    if DRY:
        return False
    if not guarded_write(rel, content, MAN):
        skipped.append(rel)
        return False
    return True

for n in order:
    vs=versions[n]; kind=None
    for v in vs:
        if v['kind'][0]: kind=v['kind']; break
    d=db.get(n,{})
    prof=profile_block(n)
    if n in PILOT:
        p=os.path.join(V,'10 Characters',n+'.md'); cur=io.open(p,encoding='utf-8').read()
        new=re.sub(r'## Profile\n\n.*?(?=\n## )', lambda m:'## Profile\n\n'+prof, cur, count=1, flags=re.S)
        if new!=cur and not DRY: guarded_write(os.path.relpath(p, V), new, MAN)
        for key in ('Ikran','Birthday'): fieldval(n,key)
        built.append((n,'patched' if new!=cur else 'unchanged')); continue
    navi=fieldval(n,"Na'vi Name") or ("Yueyla te Mayfam Eysi'ite" if n=='Yueyla' else None); ikran=fieldval(n,'Ikran'); bday=fieldval(n,'Birthday')
    role=d.get('Role'); sp=spears.get(n)
    groups=[]
    if kind and kind[0]=='group': groups.append(f'[[{kind[1]}]]')
    if sp: groups.append('[[Nine Spears of the Mists]]')
    family=f'[[{kind[1]}]]' if kind and kind[0]=='family' and n!='Yueyla' else None
    mb=mbti.get(n)
    fm=frontmatter({'type':'character','aliases':aliases_for(n,navi),'navi_name':navi,'source_name':srcname(n),
        'source_series':SERIES.get(n),'credit':CREDIT.get(n),'family':family,'groups':groups,
        'epithet':(sp[0] if sp else d.get('_epithet')),'role':role,'weapon':d.get('Weapon') or (sp[1] if sp else None),
        'ikran':ikran,'birthday':bday,'age':d.get('Age') or roster.get(n,{}).get('age'),'mbti':mb[-1] if mb else None,
        'status':('Deceased (dies at the end of the Wild Hunt)' if n=='Luka' else d.get('_status')),'canon':'confirmed'})
    out=[fm]; glance=[]
    for k,v in d.items():
        if k.startswith('_') or k in ("Na'vi Name",'Age','Role','Weapon','Ikran','Birthday') or not v: continue
        glance.append(f'> **{k}:** '+linkify(v,LINK,n))
    if glance: out.append('> [!abstract] At a glance\n'+'\n'.join(glance)+'\n')
    out.append('## Profile\n\n'+prof)
    r=rel_block(n)
    if r: out.append('## Relationships\n\n'+r+'\n')
    if n in case: out.append("## Name forms\n\n"+case_hdr+'\n|'+'---|'*(case_hdr.count('|')-1)+'\n'+'\n'.join(case[n])+"\n\nRules and exceptions: [[Na'vi Name Case Forms]]\n")
    keys=[k for k,v in LINK.items() if v==n]
    ph=[h for h in prov_heads if any(h.startswith(k+' ') for k in keys)]
    if ph: out.append('## Sayings\n\n'+'\n'.join(f'![[Proverbs and Sayings of the Falls#{h}]]' for h in ph)+'\n')
    ah=[h for h in acc_heads if any(h.startswith(k+' ') for k in keys)]
    if ah: out.append('## Voice\n\n'+'\n'.join(f'Voice notes: [[Astikasya Accent Reference#{h}]]' for h in ah)+'\n')
    if n=='Yueyla': out.append("## Notes\n\n- **Family.** Yueyla is an outsider to the three families, like [[Tìfyaw]], and keeps her own name, te Mayfam (ruled by Millie, 2026-11-12). Her profile sits beside the Haykxa in the Master List, but she is not a Haykxa.\n")
    if n=='Luka': out.append("## Notes\n\n- **Status.** Luka dies at the end of the Wild Hunt (ruled by Millie, October 2026, confirmed 2026-11-12). The Character Database's \"escaped/at large\" is superseded.\n")
    if n in mbti_extra:
        lab,c=mbti_extra[n]; out.append(f'## Notes\n\n- **One note, two names.** Tìmeyo and Kerevi are a DID system, so they share this note (ruled by Millie, 2026-11-12).\n- **{lab}** has a separate entry in the MBTI Reference: '+' · '.join(x for x in c[1:] if x)+'\n')
    if n=="Nì'syu": out.append("## Notes\n\n- **One note, two names.** 'Awll took Nì'syu's name, but she knows who she is (ruled by Millie, 2026-11-12).\n")
    if n=='Txewan': out.append("## Notes\n\n- **Txewì** is a nickname for Txewan, the way Bocchi is for Hitori (ruled by Millie, 2026-11-12).\n")
    out.append('## Appears in\n\n```base\nfilters:\n  and:\n    - note.type == "scene"\n    - note.characters.contains(link("%s"))\nviews:\n  - type: table\n    name: Scenes\n    order:\n      - file.name\n      - note.arc\n      - note.era\n      - note.language\n```\n' % n)
    ok=put(f'10 Characters/{n}.md','\n'.join(out)); built.append((n,'written' if ok else 'SKIPPED (edited by Millie)'))

# ---- groups
def members(prop_expr, cols):
    return '```base\nfilters:\n  and:\n    - note.type == "character"\n    - file.inFolder("10 Characters")\n    - %s\nviews:\n  - type: table\n    name: Members\n    order:\n%s\n```\n' % (prop_expr, '\n'.join('      - '+c for c in cols))
FAMCOLS=['file.name','note.navi_name','note.role','note.ikran','note.birthday','note.mbti']
GROUPS=[('Haykxa','family',['Haykxa Family','te Haykxa'],'Chainsaw Man'),('Ngotxì','family',['Ngotxì Family','te Ngotxì'],'Bocchi the Rock!'),('Korhe','family',['Korhe Family','te Korhe'],None),
 ('The Lost Cohort','faction',['Lost Cohort'],"BanG Dream! It's MyGO!!!!!"),('The Scattered Ashes','faction',['Scattered Ashes'],'BanG Dream! Ave Mujica'),
 ('Earth House','faction',['The Resistance','The Resistance (Earth House)'],None),('ANAKT Fireteam','unit',['ANAKT','The ANAKT Fireteam','Recombinant Unit-09'],'Alien Stage'),
 ('The Flying Troupe','faction',['Flying Troupe','Aytepvi Tswayona Pongu','the Troupe'],'Soul Eater')]
for g,kindg,al,ser in GROUPS:
    body=[frontmatter({'type':'group','kind':kindg,'aliases':al,'source_series':ser})]
    gi=groupintro.get(g,[])
    _gp=os.path.join(BUILD, 'renovated', 'groups', f'{g}.md')
    if os.path.exists(_gp): body.append('> [!info] Synopsis written 2026-11-12 from the notes in this vault. Nothing in it is new canon; gaps are listed under Still open.\n\n'+io.open(_gp,encoding='utf-8').read().strip()+'\n')
    if gi:
        intro=next((i for _,i,_o in gi if i),''); outro_g=next((o for _,_i,o in gi if o),'')
        if intro: body.append(intro+'\n')
    body.append('## Members\n\n'+members('note.family == link("%s")'%g if kindg=='family' else 'note.groups.contains(link("%s"))'%g, FAMCOLS if kindg=='family' else ['file.name','note.epithet','note.role','note.ikran','note.status','note.mbti']))
    if gi and outro_g: body.append('## Closing note\n\n'+outro_g+'\n')
    put(f'20 Groups/{g}.md','\n'.join(body))
mt=rd(MASTER,BK); ns=dict(sections(mt,2)); nsk=[k for k in ns if 'Nine Spears' in k][0]
put('20 Groups/Nine Spears of the Mists.md', frontmatter({'type':'group','kind':'unit','aliases':['Nine Spears','The Nine Spears','The Nine Spears of the Mists','the Nine']})+
    ns[nsk].strip()+'\n\n## Members\n\n'+members('note.groups.contains(link("Nine Spears of the Mists"))',['file.name','note.epithet','note.weapon','note.ikran','note.family'])+
    '\n## From the Character Database\n\n'+linkify(spear_db,LINK)+'\n'+
    ('\n> [!quote]- Earlier version — 05_Lore_and_Traditions\n'+quote(dict(sections(rd('Local_Only_Core/05_Lore_and_Traditions.md',BK),2)).get('The Nine Spears of the Mists','').strip())+'\n'))
clan=dict(sections(roster_t,2)).get('The Astikasya Clan','').strip()
_pre=mt[:mt.index('## Table of Contents')]; _pre=re.sub(r'\A\s*# .+\n','',_pre).strip()
_epi=('> [!quote] Epigraph of the Master List\n'+quote(_pre)+'\n\n') if _pre else ''
put('20 Groups/Astikasya.md', frontmatter({'type':'group','kind':'clan','aliases':['Astikasya Clan','The Astikasya Clan','the Astikasya']})+_epi+clan+'\n')

# ---- open questions
blank=[n for n in order if n not in PILOT and not SERIES.get(n)]
Q=['<!-- cast-build:start -->','## From the full cast build','',
 '### Fields that disagree between files','']+[f'- [ ] {c}' for c in conflicts]+['',
 '### Profiles where versions differed','',
 'Rule applied (your ruling, 2026-11-11): the newest version is the profile, older ones are folded under "Earlier version" on the same note. Glance through when you have time.','']+\
 [f"- [ ] [[{n}]] — profile from `{b}`; earlier text kept from {', '.join('`'+k+'`' for k in ks)}" for n,b,ks in versnotes]+['',
 '### Ruled on 2026-11-12','',
 "- [x] **[[Ketxe]] — ikran.** Master List says *Kxäng*, the older family file says *Tìrol*. **Ruled: Kxäng.**",
 '- [x] **Children with no series.** '+', '.join(f'[[{n}]]' for n in KIDS)+" are Millie's own original characters. The Jeturk twins, [[Tulìpey]] and [[Eantu]], are original characters by @lindholm_lizzie (Twitter).",
 "- [x] **[[Yueyla]] — family.** **Ruled:** she is an outsider like [[Tìfyaw]] and keeps the Mayfam name; no clan family is set.",
 "- [x] **[[Luka]] — status.** **Ruled:** he dies at the end of the Wild Hunt. The database's ESCAPED/AT LARGE is superseded.",
 '<!-- cast-build:end -->']
p=os.path.join(V,'00 Home/Open Questions.md'); cur=io.open(p,encoding='utf-8').read()
cur=re.sub(r'\n*<!-- cast-build:start -->.*?<!-- cast-build:end -->\n?','',cur,flags=re.S).rstrip('\n')+'\n\n'+'\n'.join(Q)+'\n'
if not DRY:
    guarded_write(os.path.relpath(p, V), cur, MAN); json.dump(MAN,open(MAN_P,'w'),ensure_ascii=False,indent=0)
print('characters:',len(order)); 
from collections import Counter; print(Counter(s for _,s in built)); print('skipped:',skipped)
print('conflicts',len(conflicts)); [print(' ',c[:230]) for c in conflicts]
print('versions differed',len(versnotes)); print('blank series:',blank)
print('spears',spears); print('no DB entry:',[n for n in order if n not in db]); print('no MBTI:',[n for n in order if n not in mbti]); print('no quickref:',[n for n in order if n not in quick]); print('no case:',[n for n in order if n not in case and n not in HUMAN and n not in ANAKT])
print('groupintro',{k:[(f,len(i),len(o)) for f,i,o in v] for k,v in groupintro.items()})
