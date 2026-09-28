---
name: nami-ipod-lab
description: Safely inspect, build, diagnose, install, verify, and document custom character applications for an iPod nano 7G using NanoApps-style workflows. Use for bounded app updates, launch failures, input or animation tuning, resident RAM traces, evidence capture, and recovery-aware experiment planning; do not use as permission for firmware, DFU, partition, bootloader, driver, or destructive storage changes.
---

# NAMI iPod Lab

Treat the iPod as a real device with a recoverable history, not as a generic
development board. Separate source evidence, host tests, installation evidence,
and owner-observed behavior. A successful build never proves hardware behavior.

## Route the request

1. Read [references/safety-and-evidence.md](references/safety-and-evidence.md)
   before any real-device operation or hardware claim.
2. For inspection, app builds, controlled updates, readback, or trace capture,
   read [references/workflows.md](references/workflows.md).
3. For reboot, missing icon, short trace, stutter, repeated actions, or poor
   image quality, read [references/troubleshooting.md](references/troubleshooting.md).
4. For repository documentation or public release, read
   [references/publishing.md](references/publishing.md).

## Working contract

- Discover and obey the target repository's `AGENTS.md`, architecture, evidence
  register, experiment template, accepted ADRs, and current resume point.
- Resolve the exact device afresh before every operation. Never infer identity
  from a drive letter, `/dev/sdX`, USB bus ID, or product name alone.
- Preserve an external, hash-checked recovery artifact. Never overwrite the
  only backup or place firmware, device dumps, personal logs, proprietary assets,
  serial numbers, Soul data, or credentials in Git.
- Stop for explicit owner authorization before firmware/DFU/bootloader/partition,
  raw-disk, uncertain-write, destructive repair, driver, or Soul-restore work.
  A project may record narrower standing authorization for checked app updates;
  verify that exact scope instead of assuming it applies.
- Keep upper runtime code behind HAL ports. Put concrete NanoApps calls in the
  Nano adapter or composition root. Diagnostic logs are observations, not Soul
  memory, identity, presence authority, or a USB application protocol.
- Before a device update, require pinned sources/toolchain, native tests,
  reproducible builds, a binary/relocation audit, measured size/arena bounds,
  an experiment record, exact candidate hashes, and a known rollback artifact.
- Perform at most the reviewed operation count. Abort on mismatch, timeout,
  reboot, short transfer, ambiguous target, mounted Linux target where unmounted
  access is required, or any unplanned side effect. Do not hide a failure with
  retries.
- After an update, detach only forwarding owned by the current run, wait for the
  Windows volume to return, hash the actual installed files, capture volatile
  trace evidence when available, and request one bounded physical observation.

## Outputs

Leave a reviewable chain: source hashes, tool versions, tests, binary hash and
allocation, package hashes, exact target facts with private identifiers redacted,
operation log, device readback, trace hash, owner observation, evidence status,
and remaining unknowns. Update the experiment, hardware evidence, changelog,
and resume point when the repository uses them.

Use `scripts/validate_evidence.py <manifest.json>` to sanity-check a portable
offline build manifest before packaging. This helper does no device access.
