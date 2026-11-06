---
name: reticle
description: Verify a change against the running app, from inside it, before calling it done.
---

Reticle exposes the running app to you as `reticle_*` MCP tools. Look, act, observe, assert.

Only `reticle_act_and_wait` and `reticle_assert` produce a verdict. Everything else moves or
reads the app and proves nothing, so a drive that ends without one of those has no result however
many tools it used.

`verified: "unknown"` is not a pass: it means Reticle could not tell what happened.
`verified: "no-fault"` is not a pass either, because nothing was declared to prove. Never weaken a
check to make it pass.

The cheapest path that answers the question:

- "did my edit break anything?" -> `reticle_verify { action: "change", files: [...] }`
- "does this known journey still work?" -> `reticle_verify { action: "flows", names: ["..."] }`
- "does this new behaviour work?" -> `reticle_act { steps: [...] }` for the setup, then ONE `reticle_act_and_wait`
- "nothing is recorded yet" -> drive the journey yourself with `reticle_act_and_wait` and an `until` on its
  last step; it is saved as a flow, so the next run replays with no model in the loop. With a linked
  project, `reticle_verify { action: "explore", persona: "<who does what>" }` drives it for you
