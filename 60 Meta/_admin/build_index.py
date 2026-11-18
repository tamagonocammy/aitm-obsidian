#!/usr/bin/env python3
"""Rebuild administrative indexes. Run with _admin/.venv/bin/python from any directory."""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADMIN = Path('60 Meta/_admin')
QUESTION_INDEX = ADMIN / 'Open Questions Index.md'


def load_yaml():
    try:
        import yaml
    except ImportError:
        raise SystemExit('PyYAML is required; use 60 Meta/_admin/.venv/bin/python. No output written.')
    return yaml


def build(root=ROOT, check=False):
    yaml = load_yaml()
    root = Path(root)
    # Only active note folders; exclude generated content and maintenance internals.
    paths = sorted(p for folder in root.iterdir()
                   if folder.is_dir() and folder.name[:2] in ('00', '10', '20', '30', '40', '50', '60')
                   for p in folder.rglob('*.md')
                   if '_migration scripts' not in p.parts and '.venv' not in p.parts)
    texts = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8') for p in paths
             if p.relative_to(root) != QUESTION_INDEX}
    opens = {}
    for p, text in texts.items():
        questions = [line[6:] for line in text.splitlines() if line.startswith('- [ ]')]
        if questions:
            opens[p] = questions
    count = sum(map(len, opens.values()))
    today = datetime.date.today().isoformat()
    out = ['---', 'type: "meta"', '---',
           'Generated list of every unticked question in the vault, grouped by note. Rebuilt by `60 Meta/_admin/build_index.py`; do not edit by hand. Tick questions on the note they live on.', '',
           f'Total open: **{count}** across {len(opens)} notes (built {today}).', '']
    for p in sorted(opens, key=lambda k: (-len(opens[k]), k)):
        out.append(f'## [[{Path(p).stem}]] ({len(opens[p])})')
        out.extend('- ' + line.replace('[[', '').replace(']]', '')[:200] for line in opens[p])
        out.append('')
    texts[QUESTION_INDEX.as_posix()] = '\n'.join(out)
    idx, titles = {}, {}
    for p, text in sorted(texts.items()):
        fm = {}
        if text.startswith('---\n'):
            m = re.match(r'---\n(.*?)\n---(?:\n|$)', text, re.S)
            if not m:
                raise ValueError('Unterminated frontmatter: ' + p)
            fm = yaml.safe_load(m.group(1)) or {}
            if not isinstance(fm, dict):
                raise ValueError('Frontmatter must be a mapping: ' + p)
        aliases = fm.get('aliases') or []
        if not isinstance(aliases, list):
            raise ValueError('Aliases must be a list: ' + p)
        body = re.sub(r'```.*?```', '', text, flags=re.S)
        links = sorted(set(x.split('#')[0] for x in re.findall(r'\[\[([^\]|]+)', body)))
        idx[p] = dict(title=Path(p).stem, type=fm.get('type'), aliases=aliases,
                      canon=fm.get('canon'), sha=hashlib.sha256(text.encode()).hexdigest()[:16],
                      bytes=len(text.encode()), links=links,
                      open=sum(line.startswith('- [ ]') for line in text.splitlines()))
        for title in [Path(p).stem, *aliases]:
            titles.setdefault(str(title), p)
    for folder in root.iterdir():
        if folder.is_dir() and folder.name[:2] in ('00', '10', '20', '30', '40', '50', '60'):
            for p in folder.rglob('*.base'):
                titles[p.name] = str(p)
    broken = sorted({(p, link) for p, d in idx.items() for link in d['links']
                     if link and link not in titles})
    if not check:
        (root / QUESTION_INDEX).write_text(texts[QUESTION_INDEX.as_posix()], encoding='utf-8')
        (root / ADMIN / 'index.json').write_text(json.dumps({'built': today, 'notes': idx},
                                                         ensure_ascii=False, indent=0), encoding='utf-8')
    print(f'{len(idx)} notes, {count} unchecked items, {len(broken)} unresolved note links')
    for p, link in broken[:20]:
        print('  unresolved:', p, '->', link)
    return idx, broken


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check without writing generated indexes')
    args = parser.parse_args()
    _, broken = build(check=args.check)
    raise SystemExit(bool(broken))
