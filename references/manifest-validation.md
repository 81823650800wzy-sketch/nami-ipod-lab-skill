# Offline manifest validation

Use Python 3.10+ and the absolute skill folder; no third-party packages required:

```powershell
python "$skillDir/scripts/validate_evidence.py" "$manifestPath"
python "$skillDir/scripts/validate_evidence.py" "$manifestPath" --blob "$blobPath"
python "$skillDir/scripts/doctor.py"
python "$skillDir/scripts/test_validate_evidence.py"
```

Set the variables to actual local paths first. Helpers have no USB, network or
dependency-install behavior. PASS exits 0; invalid inputs exit 1 with JSON.

Accepted families:

- Motion-player: `outputs.nami.hbapp` has `sha256` and `bytes`; optional nested
  `package` contains `deviceAccess:false`, `packageTreesEqual:true` and `package`.
- Arcade: top-level `packageTreesEqual:true` and `package` map the three NAMI
  files to hashes. It may omit `outputs` and the old staging flag.

Both require `deviceAccess:false`, a 40-character lowercase upstream commit,
nonempty source-hash map, `hbappConsecutiveBuildsEqual:true` and `blobAudit` with
SHA-256, bytes, entryOffset, imageBytes, spanBytes, bssBytes,
arenaAllocationBytes and relocations. Supplied hardwareGatesAdvanced must be
empty. A supplied staging flag must be boolean; host staging is allowed and
reported, since staging is distinct from device access. Missing staging is
reported UNDECLARED, never converted to a no-side-effects claim.

Pinned HRL1 requires bytes = 24 + imageBytes + 4*relocations,
span = imageBytes + bssBytes, arena = span + 16 and an even entry inside the
image. A packaged app must match the audit hash. Unknown shapes fail.

`--blob` verifies the actual SHA-256, header, extents, relocation offsets and
target bounds. It does not replace the project's ELF audit, source-hash checks
or runtime tests. The 2 MiB parser bound is not a safe Nano app size. Duplicate
JSON keys, malformed types and mismatches are rejected. Consistency cannot
authenticate a forged manifest or prove its claimed tests actually ran.
