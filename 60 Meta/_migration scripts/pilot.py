import re, os
from common import *
LINK = registry(); NAMES = set(LINK)|set(LINK.values())
def rd(rel, base=SRC, moj=False):
    return fix_name_apos(read(rel, base, moj), NAMES)

prof = dict((h.split(' (')[0], (h, b)) for h,b in sections(rd('AITM_02_Samaya_Family_Profiles.md'),3))
dbt = rd('Astikasya_Character_Database.md', moj=True)
db = {}
for h,b in sections(dbt,3):
    b = b.split('\n---')[0]
    f = dict((m.group(1).strip(), m.group(2).strip()) for m in re.finditer(r'^\*\*(.+?):\*\*\s*(.*)$', b, re.M))
    db[h.split(' (')[0]] = f
mbti_t = rd('AITM_MBTI_Reference.md'); case_t = rd('AITM_Navi_Name_Case_Forms.md')
quick = dict(sections(rd('AITM_Relationships_QuickRef.md'),3))
lore_t = rd('AITM_Relationships_Lore.md'); lore_heads = [h for h,_ in sections(lore_t,3)]
prov_t = rd('AITM_Navi_Proverbs.md'); prov_heads=[h for h,_ in sections(prov_t,2)]
acc_t = rd('AITM_Astikasya_Accent_Reference.md'); acc_heads=[h for h,_ in sections(acc_t,3)]
roster = rd('AITM_01_Clan_Overview_and_Groups.md')

def table_row(text, name):
    for line in text.splitlines():
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if cells and cells[0].strip('*')==name: return cells
def case_header():
    for line in case_t.splitlines():
        if line.startswith('| Name |'): return line

SERIES = {'Atanvi':'Mobile Suit Gundam: The Witch from Mercury','Mìreya':'Mobile Suit Gundam: The Witch from Mercury',
 'Kaymi':'Mobile Suit Gundam: The Witch from Mercury',"'Ipxerey":'Mobile Suit Gundam: The Witch from Mercury',
 'Eyfuwen':'Mobile Suit Gundam: The Witch from Mercury','Sänrri':"BanG Dream! It's MyGO!!!!!","Lì'may":'Original character','Rawìl':'Original character','Notä':'Original character'}
CREDIT={"Lì'may":'Millie','Rawìl':'@lindholm_lizzie (Twitter)','Notä':'@lindholm_lizzie (Twitter)'}
ORDER = ['Eyfuwen',"'Ipxerey",'Kaymi','Sänrri',"Lì'may",'Atanvi','Mìreya','Rawìl','Notä']
conflicts=[]; report=[]
for name in ORDER:
    head, body = prof[name]; d = db.get(name,{})
    src = head[head.index('(')+1:head.rindex(')')]
    ik = re.search(r'^\*\*Ikran\*\*:\s*(.+)$', body, re.M); bd = re.search(r'^\*\*Birthday\*\*:\s*(.+)$', body, re.M)
    ikran = ik.group(1).strip() if ik else None; bday = bd.group(1).strip() if bd else None
    text = re.sub(r'^\*\*(Ikran|Birthday)\*\*:.*\n?', '', body, flags=re.M).strip()
    if ikran and d.get('Ikran') and d['Ikran']!=ikran:
        conflicts.append(f"**[[{name}]] — ikran.** The family profile says *{ikran}*; the Character Database says *{d['Ikran']}*. The note uses the profile's (*{ikran}*) until you rule.")
    if bday and d.get('Birthday') and d['Birthday']!=bday:
        conflicts.append(f"**[[{name}]] — birthday.** Profile: {bday}. Database: {d['Birthday']}.")
    navi = d.get("Na'vi Name")
    m = re.search(r'\*\*%s \(.*?\)\*\*\s*\n\s*\*\*Na.vi Name\*\*:?\s*:?\s*(.+)' % re.escape(name), roster)
    if m and navi and m.group(1).strip()!=navi:
        conflicts.append(f"**[[{name}]] — full Na'vi name.** Roster: *{m.group(1).strip()}*. Database: *{navi}*.")
    mb = table_row(mbti_t, name); mbti = mb[-1] if mb else None
    if mb and navi and mb[1]!=navi: conflicts.append(f"**[[{name}]] — full Na'vi name.** MBTI Reference: *{mb[1]}*. Database: *{navi}*.")
    role = d.get('Role'); ep = re.search(r'(The [A-Z]\w+)', role or '') if role and 'Nine Spears' in role else None
    aliases=[]
    for part in src.split('/'):
        part=part.strip(); aliases.append(part)
        if ' ' in part: aliases.append(part.split(' ')[0])
    if name=='Sänrri': aliases += ['Tomori Takamatsu','Dr. Tomori Takamatsu']
    if navi: aliases.append(navi)
    aliases=[a for i,a in enumerate(aliases) if a not in aliases[:i] and a!=name]
    fm = frontmatter({'type':'character','aliases':aliases,'navi_name':navi,'source_name':src,
        'source_series':SERIES.get(name),'credit':CREDIT.get(name),'family':'[[Samaya]]',
        'groups':['[[Nine Spears of the Mists]]'] if ep else [], 'epithet':ep.group(1) if ep else None,
        'role':role,'weapon':d.get('Weapon'),'ikran':ikran or d.get('Ikran'),'birthday':bday or d.get('Birthday'),
        'age':d.get('Age'),'mbti':mbti,'canon':'confirmed'})
    out=[fm]
    glance=[]
    if d.get('Family'): glance.append('> **Family:** '+linkify(d['Family'],LINK,name))
    for k in ('Personality Snapshot','Key Traits'):
        if d.get(k): glance.append(f'> **{k}:** '+linkify(d[k],LINK,name))
    if glance: out.append('> [!abstract] At a glance\n'+'\n'.join(glance)+'\n')
    out.append('## Profile\n\n'+text+'\n')
    rel=[]
    if name in quick: rel.append(linkify(quick[name].strip(),LINK,name))
    lh=[h for h in lore_heads if re.search(r"(?<![\w'])%s(?![\w]|'\w)"%re.escape(name), h)]
    if lh: rel.append('\n**The longer story:** '+' · '.join(f'[[Relationship Lore#{h}|{h}]]' for h in lh))
    if rel: out.append('## Relationships\n\n'+'\n'.join(rel)+'\n')
    cr = table_row(case_t, name)
    if cr:
        hdr=case_header(); out.append("## Name forms\n\n"+hdr+'\n'+'|'+'---|'*(hdr.count('|')-1)+'\n| '+' | '.join(['**'+name+'**']+cr[1:])+' |\n\nRules and exceptions: [[Na\'vi Name Case Forms]]\n')
    ph=[h for h in prov_heads if h.startswith(name+' ')]
    if ph: out.append('## Sayings\n\n'+'\n'.join(f'![[Proverbs and Sayings of the Falls#{h}]]' for h in ph)+'\n')
    ah=[h for h in acc_heads if h.startswith(name+' ')]
    if ah: out.append('## Voice\n\n'+'\n'.join(f'Voice notes: [[Astikasya Accent Reference#{h}]]' for h in ah)+'\n')
    out.append('## Appears in\n\n```base\nfilters:\n  and:\n    - note.type == "scene"\n    - note.characters.contains(link("%s"))\nviews:\n  - type: table\n    name: Scenes\n    order:\n      - file.name\n      - note.arc\n      - note.era\n      - note.language\n```\n' % name.replace('"','\\"'))
    write(f'10 Characters/{name}.md', '\n'.join(out))
    report.append((name, ikran, bday, navi, mbti, bool(cr), len(text)))

# reference docs the pilot links into (originals stay in root for now)
write("20 Groups/Relationship Lore.md", frontmatter({'type':'reference','aliases':['AITM_Relationships_Lore']})+lore_t)
write("50 Language/Proverbs and Sayings of the Falls.md", frontmatter({'type':'reference','aliases':['AITM_Navi_Proverbs']})+prov_t)
write("50 Language/Astikasya Accent Reference.md", frontmatter({'type':'reference','aliases':['AITM_Astikasya_Accent_Reference']})+acc_t)
write("50 Language/Na'vi Name Case Forms.md", frontmatter({'type':'reference','aliases':['AITM_Navi_Name_Case_Forms']})+case_t)

write('20 Groups/Samaya.md', frontmatter({'type':'group','kind':'family','aliases':['Samaya Family','te Samaya']}) + '''## Members

```base
filters:
  and:
    - note.type == "character"
    - note.family == link("Samaya")
views:
  - type: table
    name: Members
    order:
      - file.name
      - note.navi_name
      - note.role
      - note.ikran
      - note.birthday
      - note.mbti
```

## Notes

''')
import json; json.dump({'conflicts':conflicts,'report':report}, open(os.path.join(BUILD, 'pilot_out.json'),'w'), ensure_ascii=False, indent=1)
for r in report: print(r)
print('\n'.join(conflicts))
