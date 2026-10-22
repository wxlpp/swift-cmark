#!/usr/bin/env python3
"""Release validation must fail closed even with python -O."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class GeneratorGateTests(unittest.TestCase):
    def test_optimized_python_rejects_corrupted_inputs_and_output(self):
        for change in ('version', 'checksum', 'output'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name in ('tools/cjk-data', 'test/cjk-fixtures'):
                    shutil.copytree(ROOT / name, root / name)
                (root / 'src').mkdir()
                shutil.copy(ROOT / 'src/cjk_tables.h', root / 'src/cjk_tables.h')
                shutil.copy(ROOT / 'tools/generate-cjk-tables.py', root / 'tools/generate-cjk-tables.py')
                manifest = root / 'tools/cjk-data/manifest.json'
                data = json.loads(manifest.read_text())
                if change == 'version':
                    data['unicodeVersion'] = '17.0.0'
                elif change == 'checksum':
                    data['inputs'][0]['sha256'] = '0' * 64
                else:
                    (root / 'src/cjk_tables.h').write_text('stale')
                manifest.write_text(json.dumps(data))
                result = subprocess.run([sys.executable, '-O', str(root / 'tools/generate-cjk-tables.py'), '--check'], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('tables verified', result.stdout)


if __name__ == '__main__':
    unittest.main()
