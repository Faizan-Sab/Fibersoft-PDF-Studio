# Running and maintaining Fibersoft

This guide records the local source and CI configuration reviewed on 2026-10-05.
Commands below are reference instructions, not commands executed on a live site
during this review. Use a configured test site for validation.

## Installation and configuration creation

The package is built by flit. `pyproject.toml` requires Python >=3.10 and declares
Frappe >=14,<17. It has no hard pip dependencies; the app expects Frappe and its
environment to supply common libraries. Playwright and requests/Gotenberg are
listed as optional extras.

The root README documents:

```sh
bench get-app fibersoft /path/to/this/repository
bench --site <site> install-app fibersoft
bench --site <site> migrate
```

Use the renamed checkout and a fresh site. Read [CUTOVER.md](../CUTOVER.md) before
moving an existing installation to the new app id.

`after_install` runs `ensure_config()`. `after_migrate` runs it again and clears
engine probes. Configuration installation:

1. Ensure the Fibersoft Module Def exists.
2. Create missing Custom DocTypes in dependency order.
3. Add missing fields to existing DocTypes using Custom Fields.
4. Defer Link fields whose target DocType is unavailable, such as Company on a
   plain Frappe site. Later runs can add those fields.
5. Seed **Quotation - Starter** and a mapping if Quotation exists and the relevant
   starter/mapping is missing. Existing defaults are preserved.
6. Commit successful steps separately; roll back and log failed steps.

Installation is deliberately nonfatal, so a completed migration is not proof
that every configuration record exists. `check_config()` is the stricter check.
The separate `run(as_custom=False)` path requires developer mode and is described
as exporting standard DocTypes; the normal hooks call `run(as_custom=True)`.

## Site configuration keys

`config.conf(key)` reads `fibersoft_<key>`, then legacy `brandpdf_<key>`, then its
default. Configuration stored on Fibersoft Settings is a separate mechanism.

| Key | Default / role |
| --- | --- |
| `fibersoft_engine` | `frappe_chrome`; selects renderer. |
| `fibersoft_chromium_path` | Unset; optional executable path for Playwright. |
| `fibersoft_render_url` | `http://localhost:3000`; Gotenberg base URL. |
| `fibersoft_page_format` | `A4`; default renderer option, though visual layout explicitly uses A4 dimensions. |
| `fibersoft_render_timeout` | 120 seconds; used in queue/HTTP/renderer timeout calculations. |
| `fibersoft_render_slots` | Worker helper defaults to 2, clamped to 1–8; not listed in config.DEFAULTS. |
| `fibersoft_feedback_email` | Maintainer address in code; separately supports `brandpdf_feedback_email`. |
| `fibersoft_gemini_key` | AI key fallback; encrypted AI Settings value takes priority. |

The model comes from Fibersoft AI Settings rather than `config.conf()`. The code's
key resolver does not implement a distinct `brandpdf_gemini_key` fallback.

Do not assume the Settings DocType's `default_engine` selector determines the
active engine. `render.base.get_renderer()` reads site configuration instead.

## Queues, locks and cleanup

Document PDF and preview jobs need an active `long` queue worker. The API returns
a job token, and the UI polls Redis-backed state. A scheduler is needed for daily
temporary-file cleanup.

- Normal document and bulk jobs use numbered render-slot locks; default two.
- Preview, synchronous native print, and report paths use a separate unsuffixed lock.
- Lock TTL is 240 seconds. Acquisition failure due to Redis exceptions permits
  the render and relies on the worker setup; it is not strict fail-closed locking.
- Normal document/preview jobs re-enqueue up to 60 times when busy. Bulk jobs
  instead report busy immediately.
- Job status TTL is 900 seconds, renewed whenever state is written.
- Daily cleanup deletes private Files matching `%-fibersoft.pdf` older than a day.
- Auto-submit attachments end in `-branded.pdf` and are retained by that cleanup.

These mechanisms do not impose one global Chromium limit across every entry
point. See [CODE_CAVEATS.md](CODE_CAVEATS.md) for lock-path details.

## Validation appropriate to a change

For Python syntax, from the app repository:

```sh
python -m compileall -q fibersoft
```

For a configured test site, from the Bench directory:

```sh
bench --site <test-site> execute fibersoft.setup.install_config.check_config
bench --site <test-site> execute fibersoft.lint.check_all --kwargs "{'strict': True}"
```

The linter checks selected layout issues: fixed Row widths, off-page blocks,
unrecognized fonts, image paths, and HTML-box information. It is not a complete
schema validator or a PDF comparison test. Strict mode fails on errors, not warnings.

For browser or layout changes, exercise the affected action and inspect actual
PDF output. Useful cases include a short record, many item rows, long terms,
Arabic/English text, portrait/landscape, repeated bands, photos, and a report with
real filters. Choose cases relevant to the change rather than running everything
for a documentation-only edit.

The checked-in CI matrix uses Frappe 15/Python 3.12/Node 20 and Frappe 16/Python
3.14/Node 24, plus MariaDB and Redis. It installs the app, checks config before
and after migration, runs format lint, calls idempotent configuration setup,
clears probe caches, byte-compiles modules, and lists installed apps. No dedicated
unit-test files are present in the reviewed tree. This workflow does not exercise
all browser behavior or compare final PDF pages.

## Troubleshooting map

| Symptom | Start here |
| --- | --- |
| Builder fails with missing config table | Error Log, `ensure_config()`, then `check_config()`. |
| Saved format cannot open on canvas | `get_format()` reason; template may be Jinja or legacy block rows without definition. |
| Button missing on a document | Enabled mappings, `enabled_doctypes()`, read permission, saved/new document state, Desk script load. |
| PDF stays queued | `long` worker, queue errors, Redis state, locks and client polling timeout. |
| Wrong template/default | Explicit template argument, company/global mapping, priorities, conditions, and entry-point differences. |
| Old PDF displayed | Browser `S.files` cache first, then `_fresh_render()` invalidation inputs. |
| Landscape clipped | `engine_diag()`, cached landscape verdict, pdfkit/wkhtml fallback availability. |
| Bands overlap content | Definition heights/gaps, renderer margins, margin-probe caveat, and compose fallback logs. |
| Image missing | Site-file path, existence, source allowlist, nested-image collection, and private/public file directories. |
| Fonts differ from canvas | Selected bundled/nonbundled font, Arabic font, remote-font access and engine support. |
| Report sample cannot load | Mandatory report filters and report permissions; sample defaults are best effort. |
| AI returns no format after a short wait | 15-second RPC timeout versus server request duration, model/key errors, network access. |
| Bulk PDF fails for several records | `_merge()` missing `io` import noted in caveats. |
| Side-margin or paper-color edit fails | Undefined `touch()` call noted in caveats. |

`/api/method/fibersoft.api.engine_diag` is manager-only and performs real probe
renders. It is useful diagnostics, not just a configuration dump.

## Existing repository documentation

- [README.md](../README.md): product features and normal installation.
- [CUTOVER.md](../CUTOVER.md): historical `brandpdf` to `fibersoft` migration.
  Its uninstall commands are historical migration steps, not normal upgrade steps.
- [PUBLISHING.md](../PUBLISHING.md): marketplace publishing notes; its version
  checklist says 1.1.0 whereas the package now reports 1.8.0.
- [license.txt](../license.txt) and [TRADEMARKS.md](../TRADEMARKS.md): repository
  license and trademark text; not replaced or interpreted by these technical notes.

Keep the internal app ID `fibersoft` stable on installed sites. The hooks and cutover
documentation explain why changing a registered app's import name can break Bench.
