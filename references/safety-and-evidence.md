# Safety and evidence

## Evidence vocabulary

Use one status per hardware claim:

- `CONFIRMED`: reproducible direct evidence on the exact target, reviewed.
- `OBSERVED`: seen on the real target, but mechanism or repeatability remains incomplete.
- `INFERRED`: supported by source, specification, or reasoning only.
- `UNKNOWN`: insufficient evidence.
- `FAILED`: a defined experiment missed its acceptance criteria.

Always include the source and a reproducible artifact or procedure. Component
specifications do not prove programmable access from custom code. Emulator,
sanitizer, simulator, and desktop previews are software evidence only.

## Effect classes

| Class | Typical action | Required handling |
|---|---|---|
| Read only | metadata, hashes, bounded trace read | Fresh exact-target check; preserve raw capture |
| Logical app update | reviewed `/Apps` replacement and known filesystem step | Exact scoped authorization, package/readback hashes, rollback |
| System write | firmware, DFU, bootloader, partition, raw disk | Stop and obtain explicit authorization after review |
| Host binding | bind/unbind/install Windows driver | Separate explicit authorization and recovery plan |
| Soul recovery | restore authoritative identity/history | Separate workflow; never couple to app rollback |

Uncertain write behavior belongs in the system-write class until source review
proves otherwise. A tool named “inspect,” “repair,” or “install” is not evidence
of its effects; inspect its implementation and invocation.

## Exact-target fencing

Build a private identity fence from stable device/interface facts, then expose a
redacted digest in records. Independently verify on both host sides when USB
forwarding is used. Re-resolve after replug: Windows disk number, drive letter,
Linux block device, and bus ID are ephemeral.

Require a single candidate device, expected VID:PID, capacity, firmware, storage
layout and health. Verify the target is unmounted in Linux before direct access.
Never enumerate paths in one shell and construct a destructive command in another.

## Recovery and privacy

Recovery evidence distinguishes “artifact exists,” “ciphertext hash checked,”
“decryption streamed,” and “restore rehearsed.” Do not collapse these states.
Keep unique identifiers, raw traces, dumps, licensed character assets, firmware,
and personal memory outside Git. Public records contain schemas, procedures,
redacted facts and hashes only.
