#!/usr/bin/env python3
"""Rebuild download/harness-template.zip from harness-template/ (top-level folder preserved)."""
import zipfile
from pathlib import Path

ROOT = Path('/home/z/my-project')
SRC = ROOT / 'harness-template'
DST = ROOT / 'download' / 'harness-template.zip'

old_count = None
if DST.exists():
    with zipfile.ZipFile(DST) as z:
        old_count = len(z.namelist())

files = sorted(p for p in SRC.rglob('*') if p.is_file())
with zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, p.relative_to(ROOT).as_posix())

with zipfile.ZipFile(DST) as z:
    names = z.namelist()
    bad = z.testzip()
    proto = z.read('harness-template/PROTOCOL.md').decode()
    assert '11. An adoption gap is not authorization' in proto, 'rule 11 missing in zip!'
    assert 'v1.1' in proto, 'version bump missing in zip!'

print(f'old entries: {old_count} -> new entries: {len(names)}; testzip: {bad}')
print('rule 11 + v1.1 verified inside zip: OK')
for n in names:
    print(' ', n)
