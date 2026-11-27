"""AITM canon check: read-only lint for the lore and style rules in Canon Rules.

proof.py checks structure (links, headings, encoding against the archive).
This script checks canon: the Three Laws of Eywa, Na'vi contractions,
Na'vi reading/writing, banned style words, retired spellings, and
frontmatter hygiene. It never writes into the vault unless --out is given.

The rule lists are read from the vault itself (Canon Rules, Name Fixes to
Apply), so editing those notes changes what this script checks.

Usage, from the vault root:
  "60 Meta/_admin/.venv/bin/python" -B "60 Meta/_admin/canon_check.py"
  ... canon_check.py --notes "40 Story/Scenes/Kava with the Nine.md"
  ... canon_check.py --only laws,contractions
  ... canon_check.py --out "60 Meta/_admin/reports/canon-check.md"
  ... canon_check.py --format json

Exit status: 0 = no errors (review items may exist), 1 = errors found,
2 = bad usage. Errors are near-certain problems; "review" items are leads
for a human (or agent) to judge, never automatic fixes.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

EXCLUDED_DIRS = ('99 Archive', '90 Sources', '60 Meta/_migration scripts',
                 '.obsidian', '_templates', 'catppuccin-bandito-mocha', '.venv')
LORE_DIRS = ('10 Characters', '20 Groups', '30 World', '40 Story', '_inbox')
STORY_DIRS = ('40 Story', '_inbox')
CANON_VALUES = {'confirmed', 'tentative', 'discarded'}
FOLDER_TYPES = {'10 Characters': {'character'}, '40 Story/Scenes': {'scene'},
                '40 Story/Arcs': {'arc'}}
CHECKS = ('laws', 'contractions', 'writing', 'style', 'spelling', 'encoding',
          'frontmatter', 'inbox')

# The Three Laws of Eywa (Rulings Log, 2026-11-26). Hearth stones, levers,
# ropes, slings, sleds and counterweights are allowed, so they are not listed.
# Words with a common harmless sense (gear, nails, quarry as prey, forge as a
# metaphor, eje as a spear shaft) are left out or narrowed on purpose.
LAW_TERMS = {
    'wheel': r'wheels?|wheeled|pulleys?|cogwheels?|cogs|carts?|wagons?|axles?|'
             r'wheelbarrows?|spinning wheels?|'
             r'ruedas?|poleas?|engranajes?|carretas?|carretillas?',
    'stone': r'bricks?|mortar|masonry|stonework|stone walls?|stone houses?|'
             r'stone buildings?|stone upon stone|mining|mined|mines?\b(?= (?:for|of|in))|'
             r'ladrillos?|mampostería|piedra sobre piedra|muros? de piedra|minería',
    'metal': r'metal|metals|metallic|iron(?! (?:self-control|will|grip|discipline|resolve))|'
             r'steel|bronze|copper|blacksmith|smithy|anvil|metal ore|'
             r'(?:a|the) forge|forg\w* (?:\w+ ){0,2}(?:tools?|weapons?|blades?|knives|knife|'
             r'spearheads?|arrowheads?|metal)|'
             r'hierro|acero|bronce|cobre|forja|herrer[oa]|yunque',
}
MINING_CONTEXT_OK = re.compile(r'\bRDA\b|Sky People|Outpost', re.IGNORECASE)
WRITING_TERMS = (r'(?<!yet )wr(?:ite|ites|ote|itten|iting)|letters? (?:to|from)|scrolls?|ink|'
                 r'notebooks?|journals?|books?|alphabet|'
                 r'read(?:s|ing)? (?:the |her |his |their )?(?:words?|letters?|marks|'
                 r'scrolls?|notes?|page)|'
                 r'escrib\w*|escrit[oa]s?|tinta|libros?|cuadernos?')
CONTRACTION = re.compile(
    r"\b(?:\w+n[’']t|(?:I|you|we|they|he|she|it|that|what|there|here|who|where|how|"
    r"let)[’']s|(?:I|you|we|they|he|she|it|that|there)[’'](?:ll|re|ve|d|m))\b"
    r"|\bain[’']t\b"
    r"|\b[A-Z][\w'’]*[’']s (?=(?:going|gonna|not|been|got|coming|getting|always|never|"
    r"just|still|already|right|okay|fine|the|a|an)\b)", re.IGNORECASE)
SPEECH_VERBS = (r'said|says|asked|asks|added|replied|whispered|shouted|roared|muttered|'
                r'called|cried|laughed|snapped|answered|murmured|admitted|told|dijo|preguntó|'
                r'gritó|susurró|respondió')
QUOTE = re.compile(r'"([^"\n]{2,})"|“([^”\n]{2,})”')
META_PARA = re.compile(r'^(?:\[!|- \[[ x]\]|\||Millie\b|\*\*Ruled|\(Millie|Supporting reading)')
INLINE_CODE = re.compile(r'`[^`]*`')
MOJIBAKE = re.compile(r'Ã[¡-ÿ]|Â[ -¿]|â€|Å«')
WIKILINK = re.compile(r'\[\[([^\]|#]+)')


class Note:
    def __init__(self, path, rel, text):
        self.path, self.rel, self.text = path, rel, text
        self.meta, self.body, self.body_start = split_frontmatter(text)

    def under(self, *dirs):
        return any(self.rel == d or self.rel.startswith(d + '/') for d in dirs)


def split_frontmatter(text):
    if not text.startswith('---\n'):
        return {}, text, 1
    end = text.find('\n---', 4)
    if end == -1:
        return {}, text, 1
    raw = text[4:end]
    try:
        import yaml
        meta = yaml.safe_load(raw) or {}
    except ImportError:
        meta = simple_yaml(raw)
    except Exception as exc:
        meta = {'__error__': str(exc)}
    body_start = text[:end + 4].count('\n') + 2
    return (meta if isinstance(meta, dict) else {}), text[end + 4:].lstrip('\n'), body_start


def simple_yaml(raw):
    """Fallback for plain `key: value` and `  - item` lists (no PyYAML)."""
    meta, key = {}, None
    for line in raw.splitlines():
        m = re.match(r'^([A-Za-z_][\w-]*):\s*(.*)$', line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            meta[key] = [] if val == '' else unquote(val)
        elif key and re.match(r'^\s+-\s+', line):
            if not isinstance(meta.get(key), list):
                meta[key] = []
            meta[key].append(unquote(re.sub(r'^\s+-\s+', '', line)))
    return meta


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
        return v[1:-1]
    if v.startswith('[') and v.endswith(']'):
        return [unquote(x) for x in v[1:-1].split(',') if x.strip()]
    return v


def as_list(v):
    if v is None or v == '':
        return []
    return v if isinstance(v, list) else [v]


def prose_paragraphs(note):
    """Yield (line_number, paragraph) for live prose.

    Skips code blocks (Bases), callouts that keep earlier versions
    (> [!quote]-), and HTML comments, so preserved original wording is
    never flagged.
    """
    lines = note.body.splitlines()
    start = note.body_start
    para, para_line, in_code, in_old = [], None, False, False
    for i, line in enumerate(lines):
        n = start + i
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r'^>\s*\[!quote\]-', s):
            in_old = True
            continue
        if in_old:
            if s.startswith('>'):
                continue
            in_old = False
        if s == '' or s.startswith('#') or s == '---':
            if para:
                yield para_line, ' '.join(para)
            para, para_line = [], None
            continue
        if para_line is None:
            para_line = n
        para.append(s.lstrip('> ').strip())
    if para:
        yield para_line, ' '.join(para)


def snippet(text, start, end, width=70):
    a, b = max(0, start - width), min(len(text), end + width)
    return ('…' if a else '') + text[a:b].strip() + ('…' if b < len(text) else '')


def load_notes(root, only_paths=None):
    notes = []
    for p in sorted(root.rglob('*.md')):
        rel = p.relative_to(root).as_posix()
        if any(rel == d or rel.startswith(d + '/') or ('/' + d + '/') in rel
               for d in EXCLUDED_DIRS):
            continue
        notes.append(Note(p, rel, p.read_text(encoding='utf-8', errors='replace')))
    if only_paths:
        wanted = {Path(x).as_posix().lstrip('./') for x in only_paths}
        missing = wanted - {n.rel for n in notes}
        if missing:
            raise SystemExit(f'canon_check: not found or excluded: {", ".join(sorted(missing))}')
        return notes, [n for n in notes if n.rel in wanted]
    return notes, notes


def build_cast(notes):
    """Map every name and alias to (canonical name, is_sky_person).

    Sky People (humans, Recoms, avatar drivers) are the characters with no
    navi_name; they may use contractions and may read and write.
    """
    cast = {}
    for n in notes:
        if not n.rel.startswith('10 Characters/'):
            continue
        stem = n.path.stem
        sky = not str(n.meta.get('navi_name') or '').strip()
        names = {stem, *[str(a) for a in as_list(n.meta.get('aliases'))]}
        nn = str(n.meta.get('navi_name') or '').strip()
        if nn:
            names.add(nn.split(' te ')[0].split('/')[0])
        for name in names:
            name = name.strip()
            if len(name) >= 3:
                cast[name] = (stem, sky)
    return cast


def cast_regex(cast):
    names = sorted(cast, key=len, reverse=True)
    return re.compile(r"(?<![\w'’])(" + '|'.join(re.escape(x) for x in names) + r")(?![\w])")


def read_rules(root):
    """Pull banned words/patterns from Canon Rules and old spellings from Name Fixes."""
    words, patterns, fixes = [], [], {}
    rules = root / '00 Home/Canon Rules.md'
    if rules.exists():
        for line in rules.read_text(encoding='utf-8').splitlines():
            if line.startswith('- Banned words:'):
                for w in line.split(':', 1)[1].strip().rstrip('.').split(','):
                    w = w.strip().strip('"')
                    soft = '(' in w
                    w = re.sub(r'\s*\(.*?\)', '', w).strip()
                    if w:
                        words.append((w, soft))
            elif line.startswith('- Banned patterns:'):
                for chunk in line.split(':', 1)[1].split(';'):
                    for alt in re.findall(r'"([^"]+)"', chunk):
                        alt = alt.replace('...', '').replace('…', '').rstrip('.?:').strip()
                        pieces = [x.strip() for x in alt.split(' / ')]
                        head = pieces[0].split(' ')[0]
                        for i, piece in enumerate(pieces):
                            phrase = piece if i == 0 else f'{head} {piece}'
                            pat = re.escape(phrase).replace('X', r'[^,.;]+?').replace('Y', r'[^,.;]+?')
                            # AI-voice openers count at a sentence start only
                            if phrase[0].isupper():
                                pat = r'(?:^|(?<=[.!?:]\s)|(?<=[.!?:]\*\*\s))' + pat
                            patterns.append((phrase, pat))
    fx = root / '50 Language/Name Fixes to Apply.md'
    if fx.exists():
        for line in fx.read_text(encoding='utf-8').splitlines():
            m = re.match(r'^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`', line)
            if m and '(' not in m.group(1):
                fixes[m.group(1)] = m.group(2)
    return words, patterns, fixes


def run(root, only_paths=None, checks=CHECKS):
    all_notes, notes = load_notes(root, only_paths)
    cast = build_cast(all_notes)
    names_re = cast_regex(cast) if cast else None
    words, patterns, fixes = read_rules(root)
    known = {n.path.stem for n in all_notes}
    for n in all_notes:
        known.update(str(a) for a in as_list(n.meta.get('aliases')))
    out = []

    def add(level, check, note, line, msg, text=''):
        out.append({'level': level, 'check': check, 'note': note.rel,
                    'line': line, 'message': msg, 'text': text})

    def who(paragraphs, idx):
        """Characters named in this paragraph, else the two before it."""
        for back in range(0, 3):
            if idx - back < 0 or not names_re:
                break
            found = {cast[m][0]: cast[m][1] for m in names_re.findall(paragraphs[idx - back][1])}
            if found:
                return found
        return {}

    def speaker(p, q):
        """Name attached to this quote by a speech tag, if any."""
        if not names_re:
            return None
        after, before = p[q.end():q.end() + 60], p[max(0, q.start() - 60):q.start()]
        for text, rx in ((after, r'^[\s,.!?*]*(?:(\S.*?) (?:' + SPEECH_VERBS + r')|(?:'
                          + SPEECH_VERBS + r') (\S.*?))\b'),
                         (before, r'(\S+(?: \S+)?) (?:' + SPEECH_VERBS + r')[^"“]*[:,]?\s*\**$')):
            m = re.search(rx, text)
            if m:
                found = names_re.findall(m.group(0))
                if found:
                    return cast[found[0]]
        return None

    for note in notes:
        paras = [(ln, p) for ln, p in prose_paragraphs(note) if not META_PARA.match(p)]
        lore = note.under(*LORE_DIRS)
        story = note.under(*STORY_DIRS)

        if 'laws' in checks and lore:
            for law, terms in LAW_TERMS.items():
                rx = re.compile(r'\b(?:' + terms + r')\b', re.IGNORECASE)
                for i, (ln, p) in enumerate(paras):
                    for m in rx.finditer(p):
                        if law == 'stone' and MINING_CONTEXT_OK.search(p):
                            continue  # RDA mining is the enemy's, not a Law break
                        people = who(paras, i)
                        if people and all(people.values()):
                            continue  # only Sky People here: their tools are fine
                        tag = ', '.join(sorted(people)) or 'no named character'
                        add('review', 'laws', note, ln,
                            f'Three Laws ({law}): "{m.group(0)}" — {tag}',
                            snippet(p, m.start(), m.end()))

        if 'contractions' in checks and story:
            for i, (ln, p) in enumerate(paras):
                for q in QUOTE.finditer(p):
                    said = q.group(1) or q.group(2)
                    c = CONTRACTION.search(said)
                    if not c:
                        continue
                    spk = speaker(p, q)
                    if spk:
                        if spk[1]:
                            continue  # a Sky Person said it: contractions are fine
                        level = 'error' if not note.rel.startswith('_inbox/') else 'review'
                        tag = f'spoken by {spk[0]}'
                    else:
                        people = who(paras, i)
                        navi = sorted(k for k, sky in people.items() if not sky)
                        if people and not navi:
                            continue
                        level = 'review'
                        if len(people) == 1 and navi:
                            tag = f'probably {navi[0]} (only character in the paragraph)'
                        else:
                            tag = ('speaker unclear; Na\'vi nearby: ' + ', '.join(navi)) if navi \
                                else 'speaker unclear'
                    add(level, 'contractions', note, ln,
                        f'Contraction "{c.group(0).strip()}" in dialogue — {tag}', said[:160])

        if 'writing' in checks and story:
            rx = re.compile(r'\b(?:' + WRITING_TERMS + r')', re.IGNORECASE)
            for i, (ln, p) in enumerate(paras):
                for m in rx.finditer(p):
                    people = who(paras, i)
                    navi = sorted(k for k, sky in people.items() if not sky)
                    if not navi:
                        continue
                    add('review', 'writing', note, ln,
                        f'Reading/writing "{m.group(0)}" near Na\'vi: {", ".join(navi)}',
                        snippet(p, m.start(), m.end()))

        if 'style' in checks and lore:
            for ln, p in paras:
                for w, soft in words:
                    for m in re.finditer(r'\b' + re.escape(w) + r'\b', p, re.IGNORECASE):
                        add('review', 'style', note, ln,
                            f'Banned word "{w}"' + (' (check the sense)' if soft else ''),
                            snippet(p, m.start(), m.end()))
                for label, pat in patterns:
                    for m in re.finditer(pat, p):
                        add('review', 'style', note, ln, f'Banned pattern "{label}"',
                            snippet(p, m.start(), m.end()))

        if 'spelling' in checks and not note.rel.startswith('50 Language/'):
            for ln, p in paras:
                present = [o for o in fixes if re.search(r"(?<![\w'])" + re.escape(o) + r"(?![\w])", p)]
                if len(present) >= 3:
                    continue  # a paragraph listing the retired spellings is about them
                for old, new in fixes.items():
                    for m in re.finditer(r"(?<![\w'])" + re.escape(old) + r"(?![\w])", p):
                        add('error', 'spelling', note, ln,
                            f'Retired spelling "{old}" → "{new}"', snippet(p, m.start(), m.end()))

        if 'encoding' in checks:
            for i, line in enumerate(note.text.splitlines(), 1):
                m = MOJIBAKE.search(INLINE_CODE.sub('', line))
                if m:
                    add('error', 'encoding', note, i, f'Garbled accent "{m.group(0)}"',
                        line.strip()[:120])

        if 'frontmatter' in checks and note.under(*LORE_DIRS):
            meta = note.meta
            if '__error__' in meta:
                add('error', 'frontmatter', note, 1, 'Frontmatter does not parse',
                    meta['__error__'][:120])
            canon = meta.get('canon')
            allowed = CANON_VALUES | ({'proposal'} if note.rel.startswith('_inbox/') else set())
            if note.rel.startswith('_inbox/') and str(canon) == 'proposed':
                add('review', 'frontmatter', note, 1,
                    'canon is "proposed"; the other inbox notes say "proposal"')
            elif canon not in (None, '') and str(canon) not in allowed:
                add('error', 'frontmatter', note, 1,
                    f'canon is "{canon}"; expected one of {sorted(CANON_VALUES)}')
            for folder, types in FOLDER_TYPES.items():
                if note.rel.startswith(folder + '/') and meta and meta.get('type') not in types:
                    add('error', 'frontmatter', note, 1,
                        f'type is "{meta.get("type")}"; notes in {folder} use {sorted(types)}')
            for field in ('characters', 'family', 'groups', 'arc', 'era'):
                for v in as_list(meta.get(field)):
                    for target in WIKILINK.findall(str(v)):
                        if target.strip() not in known:
                            add('error', 'frontmatter', note, 1,
                                f'{field} links to [[{target}]], which has no note or alias')

        if 'inbox' in checks and note.rel.startswith('_inbox/'):
            if not re.match(r'^\d{4}-\d{2}-\d{2} ', note.path.name):
                add('error', 'inbox', note, 1, 'Inbox notes start with a date: "YYYY-MM-DD Title"')

    return out


def render_md(findings, scanned):
    errors = [f for f in findings if f['level'] == 'error']
    reviews = [f for f in findings if f['level'] == 'review']
    lines = ['# AITM canon check', '',
             f'{scanned} notes scanned. **{len(errors)} errors**, {len(reviews)} items to review.',
             '', 'Errors are near-certain. Review items are leads: judge each one against',
             'the Rulings Log; nothing here is a ruling and nothing was changed.', '']
    for level, title in (('error', 'Errors'), ('review', 'To review')):
        group = [f for f in findings if f['level'] == level]
        if not group:
            continue
        lines += [f'## {title}', '']
        for check in CHECKS:
            items = [f for f in group if f['check'] == check]
            if not items:
                continue
            lines += [f'### {check} ({len(items)})', '']
            for f in items:
                lines.append(f'- `{f["note"]}:{f["line"]}` {f["message"]}')
                if f['text']:
                    lines.append(f'  > {f["text"]}')
            lines.append('')
    return '\n'.join(lines) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', default=str(ROOT), help='vault root (default: inferred)')
    ap.add_argument('--notes', nargs='+', help='only these notes (paths from the vault root)')
    ap.add_argument('--only', help='comma list of checks: ' + ','.join(CHECKS))
    ap.add_argument('--format', choices=('md', 'json'), default='md')
    ap.add_argument('--out', help='write the report here instead of stdout')
    a = ap.parse_args(argv)
    checks = CHECKS
    if a.only:
        checks = tuple(c.strip() for c in a.only.split(','))
        bad = set(checks) - set(CHECKS)
        if bad:
            ap.error(f'unknown checks: {", ".join(sorted(bad))}')
    root = Path(a.root).resolve()
    findings = run(root, a.notes, checks)
    scanned = len(a.notes) if a.notes else len(load_notes(root)[1])
    report = (json.dumps(findings, ensure_ascii=False, indent=2) + '\n'
              if a.format == 'json' else render_md(findings, scanned))
    if a.out:
        out = (root / a.out) if not Path(a.out).is_absolute() else Path(a.out)
        rel = out.resolve().as_posix()
        if '/99 Archive/' in rel:
            raise SystemExit('canon_check: refusing to write into 99 Archive')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding='utf-8')
    else:
        sys.stdout.write(report)
    return 1 if any(f['level'] == 'error' for f in findings) else 0


if __name__ == '__main__':
    sys.exit(main())
