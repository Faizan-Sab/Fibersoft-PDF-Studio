# AI Talk

Shared Markdown notes for working with AI assistants on Fibersoft PDF Studio.
Keep project context here so a new conversation can continue from the last session.

## Understanding the application

Start with **[How Fibersoft works](HOW_FIBERSOFT_WORKS.md)** for the complete flow
from designing a format to printing a PDF. These guides describe the local 1.8.0
source reviewed on 2026-10-05.

| Guide | Purpose |
| --- | --- |
| [HOW_FIBERSOFT_WORKS.md](HOW_FIBERSOFT_WORKS.md) | Architecture, document/report printing, composition and storage |
| [FILE_MAP.md](FILE_MAP.md) | All 93 original files, their roles, and Python symbol navigation |
| [DATA_AND_LAYOUT.md](DATA_AND_LAYOUT.md) | DocTypes, JSON example, blocks, field binding, fonts and images |
| [FRONTEND_AND_AI.md](FRONTEND_AND_AI.md) | Editor state, bridge messages, templates, history and Gemini flow |
| [API_REFERENCE.md](API_REFERENCE.md) | Endpoint inputs, outputs and access-check differences |
| [OPERATIONS.md](OPERATIONS.md) | Installation, configuration, queues, CI and troubleshooting |
| [CODE_CAVEATS.md](CODE_CAVEATS.md) | Static findings, likely defects and behavior that needs runtime verification |

The review includes an inventory of every original file. Binary fonts/screenshots
were cataloged, not visually inspected. No live Frappe or Gemini tests were run.

## Files

| File | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Instructions for maintaining these notes |
| [PROJECT.md](PROJECT.md) | Project overview, source map, and validation guidance |
| [TASKS.md](TASKS.md) | Requested work and its status |
| [DECISIONS.md](DECISIONS.md) | Agreed decisions and their reasons |
| [HANDOFF.md](HANDOFF.md) | Latest session outcome and next steps |

## Starting a conversation

Copy this message and add your request:

> Read `ai talk/README.md`, `ai talk/AGENTS.md`, `ai talk/PROJECT.md`,
> `ai talk/HOW_FIBERSOFT_WORKS.md`, `ai talk/CODE_CAVEATS.md`,
> `ai talk/TASKS.md`, and `ai talk/HANDOFF.md` for context. My task is: [describe
> the change and the expected result]. After working, update the task status and
> handoff with what changed and what was verified.

These are ordinary project files. Assistants do not necessarily read this folder
automatically; explicitly point them here. The AGENTS.md in this folder applies
to this folder, not automatically to the entire repository.

## Keeping notes useful

- Record confirmed facts and distinguish proposals from accepted decisions.
- Keep the latest session summary in HANDOFF.md and ongoing work in TASKS.md.
- Link to source files instead of copying large sections of code.
- Never store passwords, API keys, private customer documents, or credentials here.
- Update notes when the code changes so future conversations use current context.
