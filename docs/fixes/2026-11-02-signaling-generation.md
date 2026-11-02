# Intermittent join: stale signaling controls — 2026-11-02

Source fix only. No launcher/emulator/mod build, deployment or game launch.

## Evidence

Reviewed snapshot `coop-diagnostics/join-20261102-0603` and the existing
2026-11-01 slow-rejoin / 2026-11-02 launcher-network-join reviews.
The old stale broker claim and native role retry guard already have fixes in
both mod trees. Existing uncommitted emulator changes also retransmit readiness
and reduce keepalive interval 45s -> 5s; preserved and tested, not authored here.

Snapshot: connection 22089 is declared dead after 88s without signaling replies
at 06:02:47.407 although vport40 traffic continues. Fresh 22090 is mutually
activated at 06:02:57.460; native guest task closes it at 06:03:02.838 before
JoinRoom. Incoming peer Close follows, so stale Close is NOT proven as the cause
of that specific recorded rejection. The exact native rejection remains open.

## Fixed defect

HandleControlPacket selected a live connection solely by online ID. A delayed
ActivationAck, Established or Close carrying the previous peer connection ID
could change readiness or dispatch DEAD/PEER_DEACTIVATED for the replacement.
The control wire format already carries from_conn_id; now non-activation
controls require a known, matching peer_conn_id before any side effects.
ActivationRequest can still introduce a new generation and run the existing
restart handshake. No packet format, native timeout or mod policy changed.
An early Ack before the handshake learns peer identity can be ignored: Offer /
Accept / Check learn the identity independently, and handshake retries remain.

Scope: this protects controls, not arbitrary reordered Offer/ActivationRequest
packets that themselves introduce a new generation. It does not claim to solve
all native negotiation failures or establish the exact cause of every 1–2min join.

## Validation

`tests/test_signaling_generation.py`: actual production HandleControlPacket,
stale Ack/Established/Close, current Ack/readiness/Deactivate/Terminate,
new activation and old Close after restart, unknown peer generation. PASS.
Same fixture on HEAD baseline fails its stale-control assertion as expected.
Existing activation-race and readiness-loss production fixtures PASS.
Only isolated test executables compiled; no product build or installation.
Gameplay confirmation pending after a separately requested build.
