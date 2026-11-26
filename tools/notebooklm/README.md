# AITM bundles for NotebookLM and Gemini

`build_bundles.py` joins the vault's canon notes into 8 files (46 to 161 KB each) so NotebookLM stays far below its source limit.

- Reads only: it never edits a vault note, and the GitHub Action never commits or pushes.
- Canon only: `_inbox`, `99 Archive`, `_templates`, `60 Meta` and `.base` files are left out.
- Every bundle starts with the Three Laws of Eywa and the hard canon rules.

Run it by hand: `python3 tools/notebooklm/build_bundles.py . bundles`
