# LookupOnlineId server compatibility — 2026-11-02

Source fix only; user explicitly requested no build.

The active BBGL NP client sends command 41 with a u32-LE-prefixed
LookupOnlineIdRequest (string npid, field 1). It expects a similarly prefixed
LookupOnlineIdReply (uint64 account_id field 1, canonical string npid field 2).
The server pinned by packaging/windows/build_coop_server.sh at
5a849a192fd4450593c57b10697316ac324c856e, with existing patches 0001/0005,
has neither this command nor its messages/handler. Authenticated command 41
falls into DispatchCommand's unknown-command branch, returning Invalid=2.
The client translates that to COMMUNITY_ERROR_BAD_RESPONSE. This is a concrete
client/package-server incompatibility; it does not prove which server binary
was running in the friends' recorded session or establish the cause of failed joins.

Added packaging/windows/shadnet-p2p/0006-lookup-online-id.patch. It adds the
command/messages and authenticated handler to the existing cmd_account.cpp
compilation unit. Lookup uses a bound, case-insensitive database query, returning
the same user_id used by login and the registered spelling of the username.
Offline accounts can resolve too; no online presence or friendship is required.
Malformed protobuf/framing returns Malformed; invalid IDs use the existing
registration validator and return InvalidInput; missing accounts return NotFound;
query errors return DbFail. No fallback fabricates account IDs or converts Invalid
to success. No room/signaling state or timeout changes.

The active BBGL client retains the requested name in its pending lookup entry
and logs it with user_id, packet ID and error. Invalid includes a hint to check
server command-41 support. Existing error-to-game mappings remain intact.

Validation: `python tests/test_lookup_online_id_protocol.py` — 4 tests PASS.
Tests extract the exact pinned source into a temporary directory and apply every
packaging patch in order, check dispatch/auth/error guards, cross-encode/decode
client/server schemas with protoc (including 64-bit IDs), and execute the handler's
SQL against a temporary SQLite database for canonical case, missing user and bound
input. These are source/protocol checks, not compiled handler/runtime validation.

No server/client/DLL/package build, install, VPS changes or game run. Activation
requires a later server build and installation on the hosting machine. A newer
client alone cannot add command support to an old server. Actual request names,
removal of Invalid replies and any effect on state4/30-second failed joins remain
for a later multiplayer run. Standalone/bundled BBSC sources and pin unchanged:
the affected server is built from BBGL's shadnet packaging patches.
