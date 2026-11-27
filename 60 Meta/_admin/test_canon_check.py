"""Fixture tests for canon_check.py; fixtures live in a temp folder, never the vault."""
import contextlib
import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('canon_check', HERE / 'canon_check.py')
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

RULES = '''---
type: "meta"
---
## Style rules
- Banned patterns: "It's not just X, it's Y"; "more than just"; "Let's dive in / break it down / explore".
- Banned words: tapestry, vibrant, landscape (metaphor), delve.
'''
FIXES = '''| Find | Replace with | Why | Seen in |
|---|---|---|---|
| `Mowpay` | `Mawpay` | ow | x |
| `Loxtu` | `Lokxtu` | x | x |
| `Kxurryo` | `Kxuryo` | rr | x |
'''
NAVI = '---\ntype: character\nnavi_name: "Rewon te Pxeayo Txoewll\'ite"\ncanon: confirmed\n---\n'
SANRRI = '---\ntype: character\nnavi_name: Sänrri te Tsawtral\naliases: [Tomori]\ncanon: confirmed\n---\n'
HUMAN = '---\ntype: character\naliases: [Kobeni Higashiyama]\ncanon: confirmed\n---\n'


class CanonCheckTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.write('00 Home/Canon Rules.md', RULES)
        self.write('50 Language/Name Fixes to Apply.md', FIXES)
        self.write('10 Characters/Rewon.md', NAVI)
        self.write('10 Characters/Sänrri.md', SANRRI)
        self.write('10 Characters/Kobeni.md', HUMAN)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')

    def scene(self, body, name='Test.md', meta='characters: ["[[Rewon]]"]'):
        self.write(f'40 Story/Scenes/{name}', f'---\ntype: scene\n{meta}\ncanon: confirmed\n---\n{body}\n')

    def findings(self, check):
        return [f for f in cc.run(self.root) if f['check'] == check]

    def test_navi_contraction_with_speech_tag_is_error(self):
        self.scene('"That\'s what makes it beautiful," Sänrri said softly.')
        f = self.findings('contractions')
        self.assertEqual([(x['level'], 'Sänrri' in x['message']) for x in f], [('error', True)])

    def test_alias_speech_tag_resolves(self):
        self.scene('"I\'m here," said Tomori.')
        self.assertEqual(self.findings('contractions')[0]['level'], 'error')

    def test_name_is_contraction_detected_but_possessive_is_not(self):
        self.scene('"Rewon\'s going to faint," Sänrri said.\n\n"Rewon\'s spear is ready," Sänrri said.')
        msgs = [f['message'] for f in self.findings('contractions')]
        self.assertEqual(len(msgs), 1)

    def test_sky_person_may_use_contractions(self):
        self.scene('"I can\'t do this," Kobeni said, shaking.')
        self.assertEqual(self.findings('contractions'), [])

    def test_unattributed_dialogue_is_review_only(self):
        self.scene('Rewon looked at the river.\n\n"We\'ve seen enough."')
        f = self.findings('contractions')
        self.assertEqual([x['level'] for x in f], ['review'])

    def test_three_laws_flag_navi_but_not_sky_people(self):
        self.scene('Rewon pulled the cart over the ridge.\n\nKobeni fixed the cart with steel.')
        f = self.findings('laws')
        self.assertEqual(len(f), 1)
        self.assertIn('Rewon', f[0]['message'])

    def test_rda_mining_and_metaphors_are_not_law_breaks(self):
        self.scene('Rewon watched the RDA mining scar.\n\nRewon forged her own path with iron will.')
        self.assertEqual(self.findings('laws'), [])

    def test_earlier_version_boxes_are_ignored(self):
        self.scene('> [!quote]- Earlier version\n> Rewon pulled a cart and said "it\'s vibrant."\n\nRewon rested.')
        self.assertEqual(self.findings('laws') + self.findings('contractions') + self.findings('style'), [])

    def test_banned_style_from_canon_rules(self):
        self.scene('Rewon was more than just a warrior. A vibrant dawn rose.\n\nLet\'s explore the Falls.')
        labels = sorted(f['message'] for f in self.findings('style'))
        self.assertEqual(len(labels), 3)
        self.assertTrue(any("Let's explore" in m for m in labels))

    def test_explore_as_ordinary_verb_is_fine(self):
        self.scene('After the challenge Rewon left to explore the world.')
        self.assertEqual(self.findings('style'), [])

    def test_retired_spelling_from_name_fixes(self):
        self.scene('Mowpay laughed.')
        self.assertEqual(self.findings('spelling')[0]['level'], 'error')

    def test_audit_paragraph_listing_old_spellings_is_skipped(self):
        self.write('60 Meta/Audit.md', 'Checked: no Mowpay, Loxtu or Kxurryo found.\n\nMowpay (11) is listed.\n')
        f = self.findings('spelling')
        self.assertEqual([x['line'] for x in f], [3])

    def test_frontmatter_link_and_canon_value(self):
        self.scene('Quiet.', meta='characters: ["[[Nobody]]"]\nkind: x')
        self.write('10 Characters/Odd.md', '---\ntype: character\nnavi_name: x\ncanon: maybe\n---\n')
        msgs = [f['message'] for f in self.findings('frontmatter')]
        self.assertTrue(any('[[Nobody]]' in m for m in msgs))
        self.assertTrue(any('"maybe"' in m for m in msgs))

    def test_inbox_proposal_allowed_and_dates_required(self):
        self.write('_inbox/2026-11-26 Idea.md', '---\ncanon: proposal\n---\nText.\n')
        self.write('_inbox/Undated idea.md', '---\ncanon: proposal\n---\nText.\n')
        self.assertEqual([f['note'] for f in self.findings('inbox')], ['_inbox/Undated idea.md'])
        self.assertEqual(self.findings('frontmatter'), [])

    def test_mojibake_outside_code_only(self):
        self.write('30 World/Place.md', 'Fix `MÃ¬reya` like this.\n\nMÃ¬reya is broken here.\n')
        self.assertEqual(len(self.findings('encoding')), 1)

    def test_archive_is_never_scanned(self):
        self.write('99 Archive/old.md', 'Mowpay pulled a cart. MÃ¬reya.\n')
        self.assertEqual([f for f in cc.run(self.root) if f['note'].startswith('99 Archive')], [])

    def test_read_only_and_exit_codes(self):
        self.scene('"That\'s it," Sänrri said.')
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cc.main(['--root', str(self.root)]), 1)
            self.assertEqual(cc.main(['--root', str(self.root), '--only', 'laws']), 0)
        after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_out_refuses_archive(self):
        with self.assertRaises(SystemExit):
            cc.main(['--root', str(self.root), '--out', '99 Archive/report.md'])

    def test_notes_filter_and_unknown_path(self):
        self.scene('Mowpay.', name='A.md')
        self.scene('Fine.', name='B.md')
        f = cc.run(self.root, ['40 Story/Scenes/B.md'])
        self.assertEqual(f, [])
        with self.assertRaises(SystemExit):
            cc.run(self.root, ['40 Story/Scenes/Missing.md'])


if __name__ == '__main__':
    unittest.main()
