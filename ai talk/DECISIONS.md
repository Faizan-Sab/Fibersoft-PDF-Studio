# Decisions

## 2026-10-06: Fibersoft application rename

- User direction: replace original visible branding and repeatedly replace the
  remaining original app name with Fibersoft.
- Assistant implementation choice: align app/package id `fibersoft`, module
  `Fibersoft`, seven config DocTypes, pages, assets, RPC messages and internal
  references with the new name. Treat this as a fresh-install change; no live
  site registration or database migration was performed.
- Keep original copyright/licence attribution and minimal legacy config/storage
  reads so branding changes do not misstate ownership or discard preferences.
- Feedback recipient: require `fibersoft_feedback_email`, with no inherited
  publisher email and no invented Fibersoft contact address.
- Deployment procedure: [CUTOVER.md](../CUTOVER.md).

## 2026-10-05: Markdown collaboration folder

- Request: The user asked for `.md` files in the existing `ai talk` folder.
- Implementation choice: Add a guide, folder instructions, project context,
  task tracker, decision log, and handoff notes.
- Reason: Give future AI conversations a clear starting point and a place to
  record progress.
- Scope: Documentation inside `ai talk/`.

## 2026-10-05: Source-based application guides

- Status: Accepted implementation choice for the user's documentation request.
- Decided by: Assistant organization of requested notes.
- Decision: Keep a plain-language overview with separate file, data, frontend/AI,
  API, operations and caveat guides.
- Reason: Future conversations can read the relevant area without rereading the
  whole source tree, while keeping static findings distinct from runtime results.
- Scope: Documentation only. Apparent defects are recorded as follow-up candidates;
  this request does not schedule code fixes.

## New decision template

```md
## YYYY-MM-DD: [decision title]
- Status: Proposed / Accepted / Superseded
- Decided by: [user or assistant implementation choice]
- Decision: [what was chosen]
- Reason: [why]
- Affected files: [links]
```
