# Troubleshooting routes

## App icon disappears after reboot

Distinguish app-file persistence from volatile registration. Hash `/Apps` after
the event. If files remain but registration is absent, document the volatile
resident limitation. Do not call this autonomous boot. Re-registration is an
interim development workflow, not completion of cold-boot HOME.

## Launch causes reboot

Stop repeated launches. Capture resident trace and installed-file hashes before
rollback. Compare file size, image span, BSS, total arena and relocation table
with a known-working binary. Emulate the exact blob at multiple bases, but keep
the cause `UNKNOWN` unless direct evidence establishes it. Optimize a separate
candidate, then use one bounded physical launch check.

## Trace is four bytes, short, or has bad magic

Treat it as unavailable, not empty. Confirm the runtime handler is ready through
the documented benign UI transition or replug procedure; then perform a new
bounded read only if permitted. Never parse partial data, inject blindly, reset
the ring, or claim readiness from a successful USB attach alone.

## Actions repeatedly restart

Instrument raw and accepted input separately. Qualify both press and release,
emit a single rising edge, and discard new action requests while a response is
active. Preserve pause/wake position. Test contact chatter, held contact, noisy
release, simultaneous input and one intentional action against the actual
composition. Do not blame motion noise when touch/button edges remain untested.

## Sensor numbers drift at rest

Avoid redrawing numeric text every callback. Add bounded filtering, stable-center
qualification, hysteresis, cooldown and invalid-sample reset in a pure policy
behind the HAL. Suppress automatic reactions during active animation, pause,
quiet mode and log view. Keep units explicitly uncalibrated.

## Animation is choppy

Measure guest work and framebuffer writes. Eliminate per-output-pixel division,
reuse duplicated expanded rows, avoid unchanged status redraws and decode only
when the displayed frame changes. Preserve visual equivalence and test decoder
bounds. Host instruction counts are comparative evidence, not FPS.

## Image is pixelated

Separate stored resolution from output geometry. Inspect which source frames the
accepted runtime can actually reach. A higher-resolution visible working set may
fit when unreachable frames are excluded, provided mapping, response frames,
blink, timing, attribution and original archive remain intact. Test exact pixel
mapping, allocation and startup cost. Do not advertise nearest-neighbor scaling
as native resolution or silently reduce visible motion.

## USB capture works only sometimes

USB attach can complete before storage enumerates. Wait for enumeration with a
short deadline; retry enumeration only. Do not retry a device transfer, target
mismatch, corrupt header or short read automatically. Preserve the first failed
capture as evidence and detach owned forwarding in all paths.
