# How Fibersoft PDF Studio works

Source review: 2026-10-05. Local application version: **1.8.0**.
This explains the checked-out code, not a running site's configuration. Runtime
behavior has not been tested on a Frappe site during this documentation task.

## Read this first

Fibersoft is a Frappe application that turns business records and report results
into branded PDFs. A designer builds a format from blocks. The app stores the
format in the site's database as JSON. When someone prints, Python fills those
blocks with real data, makes HTML, asks a PDF engine to render it, and assembles
the final pages.

The builder's AI copilot is optional. It helps create or change the layout JSON;
ordinary editing and printing do not require an AI call.

| Guide | What it explains |
| --- | --- |
| [FILE_MAP.md](FILE_MAP.md) | Every repository file and the important code entry points |
| [DATA_AND_LAYOUT.md](DATA_AND_LAYOUT.md) | Database records, JSON definitions, blocks, fields, and styling |
| [FRONTEND_AND_AI.md](FRONTEND_AND_AI.md) | Builder state, editing, browser/server bridge, and Gemini |
| [API_REFERENCE.md](API_REFERENCE.md) | Callable endpoints grouped by purpose |
| [OPERATIONS.md](OPERATIONS.md) | Configuration, installation, validation, and troubleshooting |
| [CODE_CAVEATS.md](CODE_CAVEATS.md) | Differences, limitations, and apparent defects found in source |

## The main parts

| Part | Responsibility |
| --- | --- |
| Frappe Desk | Login, roles, records, routing, uploads, email, queues, and file access |
| Builder iframe | Interactive canvas, templates, settings, local drafts, and JSON export |
| Builder host page | Bridges iframe messages to approved Frappe methods |
| API | Saves layouts, selects formats, checks print access, and starts jobs |
| Resolver | Chooses a mapping/template and company branding |
| Block engine | Turns layout blocks and document values into HTML |
| Composer | Renders body pages and overlays repeated bands and watermarks |
| Renderer | Converts HTML into PDF bytes through the selected engine |
| Background job | Runs document printing, saves a private File, and updates job status |

There is no separate Node application or frontend package.json in this checkout.
The main editor is a large HTML file containing its own CSS and vanilla JavaScript.
Frappe supplies the surrounding application and asset system.

## A document's complete journey

1. `hooks.py` loads `public/js/fibersoft_button.js` into Desk. That script asks
   `api.enabled_doctypes()` where the feature is enabled and adds form and list actions.
2. On a saved document, **Print with Fibersoft** routes to
   `/app/fibersoft-print/<doctype>/<name>`.
3. The print page asks `api.list_formats()` for formats and selects the marked
   default, or the first available format. It holds rendered files in browser memory.
4. Selecting an uncached format calls `api.request_pdf(doctype, name, template)`.
   `_authorize()` checks login, enabled DocType, document read permission, and print permission.
5. `_fresh_render()` looks for a recent attached file matching the document and
   format filename suffix. A hit returns file information immediately. Otherwise,
   the API stores a queued status and enqueues `pdf_job.generate` on the `long` queue.
6. The worker acquires a render slot, switches to the requesting user, loads the
   document, repeats the permission checks, and applies field-level read permissions.
7. `compose.compose_pdf()` resolves the requested or mapped template and renders it.
8. `_save_private_file()` inserts a private Frappe File attached to the original
   business record. Job status becomes `done`, including `file_url`, `file_name`,
   and `file_id`. Failures are logged and become an error status.
9. The browser polls `api.get_job_result()`. Only the user who owns the job can
   retrieve its status. It displays the actual PDF in an iframe once ready.
10. Print and download use that file. Email opens Frappe's CommunicationComposer
    with the File already attached; it does not automatically send the email.

Job states use Redis cache keys `fibersoft:job:<id>` and expire after 900 seconds.
This is transient job state, not a permanent job-history DocType.

## How the format is selected

An explicit template passed to document composition wins if its target DocType
matches the document. Otherwise `resolver.resolve_template()` checks enabled
Fibersoft Mapping records for that DocType:

- A mapping for the document's company takes precedence over a global mapping.
- A mapping belonging to a different company is excluded.
- Within that scope, lower `priority` wins; creation order breaks ties.
- All structured mapping conditions must match.
- A visual template yields a block definition; other templates yield a Jinja
  file path or a stored HTML/Jinja body.
- If nothing resolves, Quotation has a shipped Jinja fallback. Other DocTypes
  without a configured template raise an error.

Not every format-picker/default helper evaluates the same conditions. The print
screen also does not pass company to its initial format list. See the caveats
before assuming every entry point chooses an identical default.

Saving an existing format does **not** automatically replace an existing mapping.
Save bootstraps a mapping only when none exists for the target. The first-save UI
can separately call a set-default endpoint. Those are two distinct operations.

## How a multi-page PDF is assembled

The common visual definition has `layout: "absolute"`, but normal body blocks
still flow vertically. In `compose._compose()`:

1. Determine A4 portrait or landscape dimensions, side margins, and band heights.
2. Resolve company branding and per-format overrides. Remove hidden or conditionally
   excluded top-level blocks from the print.
3. Partition blocks into header, body, and footer. Sort non-floating body blocks
   by `pos.y`. Generate banner blocks from the effective company/format images.
4. Render the body as flowing HTML with space reserved for bands and their gaps.
   Tables can span pages; other top-level blocks are kept together when possible.
5. Read the resulting PDF to find the actual number of pages.
6. If configured, render a watermark page and place it behind each body page.
7. Render header/footer overlays and merge them above the body using pypdf.
   Repeating bands appear on every page. A non-repeating header appears on the
   first page; a non-repeating footer appears on the last.
8. Supply the current and total page counts when rendering page-number blocks.
   Reuse an overlay when its content does not require a new render.

The intended margin probe distinguishes engines that honor margins from engines
that need repeating table spacers. The current probe has an apparent missing
import, documented in [CODE_CAVEATS.md](CODE_CAVEATS.md).

If composition raises an error, the entry point logs it and attempts a single-pass
render. That fallback can keep a PDF available while losing the intended page
composition, so successful download alone does not prove correct layout.

## The three renderer choices

| Engine | Implementation |
| --- | --- |
| `frappe_chrome` | Default. Calls the host's `frappe.utils.pdf.get_pdf`, asking for Chrome when the function supports that argument. |
| `playwright` | Launches Chromium using Playwright, loads the generated HTML, waits for fonts, and calls `page.pdf()`. |
| `gotenberg` | Posts self-contained HTML to a configured Gotenberg service and returns the response bytes. |

The host renderer inspects landscape output. If the result is still portrait, it
tries pdfkit/wkhtmltopdf directly. The landscape verdict is cached for a day.
Migration clears both landscape and margin probe caches.

## Reports follow a different entry path

Reports have columns and rows rather than one business document. `report.py`
adapts them through `ReportDoc`, whose `_bpdf_report` payload contains the report
name, columns, formatted rows, filters, print date, and optional native HTML.

There are two paths:

- **Branded PDF toolbar button:** sends report name and current filters to
  `report.report_pdf()`. It checks report access, reruns the report through
  Frappe's query-report runner, normalizes values, and chooses a report mapping
  or a generated default layout. It renders synchronously and returns PDF bytes.
- **Native Report > PDF override:** receives already-rendered HTML. If any
  Fibersoft Settings row enables `brand_reports`, it wraps that HTML in branded
  bands. Otherwise it delegates to Frappe's native endpoint.

Real report output is capped at 5,000 rows. Builder PDF preview caps output at
150 rows and can guess company/date/fiscal-year filters. Column sampling normally
returns up to 50 rows, accepts 1–200, and the builder requests 20. A report with
more than six columns defaults to landscape when no layout overrides it.
The `truncated` flag exists in report data, but the PDF table renderer does not
currently show a truncation notice.

## Other printing paths

**Bulk printing:** the API accepts up to 50 names, authorizes each, then queues one
job. The worker renders each in order, merges successful PDFs, and reports skipped
names. The merged File is attached to the first selected document. There is a
missing-import issue in the multi-document merge path; see the caveats.

**Native document Print > PDF:** `overrides.download_pdf()` uses mappings with
`replace_print_pdf` enabled. It renders synchronously under a lock. A busy lock or
render failure falls back to native printing; an explicit permission denial is
re-raised.

**Attach after Submit:** the `*` document hook checks `auto_attach`, queues work
after commit, and stores `<document>-branded.pdf`. That worker has a different
locking/permission path from interactive printing and should not be described as
identical to `pdf_job.generate()`.

## What persists and what expires

| Data | Location/lifetime |
| --- | --- |
| Saved formats, mappings, branding, snippets | Frappe database |
| Gemini key | Password field in the AI Settings Single, or site configuration |
| Unsaved design draft | Browser localStorage, key `fibersoft_draft` |
| Undo history and copied blocks | Current iframe's JavaScript memory |
| Generated interactive PDFs | Private Frappe Files; daily cleanup removes matching files older than one day |
| Submit-time branded attachments | Private Files ending `-branded.pdf`; excluded from that cleanup pattern |
| Polling status | Redis cache, 15-minute TTL |
| Engine probe verdicts | Redis cache, normally one-day TTL |

Source entry points: [hooks.py](../fibersoft/hooks.py), [api.py](../fibersoft/api.py),
[compose.py](../fibersoft/compose.py), [pdf_job.py](../fibersoft/pdf_job.py),
[report.py](../fibersoft/report.py), and [overrides.py](../fibersoft/overrides.py).
