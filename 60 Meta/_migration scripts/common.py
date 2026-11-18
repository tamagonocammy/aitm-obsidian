import re, os, io, json, hashlib
from pathlib import Path
BUILD = str(Path(__file__).resolve().parent)
V = str(Path(BUILD).parent.parent)
MANIFEST = os.path.join(BUILD, 'manifest.json')
SRC = os.path.join(V, '99 Archive', '2026-11-11 originals')
BK = os.path.join(SRC, '_backup_2026-11-01')

NAME_FIXES = [("Ean'tu","Eantu"),("Mowpay","Mawpay"),("Kxurryo","Kxuryo"),("Äwsun","Awsun"),
              ("Loxtu","Lokxtu"),("Txayo'itu","Mawnä'itu"),("Lì'fya Astikasyaä","Lì'fya Astikasyayä")]

def demojibake(s):
    def fix(m):
        t = m.group(0)
        for enc in ('cp1252','latin-1'):
            try: return t.encode(enc).decode('utf-8')
            except Exception: pass
        return t
    return re.sub(r'[^\x00-\x7f]+', fix, s)

def clean(s, mojibake=False):
    if mojibake: s = demojibake(s)
    s = s.replace('\u200b','')
    s = re.sub(r'\\([!\-.#_()\[\]*~>+=&|])', r'\1', s)       # stray markdown escapes
    s = re.sub(r"(?<=\w)[\u2019\u2018](?=\w)", "'", s) if False else s
    s = s.replace('Na\u2019vi', "Na'vi")
    for a,b in NAME_FIXES: s = s.replace(a,b)
    return s

def read(rel, base=SRC, mojibake=False):
    return clean(io.open(os.path.join(base, rel), encoding='utf-8').read(), mojibake)

def fix_name_apos(s, names):
    for n in names:
        if "'" in n:
            for c in ('\u2019','\u2018'):
                s = s.replace(n.replace("'", c), n)
    return s

def sections(text, level=3):
    """split by heading of given level -> list of (heading, body); stops body at same/higher heading"""
    pat = re.compile(r'^(#{1,%d}) +(.+?)\s*$' % level, re.M)
    out=[]; ms=list(pat.finditer(text))
    for i,m in enumerate(ms):
        if len(m.group(1))!=level: continue
        end = ms[i+1].start() if i+1<len(ms) else len(text)
        out.append((m.group(2).strip().strip('*').strip(), text[m.end():end].strip('\n')))
    return out

def yq(v):
    return '"' + str(v).replace('\\','\\\\').replace('"','\\"') + '"'

def frontmatter(d):
    L=['---']
    for k,v in d.items():
        if v is None or v=='' or v==[]: continue
        if isinstance(v, list):
            L.append(f'{k}:'); L += [f'  - {yq(x)}' for x in v]
        else: L.append(f'{k}: {yq(v)}')
    L.append('---'); return '\n'.join(L)+'\n'

def guarded_write(rel, content, manifest):
    """Write generated output only if the existing bytes match its manifest."""
    root = Path(V).resolve()
    p = (root / rel).resolve()
    if not p.is_relative_to(root) or p.relative_to(root).parts[0] == '99 Archive':
        raise ValueError('Refusing write outside the vault or into originals: ' + rel)
    data = content.encode('utf-8')
    if p.exists():
        current = p.read_bytes()
        if current == data:
            return True
        if manifest.get(rel) != hashlib.sha256(current).hexdigest():
            print('SKIP: manually edited or untracked file:', rel)
            return False
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    manifest[rel] = hashlib.sha256(data).hexdigest()
    return True


def write(rel, content, overwrite=True):
    p = Path(V) / rel
    if p.exists() and not overwrite:
        return False
    manifest = json.loads(Path(MANIFEST).read_text()) if Path(MANIFEST).exists() else {}
    changed = guarded_write(rel, content.rstrip('\n') + '\n', manifest)
    if changed:
        Path(MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=0))
    return changed

# ---------- name registry ----------
PROFILE_FILES = [('AITM_02_Samaya_Family_Profiles.md',SRC),('AITM_03_Haykxa_Family_Profiles.md',SRC),
  ('AITM_04_Ngotxi_and_Korhe_Family_Profiles.md',SRC),('AITM_05_Factions_Profiles.md',SRC),
  ('AITM_07_The_Flying_Troupe.md',SRC),('Local_Only_Core/AITM_06_Other_Characters_and_Lore.md',BK),
  ('04_Character_Profiles_Groups_and_Others.md',SRC)]
SPECIAL = {  # heading prefix -> (note name, extra aliases)
  'Tìmeyo (Mutsumi Togawa) and Kerevi': ('Tìmeyo',['Kerevi']),
  "Nì'syu/": ("Nì'syu",["'Awll"]),
  'Txewan/Txewì': ('Txewan',['Txewì']),
  'Nika Nanaura-Fardin': ('Nika',[]), 'Chuatury': ('Chuchu',[]), 'Aliya Mahvash': ('Aliya',[]),
  'Cpl. Kobeni': ('Kobeni',[]), 'Cpl. Miri Sugo': ('Miri Sugo',[]),
}
def registry():
    link = {}   # shown text -> note name
    for f,b in PROFILE_FILES:
        t = read(f,b).replace('\u2018',"'").replace('\u2019',"'")
        for h,_ in sections(t,3):
            if h.endswith('Family'): continue
            name=None
            for k,(n,al) in SPECIAL.items():
                if h.startswith(k): name=n; [link.setdefault(a,n) for a in al]
            if not name: name = h.split(' (')[0].strip()
            link.setdefault(name,name)
    for n in ['Ivan','Sua','Mizi','Hyuna','Luka']: link.setdefault(n,n)
    return link

def linkify(text, link, self_name=None):
    names = sorted(link, key=len, reverse=True)
    pat = re.compile(r"(?<![\w\[|'])(" + '|'.join(re.escape(n) for n in names) + r")(?!\w|'\w|\])")
    def rep(m):
        shown=m.group(1); tgt=link[shown]
        if tgt==self_name: return shown
        return f'[[{tgt}]]' if tgt==shown else f'[[{tgt}|{shown}]]'
    return pat.sub(rep, text)
