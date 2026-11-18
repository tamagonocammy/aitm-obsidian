import re, os, glob, io, subprocess, argparse, shutil
try:
    import yaml
except ImportError:
    raise SystemExit('PyYAML is required; use 60 Meta/_admin/.venv/bin/python.')
parser = argparse.ArgumentParser(description='Read-only migration proof. Full archival checks require --full.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--full', action='store_true', help='Validate all active notes against archived prose')
group.add_argument('--notes', nargs='+', help='Check selected vault-relative notes; no archival prose scan')
parser.add_argument('-v', action='store_true', help='Show examples of unmatched prose')
args = parser.parse_args()
if args.full and not shutil.which('pandoc'):
    raise SystemExit('Pandoc is required for full proof; no validation performed.')
from common import *
LINK=registry() if args.full else {}; LINK['Till']='Till'; LINK['Yueyla']='Yueyla'; NAMES=set(LINK)|set(LINK.values())
norm=lambda s: re.sub(r'\s+',' ',re.sub(r'[*_`>#|]','',s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('&#10;',' '))).strip()
unlink=lambda s: re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s)
notes={}
selected = [os.path.join(V, p) for p in args.notes] if args.notes else glob.glob(V+'/**/*.md',recursive=True)
for p in selected:
    if not os.path.realpath(p).startswith(os.path.realpath(V) + os.sep):
        raise SystemExit('Note path escapes the vault: ' + p)
    r=os.path.relpath(p,V)
    if r[:2] in ('00','10','20','30','40','50','60') and '_migration scripts' not in r and '.venv' not in r: notes[r]=io.open(p,encoding='utf-8').read()
if not notes:
    raise SystemExit('No active notes selected; validation not performed.')
blob=norm(unlink(' '.join(notes.values())))
A=os.path.join(V,'99 Archive/2026-11-11 originals')
rows=[]; 
for p in sorted(glob.glob(A+'/**/*',recursive=True)) if args.full else []:
    if not os.path.isfile(p): continue
    r=os.path.relpath(p,A)
    if p.endswith('.md'): t=io.open(p,encoding='utf-8',errors='replace').read()
    elif p.endswith('.docx'): t=subprocess.run(['pandoc',p,'-t','markdown','--wrap=none'],capture_output=True,text=True,check=True).stdout
    else: rows.append((r,None,None,[])); continue
    t=fix_name_apos(clean(t, mojibake=('Character_Database' in r or 'Worldbuilding' in r)),NAMES)
    paras=[norm(x) for x in re.split(r'\n\s*\n|\n(?=[-*\d#|])', t)]
    paras=[x for x in paras if len(x)>60]
    miss=[x for x in paras if x not in blob]
    rows.append((r,len(paras),len(miss),miss[:2]))
for r,n,m,ex in rows:
    if n is None: print(f'--    {r}  (not text)')
    else:
        print(f'{n-m:4d}/{n:<4d} {r}')
        if m and '-v' in os.sys.argv:
            for e in ex: print('        e.g.',e[:110])
# links
titles={}
if args.notes:
    import json
    with open(os.path.join(V, '60 Meta/_admin/index.json'), encoding='utf-8') as f:
        for path, entry in json.load(f)['notes'].items():
            for name in [entry['title'], *entry['aliases']]:
                titles.setdefault(str(name), path)
for k,t in notes.items():
    titles.setdefault(os.path.basename(k)[:-3],k)
for k,t in notes.items():
    fm=yaml.safe_load(re.match(r'---\n(.*?)\n---',t,re.S).group(1)) if t.startswith('---') else {}
    for a in (fm or {}).get('aliases') or []: titles.setdefault(str(a),k)
for b in glob.glob(V+'/**/*.base',recursive=True):
    titles[os.path.basename(b)]=b; yaml.safe_load(open(b,encoding='utf-8'))
heads={k:set(h for lv in (1,2,3,4) for h,_ in sections(t,lv)) for k,t in notes.items()}
unres={}; bad=[]
for k,t in notes.items():
    body=re.sub(r'```.*?```','',t,flags=re.S)
    for tgt in re.findall(r'\[\[([^\]|]+)', body):
        name,_,h=tgt.partition('#')
        if not name:
            name = os.path.basename(k)[:-3]
        if name not in titles or not os.path.exists(os.path.join(V, titles[name])): unres.setdefault(name,[]).append(k)
        elif h and not titles[name].endswith('.base'):
            target = titles[name]
            if target not in heads:
                target_text = io.open(os.path.join(V, target), encoding='utf-8').read()
                heads[target] = set(heading for lv in (1,2,3,4) for heading,_ in sections(target_text,lv))
            if h not in heads[target]: bad.append((k,tgt))
print('notes:',len(notes),'| unresolved:',{k:v[:2] for k,v in unres.items()},'| broken heading links:',bad[:5])
encoding_errors = [k for k,t in notes.items() if re.search(r'Ã.|â€',t) and 'Vault Design' not in k and 'Name Fixes' not in k]
print('mojibake:', encoding_errors)
import collections; print(collections.Counter(k.split('/')[0] for k in notes))

raise SystemExit(bool(unres or bad or encoding_errors or any(m for _,_,m,_ in rows)))
