# Builder frontend and AI copilot

Reviewed 2026-10-05. Source: [builder HTML](../fibersoft/public/builder/index.html),
[Desk host](../fibersoft/fibersoft/page/fibersoft_builder/fibersoft_builder.js), and
[ai.py](../fibersoft/ai.py).

## Browser structure

`/app/fibersoft-builder` is a System Manager Desk page. Its JavaScript creates an
iframe pointing at `/assets/fibersoft/builder/index.html`. That HTML contains the
editor markup, CSS, dialogs, template definitions, and JavaScript. It is not a
React/Vue application and does not have a separate frontend dependency manifest.

The host loads an active design and field metadata, mirrors the Desk theme, and
handles file uploads, fullscreen, saving, and real PDF previews. The HTML can also
open as a standalone demo, but its normal server RPC returns null outside the
iframe. Demo Save logs a definition; it does not persist to a Frappe database.

## State and editing

The main `state` contains target DocType, target kind, report name, page settings,
header, footer, watermark, branding, and blocks. UI state includes selection,
editing scope, panel tabs, zoom, save/dirty flags, and format-manager company scope.

| Code area | Role |
| --- | --- |
| `DSET`, `dstyle`, `mk`, `childMk` | Create block settings, styles and temporary IDs. |
| `R`, `tblSkin`, `dtCellHtml`, `styleCss`, `cellCss` | Browser-side block and style rendering. |
| `_renderNow`, `flowBlk`, `absBlk` | Assemble the canvas, flowing body, positioned blocks and bands. |
| `computeBreaks` | Measure offscreen DOM and estimate page cuts at block/table-row boundaries. |
| `renderProps`, `renderPage`, `renderBrand` | Build the inspector controls. |
| `recordHistory`, `resetHistory`, `undo`, `redo` | Snapshot history, capped at 80 entries. |
| `autosaveNow`, `restoreDraft`, `clearDraft` | Maintain the local browser draft. |
| `definition`, `loadDefinition` | Serialize saved JSON and rebuild editable state. |
| `rpc`, `uploadImage` | Request services from the Desk host. |

The render scheduler coalesces changes at roughly 120 ms intervals and avoids
replacing the DOM while inline editing is active. Typing/dragging history is
debounced at 450 ms. Autosave waits 700 ms and also runs when the page hides.

Normal body dragging reorders blocks. Header/footer and floating-block dragging
changes coordinates and uses 2 mm snapping. Row dividers resize adjacent columns.
Leaf blocks can move into row cells or back out into the body. The palette,
inspector, inline editing, and Layers rail all modify the same state.

Layers groups header/body/footer, includes floating blocks, and controls hiding
and locking. Hidden blocks remain ghosted in the canvas but are excluded by the
server's top-level visibility logic. Locked blocks remain printable.

`computeBreaks()` is a browser approximation. The real Preview PDF runs the server
renderer and composer. Fonts, real data, hidden blocks, conditions, engine support,
and band repetition can make that PDF differ from the canvas.

## Creating, loading, and saving a format

The wizard has three steps: choose document/report target, choose a starting
point, then name the new format. Starting points include blank, bundled studio
templates, saved formats, site gallery, and imported JSON.

`FORMATS` currently contains 19 document starters, including the bilingual
Merchant Statement and Tax Invoice layouts. `REPORTFORMATS` has eight report
starters: Sterling, Equinox, Horizon, Compass, Summit, Keystone, Cascade, and
Harbor. These are JavaScript definition factories, not preinstalled Template
database records. Report starters style the report selected by the user; their
names do not themselves run a different report.

The home screen calls `api.home_formats()`, displays visual formats as cards,
and filters by document/report and name. A design pushed by the host on boot
opens directly instead of leaving the home overlay visible.

The first Save opens a name/default dialog. The iframe sends `fibersoft-save`;
the host calls `save_format` and replies with `fibersoft-saved`. If the user chose
to make it default, a separate set-default RPC follows the successful reply.
The server stores JSON in a Fibersoft Template. Setting the default is distinct
from enabling native Print > PDF replacement.

**My blocks** are database snippets. Adding one deep-copies its JSON and generates
new IDs, so later snippet edits do not change formats that already used it.
Ready sections are similar groups generated directly in JavaScript.

Export downloads JSON. Import parses a local JSON file and checks for a `blocks`
array, then loads it into the editor; saving to the site is a later action.

## Browser/server message contract

| Message | Direction / purpose |
| --- | --- |
| `fibersoft-rpc` | Iframe to host: method, args, request ID. |
| `fibersoft-rpc-res` | Host to iframe: request ID, success flag, result. |
| `fibersoft-save` / `fibersoft-saved` | Save definition and acknowledge success/failure. |
| `fibersoft-load` | Host supplies a saved definition. |
| `fibersoft-fields` | Host supplies document field metadata. |
| `fibersoft-preview` | Queue an unsaved document-layout PDF, then poll. |
| `fibersoft-preview-report` | POST an unsaved report layout and open the returned PDF blob. |
| `fibersoft-upload` / `fibersoft-upload-res` | Host opens Frappe FileUploader and returns an uploaded path. |
| `fibersoft-theme` | Mirror light/dark theme. |
| `fibersoft-fullscreen` | Expand or restore the iframe. |

The host validates both the sender origin and iframe window and permits only
methods in its `ALLOWED` table. The iframe receiver checks origin. Adding an API
method alone is insufficient for browser RPC: it also needs the host allowlist.
The generic iframe RPC timeout is 15 seconds.

## What the AI does

The copilot supports `edit`, `create`, and `clone`. It makes a synchronous request
to Gemini and returns a new definition. It does not execute generated Python,
run SQL, or directly save a format. The user can inspect the resulting canvas and
save it through the normal format API.

1. `openCopilot()` checks `ai_status()` and offers key/model configuration.
2. `cpRun()` sends the instruction, current JSON, target DocType, and optionally
   clone text or a reference image/PDF.
3. `ai_format()` enforces System Manager, resolves the key, validates attachment
   type/base64/size, and builds a prompt.
4. The prompt includes `SCHEMA_BRIEF`, available fieldnames and child-table
   metadata, the instruction, and mode-dependent current/sample JSON.
5. `_generate()` calls Gemini's `generateContent` endpoint, requests JSON output,
   and uses temperature 0.25. Each HTTP request has a 90-second timeout.
6. Certain HTTP failures trigger attempts with alternate model names. Key errors
   are reported without returning the key.
7. `sanitize_definition()` drops unsupported block types and style keys, clamps
   selected numbers, cleans nested structures, and returns a definition.
8. The frontend calls `loadDefinition()` to show it. The current load/history path
   has a caveat for the promised Ctrl+Z recovery; see the caveat guide.

The request is sent to Google's API. Current definitions, supplied reference
documents, and clone text can contain data; whatever the user supplies in those
inputs can enter the request. Metadata briefing itself sends fieldnames/labels,
not an automatically fetched full business document.

## AI configuration and limits in this checkout

| Setting/limit | Value or behavior |
| --- | --- |
| Key priority | AI Settings Password field, then `fibersoft_gemini_key` in site config. |
| Model | AI Settings `gemini_model`, otherwise the code's `gemini-flash-latest`. |
| Model discovery | Lists supported generateContent models for the configured key. |
| Instruction text | First 4,000 characters included in the prompt. |
| Reference attachment | Maximum 12 MiB decoded content. |
| Browser types | PNG, JPEG, WebP, PDF. |
| Server types | Browser types plus HEIC/HEIF; PDF signature checked. |
| Top-level AI blocks | At most 80 considered. |
| Row children | At most four cells and 20 children per cell; no nested Rows. |
| Settings cleanup | Depth and collection/string limits, rather than a strict per-block key schema. |
| Output target | Sanitizer forces document kind and clears report name. |

Model names here are strings in the repository, not a claim that those models
are currently available for a particular key. No external model calls were made
for this review.

## Where to change things later

- New block: update server `DEF_RENDERERS`, browser `META`/`DSET`/`R`, palette,
  inspector, row eligibility where appropriate, and AI allowlist/schema if desired.
- New styling control: implement both browser markup/CSS and Python rendering.
- New backend builder operation: add its API permission checks, host allowlist,
  and iframe RPC caller.
- Pagination change: inspect both `computeBreaks()` and Python `_flow_body_html()`/
  composition, and compare real PDFs rather than relying only on the canvas.
- New saved state: check serialization, loading, history, drafts, AI cleaning,
  and backward compatibility with existing definitions.
