# Tasks

## Active

No active work remains. Local Fibersoft rename and validation are complete.

## Completed

- [x] Rename the application from its original branding to Fibersoft.
  - Date: 2026-10-06
  - Request: replace ERPNext labels, use Fibersoft PDF Studio / Print with
    Fibersoft, and carefully replace the remaining original app name.
  - Acceptance criteria: consistent visible branding, package/module names,
    routes, DocTypes, assets, RPC messages, config and documentation.
  - Deliverables: `fibersoft/` application package; updated packaging, CI,
    installation instructions and technical guide links.
  - Validation: all 25 Python modules parsed; JavaScript, JSON and TOML syntax
    checked; 190 local Markdown links resolve; independent reference review
    verified methods, RPC allowlist, messages, DocTypes, pages and assets.
    Config precedence and feedback behavior checked with a minimal Frappe adapter;
    browser draft/preference transfer checked in Node for old/new values and
    blocked localStorage.
  - Limitations: no live Frappe installation or PDF/AI flow was exercised.
    Existing sites need the fresh-install procedure in CUTOVER.md. Original legal
    attribution and legacy config/browser-storage migration keys remain.

- [x] Review the Fibersoft source and save an explanation of how it works.
  - Date: 2026-10-05
  - Acceptance criteria: document architecture, original files, data/layout model,
    frontend, AI, APIs, PDF/report flows, configuration, and relevant code caveats.
  - Deliverables: seven linked technical guides indexed in README.md.
  - Coverage: 93 original files inventoried; all 54 original text files decoded;
    25 Python files parsed. Binary assets cataloged without visual inspection.
  - Validation: local source tracing, gallery counts, Python AST parsing, Markdown
    links and fenced JSON examples checked. Live Frappe/PDF/AI tests not run.
  - Follow-ups: CODE_CAVEATS.md contains findings, not authorized fix tasks.

- [x] Set up the `ai talk` folder with Markdown context and collaboration notes.
  - Date: 2026-10-05
  - Acceptance criteria: provide a folder guide, AI instructions, project context,
    task tracker, decision log, and session handoff.

## Template for the next request

```md
### Task: [short title]
- Status: Pending / In progress / Blocked / Complete
- Request: [what the user wants]
- Acceptance criteria: [observable result]
- Relevant files: [paths]
- Validation: [checks and actual results]
- Remaining work: [next steps or none]
```
