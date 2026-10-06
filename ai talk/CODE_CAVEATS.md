# Code caveats and follow-up candidates

Recorded 2026-10-05 while documenting the local source. These are **static source
findings**, not results from running a production site. No application code was
changed. These are follow-up candidates, not an approved implementation backlog.

## Apparent defects with direct source evidence

| Area | Evidence | Likely consequence / verification needed |
| --- | --- | --- |
| Multi-document merge | `pdf_job._merge()` calls `io.BytesIO`, but pdf_job.py has no `import io`. | Merging more than one successful PDF should raise NameError; the single-part shortcut avoids that line. Test a two-document batch. |
| Margin probe | `compose._margins_honored()` uses `PdfReader` without a module/global import. Imports inside `_compose()` are local to that other function. | Probe exception is caught; it logs and assumes margins are honored, so intended spacer fallback is not reliably selected. |
| Page controls | Builder `setPageMarginX()` and `setPageBg()` call `touch()`, with no definition found in the builder or other JS files. | State may change, then the handler errors before scheduled render/update. Exercise both controls. |
| AI response deadline | Generic builder `rpc()` times out after 15 seconds; `_generate()` allows 90 seconds per HTTP attempt and may try alternatives. | A valid server answer can arrive after the browser has discarded its callback. |
| AI undo promise | `cpRun()` applies output through `loadDefinition()`, which calls `resetHistory()`, then advertises Ctrl+Z recovery. | Prior design history is cleared, so the previous format is not preserved by this path. |
| Duplicate report metadata | `api.duplicate_format()` copies target_doctype and content, but omits target_kind, report_name, email_subject and email_body. | A copied report/covering-email format may lose metadata. Compare source and copy records. |

## Selection, defaults, and caching

- `resolver.resolve_template()` evaluates company scope **and** structured mapping
  conditions. `_default_template()` and `overrides._mapping()` select without
  evaluating those conditions. Passing an explicit matching template bypasses
  resolver conditions entirely. These entry points can select different layouts.
- The print page asks `list_formats` with DocType but no company. Company-scoped
  defaults supported by the backend are therefore not fully reflected in that
  page's initial selection.
- `get_format(target_doctype=...)` selects the first enabled mapping without the
  company filtering used by `_default_template()`.
- `_fresh_render()` considers document modified time, explicit template modified
  time, and an arbitrary Settings row's modified time. It does not fully track
  mapped-template changes when template is omitted, the correct company's settings,
  linked-record changes, image contents, source-code changes, or permission changes.
- The print page's own `S.files` cache can reuse a URL without calling the server
  again for the same document/format. There is no freshness check at that step.
- `set_default_format()` updates or creates a mapping but does not set
  `replace_print_pdf`. Making a format default does not by itself turn on native
  document Print > PDF replacement.
- The response from `save_format()` always includes `activated: True`, although
  its activation helper preserves existing mappings. Do not interpret that flag
  as proof the just-saved format became the default.
- `delete_format()` attempts to delete the Template before updating its linked
  mappings. Actual behavior depends on Frappe's link validation; test deletion of
  a mapped format before relying on its fallback logic.

## Permission and asset boundaries are not uniform

- Normal document request/worker paths explicitly check read and print permissions
  and apply field-level filtering. `builder_sample()` is manager-only but does not
  apply the same per-document/field-level sequence; direct field metadata also
  lacks the permlevel filter used by linked/child metadata.
- Linked fields check target **DocType** read permission and fetch a cached target
  document. The helper does not call the target document's own `check_permission()`.
- `lint_format()` and the report branch of `list_formats()` have no explicit
  manager/report-document permission check inside those functions. They remain
  subject to the framework's normal request handling; do not call them uniformly
  permission-gated based only on other endpoints.
- `_validate_image_srcs()` and `collect_image_srcs()` inspect top-level image
  blocks and banners, but do not recurse into Row children. Snippet validation
  and document-derived Data Table image collection **do** recurse.
- `inline_images()` only filters against its allowlist if the set is nonempty.
  An empty set does not mean deny all. Filesystem path confinement still applies.
- `neutralize_remote()` uses regexes for selected HTML/CSS reference forms and
  allows Google Fonts hosts. Playwright does not install a network-blocking route
  handler here. Do not describe this as a complete renderer network sandbox.

## Rendering differences and limits

- Normal/bulk jobs use numbered slot locks; preview/report/native-print paths use
  a different unsuffixed lock. Submit-time `_attach_pdf()` does not use either.
  These are not a single global render semaphore despite older comments.
- Lock expiry is fixed at 240 seconds with no renewal. Bulk job timeouts can be
  much longer. `_release()` deletes by key without checking ownership. Concurrency
  behavior under slow jobs warrants a runtime test.
- `_attach_pdf()` does not explicitly capture/restore the submitting user or repeat
  the interactive worker's read/print checks. Its execution context needs review
  if changing automatic attachment behavior.
- `_merge()` requires pypdf directly; unlike `_compose()`, it has no PyPDF2 fallback.
  Frappe 14 compatibility of this path is not established by the current CI matrix.
- Real report rows stop at 5,000 (preview: 150). The payload says `truncated`, but
  `_d_report_table()` does not print a warning or pagination/export alternative.
- Page-number context is only correct after the body PDF is counted. Body page
  numbers default to 1/1. Overlay-cache detection scans top-level band blocks,
  so a Page No nested inside a band Row can reuse the wrong page-specific overlay.
- Browser continuation pages render both band functions without honoring all
  first/last-only conditions from the server composer. Canvas hidden-block ghosting
  and conditional visibility also do not exactly match the server output.
- The browser adds 4 mm top padding to its flowing body; server `_flow_body_html()`
  uses zero vertical padding on its outer container. Measure real output when
  diagnosing small vertical differences.
- `_render_child()` does not call `_visible()`. Top-level visibility semantics
  should not be assumed for arbitrary nested JSON blocks.
- Settings include `page_size`, `default_engine`, `footer_registration_text`, and
  mapping flags `replace_email_attach` / `replace_report_pdf`. Several have no
  corresponding runtime read in this source. Native report wrapping is controlled
  by `brand_reports`, not the per-report replacement flag.

## AI cleaner and browser state limitations

- `sanitize_definition()` forces document target kind and clears report_name.
  Copilot output is not a general report-layout round trip.
- `STYLE_KEYS` omits `fontAr` despite the schema text describing it. The cleaner
  preserves document-level font_ar but drops block-level fontAr.
- Watermark rules and angle are not preserved by the AI definition cleaner.
- `_clean_settings()` limits nested sizes but is not a strict allowed-key validator
  for each block type. The module's introductory wording is broader than the code.
- AI key resolution prefers encrypted Settings over site config, whereas
  `ai_status().key_source` reports site_config whenever that config key exists.
- `snapState()` does not include report name, target kind, or format name. Undo
  covers the captured design state rather than every visible UI choice.
- The draft uses one localStorage key for the origin, not per format or per user.
- `_doSave()` clears the local draft immediately after sending the save message,
  before server acknowledgment. A failed save can remove the recovery draft.

## Documentation drift

The root README, comments, and publishing notes describe different points in the
project's history. Examples: the current document gallery contains 19 entries,
publishing notes still mention version 1.1.0, and some comments call Playwright
the default or describe one render lock. Use executable code and current package
version when updating these notes.

Relevant sources: [pdf_job.py](../fibersoft/pdf_job.py),
[compose.py](../fibersoft/compose.py), [api.py](../fibersoft/api.py),
[blocks.py](../fibersoft/blocks.py), [assets.py](../fibersoft/assets.py),
[ai.py](../fibersoft/ai.py), [overrides.py](../fibersoft/overrides.py),
[report.py](../fibersoft/report.py), and
[builder HTML](../fibersoft/public/builder/index.html).
