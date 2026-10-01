#!/usr/bin/env python3
"""Offline manifest/optional HRL1 checks; Python 3.10+, stdlib only, no USB."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

LIMIT = 2 * 1024 * 1024  # Parser bound, never a hardware budget.


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def obj(value, name):
    require(isinstance(value, dict), name + ' must be an object')
    return value


def digest(value):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value), 'invalid SHA-256')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def bounded_read(path):
    with Path(path).open('rb') as stream:
        raw = stream.read(LIMIT + 1)
    require(len(raw) <= LIMIT, 'input exceeds parser bound')
    return raw


def check_blob(path, audit):
    raw = bounded_read(path)
    require(len(raw) >= 24, 'short HRL1 header')
    require(hashlib.sha256(raw).hexdigest() == audit['sha256'], 'blob hash mismatch')
    magic, entry, size, span, count, align = struct.unpack_from('<6I', raw)
    require(magic == 0x314c5248 and align == 16, 'invalid HRL1 magic/alignment')
    require(0 < size <= span <= LIMIT and entry % 2 == 0 and entry < size, 'invalid HRL1 entry/span')
    require(len(raw) == 24 + size + count * 4, 'invalid HRL1 extent')
    expected = {'bytes': len(raw), 'entryOffset': entry, 'imageBytes': size,
                'spanBytes': span, 'bssBytes': span-size,
                'arenaAllocationBytes': span+align, 'relocations': count}
    for key, value in expected.items():
        require(audit.get(key) == value, 'blob/audit mismatch: ' + key)
    offsets = struct.unpack_from('<' + str(count) + 'I', raw, 24 + size)
    require(list(offsets) == sorted(set(offsets)), 'unordered/duplicate relocations')
    for offset in offsets:
        require(offset % 4 == 0 and offset + 4 <= size, 'invalid relocation offset')
        require(struct.unpack_from('<I', raw, 24 + offset)[0] <= span, 'relocation target exceeds span')


def validate(path, blob_path=None):
    data = obj(json.loads(bounded_read(path).decode('utf-8-sig'), object_pairs_hook=unique_object), 'manifest')
    require(data.get('deviceAccess') is False, 'deviceAccess must be false')
    require(data.get('hardwareGatesAdvanced', []) == [], 'host evidence cannot advance gates')
    if 'managedHostAppStaged' in data:
        require(type(data['managedHostAppStaged']) is bool, 'invalid staging flag')
    require(data.get('hbappConsecutiveBuildsEqual') is True, 'build equality not established')
    require(isinstance(data.get('nanoAppsCommit'), str) and re.fullmatch(r'[0-9a-f]{40}', data['nanoAppsCommit']), 'invalid upstream commit')
    sources = obj(data.get('sources'), 'sources')
    require(bool(sources), 'no pinned sources')
    for source, value in sources.items():
        require(bool(source.strip()), 'empty source name')
        digest(value)
    audit = obj(data.get('blobAudit'), 'blobAudit')
    require(audit.get('deviceAccess', False) is False, 'audit reports device access')
    digest(audit.get('sha256'))
    for key in ('bytes', 'imageBytes', 'spanBytes', 'arenaAllocationBytes', 'entryOffset', 'bssBytes', 'relocations'):
        value = audit.get(key)
        require(type(value) is int and 0 <= value <= LIMIT, 'invalid ' + key)
    require(audit['imageBytes'] > 0 and audit['entryOffset'] % 2 == 0 and audit['entryOffset'] < audit['imageBytes'], 'invalid audit entry')
    require(audit['imageBytes'] + audit['bssBytes'] == audit['spanBytes'], 'invalid BSS/span')
    require(audit['arenaAllocationBytes'] == audit['spanBytes'] + 16, 'invalid pinned loader arena')
    require(audit['bytes'] == 24 + audit['imageBytes'] + 4*audit['relocations'], 'invalid audit extent')
    profiles = []
    if 'outputs' in data:
        output = obj(obj(data['outputs'], 'outputs').get('nami.hbapp'), 'outputs.nami.hbapp')
        require(output.get('sha256') == audit['sha256'] and type(output.get('bytes')) is int and output['bytes'] == audit['bytes'], 'output and audit disagree')
        profiles.append('outputs')
    if 'package' in data:
        package = obj(data['package'], 'package')
        if 'package' in package:
            require(package.get('deviceAccess') is False, 'package reports device access')
            equal = package.get('packageTreesEqual')
            package = obj(package['package'], 'package.package')
        else:
            equal = data.get('packageTreesEqual')
        require(equal is True, 'package equality not established')
        for key in ('AllApps.pack', 'Executables/NAMI.hbapp', 'Icons/NAMI.bin'):
            digest(package.get(key))
        require(package['Executables/NAMI.hbapp'] == audit['sha256'], 'package/audit hash mismatch')
        profiles.append('package')
    require(bool(profiles), 'unsupported manifest: requires outputs or package')
    if blob_path is not None:
        check_blob(blob_path, audit)
    return {'result': 'PASS', 'profiles': profiles, 'version': data.get('version'),
            'appSha256': audit['sha256'], 'bytes': audit['bytes'],
            'arenaAllocationBytes': audit['arenaAllocationBytes'], 'artifactVerified': blob_path is not None,
            'managedHostAppStaged': data.get('managedHostAppStaged', 'UNDECLARED'),
            'limitations': 'No source/ELF verification, ARM execution, identity, authorization or hardware proof'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--blob', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.manifest, args.blob), indent=2))
    except (OSError, ValueError, TypeError, RecursionError, struct.error) as error:
        print(json.dumps({'result': 'FAILED', 'reason': str(error)}, indent=2))
        raise SystemExit(1)
