#!/usr/bin/env python3
"""Build NotebookLM / Gemini bundles from the AITM vault.

Read-only on the vault: it only reads .md notes and writes bundle files to
the output folder (default ./bundles). Canon only: _inbox, 99 Archive,
_templates, 60 Meta and .base files are never included.
Usage: python3 tools/notebooklm/build_bundles.py [vault_root] [out_dir]
"""
import re, sys, datetime
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
out = Path(sys.argv[2] if len(sys.argv) > 2 else root / "bundles").resolve()
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("AITM_*.md"):
    old.unlink()

LAWS = """# TOP RULE: THE THREE LAWS OF EYWA (overrides everything below)

In the vault and in every Na'vi scene, the Na'vi of this AU never:
1. set stone upon stone (no stacked masonry),
2. use the turning wheel (no wheels, pulleys or gears),
3. use the metals of the ground (no mined or smelted metal).

Check every draft for wheels, pulleys, metal and stacked masonry. Only Millie can change this rule.
"""

HEADER = """> AITM canon bundle. Source of truth is Millie's Obsidian vault "Into the Mists"; this file is a read-only copy.
> Built {date}. Contains approved canon only: no _inbox proposals, no archive, no drafts.
> Rules that always apply: Na'vi have no written language; Na'vi never use contractions (Sänrri neither; humans, Recoms and avatar drivers do); never invent Na'vi words; use Na'vi names, never the original anime names. If something is not in these files, say so instead of inventing it.

"""

def clean(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return text.strip()

def notes(*globs, skip=()):
    files = []
    for g in globs:
        files += sorted((root / g[0]).glob(g[1]))
    return [f for f in files if f.name not in skip and not f.name.startswith(".")]

def fm_title(path):
    return path.stem

def write(name, title, files, extra_head=""):
    body = [f"# {title}\n", LAWS, HEADER.format(date=datetime.date.today().isoformat()), extra_head]
    toc = "## Contents\n" + "\n".join(f"- {f.stem}" for f in files) + "\n"
    body.append(toc)
    for f in files:
        body.append(f"\n\n---\n\n# {f.stem}\n\n" + clean(f.read_text(encoding="utf-8")))
    text = "\n".join(body) + "\n"
    (out / name).write_text(text, encoding="utf-8")
    print(f"{name}: {len(files)} notes, {len(text)//1000} KB")

def split(files, n):
    size = sum(f.stat().st_size for f in files)
    target, parts, cur, acc = size / n, [], [], 0
    for f in files:
        cur.append(f); acc += f.stat().st_size
        if acc >= target and len(parts) < n - 1:
            parts.append(cur); cur, acc = [], 0
    parts.append(cur)
    return parts

# 1 Rules, rulings, index
write("AITM_1_Canon_Rules_and_Rulings.md", "AITM 1: Canon Rules, Rulings Log, Index",
      notes(("00 Home", "INDEX.md"), ("00 Home", "Canon Rules.md"), ("00 Home", "Rulings Log.md"),
            ("00 Home", "Open Questions.md"), ("00 Home", "How This Vault Works.md")))

# 2-4 Characters (split alphabetically so each file stays easy for NotebookLM)
chars = notes(("10 Characters", "*.md"))
for i, part in enumerate(split(chars, 3), 1):
    write(f"AITM_2{'abc'[i-1]}_Characters.md",
          f"AITM 2{'abc'[i-1]}: Characters ({part[0].stem} to {part[-1].stem})", part)

# 3 Groups
write("AITM_3_Groups_and_Relationships.md", "AITM 3: Groups, Families and Relationships", notes(("20 Groups", "*.md")))

# 4 World + Language
write("AITM_4_World_and_Language.md", "AITM 4: World, Customs and Na'vi Language Notes",
      notes(("30 World", "*.md"), ("50 Language", "*.md")))

# 5 Story
write("AITM_5_Story_Timeline_Arcs.md", "AITM 5: Timeline, Eras and Arcs",
      notes(("40 Story", "Timeline.md"), ("40 Story/Eras", "*.md"), ("40 Story/Arcs", "*.md")))

# 6 Scenes (written scenes, kept apart from canon facts)
write("AITM_6_Scenes.md", "AITM 6: Written Scenes", notes(("40 Story/Scenes", "*.md")),
      "> These are written scenes marked draft in the vault (canon: confirmed). Treat them as story text, not as a rulings list.\n")
