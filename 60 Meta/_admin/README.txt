AITM administration — read CHECKPOINT.md first. One writer at a time.

Validation setup on this Mac:
- Python environment: 60 Meta/_admin/.venv (PyYAML 6.0.3).
- Pandoc 3.13 installed through Homebrew, required for full archival proof.
- These dependencies were installed with Millie's approval on 2026-11-12.
- After moving the vault, recreate .venv; virtual environments are machine-specific.
  Ask before installing software. Requirements are in requirements.txt.

Commands from the vault root (absolute script paths also work from other folders):
"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_admin/test_maintenance.py"
"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_admin/build_index.py" --check
"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_admin/build_index.py"
"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_migration scripts/proof.py" --notes "00 Home/Canon Rules.md"

Only at the final validation gate:
"60 Meta/_admin/.venv/bin/python" -B "60 Meta/_migration scripts/proof.py" --full
Optional -v prints examples of unmatched archived prose.

build_index.py reads active Markdown notes and writes only index.json and
Open Questions Index.md. --check performs the same indexing without writes.
The count includes administrative Markdown; unchecked items include review tasks.
proof.py --notes uses the saved index for other note names and aliases, and reads
heading targets as needed. Refresh the index after renames or alias changes.
It is a structural check, not a canon or Na'vi-language verifier.
Full proof checks normalized prose fragments longer than 60 characters; it is
not a byte-for-byte archive integrity test or proof of semantic equivalence.

Do not rerun migration builders for routine maintenance. Their shared guarded
writer refuses changed/untracked replacements and forbids writes into 99 Archive.
The manifest lives beside the migration scripts; no external build folder is used.
Guards do not coordinate simultaneous writers. Confirm ownership before edits.

Pre-maintenance recovery:
90 Sources/maintenance-backup-20261112-114246.tar.gz contains 14 original files.
Extract into a separate temporary directory, compare, and restore only the desired
files after confirming ownership. Do not blindly overwrite newer work.
New test/config files and .venv were created after this backup.

Maintenance verification, 2026-11-12:
- 8 fixture tests passed, including manual/untracked note preservation,
  archive/path protection, stable generated hashes, missing/invalid YAML,
  execution outside the vault directory, and targeted proof failure detection.
- Administrative index: 150 notes = 147 outside _admin + 3 administrative notes;
  130 unchecked items across 17 notes; no unresolved note links.
- Targeted proof of Canon Rules, CHECKPOINT, Operations Protocol and the
  generated question index: no unresolved links, broken headings or mojibake.
- All administrative Python scripts parsed; the live generated hash matched.
- Canon Rules compared to backup: only its family-reference link changed.
- No full archival proof or migration builder was run.

Modified files:
60 Meta/_admin/build_index.py
60 Meta/_admin/index.json
60 Meta/_admin/Operations Protocol.md
60 Meta/_admin/CHECKPOINT.md
60 Meta/_admin/README.txt
60 Meta/_admin/tasks.json
60 Meta/_migration scripts/common.py
60 Meta/_migration scripts/proof.py
60 Meta/_migration scripts/cast.py
60 Meta/_migration scripts/phase4.py
60 Meta/_migration scripts/pilot.py
60 Meta/_migration scripts/skeleton.py
00 Home/Canon Rules.md (reference path only)
Open Questions Index.md was regenerated with identical content.
Added: _admin/test_maintenance.py, _admin/requirements.txt, _admin/.venv,
and the recovery archive in 90 Sources. No manifest hashes were reset.

Maintenance writer released on completion. Confirm ownership again before
new edits; Claude's usage reset alone is not a handoff.
