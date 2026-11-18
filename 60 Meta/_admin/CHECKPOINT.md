---
type: "meta"
---
# AITM vault checkpoint

**Last updated:** 2026-11-17, Claude chat (Bogotá): added the 2026-11-17 ruling on the Ke'awa origin the Anufi/Nesim mappings, and Eyfuwen in Tsu'lo's role. Before that, 2026-11-16: added the 2026-11-16 ruling on why the ANAKT exists (Ardmore, the Mangkwan play, Luka) and Luka's kuru (Tsu'lan brings it back). Previous: 2026-11-15, Narayra and the Falls thread. Previous: 2026-11-12, maintenance handoff. **Phase:** migration built and cleaned; now in maintenance and renovation.

## State

- 150 indexed Markdown notes: 147 outside `_admin`, plus 3 administrative notes. Last full validation (recorded before this maintenance pass): all original prose accounted for, no broken links, no broken encoding.
- Originals: `99 Archive/2026-11-11 originals/` (75 files, never edit).
- Canon authority, in order: Millie > [[Rulings Log]] > Timeline and Era notes > older documents.
- 130 unchecked items across 17 notes; see [[Open Questions Index]]. These include review checklist items, not only unresolved canon questions. The previous checkpoint records that none blocks the remaining tasks.

## Tasks

Machine-readable list: `60 Meta/_admin/tasks.json`.

**Blocked on Millie:** six project-only documents must be downloaded from the Claude project into `_inbox` (the assistant cannot copy them without retyping).
**Pending:** renovate the Worldbuilding Reference; pair arcs with eras; refresh the Claude project from the vault; the hands-on walkthrough; one final validation.

## How to resume in a fresh session (any model)

1. Read this note, [[Operations Protocol]], [[Rulings Log]], and [[Canon Rules]], then `tasks.json`. Do not read the whole vault. Confirm a single writer before editing.
2. For canon, read [[Rulings Log]] only. For one arc or character, read that one note.
3. Rebuild indexes only when needed: `"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_admin/build_index.py"`. Add `--check` for no writes. Run these example commands from the vault root; the scripts locate the vault from their own paths, so absolute script paths also work from elsewhere.
4. Validate affected notes with `"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_migration scripts/proof.py" --notes "00 Home/Canon Rules.md"`. Use `--full` only for the final archival proof; it remains pending. See `_admin/README.txt` for dependencies and tests.
5. Do not rerun migration builders during maintenance. Their note writes now refuse to replace changed or untracked files using the local `manifest.json`; originals are write-protected by the shared helper. This is overwrite protection, not a concurrency lock. Prefer small direct edits and maintain one writer at a time.

## Rules that must not be broken

- Nothing is invented. A gap is an open question, written as `- [ ]` on the note it concerns.
- Never delete originals. Older wording is kept in a folded `> [!quote]-` box.
- Na'vi text is carried, never composed. Na'vi characters use no contractions.
- A new ruling goes into [[Rulings Log]] with its date, and onto the note it changes.

## What cost the most, and what to do instead

- Every subagent pays a large fixed cost per turn, whatever the size of its task. Measured: Haiku agents with a 10k-token source pack and 3 to 4 tool calls used 104k to 120k tokens each; Sonnet agents that explored freely used 139k to 190k.
- So: use scripts for anything deterministic; give one agent several small jobs instead of one job each; keep each agent to as few tool calls as possible; do small judgment calls in the main session.
- A long main conversation is itself expensive, because all of it is re-read on every turn. Start a fresh session from this checkpoint when a conversation gets long.

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

## Inbox

- 2026-11-14 (Claude, chat): added `_inbox/2026-11-14 Drunk Personalities of the Nine.md`, accepted in full by Millie the same day: new Rulings Log section "Ruled on 2026-11-14: the Nine when drunk", and one dated line under Notes on 18 character notes. The inbox note can be filed or left as is.
