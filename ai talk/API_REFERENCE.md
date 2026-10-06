# API reference from the local source

Reviewed 2026-10-05. These are Frappe whitelisted Python methods, normally invoked
with `frappe.call` or through `/api/method/<method>`. This table records code-level
behavior; it is not a live API test or a complete security audit.

## Document printing and jobs — `fibersoft.api`

| Method | Inputs | Result / behavior |
| --- | --- | --- |
| `request_pdf` | `doctype`, `name`, optional `template` | Cached done result, or `{job_id}` for queued PDF. |
| `request_bulk_pdf` | `doctype`, `names`, optional `template` | Authorizes selected names, takes first 50, returns job ID and total. |
| `request_preview` | `definition`, `doctype="Quotation"`, optional `name` | Manager-only unsaved layout job; chooses recent document if name omitted. |
| `get_job_result` | `job_id` | User-owned queued/working/done/error state, or unknown. |
| `format_email` | `template`, `doctype`, `name` | Document-rendered email subject/body; does not send mail. |
| `enabled_doctypes` | None | Enabled targets filtered by caller's DocType read permission. |
| `engine_diag` | None | Manager-only rendering probes and engine/version information; clears probe cache afterwards. |

`request_pdf`, `request_bulk_pdf`, and `format_email` use `_authorize()` for enabled
DocType, login, read, and print permission. Document workers recheck access.
Preview begins with a manager check and validates access again inside its worker.

Successful saved-file state includes `status`, `file_url`, `file_name`, and
`file_id`. Bulk working state includes `done` and `total`; final bulk state may
also include `printed` and `skipped`. Client code must handle both immediate cache
hits and queued jobs.

## Format management — `fibersoft.api`

Except `list_formats`, the methods below call `_require_manager()`.

| Method | Inputs / purpose |
| --- | --- |
| `list_formats` | `doctype`, optional `company`, or `report_name`; returns labels, standard/default/visual flags. Document branch checks DocType read access; report branch lacks an explicit report-permission check here. |
| `home_formats` | Optional `limit=200`; visual-format cards, target, modified time, color, orientation and default status. |
| `list_companies` | Company names for default scope; empty if Company DocType is absent. |
| `save_format` | `definition`, optional `name`; creates/updates visual Template and bootstraps mapping when missing. |
| `get_format` | Optional `name`, `target_doctype="Quotation"`, `report_name`; returns parsed definition, or missing/not_visual/empty for an explicit name. |
| `set_default_format` | `doctype`, `template`, optional `company`; updates/creates scope mapping and removes duplicate rows in that scope. |
| `set_default_report_format` | `report_name`, `template`; updates/creates report mapping and collapses duplicates. |
| `duplicate_format` | `name`, optional `new_name`; makes a uniquely named nonstandard, nongallery copy. See caveat about omitted fields. |
| `delete_format` | `name`; rejects standard templates, attempts deletion and repointing/disabling mappings. |
| `set_gallery` | `name`, `on`; toggles a visual format's site gallery flag. |
| `gallery_list` | Returns gallery entries with name, label and document target. |

Stored visual JSON is not comprehensively sanitized by `save_format()`; its image
path checks differ from the AI sanitizer and snippet validation. Standard templates
cannot be overwritten by normal save. An existing non-block template cannot be
silently replaced by a visual definition using the same name.

## Builder metadata — `fibersoft.api`

All these methods require System Manager.

| Method | Purpose |
| --- | --- |
| `builder_doctypes()` | Existing common business DocTypes plus targets already represented by saved templates. |
| `builder_reports(limit=300)` | Enabled report candidates with metadata. |
| `doctype_fields(doctype="Quotation")` | Value-bearing fields plus name; skips layout/container types. |
| `doctype_link_fields(doctype="Quotation")` | Readable Link targets with permlevel-zero source/target fields. |
| `child_tables(doctype="Quotation")` | Table fields with child field options and idx. |
| `builder_docs(doctype, limit=20)` | Recent document names for preview selection. |
| `builder_sample(doctype, name)` | Formatted parent values and sample items, taxes, payment schedule and generic child tables. |

Do not assume all metadata/sample methods apply the same field-level filtering:
the direct field/sample paths and link/child paths differ in this checkout.

## Snippets and feedback — `fibersoft.api`

All require System Manager.

| Method | Purpose |
| --- | --- |
| `list_snippets()` | At most 200 saved blocks, newest first, including parsed JSON. |
| `save_snippet(name, block)` | Creates/overwrites named block; recursively checks nested image paths. |
| `delete_snippet(name)` | Deletes a saved snippet; already-inserted copies remain in formats. |
| `submit_feedback(message, reply_to=None)` | Queues email through Frappe with escaped message and site/user/version context. |

## Reports — `fibersoft.report`

| Method | Inputs / result |
| --- | --- |
| `report_to_pdf` | Native endpoint wrapper: `html`, `orientation="Landscape"`; branded or native PDF response. |
| `report_pdf` | `report_name`, optional `filters`, `template`, `orientation`, `definition`, `preview=0`; synchronous PDF response. |
| `report_sample` | `report_name`, optional `filters`, `limit=50`; normalized columns/rows and sampling notes. |

Named-report methods check the Report document and reference-DocType report
permission and use Frappe's report runner. An ad-hoc definition is honored only
for System Manager. Preview mode merges guessed defaults with supplied filters;
normal report printing uses the supplied filters.

## AI — `fibersoft.ai`

All require System Manager.

| Method | Inputs / result |
| --- | --- |
| `ai_status()` | Ready flag, model, ability to set key, and reported key source; never the key. |
| `save_ai_key(api_key=None, model=None)` | Updates AI Settings and returns status. |
| `list_models()` | Calls Gemini model discovery using the stored key. |
| `ai_format(instruction, definition=None, mode="edit", target_doctype=None, sample=None, attachment=None)` | Returns sanitized definition and short notes; no format persistence. |

## Other entry points

- `fibersoft.overrides.download_pdf(doctype, name, format=None, doc=None, ...)`
  wraps native document PDF printing.
- `fibersoft.lint.lint_format(name)` returns saved-definition diagnostics. It has
  no explicit manager or Template read check inside the function.
- `fibersoft.setup.install_config.check_config` and `fibersoft.lint.check_all` are
  Bench/CI helpers, not whitelisted browser endpoints.

Source: [api.py](../fibersoft/api.py), [report.py](../fibersoft/report.py),
[ai.py](../fibersoft/ai.py), [lint.py](../fibersoft/lint.py),
[overrides.py](../fibersoft/overrides.py).
