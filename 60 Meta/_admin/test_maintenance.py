"""Targeted maintenance regression tests; fixtures never write into the real vault."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / '60 Meta/_migration scripts'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '60 Meta/_admin').mkdir(parents=True)
        (self.root / '00 Home').mkdir()
        self.note = self.root / '00 Home/Test.md'
        self.note.write_text('---\ntype: meta\naliases: [Example]\n---\n# Heading\n- [ ] Check me\n[[Example#Heading]]\n')
        self.builder = module('aitm_index', ROOT / '60 Meta/_admin/build_index.py')
        self.common = module('aitm_common', SCRIPTS / 'common.py')
        self.common.V = str(self.root)
        self.common.MANIFEST = str(self.root / 'manifest.json')

    def build(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.builder.build(self.root)

    def test_generated_hash_and_repeat_run(self):
        idx, broken = self.build()
        self.assertFalse(broken)
        p = '60 Meta/_admin/Open Questions Index.md'
        first = (self.root / '60 Meta/_admin/index.json').read_bytes()
        self.assertEqual(idx[p]['sha'], hashlib.sha256((self.root / p).read_bytes()).hexdigest()[:16])
        self.build()
        self.assertEqual(first, (self.root / '60 Meta/_admin/index.json').read_bytes())

    def test_manual_and_untracked_files_preserved(self):
        original = self.note.read_bytes()
        manifest = {'00 Home/Test.md': hashlib.sha256(original).hexdigest()}
        self.note.write_text('Manual revision\n')
        self.assertFalse(self.common.guarded_write('00 Home/Test.md', 'Generated\n', manifest))
        self.assertFalse(self.common.write('00 Home/Test.md', 'Generated'))
        self.assertEqual(self.note.read_text(), 'Manual revision\n')

    def test_tracked_output_updates_manifest(self):
        manifest = {'00 Home/Test.md': hashlib.sha256(self.note.read_bytes()).hexdigest()}
        self.assertTrue(self.common.guarded_write('00 Home/Test.md', 'Updated\n', manifest))
        self.assertEqual(manifest['00 Home/Test.md'], hashlib.sha256(self.note.read_bytes()).hexdigest())

    def test_archive_and_path_escape_refused(self):
        for p in ['99 Archive/original.md', '../escape.md']:
            with self.assertRaises(ValueError):
                self.common.guarded_write(p, 'Never write', {})

    def test_bad_yaml_leaves_outputs_unchanged(self):
        self.build()
        p = self.root / '60 Meta/_admin/index.json'
        old = p.read_bytes()
        self.note.write_text('---\naliases: [\n---\n')
        with self.assertRaises(Exception):
            self.build()
        self.assertEqual(old, p.read_bytes())

    def test_missing_yaml_fails_without_output(self):
        script = self.root / '60 Meta/_admin/build_index.py'
        shutil.copyfile(ROOT / '60 Meta/_admin/build_index.py', script)
        run = subprocess.run([sys.executable, '-B', '-S', str(script)], cwd='/private/tmp', capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('PyYAML is required', run.stderr)
        self.assertFalse((self.root / '60 Meta/_admin/index.json').exists())

    def test_portable_index_and_targeted_proof(self):
        scripts = self.root / '60 Meta/_migration scripts'
        scripts.mkdir()
        for name in ['common.py', 'proof.py']:
            shutil.copyfile(SCRIPTS / name, scripts / name)
        indexer = self.root / '60 Meta/_admin/build_index.py'
        shutil.copyfile(ROOT / '60 Meta/_admin/build_index.py', indexer)
        run = subprocess.run([sys.executable, '-B', str(indexer)], cwd='/private/tmp', capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        proof = scripts / 'proof.py'
        run = subprocess.run([sys.executable, '-B', str(proof), '--notes', '00 Home/Test.md'], cwd='/private/tmp', capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr + run.stdout)
        self.note.write_text('[[Missing]]\n')
        run = subprocess.run([sys.executable, '-B', str(proof), '--notes', '00 Home/Test.md'], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)

    def test_full_proof_requires_explicit_selection(self):
        run = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'proof.py')], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('required', run.stderr)


if __name__ == '__main__':
    unittest.main()
