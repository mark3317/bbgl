---
name: bbsc-items-design-decisions
description: "User's design rules for items in the BBSC co-op mod (guest pickups, gifts, home giving, repeats)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 958cbc2f-060b-413d-bd28-1369b87765e0
  modified: 2026-10-29T08:52:12.370Z
---

Items in the BBSC co-op (Bloodborne) are each player's own:
- A guest picks up everything itself, immediately in the host's world (consumables, weapons, attire, gems, runes, keys); the host and guests get equal rights.
- Minimize items a guest receives for the host's actions (shared keys/tools 0x29 are an accepted exception kept as a PT-1 workaround).
- Do not give items to a guest after it returns to its own world "if at all possible"; the check "does the guest have everything" belongs at the join to a host.
- Talk gifts (e.g. Valtr's Impurity rune) go only to the player who did the talk.
- Retro repair of lost items: only keys, workshop tools, hunter badges, chalices — not consumables or NPC quest hand-in items.
- A repeated one-time lot (item already owned): block it and log `BBSC CHECK FAIL K3-repeat`.

**Why:** stated by the user on 2026-10-29 while fixing K2/K3 (PT-1, PT-5); the home-giving rule had to be bent (silent put-back of picked key items, 2 min watch) because the game restores a cooperator's inventory from its join snapshot — see BBSC `docs/HANDOFF.md` §3.1.
**How to apply:** design any item/quest/reward change against these rules; if a rule can't be met, say so and explain, as was done for the home put-back. Related: [[bbsc-handoff-state]].
