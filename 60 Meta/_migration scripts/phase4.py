import re, os, io, json, hashlib, subprocess
from common import *
LINK=registry(); LINK['Till']='Till'; LINK['Yueyla']='Yueyla'
NAMES=set(LINK)|set(LINK.values())
raw=lambda rel,base=SRC: io.open(os.path.join(base,rel),encoding='utf-8').read()
def rd(rel, base=SRC, moj=False): return fix_name_apos(read(rel, base, moj).replace('‘',"'"), NAMES)
norm=lambda s: re.sub(r'\s+',' ',s.replace('*','').replace('’',"'")).strip()
MAN_P=MANIFEST; MAN=json.load(open(MAN_P))
sha=lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest(); skipped=[]; made=[]
def put(rel, content):
    if not guarded_write(rel, content.rstrip('\n') + '\n', MAN):
        skipped.append(rel)
        return False
    made.append(rel)
    return True
NAMEPAT=re.compile(r"(?<![\w\[|'])(" + '|'.join(re.escape(n) for n in sorted(LINK,key=len,reverse=True)) + r")(?!\w|'(?!s\b)\w)")
def chars_in(text):
    out=[]
    for m in NAMEPAT.finditer(text.replace('’',"'")):
        t=LINK[m.group(1)]
        if t not in out: out.append(t)
    return [f'[[{t}]]' for t in out]
def lang(text):
    t=' '+text.lower()+' '
    return 'es' if sum(t.count(w) for w in (' que ',' los ',' una ',' con '))>sum(t.count(w) for w in (' the ',' and ',' with ',' was ')) else 'en'
def strip_h1(t): return re.sub(r'\A\s*# .+\n+','',t,count=1)

ARCS=[('A Torchlight',"Tomori's first steps, to Pandora, the flashback to 2154 to the Battle of the Hallelujah Mountains, her being found by the Astikasya, and ending into her consciousness transfer as Sänrri, and her mating with Kaymi."),
 ('The Great Games',"The Great Games of the Western Frontier take place, the children are conceived and born. One by one, she becomes a better tsakarem."),
 ('The Thanator and the Slinger',"Tsu'ong and Ketxe come to the Falls seeking uturu, the young Korhe twins already mingling with the rest. Old wounds resurface, until a boiling point. The knowledge of Sänrri mediates between the old and the new. The Resistance gets a place near the Falls."),
 ('Scattered Ashes, Burning Hearts',"Syayvi's story, from her rise, her friendship with the Cohort, Sänrri, and all, until her exile to the Mangkwan with 'Awll and Tìmeyo."),
 ('The Reckoning','The rapture of the Cohort, the "SAI" era of the AU. First look at the overall state of affairs of Pandora, cameos of the main characters.'),
 ('Ambition and Hope — The Ones Who Know All','"The Outside" of the AU: Sänrri gets the knowledge of the previous Toruk Makto, Roneyu is introduced.'),
 ('Prelude to Fire','The comeback. Sänrri has more power, the comeback, "They Are Coming."'),
 ('Siege of the Falls','Oh, you already know.'),
 ('The Wild Hunt','The vendetta against the lost ANAKT fireteam, the contact to the Anurai, The Flying Troupe take stage. Tsu\'lan vs Luka. Sänrri lost in thought, catatonic, "The Contract"')]
ARCN={n:i+1 for i,(n,_) in enumerate(ARCS)}; ARCS_D=dict(ARCS)
# ================= WORLD =================
wb=rd('Astikasya_Worldbuilding_Reference.md',moj=True)
master=rd('Local_Only_Core/AITM_00_Master_List.md',BK); msec=dict(sections(master,2))
ATOM={'Sheltering Falls (Home Settlement)':('Sheltering Falls','place',['The Falls','Sheltering Falls (Home Settlement)']),
 "Cave of Truth (Na'vi: Tìngayä Slär)":('Cave of Truth','place',['Tìngayä Slär']),
 'Ikran-Mounted Crossbow':('Ikran-Mounted Crossbow','technology',['ikran crossbow']),
 'Woodshaping Techniques':('Woodshaping','technology',['Woodshaping Techniques']),
 'Laysrew (Free Dance)':('Laysrew','custom',['Free Dance','Laysrewtsyìp']),
 'Gender Transition Through Eye of Eywa':('Gender Transition Through Eye of Eywa','custom',['Eye of Eywa']),
 'Communication with Ancestors':('Communication with Ancestors','custom',[]),
 'Food & Cuisine':('Food & Cuisine','custom',[]),'Music & Arts':('Music & Arts','custom',[]),'Education':('Education','custom',[]),
 'Allied Clans':('Allied Clans','reference',[]),'Hostile Forces':('Hostile Forces','reference',[])}
extra={'Laysrew':[('Master List',msec.get('Laysrew',''))]}
lt=rd('Local_Only_Core/05_Lore_and_Traditions.md',BK); ltsec=dict(sections(lt,2))
if ltsec.get('Laysrew') and norm(ltsec['Laysrew']) not in norm(msec.get('Laysrew','')): extra['Laysrew'].append(('05_Lore_and_Traditions',ltsec['Laysrew']))
out_ref=wb
for h,(name,typ,al) in ATOM.items():
    m=re.search(r'^### %s[ \t]*\n(.*?)(?=^#{1,3} |\Z)'%re.escape(h), wb, re.M|re.S); assert m, h
    body=m.group(1).strip(); body=re.sub(r'\n-{3,}\s*$','',body).strip()
    parts=[body] if name!='Laysrew' else []
    if name=='Laysrew':
        parts.append(extra['Laysrew'][0][1].strip())
        parts.append('## From the Worldbuilding Reference\n\n'+body)
        for src,t in extra['Laysrew'][1:]: parts.append(f'## From {src}\n\n'+t.strip())
    text='\n\n'.join(parts)
    put(f'30 World/{name}.md', frontmatter({'type':typ,'aliases':al,'characters':chars_in(text),'canon':'confirmed'})+text)
    out_ref=out_ref.replace(m.group(0), f'### {h}\n\nMoved to its own note: [[{name}]]\n\n')
out_ref=out_ref.replace('### The Nine Spears of the Mists\n','### The Nine Spears of the Mists\n\nSee also the group note: [[Nine Spears of the Mists]]\n',1).replace('### The Resistance (Earth House)\n','### The Resistance (Earth House)\n\nSee also the group note: [[Earth House]]\n',1)
put('30 World/Worldbuilding Reference.md', frontmatter({'type':'reference','aliases':['Astikasya_Worldbuilding_Reference','Astikasya Clan - World-Building Reference']})+strip_h1(out_ref))
art=msec.get('The Artisan of the Spears','').strip()
put('30 World/The Artisan of the Spears.md', frontmatter({'type':'custom','aliases':['Artisan of the Spears'],'characters':chars_in(art),'canon':'confirmed'})+art)
for src,base,name,typ,al in [('AITM_Geography_The_Lake.md',SRC,'The Lake','place',['Geography of the Western Frontier: The Lake','the Lake']),
    ('AITM_Earth_House_Mark.md',SRC,'The Mark of Earth House','custom',['Earth House Mark']),
    ('claude/AITM_Astikasya_Yellow.md',SRC,'Astikasya Yellow','custom',['Tìrim','Tìrim — The Yellow of the Astikasya','Bandito yellow'])]:
    t=rd(src,base); put(f'30 World/{name}.md', frontmatter({'type':typ,'aliases':al,'characters':chars_in(t),'canon':'confirmed'})+strip_h1(t))
ltrest=[k for k in ltsec if k not in ('Laysrew',) and norm(ltsec[k]) not in norm(master)]
print('lore&trad sections not in master:',ltrest)

# ================= STORY =================
tl=raw('claude/AITM_Story_Timeline.md'); tsec=sections(tl,2)
intro=strip_h1(tl[:re.search(r'^## ',tl,re.M).start()]).strip(); intro=re.sub(r'\n-{3,}\s*$','',intro).strip()
eras=[]; threads=''
for i,(h,b) in enumerate(tsec):
    b=re.sub(r'\n-{3,}\s*$','',b.strip()).strip()
    if h.lower().startswith('open threads'): threads=b; continue
    eras.append(h)
    put(f'40 Story/Eras/{h}.md', frontmatter({'type':'era','order':str(len(eras)),'aliases':[h.split(' — ')[0]] if ' — ' in h and h.split(' — ')[0]!='Overcompensate' else [],'characters':chars_in(b),'canon':'confirmed'}).replace('order: "%d"'%len(eras),'order: %d'%len(eras))+b)
put('40 Story/Timeline.md', frontmatter({'type':'timeline','aliases':['Story Timeline','AITM_Story_Timeline']})+intro+'\n\n## The eras, in order\n\n'+'\n'.join(f'{i+1}. [[{e}]]' for i,e in enumerate(eras))+'\n\n## The arcs, in order\n\nNamed by Millie on 2026-11-12. The eras above are the Twenty One Pilots lens; the arcs are the story itself.\n\n'+'\n'.join(f'{i+1}. [[{n}]]' for i,(n,_) in enumerate(ARCS))+'\n\n![[Story.base#Arcs]]\n\n## Open threads\n\nKept with the other rulings in [[Open Questions#Story threads]].\n')
ERA={e.split(' — ')[0]:e for e in eras}
def arc_fm(name,al,era,text,status='outline'):
    fm=frontmatter({'type':'arc','kind':('flashback arc' if name.startswith('Scattered Ashes') else None),'order':'@@','aliases':al,'era':f'[[{era}]]' if era else None,'characters':chars_in(text+' '+ARCS_D[name]),'status':status,'canon':'confirmed'}).replace('order: "@@"','order: %d'%ARCN[name])
    extra=("> [!note] Where this arc sits\n> A flashback arc, told out of order, like Turn Back the Pendulum in Bleach (ruled by Millie, 2026-11-12). In the story's chronology the twins' exile still belongs to the Prologue; see [[Prologue — The Forest and the Falls]].\n\n" if name.startswith('Scattered Ashes') else '')
    return fm+"> [!summary] Millie's summary of this arc (2026-11-12)\n> "+ARCS_D[name]+'\n\n'+extra
def arc(src,base,name,era,al,rawread=False,pre=None):
    t=raw(src,base) if rawread else rd(src,base)
    if pre: t=pre(t)
    rp=os.path.join(BUILD, 'renovated', f'{name}.md')
    if os.path.exists(rp):
        r=io.open(rp,encoding='utf-8').read().strip()
        q='\n'.join('> '+l if l.strip() else '>' for l in t.strip().split('\n'))
        put(f'40 Story/Arcs/{name}.md', arc_fm(name,al,era,t+' '+r)+r+'\n\n> [!quote]- Earlier version — the original summary this note was built from\n'+q+'\n')
    else:
        put(f'40 Story/Arcs/{name}.md', arc_fm(name,al,era,t)+t.strip())
arc('AITM_08_The_Wild_Hunt_Arc.md',SRC,'The Wild Hunt',ERA.get('Breach'),['The Wild Hunt Arc','Wild Hunt'],pre=lambda t: re.sub(r'\A# .+\n## The Wild Hunt Arc\n','',t))
arc('Siege of the Falls Arc .md',SRC,'Siege of the Falls',ERA.get('Clancy'),['The Siege of the Falls','Siege of the Falls Arc','the Siege','Asedio de las Cascadas'])
for _n,_s in ARCS:
    if _n in ('Siege of the Falls','The Wild Hunt'): continue
    _era=ERA.get('Scaled and Icy') if _n=='The Reckoning' else None
    _al=['Ambition and Hope','The Ones Who Know All'] if _n.startswith('Ambition') else []
    _rp=os.path.join(BUILD, 'renovated', f'{_n}.md')
    _body=(io.open(_rp,encoding='utf-8').read().strip()+'\n\n') if os.path.exists(_rp) else '## Outline\n\n\n'
    put(f'40 Story/Arcs/{_n}.md', arc_fm(_n,_al,_era,_body,status=('synopsis' if os.path.exists(_rp) else 'named') if not _n.startswith('Ambition') else 'working title')+_body+'## Scenes\n\n```base\nfilters:\n  and:\n    - note.type == "scene"\n    - note.arc == link("%s")\nviews:\n  - type: table\n    name: Scenes\n    order:\n      - file.name\n      - note.language\n      - note.status\n```\n' % _n)
def scene(name,text,arcname=None,era=None,al=None,title=None,tr=None,canon='confirmed',kind=None):
    put(f'40 Story/Scenes/{name}.md', frontmatter({'type':'scene','kind':kind,'title':title or name,'aliases':al or [],'arc':f'[[{arcname}]]' if arcname else None,'era':f'[[{era}]]' if era else None,
        'characters':chars_in(text),'language':lang(text),'translation_of':tr,'status':'draft','canon':canon})+text.strip())
scene('La Piadosa y la Bruja', rd('La Piadosa y la Bruja .md'), arcname='Siege of the Falls', era=ERA.get('Clancy'), al=['El Corredor al Santuario'])
scene('Kava with the Nine', strip_h1(raw('claude/AITM_Scene_Kava_With_The_Nine.md')), al=['AITM — Kava with the Nine'], kind='side story')
scene('The Night the Warriors Lost Their Dignity', strip_h1(raw('claude/AITM_Night_Warriors_Lost_Their_Dignity.md')), al=['Txon a aysamsiyul meuiat holan'], kind='side story')
scene('The Great Games Legacy', strip_h1(rd('The Great Games Legacy.md')), arcname='The Great Games', era=ERA.get('The Dreamwalker Years') or 'The Dreamwalker Years')
tr=subprocess.run(['pandoc',os.path.join(SRC,'WELCOME BACK TO TRENCH.docx'),'-t','markdown','--wrap=none'],capture_output=True,text=True,check=True).stdout
tr=re.sub(r'^([IVX]+\. .+)$', r'## \1', tr, flags=re.M)
scene('Welcome Back to Trench', tr, title='WELCOME BACK TO TRENCH', arcname='Prelude to Fire', era=ERA.get('Overcompensate'), al=['WELCOME BACK TO TRENCH'])
unplaced=[]

# ================= LANGUAGE / META =================
def ref(folder,src,name,al,base=SRC,clean_it=False,typ='reference'):
    t=rd(src,base) if clean_it else raw(src,base)
    put(f'{folder}/{name}.md', frontmatter({'type':typ,'aliases':al})+strip_h1(t) if t.lstrip().startswith('# ') else frontmatter({'type':typ,'aliases':al})+t)
ref('50 Language','claude/AITM_Reef_Navi_Reference.md',"Reef Na'vi Reference",['AITM_Reef_Navi_Reference','Reef Navi'])
ref('50 Language','claude/AITM_Naviteri_Notes.md',"Notes from Na'viteri",['AITM_Naviteri_Notes',"Na'viteri Notes"])
ref('50 Language','claude/AITM_Navi_Name_Audit.md',"Na'vi Name Audit",['AITM_Navi_Name_Audit'])
ref('50 Language','claude/AITM_Name_Fixes.md','Name Fixes to Apply',['AITM_Name_Fixes'])
ref('50 Language','claude/AITM_Nine_Spears_Navi.md',"The Nine Spears in Na'vi",['AITM_Nine_Spears_Navi'])
ref('50 Language','Familiar terms.md','Family Terms',['Familiar terms'])
ref('60 Meta','AITM_MBTI_Reference.md','MBTI Reference',['AITM_MBTI_Reference'],clean_it=True)
ref('60 Meta','Reference/Into_the_Mists_AU_Analysis.md','AU Analysis',['Into_the_Mists_AU_Analysis'],base=BK)
for src,name,al in [('Into_the_Mists_AU_Analysis.docx','AU Analysis (October 2026)',[]),('Avatar Into the Mists — Working Reference.docx','Working Reference',['Avatar Into the Mists — Working Reference'])]:
    t=subprocess.run(['pandoc',os.path.join(BK,src),'-t','markdown','--wrap=none'],capture_output=True,text=True,check=True).stdout
    put(f'60 Meta/{name}.md', frontmatter({'type':'reference','aliases':al})+t)
cl=raw('CLAUDE.md',BK); i=cl.index('## Lore rules')
put('00 Home/Canon Rules.md', frontmatter({'type':'meta','aliases':['Lore rules','Style rules']})+'The rules every scene and note has to pass. Taken from the folder guide written for Claude; the project instructions carry the same rules.\n\n'+cl[i:].split('\n# Into the Mists')[0].strip())

# ================= BASES + HOME =================
put('40 Story/Story.base','''filters:
  or:
    - note.type == "arc"
    - note.type == "era"
    - note.type == "scene"
views:
  - type: table
    name: Scenes
    filters:
      and:
        - note.type == "scene"
    order:
      - file.name
      - note.arc
      - note.era
      - note.language
      - note.status
      - note.canon
  - type: table
    name: Arcs
    filters:
      and:
        - note.type == "arc"
    order:
      - note.order
      - file.name
      - note.era
      - note.status
  - type: table
    name: Eras
    filters:
      and:
        - note.type == "era"
    order:
      - note.order
      - file.name
  - type: table
    name: Side stories
    filters:
      and:
        - note.kind == "side story"
    order:
      - file.name
      - note.language
  - type: table
    name: Needs placing
    filters:
      and:
        - note.type == "scene"
        - note.era == null
        - note.kind != "side story"
    order:
      - file.name
      - note.language
''')
put('30 World/World.base','''filters:
  and:
    - file.inFolder("30 World")
views:
  - type: table
    name: World
    groupBy:
      property: note.type
      direction: ASC
    order:
      - file.name
      - note.type
      - note.canon
''')
home=frontmatter({'type':'home'})+'''# Avatar: Into the Mists

The front door. Everything in the vault is reachable from here.

## Cast

Families and factions: [[Astikasya]] · [[Samaya]] · [[Haykxa]] · [[Ngotxì]] · [[Korhe]] · [[Nine Spears of the Mists]] · [[The Lost Cohort]] · [[The Scattered Ashes]] · [[Earth House]] · [[The Flying Troupe]] · [[ANAKT Fireteam]] · [[Relationship Lore]]

![[Cast.base]]

## Story

Start at the [[Timeline]].

![[Story.base]]

## World

![[World.base]]

## Rulings

Things waiting on a decision from you: [[Open Questions]] · The rules: [[Canon Rules]]

![[Rulings.base]]

## Language

- [[Na'vi Name Case Forms]]
- [[Family Terms]]
- [[Proverbs and Sayings of the Falls]]
- [[Astikasya Accent Reference]]
- [[Reef Na'vi Reference]]
- [[The Nine Spears in Na'vi]]
- [[Notes from Na'viteri]]
- [[Na'vi Name Audit]] and [[Name Fixes to Apply]]

## About this vault

- [[How This Vault Works]]
- [[Vault Design]]
- [[MBTI Reference]] · [[AU Analysis]]
'''
hp=os.path.join(V,'00 Home/Home.md'); cur=io.open(hp,encoding='utf-8').read()
if False:
    guarded_write(os.path.relpath(hp, V), home, MAN); print('home rewritten')
else: print('HOME EDITED BY MILLIE - not touched')
# open questions: story threads + needs placing
p=os.path.join(V,'00 Home/Open Questions.md'); cur=io.open(p,encoding='utf-8').read()
blk='<!-- story:start -->\n## Story threads\n\nCarried over from the end of the Story Timeline, word for word.\n\n'+threads+'\n\n## Scene placement\n\n- [x] **Ruled 2026-11-12:** [[Kava with the Nine]] and [[The Night the Warriors Lost Their Dignity]] are side stories, offshoots like filler episodes in an anime. They carry `kind: side story` and need no era. [[The Great Games Legacy]] was first ruled a side story, then moved into the arc [[The Great Games]].\n- [x] **Ruled 2026-11-12:** [[Welcome Back to Trench]] is Overcompensate. It sits in [[Overcompensate — The Homecoming]], in the arc [[Prelude to Fire]].\n- [x] **Ruled 2026-11-12:** [[Scattered Ashes, Burning Hearts]] is a flashback arc, so the twins\' exile stays in the Prologue chronologically.\n- [ ] **\'Awll and the exile.** Your summary of arc 4 has \'Awll going into exile with Syayvi and Tìmeyo. The Timeline\'s Prologue names only the twins. Which is right, or did \'Awll join them later?\n<!-- story:end -->'
cur=re.sub(r'\n*<!-- story:start -->.*?<!-- story:end -->\n?','',cur,flags=re.S).rstrip('\n')+'\n\n'+blk+'\n'
guarded_write(os.path.relpath(p, V), cur, MAN)
json.dump(MAN,open(MAN_P,'w'),ensure_ascii=False,indent=0)
print('made',len(made)); print('skipped',skipped); print('eras',eras)
