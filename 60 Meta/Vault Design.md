---
type: meta
title: Vault Design
status: approved 2026-11-11; phases 1 to 4 built 2026-11-12
created: 2026-11-11
---

# Vault Design — Avatar: Into the Mists

This note is the agreed design for turning this folder into AITM's second brain. Millie approved the three sections in chat on 2026-11-11. Nothing in the vault is restructured until she approves this written version.

## Purpose

The vault is the single home of AITM canon. Millie writes and edits here. The Claude project is downstream: when it needs updating, documents are compiled from the vault and pushed up. Success means she can find anything, see how everything connects, and add to it herself without holding the whole AU in her head.

## Decisions

| Question | Decision |
|---|---|
| Depth | Full atomization: one note per character, group, place, arc and scene |
| Source of truth | Obsidian. The two "Aitm project folder sync" scheduled tasks must be paused before the migration starts |
| Language of structure | English folder and property names; note content stays in the language it was written in |

## The three tools

- **Folders** say what kind of thing a note is.
- **Links** say what it is connected to.
- **Properties** hold facts to sort and filter by.

## Folders

```
Into the Mists/
├── 00 Home/         Home, index notes, Canon Rules, Open Questions, How This Vault Works
├── 10 Characters/   one note per character, flat
├── 20 Groups/       families, factions, clans
├── 30 World/        places, customs, rituals, technology
├── 40 Story/        Timeline.md, Eras/, Arcs/, Scenes/
├── 50 Language/     Na'vi references, kept whole
├── 60 Meta/         style guide, TØP overlay, source-series mapping, this design
├── 90 Sources/      PDFs
├── 99 Archive/      every original file, untouched, plus _backup_2026-11-01
└── _templates/      Character, Group, Place, Arc, Scene
```

## Note types

### Character (`10 Characters/`)

File name is the Na'vi name alone (`Sänrri.md`); human characters use the name they go by (`Chuchu.md`). Apostrophes in file names are always the straight `'`. Every other name goes in `aliases`.

```yaml
type: character
aliases: []
navi_name:
source_character:
source_series:
family:            # link to a Groups note
groups: []         # links to Groups notes
role:
ikran:
birthday:
age:
mbti:
status:
canon: confirmed
```

Body sections, in order, each present only if source text exists for it: Profile, Relationships, Name forms, Sayings, Songs, Notes. A dual entry in the sources (Tìmeyo and Kerevi; Nì'syu/'Awll; Txewan/Txewì) becomes one note with aliases unless Millie rules otherwise; these are listed in Open Questions.

### Group (`20 Groups/`)

`type: group`, `kind: family | faction | clan | unit`, `source_series`. Holds the group's description; its member list is a live table built from character properties.

### Place and culture (`30 World/`)

`type: place | custom | technology`. Built from the Worldbuilding Reference, Geography of the Lake, Earth House Mark, Astikasya Yellow, and Lore and Traditions.

### Era, Arc, Scene (`40 Story/`)

```yaml
type: scene
title:
arc:
era:
characters: []
song:
language: en | es
translation_of:
status: draft | final
canon: confirmed | tentative | discarded
```

Eras: Prologue, The Dreamwalker Years, Blurryface, Scaled and Icy, Overcompensate, Clancy, Breach (from the Story Timeline). Scene prose is not edited and gets no inline links; connections live in properties.

### Language (`50 Language/`)

Accent Reference, Reef Na'vi Reference, Na'viteri Notes, Reykunyu lexicon, Name Audit, Name Fixes, Name Case Forms, Nine Spears in Na'vi, Proverbs and Familiar Terms stay whole. Character notes link to their own sections of these.

## Home

`00 Home/Home.md` links to: Cast (table of all characters), Story (timeline down to scenes), Rulings (everything `canon: tentative` plus Open Questions), Language, and How This Vault Works (the manual: how to add a character, file a scene, mark something discarded).

## Rules of the migration

1. **Nothing is deleted.** Every original is preserved in `99 Archive/`.
2. **Text moves verbatim.** Profiles and scenes are split and filed, never rewritten or summarized. An empty field stays empty.
3. **Conflicts go to Millie.** Spellings already settled in Name Fixes are applied. Anything else is recorded in Open Questions with both versions and their source files.
4. **No Na'vi is composed.** Existing Na'vi text is carried as written.
5. **Repairs allowed:** broken encoding (`NgotxÃ¬` → `Ngotxì`), stray escape characters (`\!`, `\-`), curly apostrophes in names.

## Sources to bring in

- The 28 notes in the vault root and 11 in `claude/`.
- From `_backup_2026-11-01`: AITM_00_Master_List, AITM_06_Other_Characters_and_Lore, 05_Lore_and_Traditions, Into_the_Mists_AU_Analysis.
- From the Claude project only: Scene Paladin Strait, Scene Overcompensate (EN and ES), Scene City Walls, Anti-Slop Style Guide, Navi Lexicon Reykunyu.
- `WELCOME BACK TO TRENCH.docx`, converted to a note; the Word file is archived.

Where the same character appears in several sources, the newest `AITM_` text is the base, and any passage that exists only in another version is kept under Notes with its source named.

## Phases

1. **Safety copy.** Copy every file into `99 Archive/` and verify byte for byte.
2. **Pilot.** Folders, templates, Home, and the nine Samaya characters. Millie reviews before anything else is built.
3. **Cast and groups.** Remaining characters and all group notes.
4. **World, story, language.**
5. **Proof.** A script confirms that every paragraph of every original exists in the new vault, no link is broken, no broken encoding remains, and every character has the required properties. The report lists anything unplaced.

## Open at time of writing

- The two sync tasks are still active; Millie pauses them.
- Mawpay's source character is Mirei Yahata (settled). The older Master List still says "Mirei Shiina"; the settled version is used and the old one stays only in the archive.
