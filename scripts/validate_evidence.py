#!/usr/bin/env python3
"""Validate a portable offline NAMI/Nano app evidence manifest; no device I/O."""
import argparse,json
from pathlib import Path

def validate(path):
    data=json.loads(path.read_text(encoding='utf-8'))
    required=('deviceAccess','managedHostAppStaged','hardwareGatesAdvanced',
              'nanoAppsCommit','sources','hbappConsecutiveBuildsEqual','blobAudit','outputs')
    missing=[name for name in required if name not in data]
    if missing:raise ValueError('missing fields: '+', '.join(missing))
    if data['deviceAccess'] is not False or data['managedHostAppStaged'] is not False:
        raise ValueError('offline manifest reports a device or staging side effect')
    if data['hardwareGatesAdvanced']!=[]:raise ValueError('host build cannot advance hardware gates')
    if data['hbappConsecutiveBuildsEqual'] is not True:raise ValueError('reproducible build not established')
    blob=data['blobAudit'];output=data['outputs'].get('nami.hbapp',{})
    for field in ('sha256','bytes','arenaAllocationBytes'):
        if field not in blob:raise ValueError('blobAudit missing '+field)
    if output.get('sha256')!=blob['sha256'] or output.get('bytes')!=blob['bytes']:
        raise ValueError('output and audit disagree')
    if len(blob['sha256'])!=64 or any(c not in '0123456789abcdef' for c in blob['sha256']):
        raise ValueError('invalid SHA-256')
    if not data['sources']:raise ValueError('no pinned sources')
    return {'result':'PASS','version':data.get('version'),'appSha256':blob['sha256'],
            'bytes':blob['bytes'],'arenaAllocationBytes':blob['arenaAllocationBytes'],
            'limitations':'Manifest consistency only; no source, binary, device, or authorization proof'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('manifest',type=Path);args=parser.parse_args()
    try:print(json.dumps(validate(args.manifest),indent=2))
    except (OSError,ValueError,json.JSONDecodeError) as error:
        print(json.dumps({'result':'FAILED','reason':str(error)},indent=2));raise SystemExit(1)
