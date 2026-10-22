#!/usr/bin/env python3
"""Small explicit contracts, independent of the reference renderer."""
import subprocess
import sys

binary = sys.argv[1]
cases = [
    ('改成**“确认这笔交易完成了”**，继续。', '<p>改成<strong>“确认这笔交易完成了”</strong>，继续。</p>\n'),
    ('a**「中文」**b', '<p>a<strong>「中文」</strong>b</p>\n'),
    ('a**〰**a', '<p>a<strong>〰</strong>a</p>\n'),
    ('a**😀**a', '<p>a**😀**a</p>\n'),
    ('a__中文__b', '<p>a__中文__b</p>\n'),
    ('`中文**“原文”**`', '<p><code>中文**“原文”**</code></p>\n'),
    (r'中文\*\*“原文”\*\*', '<p>中文**“原文”**</p>\n'),
]
strict = subprocess.check_output([binary], input=cases[0][0], text=True)
assert '<strong>' not in strict and '**' in strict, 'strict mode unexpectedly relaxed'
for source, expected in cases:
    output = subprocess.run([binary, '--cjk-friendly-emphasis'], input=source, text=True, capture_output=True, check=True).stdout
    assert output == expected, (source, output, expected)
print(f'{len(cases)} CJK contracts passed')

from pathlib import Path
fixtures = Path(__file__).parent / 'cjk-fixtures'
for golden in sorted(fixtures.glob('*.html')):
    source = golden.with_suffix('.md').read_text()
    output = subprocess.check_output([binary, '--cjk-friendly-emphasis', '--unsafe'], input=source, text=True)
    assert output == golden.read_text(), golden.name
non_cjk = (fixtures / 'gfm-non-cjk.md').read_text()
flags = [binary, '--unsafe', '-e', 'table', '-e', 'strikethrough']
strict = subprocess.check_output(flags, input=non_cjk, text=True)
relaxed = subprocess.check_output(flags + ['--cjk-friendly-emphasis'], input=non_cjk, text=True)
assert strict == relaxed, 'CJK option changed non-CJK GFM behavior'
subprocess.run([binary, '--cjk-friendly-emphasis'], input='中' + '*' * 100000 + '文', text=True, stdout=subprocess.DEVNULL, check=True, timeout=5)
print('5 community golden fixtures, non-CJK GFM parity and long delimiter passed')
