# Repeatable workflows

## Read-only inspection

Read the repository's inspection adapter before use. Capture model, firmware,
capacity, filesystem, health, interface bindings and a redacted target key.
Record freshness. Do not add repair fallbacks to an inspection path.

If USB forwarding is needed, require an existing shared target unless driver or
share changes are explicitly in scope. Start an owned, bounded helper, attach
the freshly resolved bus ID, wait for enumeration, independently verify one
matching unmounted disk, and always detach owned forwarding in cleanup.

## Offline candidate

Pin the upstream revision and compiler. Copy reviewed inputs into a new external
candidate directory; do not mutate the only original or managed upstream checkout.
Record all source and generated-asset hashes.

Test pure policies, the actual composition root, malformed data, geometry,
framebuffer canaries, long callback sequences and the reported regression.
Use sanitizers where supported. Build twice and require byte equality. Audit the
relocatable image, entry point, relocation types, file size, image span, BSS and
total allocation. Compare against a target-observed working bound, not a guessed
hardware limit. An ARM emulator can detect unmapped access and compare guest
instruction counts; it cannot prove OS allocation, cache behavior, wall-clock
smoothness or launch stability.

## Package without device access

Verify the candidate manifest and current repository sources, stage only the
intended app, package twice, require identical trees, and confirm the packaged
executable hash equals the audited build. A content tool may generate a package
but must not silently install it.

## Controlled app update

Before the authorized write checkpoint:

1. Reinspect the exact target and current installed app hashes.
2. Verify the retained recovery artifact and known-working app candidate.
3. Verify pinned tracked upstream source and resident/tool hashes match. A known,
   hash-checked untracked managed app stage may be expected; unrelated changes
   invalidate the baseline. Inspect the installer preflight and dependency list.
   Resolve compiler, Python packages and any required Rust tools in the exact
   execution environment before attaching. `CARGO_NET_OFFLINE` only governs
   Cargo; it does not prevent an installer from invoking apt or downloading tools.
   Do not accept automatic dependency bootstrap as part of a device update.
4. Attach the exact existing share; verify a sole matching unmounted disk.
5. Run a fixed, bounded read-only readiness request and require exact length.
6. Execute one reviewed app-only install with a timeout and fixed offline tools.

Afterward, capture the resident trace before detach if supported. Detach, stop
only the owned helper, wait for the Windows volume, and hash every installed
package file. A successful installer exit without readback is incomplete evidence.

Capture the real child exit status. In PowerShell, a quoted Bash `$?` can be
expanded by the wrong shell; prefer a literal single-quoted Bash command and
record `$LASTEXITCODE` immediately after `wsl.exe`. Do not run the installer
again merely because an enclosing wrapper failed after it completed: inspect
the original log and actual readback first. Use a cleanup/finally path that runs
on success, failure and timeout. Start Windows helper processes hidden and track
their PID; never terminate unrelated WSL sessions. Wait for the expected volume
with a deadline rather than assuming a fixed sleep proves readiness.

## Diagnostic trace

Review the trace implementation and fixed RAM layout. Do not initialize or reset
the ring merely to make a read pass. Use a fixed address and bounded transfer
count through a reviewed read-only command. Retain every raw chunk, stderr,
assembled bytes and SHA-256 outside Git. Verify magic, index, total count and
header consistency. Ring `count` may be a lifetime total; valid entries are
`min(total, capacity)` ordered from `(write_index - valid_count) mod capacity`.

Label callback numbers as callbacks, not seconds. Sensor estimates are
uncalibrated until a separate experiment proves scale and timing. Logs can wrap,
survive a soft reset, or disappear on power loss; they are not durable memory.

## Physical acceptance

Ask for one concise, falsifiable check: launch/no reboot, repeated interaction,
idle period, intended sensor action, pause/wake, log view, or endurance. If the
device reboots, stop repetitions and preserve incident state. Record the owner
report as `OBSERVED`, including its limits; do not promote it to a mechanistic
or calibrated claim.
