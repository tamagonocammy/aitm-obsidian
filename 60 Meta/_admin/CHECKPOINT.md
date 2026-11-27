---
type: "meta"
---
# AITM vault checkpoint

**Last updated:** 2026-11-26 (evening), Claude (Bogotá): Mutsumi (Tìmeyo and Kerevi) ruled nonbinary and renamed Luey'itu; see the Mutsumi ruling in the Rulings Log. Earlier: 2026-11-26 (evening), Claude chat (Bogotá): added `_admin/canon_check.py` (read-only canon lint) with its tests and a first report; see "Canon check — 2026-11-26" below. No lore note was edited. Before that, 2026-11-26, Claude project thread (Bogotá): logged Millie's answers on climate, the mountain settlement, timing, the nantang, Yoko'fya's death and Choso in the Rulings Log (fruit and custom name settled later the same day: utumauti, somtskxe; Kaymi 2.82 m; Kaymi's Height line updated). Before that, 2026-11-24, Claude project thread (Bogotá): logged the approved inbox notes (Lost Cohort chart, Warming the Falls and scenes, Ketxe and Sänrri, Txomì) in the Rulings Log; open choices are listed there. Character notes not yet edited. Before that, 2026-11-23, Claude project thread (Bogotá): changed Sänrri's full name to Sänrri te Tsawtral Hikari'ite in the live notes and the Rulings Log, then pushed the change to a branch of the GitHub backup. Before that, 2026-11-22, Claude project thread (Bogotá): added two inbox proposals (warm platform custom and scenes). Before that, 2026-11-21, Claude project thread (Bogotá): recorded the children's personality rulings in the Rulings Log and the children's notes. Before that, 2026-11-18, Claude chat (Bogotá): added `00 Home/INDEX.md` for assistants and pushed the missing folders to GitHub. Before that, 2026-11-17, Claude chat (Bogotá): added the 2026-11-17 ruling on the Ke'awa origin the Anufi/Nesim mappings, and Eyfuwen in Tsu'lo's role. Before that, 2026-11-16: added the 2026-11-16 ruling on why the ANAKT exists (Ardmore, the Mangkwan play, Luka) and Luka's kuru (Tsu'lan brings it back). Previous: 2026-11-15, Narayra and the Falls thread. Previous: 2026-11-12, maintenance handoff. **Phase:** migration built and cleaned; now in maintenance and renovation.

## State

- 150 indexed Markdown notes: 147 outside `_admin`, plus 3 administrative notes. Last full validation (recorded before this maintenance pass): all original prose accounted for, no broken links, no broken encoding.
- Originals: `99 Archive/2026-11-11 originals/` (75 files, never edit).
- Canon authority, in order: Millie > [[Rulings Log]] > Timeline and Era notes > older documents.
- 142 unchecked items across 20 notes (rebuilt 2026-11-21); see [[Open Questions Index]]. These include review checklist items, not only unresolved canon questions. The previous checkpoint records that none blocks the remaining tasks.

## Tasks

Machine-readable list: `60 Meta/_admin/tasks.json`.

**Blocked on Millie:** six project-only documents must be downloaded from the Claude project into `_inbox` (the assistant cannot copy them without retyping).
**Pending:** renovate the Worldbuilding Reference; pair arcs with eras; refresh the Claude project from the vault; the hands-on walkthrough; one final validation.

## How to resume in a fresh session (any model)

1. Read this note, [[Operations Protocol]], [[Rulings Log]], and [[Canon Rules]], then `tasks.json`. Do not read the whole vault. Confirm a single writer before editing.
2. For canon, read [[Rulings Log]] only. For one arc or character, read that one note.
3. Rebuild indexes only when needed: `"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_admin/build_index.py"`. Add `--check` for no writes. Run these example commands from the vault root; the scripts locate the vault from their own paths, so absolute script paths also work from elsewhere.
4. Validate affected notes with `"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_migration scripts/proof.py" --notes "00 Home/Canon Rules.md"`. Use `--full` only for the final archival proof; it remains pending. See `_admin/README.txt` for dependencies and tests.
5. Before showing Millie any edit to a lore note (characters, groups, world, story, inbox), run the canon check on the notes you changed: `"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_admin/canon_check.py" --notes "<note path>"`. Fix or explain every error; list the review items for Millie. The check never edits anything, and its findings are leads, not rulings.
6. Do not rerun migration builders during maintenance. Their note writes now refuse to replace changed or untracked files using the local `manifest.json`; originals are write-protected by the shared helper. This is overwrite protection, not a concurrency lock. Prefer small direct edits and maintain one writer at a time.

## Rules that must not be broken

- Nothing is invented. A gap is an open question, written as `- [ ]` on the note it concerns.
- Never delete originals. Older wording is kept in a folded `> [!quote]-` box.
- Na'vi text is carried, never composed. Na'vi characters use no contractions.
- A new ruling goes into [[Rulings Log]] with its date, and onto the note it changes.
- The Three Laws of Eywa (no stone upon stone, no turning wheel, no metals of the ground) come before everything else. Check every scene for pulleys, carts, stone building and Na'vi metal tools.

## What cost the most, and what to do instead

- Every subagent pays a large fixed cost per turn, whatever the size of its task. Measured: Haiku agents with a 10k-token source pack and 3 to 4 tool calls used 104k to 120k tokens each; Sonnet agents that explored freely used 139k to 190k.
- So: use scripts for anything deterministic; give one agent several small jobs instead of one job each; keep each agent to as few tool calls as possible; do small judgment calls in the main session.
- A long main conversation is itself expensive, because all of it is re-read on every turn. Start a fresh session from this checkpoint when a conversation gets long.

## Canon check — 2026-11-26 (Claude chat, at Millie's request)

- Added `_admin/canon_check.py` and `_admin/test_canon_check.py` (19 fixture tests, pass with or without PyYAML). It is read-only unless `--out` is given and refuses to write into `99 Archive`.
- It checks what `proof.py` does not: the Three Laws of Eywa, contractions in Na'vi dialogue (speaker from speech tags; characters with no `navi_name` are Sky People and may use them), Na'vi reading or writing, banned style words and patterns, retired spellings, garbled accents, frontmatter (canon values, folder types, links in `characters`/`family`/`groups`/`arc`/`era`) and dated inbox names.
- Rule lists are read live from [[Canon Rules]] and [[Name Fixes to Apply]]; edit those notes to change what it checks. Earlier-version boxes, code blocks, callouts, checklists and Millie's quoted words are skipped.
- First full run: `_admin/reports/canon-check-2026-11-26.md`. 9 errors: 8 Na'vi contractions in [[The Great Games Legacy]] (Sänrri, 'Ipxerey, Mìreya, Rewon, Atanvi) and "Mowpay" in [[Working Reference]]. Three Laws sweep of every lore note (the Rulings Log's open item): 4 leads, none a clear break; the most notable is Kaymi holding Nika's metal hand in [[The Mark of Earth House]]. One inbox note says `canon: proposed` where the rest say `proposal`.
- `GEMINI.md` now tells Gemini how and when to run the check (new section "The canon check", plus a step in its writer rules). Pre-edit copy: `90 Sources/pre-canon-check-gemini-20261126.tar.gz`.
- Nothing was fixed. Each finding waits for Millie's ruling. Pre-edit copies of CHECKPOINT and README.txt: `90 Sources/pre-canon-check-20261126.tar.gz`.
- Verified in the Cowork Linux shell with system Python. `test_maintenance.py` shows 2 errors there only because it uses the macOS path `/private/tmp`; run it on the Mac as before.

## Portability maintenance — 2026-11-12

- Authorized by Millie; Claude unavailable until 3 p.m. ChatGPT handled administrative scripts and documentation only. Confirm a new handoff before either assistant resumes writing.
- Backup: `90 Sources/maintenance-backup-20261112-114246.tar.gz`; 14 original administrative files verified byte for byte before editing. New files and the local environment are not in this pre-change backup.
- Paths now derive from script locations. Dependencies installed with approval: PyYAML 6.0.3 in `_admin/.venv`, Pandoc 3.13 via Homebrew. Recreate the virtual environment after moving the vault to another computer.
- Generated question-index hashes now describe the newly generated content. Missing YAML parsing fails explicitly. Proof requires `--notes` or `--full`, checks converter failures, and returns a failing status for detected problems.
- Targeted fixture tests passed before the index refresh. No migration builders or full archival proof were run. No character, arc, scene, language, worldbuilding, or archived source content was edited.

## Lore integration — 2026-11-12 (Claude, at Millie's instruction)

- Read the external maintenance handoff first; all 16 reviewed-file hashes matched before editing. Claude had no background writer running. The administrative changes from the maintenance pass are still awaiting Millie's acceptance or revision.
- Integrated Millie's brief on the ancient Toruk Makto into five existing notes: [[Rulings Log]], [[Ambition and Hope — The Ones Who Know All]], [[Astikasya]], [[Samaya]], [[Siege of the Falls]]. Confirmed canon, proposals and deliberately unresolved questions are kept apart on the arc note.
- No new notes were created. Whether Tunskxe and Yoko'fya get character notes or a lore note is Millie's pending choice.
- Pre-edit copies: `90 Sources/pre-lore-integration-20261112.tar.gz`.
- This vault folder is not a git repository; no sync or lock was found or touched.
- Later the same day Millie ruled: descent runs through Eyfuwen; the proposed farewell line uses 燈さん. She also accepted the maintenance pass's administrative changes as applied ("I guess so yeah"); Claude did not review that diff line by line.

## Full-proof review and name rulings — 2026-11-12 (Claude, at Millie's instruction)

- Full proof run read-only: 404 of 2,924 archived passages unmatched. All 404 are listed in `_admin/full-proof-unmatched-20261112.txt` and classified in `_admin/full-proof-classification-20261112.txt`: 402 explained (rosters now in properties, formatting, old file headers, old-folder admin text, name-table artifact, lines removed by ruling); 2 were real omissions.
- Millie ruled on them and on four name variants; recorded in [[Rulings Log]] ("after the full proof review"). Edited: [[Tsa'rawm]] (left eye section, archived passage restored), [[Tsyokanì]] (status line; Okxa), [[Sänrri]] (source name Tomori Samaya), Okxa in the Wild Hunt cast table (folded original quote untouched). [[MBTI Reference]] is a carried original and keeps Okka; the Rulings Log overrides it.
- Pre-edit copies: `90 Sources/pre-name-rulings-20261112.tar.gz`. Index rebuilt after the alias changes.
- Open for Millie: Mawpay's surname (Shiina in the vault, Yahata in the rosters); whether Kaymi (*Ericht Samaya-Takamatsu*) and Lì'may (*Miyako Samaya-Takamatsu*) also become plain Samaya.
- Full proof after these edits: 404 unmatched, the same set as classified (the restored eye passage sits inside a longer archived paragraph, so it still counts as unmatched).
- Migration closure, A–D and `tasks.json` updates are still pending Millie's approval.

## Gender and pronoun metadata — 2026-11-12 evening (Claude, at Millie's instruction)

- Single writer: Claude. Pre-edit copies: `90 Sources/pre-gender-pronouns-20261112.tar.gz` (12 files) and `pre-gender-pronouns-20261112-tswesya.tar.gz`. The vault is still not a git repository, so the tarballs are the checkpoint.
- The `_templates/Character.md` template and `Cast.base` gained `gender`, `pronouns` (list) and `transition`; the base has a new **Gender & Pronouns** view grouped by gender. The three old views are unchanged.
- Recorded on notes (frontmatter only, no prose touched): [[Rängay]] trans woman, she/her, Eye of Eywa; [[Txafwe]] trans man, he/him, Eye of Eywa; [[Atanvi]], [[Txewan]], [[Tìfyaw]] she/her with their documented Eye transitions; [[Txolaw]] he/him with his; [[Roneyu]] and [[Tswesya]] they/them. Gender left blank wherever it is not stated. New ruling in [[Rulings Log]].
- Open for Millie: one review list, `_admin/gender-pronoun-review-20261112.md` (section A has the decisions; B proposes pronouns for the other 68 from how each profile is written; C is the consistency check, which found no real mismatch).
- Tooling note: `_admin/.venv` is a macOS environment and does not run in Claude's Linux shell; this pass used the shell's own python3 with PyYAML 6.0.3. Index not rebuilt (no titles or aliases changed).
- Later the same evening Millie gave the full list of trans characters and ruled that -'itu is the nonbinary name ending (both in [[Rulings Log]]). Gender now set on 11 notes: trans women [[Txewan]], [[Atanvi]], [[Rängay]], [[Apayì]], [[Tìfyaw]], [[Zìsaw]]; trans men [[Txafwe]], [[Txolaw]]; nonbinary [[Tswesya]], [[Oarä]], [[Roneyu]]. Pre-edit copies: `90 Sources/pre-gender-rulings-20261112.tar.gz`. Oarä's name (-'ite) and pronouns are left for Millie; no Na'vi text or prose was changed.
- Third pass, same evening: Millie ruled that every trans Na'vi went through the Eye of Eywa except Roneyu (Mangkwan-born), Oarä is she/they, Kerevi is they/them, and everyone else is cis with the proposed pronouns. All 76 character notes now carry the three properties; [[Gender Transition Through Eye of Eywa]] lists every practitioner. Pre-edit copies (whole `10 Characters` folder): `90 Sources/pre-gender-cast-20261112.tar.gz`. Left open: Oarä's -'ite ending, and Tìmeyo/Kerevi's gender.
- Last answers: Oarä's name is now *Oarä te Hafyon Katirì'itu* (old form kept as an alias, Family line now "Child of"); Tìmeyo is a cis woman and Kerevi is Kerevi. Nothing left open for the gender metadata. Pre-edit copies: `90 Sources/pre-oara-timeyo-20261112.tar.gz`. Optional prose follow-up: Katirì and Tswesya still say "daughter" for Oarä.
- 2026-11-26 (evening), Mutsumi ruling: Tìmeyo and Kerevi are a nonbinary, agender, plural system using they/them, and the full name is now *Tìmeyo te Kilvay Luey'itu* (old form kept as an alias); transition left not established. Edited: Tìmeyo, Syayvi, Relationship Lore, The Scattered Ashes, MyMuji Season Plan, MBTI Reference, the Drunk Personalities inbox note, GEMINI.md and the Rulings Log (new dated entry; the 2026-11-12 lines stay as history). The "Earlier version" callouts keep the old prose. Pre-edit copies: `90 Sources/pre-mutsumi-enby-20261126.tar.gz`. Not done: the Claude project's own instructions and `gemini-skill/GEMINI.md` copy still list Kerevi alone as they/them.

## Inbox

- 2026-11-14 (Claude, chat): added `_inbox/2026-11-14 Drunk Personalities of the Nine.md`, accepted in full by Millie the same day: new Rulings Log section "Ruled on 2026-11-14: the Nine when drunk", and one dated line under Notes on 18 character notes. The inbox note can be filed or left as is.
- 2026-11-22 (Claude, project thread, Bogotá): added two proposals to `_inbox`, `2026-11-22 Warming the Falls.md` (Frontiers of Pandora research on the Spires and Clouded Forest, plus a proposed warm platform custom with Sänrri's kotatsu skirt) and `2026-11-22 Warm Platform Scenes.md` (two draft scenes). Nothing ruled, nothing else edited. Open questions are listed at the end of the first note.

## INDEX and GitHub backup: 2026-11-18 (Claude, at Millie's instruction)

- Added `00 Home/INDEX.md` (folder map, reading order, conventions, a roster read from the character properties). Approved by Millie. No existing note was edited.
- The GitHub backup lacked `60 Meta`, `_inbox`, `_templates` and `99 Archive`. Claude pushed them to `main` (commit f7a69fd, 97 files), no force push. Left out on purpose: `90 Sources` (backup tarballs, PDFs), `.venv`, `.obsidian`, the older `_backup_2026-11-01` copy and the PDF/docx files inside `99 Archive`.
- This vault folder is still not a git repository. Whoever updates the GitHub copy next must pull first (no rebase) and add this INDEX.

## Children's personalities, 2026-11-21 (Claude, at Millie's instruction)

- Single writer: Claude (project thread). Edited on a branch of the GitHub backup, not the live vault: the character notes for Anake, Kxayì, Lawarey, Mawpay, Nìla, Mìrì, Mìyo, Oarä, Netezu, Lì'may, Eantu, Tulìpey, Rawìl and Notä (Notes sections, plus frontmatter and pronoun changes for Nìla and Mawpay's source name), Rängay (one pronoun), The Great Games (Netezu's mother), the Rulings Log, and this checkpoint.
- Closed: Mawpay's surname is Yahata. Still open: Lì'may and Kaymi surnames, Nìla's name ending, Eantu's build.
- Not done: the live vault still has the old text; the changes exist only on the GitHub backup.
- Done later the same day: the indexes were rebuilt (the stale kuru question is gone), the Eye of Eywa note now says Nìla will go through it later, and the Netezu question on Ngotxì is ticked (Syulang). Oarä is nonbinary and has not passed through the Eye (Millie, same day); removed from the practitioners list.

## Inbox rulings, 2026-11-24 (Claude, at Millie's instruction)

- Single writer: Claude (project thread). Added one section to [[Rulings Log]]; no other note edited. Pre-edit copies: `90 Sources/pre-inbox-rulings-20261124.tar.gz`. Live vault only; not pushed to GitHub.
- Still open: fruit name, cold season, settlement location, timeline placement, Na'vi name for the custom, nantang habits, Yoko'fya's death, Choso. Dated lines on the Ketxe, Sänrri, Tsu'ong notes are pending.

## Inbox answers, 2026-11-26 (Claude, at Millie's instruction)

- One section added to [[Rulings Log]]. Pre-edit copies: `90 Sources/pre-inbox-answers-20261126.tar.gz`. Live vault only.

## Sänrri's full name, 2026-11-23 (Claude, at Millie's instruction)

- Single writer: Claude (project thread). Millie ruled the new name; see [[Rulings Log]] ("Ruled on 2026-11-23: Sänrri's full name"). Seven live notes edited by a Haiku subagent with one exact replacement (Tsawtral Tanhì'ite to Tsawtral Hikari'ite). No archive, migration script or proof log was touched.
- Later the same day Millie ruled the meaning: the name now means light (Hikari), so [[Sänrri]] says "light" where it said "starlight"; the open item on that note is ticked.

## Na'vi heights, 2026-11-23 (Claude, at Millie's instruction)

- Single writer: Claude (project thread). Millie ruled the heights; see [[Rulings Log]] ("Ruled on 2026-11-23: Na'vi heights"). Added that section, one dated Height line under Notes on 26 character notes, and the source note `_inbox/2026-11-23 Navi Heights from the Reze Poster.md` (accepted). Pre-edit copies: `90 Sources/pre-navi-heights-20261123.tar.gz`.
- Later the same day, Eyfuwen (185 cm, 3.08 m) and 'Ipxerey (190 cm, 3.17 m) were added with a Height line on their notes. Pre-edit copies: `90 Sources/pre-navi-heights-eyfuwen-ipxerey-20261123.tar.gz`. The same edits were pushed to the GitHub backup's `main` the same day (commit ad01080).

## Three Laws of Eywa, 2026-11-26 (Claude, at Millie's instruction)

- Single writer: Claude (project thread). Millie ruled the Three Laws as the top rule; see [[Rulings Log]] ("Ruled on 2026-11-26: the Three Laws of Eywa"). Edited [[Rulings Log]], [[Canon Rules]] and this file. Pre-edit copies: `90 Sources/pre-three-laws-20261126.tar.gz`. Live vault only; not pushed to GitHub.
- Still open: a scan of existing canon for places that cross a Law.
