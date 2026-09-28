<p align="center"><img src="assets/nami-ipod-lab.svg" alt="NAMI iPod Lab" width="100%"></p>

# NAMI iPod Lab Skill

**Turn iPod nano 7G character-app experiments into reproducible engineering.**

This Codex-compatible Skill teaches an agent how to inspect, build, diagnose,
update, verify, and document a NanoApps-style application while respecting the
line between a host test and evidence from a real device.

它整理了 NAMI 项目在真机迭代中形成的方法：精确识别设备、离线复现构建、
二进制审计、受控应用更新、USB 只读日志、安装后回读、故障停止条件，以及
`CONFIRMED / OBSERVED / INFERRED / UNKNOWN / FAILED` 五级证据表达。

> This repository contains an agent workflow, documentation, and an offline
> manifest checker. It contains no firmware, exploit payload, device dump,
> proprietary character asset, private log, recovery archive, or Soul data.

## Why this exists

Small-device work fails when “compiled,” “installed,” “appeared once,” and
“works reliably” are treated as the same fact. This Skill keeps them separate.

```mermaid
flowchart LR
  A[Pin sources and tools] --> B[Regression tests]
  B --> C[Build twice]
  C --> D[Audit image and allocation]
  D --> E{Authorized device scope?}
  E -->|No| F[Reviewable candidate]
  E -->|Yes| G[Fresh exact-target inspection]
  G --> H[One bounded app update]
  H --> I[Read back installed hashes]
  I --> J[Capture trace]
  J --> K[Owner observation]
  K --> L[Record status and unknowns]
```

## What another Agent can do

- investigate a missing icon or reboot without blindly reinstalling;
- build and audit a bounded character-app candidate offline;
- stop touch, button, or motion noise from restarting animations;
- capture a volatile resident trace without calling it persistent memory;
- improve animation work or spatial resolution without hiding frame loss;
- prepare a controlled app-only update with exact readback;
- publish honest hardware evidence and a resumable experiment record.

## Install and invoke

Clone this repository directly into your Codex skills directory:

```powershell
git clone https://github.com/81823650800wzy-sketch/nami-ipod-lab-skill.git `
  "$env:USERPROFILE\.codex\skills\nami-ipod-lab"
```

Restart or refresh Codex, then invoke it:

```text
Use $nami-ipod-lab to diagnose why my NanoApps character animation restarts.
```

Automatic discovery remains enabled. More examples:

```text
Use $nami-ipod-lab to prepare a device-free candidate and evidence manifest.
Use $nami-ipod-lab to review this launch reboot without touching the device.
Use $nami-ipod-lab to design a read-only resident trace experiment.
Use $nami-ipod-lab to turn these test results into honest hardware evidence.
```

## Skill map

| Resource | Purpose |
|---|---|
| `SKILL.md` | Routing, invariants, stop conditions, output contract |
| `references/safety-and-evidence.md` | Device actions and hardware claims |
| `references/workflows.md` | Inspection, build, package, update, trace, acceptance |
| `references/troubleshooting.md` | Reboot, missing icon, short trace, stutter, noise, pixelation |
| `references/publishing.md` | Public documentation and claim discipline |
| `scripts/validate_evidence.py` | Offline build-manifest consistency check |

## Validate

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\nami-ipod-lab
python .\nami-ipod-lab\scripts\validate_evidence.py .\build-manifest.json
```

The helper checks manifest consistency only. It cannot prove source integrity,
device identity, authorization, installation, performance, or safety.

## Safety boundary

The Skill requires fresh target resolution and separate authorization for
firmware, DFU, bootloader, partition, raw-disk, uncertain-write, destructive
repair, Windows driver, or Soul-restore work. It never turns a prior app-update
permission into blanket hardware authority.

Drive letters, `/dev/sdX` nodes, USB bus IDs, and product names are temporary
observations. A real workflow binds multiple independent facts, preserves a
recovery artifact, bounds operation counts, and stops on mismatch.

## Evidence, not mythology

The method came from a NAMI prototype that reached real iPod display, touch,
buttons, animation, motion sampling, a local event screen, and resident trace
capture. These are bounded observations. Autonomous cold boot, durable on-device
Soul memory, framed bidirectional USB transport, local voice, and final character
embodiment remain separate gates until direct evidence exists.

The workflow builds on the MIT-licensed
[NanoApps project pinned at `80d439d`](https://github.com/nfzerox/NanoApps/tree/80d439da4d9a7236501f4c23c188f226ad4a1ad2).
Source availability does not prove compatibility with a particular iPod revision
or firmware.

## License

The Skill's original instructions, helper, and artwork use the MIT License.
Third-party projects and assets retain their own licenses.
