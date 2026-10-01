# Agent handoff and invocation

## Start in the project, locate the skill separately

An installed copy belongs at `$CODEX_HOME/skills/nami-ipod-lab` (or
`~/.codex/skills/nami-ipod-lab` when CODEX_HOME is unset). This repository's
`skills/nami-ipod-lab` is a source copy; its presence alone does not register a
skill with Codex. Refresh/restart the session after installation. Explicit
invocation is `$nami-ipod-lab`; automatic discovery uses the description.

If discovery is unavailable in an already running session, read the absolute
SKILL.md path directly and follow it for the current request. Do not claim the
session's skill catalog was refreshed merely because files were copied.

## Minimum project context

Read AGENTS.md, README, product/architecture/security/testing rules, current
RESUME, hardware evidence, selected backlog and relevant ADR/experiment. Respect
user steering and current authorization; historical recommendations may be
superseded. Preserve unrelated working-tree changes.

Record: project root, skill root, approved task, last installed version/hash,
known-working evidence, external backup location, exact authorization scope,
current target identity requirements and the next uncompleted acceptance gate.
No serial, credentials or private recovery path goes into public documentation.

## Adapter map in the NAMI project

These are **project-relative discovery hints**, not bundled executors. Inspect
their current code and experiment before invocation; never hardcode a previous
drive, bus ID, Linux disk or this project's authorization on another device.

| Task | Project path | Boundary |
|---|---|---|
| Windows inspection | `services/device-service/platform/windows/inspect-device.ps1` | Read-only, fresh exact-target report |
| Trace capture/parser | `services/device-service/platform/capture_nano_trace.py`, `nano_trace.py` | Reviewed bounded read; private raw output |
| Player build | `apps/nano-runtime/motion-reaction/tools/build_offline.py` | External candidate output |
| Arcade build/package | `apps/nano-runtime/neon-orbit/build.py` | `--package` mutates managed host stage, no USB |
| HRL1 audit | `apps/nano-runtime/hiyori-player/tools/audit_blob.py` | Actual ELF/blob consistency |
| ARM execution | `apps/nano-runtime/hiyori-player/tools/emulate_launch.py` | Synthetic memory/input only |
| Install procedure | Current experiment and pinned upstream installer | Exact-target authorized writes only |

If an adapter is absent, report precisely what is unavailable. Continue source
review, test planning and candidate preparation where possible; do not invent a
generic flashing command or recreate an unreviewed executor.

## Evidence lessons from the October 1 arcade update

The checked three-game app had exact readback and an owner report of normal
launch. That proves an observed launch, not endurance, all game controls or cold
boot. An upstream installer also attempted apt dependency bootstrap despite
offline Cargo settings. Preflight its entire dependency path before the next
device operation. A prior wrapper exit error after successful installation was
resolved by original logs/readback, without repeating the device write.

## Useful invocation requests

```text
Use $nami-ipod-lab to review this build manifest and candidate blob offline.
Use $nami-ipod-lab to diagnose a reboot; preserve evidence and do not reinstall.
Use $nami-ipod-lab to prepare the next checked app update under the project's
existing authorization, stopping before any effect outside that scope.
```
