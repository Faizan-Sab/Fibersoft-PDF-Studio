# Repository file map

Inventory and source review: 2026-10-05. Paths are relative to the repository root.
The generated `ai talk` guides are indexed in [README.md](README.md).

## Coverage and limits

The review traced the Python application, renderer adapters, installer, Desk scripts,
page registrations, builder state/rendering/RPC code, template factories, packaging,
and CI. The large builder's repeated CSS, SVG icons, and control/template markup
were structurally scanned alongside detailed reads of its behavior. This is a
source architecture review, not a claim of line-by-line security certification.

All original text files were decoded during the inventory pass. Python files were
also parsed with the standard-library AST parser. Binary fonts and screenshots
were inventoried by filename and size; font glyphs and screenshot pixels were not
visually inspected. No Frappe database, installed site, or live Gemini service was
available in the supplied project snapshot for runtime validation.

Inventory: **93 original files**, including **54 text files** and **25 Python files parsed**.

## Every original file

| File | Bytes | Responsibility |
| --- | ---: | --- |
| [.gitattributes](../.gitattributes) | 45 | Text line-ending normalization and binary asset rules. |
| [.github/workflows/ci.yml](../.github/workflows/ci.yml) | 4,025 | Frappe 15/16 install, migrate, config, lint and syntax CI. |
| [.gitignore](../.gitignore) | 54 | Ignored cache, dependency, log and environment files. |
| [CUTOVER.md](../CUTOVER.md) | 5,017 | Historical app-ID migration from brandpdf to fibersoft. |
| [docs/screenshots/01-canvas-and-inspector.png](../docs/screenshots/01-canvas-and-inspector.png) | 190,322 | Documentation screenshot; visual reference, not runtime logic. |
| [docs/screenshots/02-template-gallery.png](../docs/screenshots/02-template-gallery.png) | 151,302 | Documentation screenshot; visual reference, not runtime logic. |
| [docs/screenshots/03-composable-table.png](../docs/screenshots/03-composable-table.png) | 198,861 | Documentation screenshot; visual reference, not runtime logic. |
| [docs/screenshots/04-branded-report.png](../docs/screenshots/04-branded-report.png) | 150,173 | Documentation screenshot; visual reference, not runtime logic. |
| [docs/screenshots/05-layers-and-product-photos.png](../docs/screenshots/05-layers-and-product-photos.png) | 198,316 | Documentation screenshot; visual reference, not runtime logic. |
| [license.txt](../license.txt) | 4,976 | Application license text and license history. |
| [fibersoft/__init__.py](../fibersoft/__init__.py) | 269 | Package version: 1.8.0. |
| [fibersoft/ai.py](../fibersoft/ai.py) | 29,804 | Gemini configuration, prompts, request handling and definition cleaning. |
| [fibersoft/api.py](../fibersoft/api.py) | 52,518 | Document jobs, format management, metadata, snippets, feedback and job state. |
| [fibersoft/assets.py](../fibersoft/assets.py) | 3,834 | Site-file image inlining, path confinement and selected remote-reference removal. |
| [fibersoft/blocks.py](../fibersoft/blocks.py) | 98,051 | Legacy/visual block HTML renderers, field binding, fonts, table styling and layout. |
| [fibersoft/compose.py](../fibersoft/compose.py) | 14,308 | Template resolution, body rendering, band/watermark PDF overlays and probes. |
| [fibersoft/config.py](../fibersoft/config.py) | 1,476 | Site configuration reader with legacy key fallback. |
| [fibersoft/defaults.py](../fibersoft/defaults.py) | 1,070 | Neutral branding and shipped Quotation fallback path. |
| [fibersoft/hooks.py](../fibersoft/hooks.py) | 3,470 | Desk assets, document hooks, overrides, migration and scheduler wiring. |
| [fibersoft/lint.py](../fibersoft/lint.py) | 7,596 | Static checks for saved visual definitions and site-wide lint helper. |
| [fibersoft/fibersoft/__init__.py](../fibersoft/fibersoft/__init__.py) | 418 | Frappe module package marker with historical notes. |
| [fibersoft/fibersoft/page/__init__.py](../fibersoft/fibersoft/page/__init__.py) | 0 | Empty Python package marker. |
| [fibersoft/fibersoft/page/fibersoft_builder/__init__.py](../fibersoft/fibersoft/page/fibersoft_builder/__init__.py) | 0 | Empty Python package marker. |
| [fibersoft/fibersoft/page/fibersoft_builder/fibersoft_builder.js](../fibersoft/fibersoft/page/fibersoft_builder/fibersoft_builder.js) | 8,032 | Desk iframe host: RPC allowlist, save/upload, theme and PDF preview. |
| [fibersoft/fibersoft/page/fibersoft_builder/fibersoft_builder.json](../fibersoft/fibersoft/page/fibersoft_builder/fibersoft_builder.json) | 497 | Standard builder Page registration restricted to System Manager. |
| [fibersoft/fibersoft/page/fibersoft_print/__init__.py](../fibersoft/fibersoft/page/fibersoft_print/__init__.py) | 0 | Empty Python package marker. |
| [fibersoft/fibersoft/page/fibersoft_print/fibersoft_print.js](../fibersoft/fibersoft/page/fibersoft_print/fibersoft_print.js) | 11,302 | PDF print screen: format selection, polling, viewer, download and email composer. |
| [fibersoft/fibersoft/page/fibersoft_print/fibersoft_print.json](../fibersoft/fibersoft/page/fibersoft_print/fibersoft_print.json) | 384 | Standard print Page registration; data access is handled by APIs. |
| [fibersoft/modules.txt](../fibersoft/modules.txt) | 9 | Declares the Fibersoft Frappe module. |
| [fibersoft/overrides.py](../fibersoft/overrides.py) | 6,646 | Native document PDF override and submit-time attachment jobs. |
| [fibersoft/patches.txt](../fibersoft/patches.txt) | 32 | Patch list placeholder; no active patches. |
| [fibersoft/pdf_job.py](../fibersoft/pdf_job.py) | 11,291 | Queued document/preview/bulk jobs, locks, private files and cleanup. |
| [fibersoft/public/builder/index.html](../fibersoft/public/builder/index.html) | 398,042 | Complete vanilla-JavaScript editor, CSS, dialogs, layout factories and browser rendering. |
| [fibersoft/public/fonts/almarai-arabic-400-normal.woff2](../fibersoft/public/fonts/almarai-arabic-400-normal.woff2) | 31,672 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/almarai-arabic-700-normal.woff2](../fibersoft/public/fonts/almarai-arabic-700-normal.woff2) | 32,912 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/almarai-latin-400-normal.woff2](../fibersoft/public/fonts/almarai-latin-400-normal.woff2) | 17,468 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/almarai-latin-700-normal.woff2](../fibersoft/public/fonts/almarai-latin-700-normal.woff2) | 17,392 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/amiri-arabic-400-normal.woff2](../fibersoft/public/fonts/amiri-arabic-400-normal.woff2) | 108,560 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/amiri-arabic-700-normal.woff2](../fibersoft/public/fonts/amiri-arabic-700-normal.woff2) | 99,968 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/amiri-latin-400-normal.woff2](../fibersoft/public/fonts/amiri-latin-400-normal.woff2) | 19,544 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/amiri-latin-700-normal.woff2](../fibersoft/public/fonts/amiri-latin-700-normal.woff2) | 20,300 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/cairo-arabic-400-normal.woff2](../fibersoft/public/fonts/cairo-arabic-400-normal.woff2) | 13,292 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/cairo-arabic-700-normal.woff2](../fibersoft/public/fonts/cairo-arabic-700-normal.woff2) | 13,952 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/cairo-latin-400-normal.woff2](../fibersoft/public/fonts/cairo-latin-400-normal.woff2) | 15,016 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/cairo-latin-700-normal.woff2](../fibersoft/public/fonts/cairo-latin-700-normal.woff2) | 15,284 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2](../fibersoft/public/fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2) | 42,848 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/ibm-plex-sans-arabic-arabic-700-normal.woff2](../fibersoft/public/fonts/ibm-plex-sans-arabic-arabic-700-normal.woff2) | 44,280 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/ibm-plex-sans-arabic-latin-400-normal.woff2](../fibersoft/public/fonts/ibm-plex-sans-arabic-latin-400-normal.woff2) | 19,164 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/ibm-plex-sans-arabic-latin-700-normal.woff2](../fibersoft/public/fonts/ibm-plex-sans-arabic-latin-700-normal.woff2) | 19,504 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/inter-latin-400-normal.woff2](../fibersoft/public/fonts/inter-latin-400-normal.woff2) | 23,664 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/inter-latin-600-normal.woff2](../fibersoft/public/fonts/inter-latin-600-normal.woff2) | 24,452 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/inter-latin-700-normal.woff2](../fibersoft/public/fonts/inter-latin-700-normal.woff2) | 24,356 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/montserrat-latin-400-normal.woff2](../fibersoft/public/fonts/montserrat-latin-400-normal.woff2) | 18,780 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/montserrat-latin-600-normal.woff2](../fibersoft/public/fonts/montserrat-latin-600-normal.woff2) | 18,688 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/montserrat-latin-700-normal.woff2](../fibersoft/public/fonts/montserrat-latin-700-normal.woff2) | 18,824 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/noto-kufi-arabic-arabic-400-normal.woff2](../fibersoft/public/fonts/noto-kufi-arabic-arabic-400-normal.woff2) | 43,940 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/noto-kufi-arabic-arabic-700-normal.woff2](../fibersoft/public/fonts/noto-kufi-arabic-arabic-700-normal.woff2) | 43,872 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/noto-kufi-arabic-latin-400-normal.woff2](../fibersoft/public/fonts/noto-kufi-arabic-latin-400-normal.woff2) | 10,448 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/noto-kufi-arabic-latin-700-normal.woff2](../fibersoft/public/fonts/noto-kufi-arabic-latin-700-normal.woff2) | 10,384 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/OFL-almarai.txt](../fibersoft/public/fonts/OFL-almarai.txt) | 4,572 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-amiri.txt](../fibersoft/public/fonts/OFL-amiri.txt) | 4,690 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-cairo.txt](../fibersoft/public/fonts/OFL-cairo.txt) | 4,379 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-ibm-plex-sans-arabic.txt](../fibersoft/public/fonts/OFL-ibm-plex-sans-arabic.txt) | 4,808 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-inter.txt](../fibersoft/public/fonts/OFL-inter.txt) | 4,477 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-montserrat.txt](../fibersoft/public/fonts/OFL-montserrat.txt) | 4,509 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-noto-kufi-arabic.txt](../fibersoft/public/fonts/OFL-noto-kufi-arabic.txt) | 4,355 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-plus-jakarta-sans.txt](../fibersoft/public/fonts/OFL-plus-jakarta-sans.txt) | 4,534 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/OFL-tajawal.txt](../fibersoft/public/fonts/OFL-tajawal.txt) | 4,314 | Bundled font license/attribution text. |
| [fibersoft/public/fonts/plus-jakarta-sans-latin-400-normal.woff2](../fibersoft/public/fonts/plus-jakarta-sans-latin-400-normal.woff2) | 11,816 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/plus-jakarta-sans-latin-600-normal.woff2](../fibersoft/public/fonts/plus-jakarta-sans-latin-600-normal.woff2) | 12,188 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/plus-jakarta-sans-latin-700-normal.woff2](../fibersoft/public/fonts/plus-jakarta-sans-latin-700-normal.woff2) | 12,244 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/plus-jakarta-sans-latin-800-normal.woff2](../fibersoft/public/fonts/plus-jakarta-sans-latin-800-normal.woff2) | 11,896 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/tajawal-arabic-400-normal.woff2](../fibersoft/public/fonts/tajawal-arabic-400-normal.woff2) | 8,932 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/tajawal-arabic-700-normal.woff2](../fibersoft/public/fonts/tajawal-arabic-700-normal.woff2) | 9,024 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/tajawal-latin-400-normal.woff2](../fibersoft/public/fonts/tajawal-latin-400-normal.woff2) | 10,256 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/fonts/tajawal-latin-700-normal.woff2](../fibersoft/public/fonts/tajawal-latin-700-normal.woff2) | 9,996 | Bundled font face; filename identifies family, script subset and weight. |
| [fibersoft/public/images/fibersoft-logo.svg](../fibersoft/public/images/fibersoft-logo.svg) | 760 | Source SVG logo used by app metadata. |
| [fibersoft/public/js/fibersoft_button.js](../fibersoft/public/js/fibersoft_button.js) | 7,780 | Desk form button, print route and bulk list action. |
| [fibersoft/public/js/fibersoft_report_button.bundle.js](../fibersoft/public/js/fibersoft_report_button.bundle.js) | 2,866 | Query Report toolbar button; Frappe bundles it under a hashed asset name. |
| [fibersoft/render/base.py](../fibersoft/render/base.py) | 1,615 | Renderer interface, defaults and configured engine selection. |
| [fibersoft/render/frappe_chrome_renderer.py](../fibersoft/render/frappe_chrome_renderer.py) | 8,465 | Host PDF adapter and verified-landscape wkhtml fallback. |
| [fibersoft/render/gotenberg_renderer.py](../fibersoft/render/gotenberg_renderer.py) | 2,102 | HTTP HTML-to-PDF renderer adapter. |
| [fibersoft/render/playwright_renderer.py](../fibersoft/render/playwright_renderer.py) | 5,108 | Chromium discovery and in-process Playwright renderer. |
| [fibersoft/render_html.py](../fibersoft/render_html.py) | 3,084 | Resolve/render blocks or trusted Jinja, then prepare images and remote references. |
| [fibersoft/report.py](../fibersoft/report.py) | 17,715 | Report permission checks, data normalization, samples and synchronous PDFs. |
| [fibersoft/resolver.py](../fibersoft/resolver.py) | 5,640 | Company branding, mapping precedence, conditions and standard-template protection. |
| [fibersoft/setup/install_browser.py](../fibersoft/setup/install_browser.py) | 2,341 | Manual existing-Chromium discovery helper; no browser download, not a migrate hook. |
| [fibersoft/setup/install_config.py](../fibersoft/setup/install_config.py) | 18,443 | Programmatic DocType definitions, missing-field sync, integrity checks and starter seed. |
| [fibersoft/templates/fibersoft/quotation_bstc.html](../fibersoft/templates/fibersoft/quotation_bstc.html) | 8,597 | Legacy Quotation Jinja fallback with flowing content and banners. |
| [PUBLISHING.md](../PUBLISHING.md) | 3,459 | Marketplace publishing checklist; includes historical version references. |
| [pyproject.toml](../pyproject.toml) | 993 | Flit packaging, Python/Frappe requirements and optional extras. |
| [README.md](../README.md) | 8,905 | Product overview, installation, user flow, renderer notes. |
| [TRADEMARKS.md](../TRADEMARKS.md) | 1,107 | Trademark terms supplied with the repository. |

## Suggested code reading order

1. hooks.py and setup/install_config.py: how the app joins Frappe and creates its schema.
2. Builder Desk host and public/builder/index.html: how a definition is edited and saved.
3. api.py and resolver.py: how formats, permissions and mappings are chosen.
4. blocks.py and render_html.py: how values become styled HTML.
5. compose.py, render/base.py and renderer adapters: how HTML becomes final pages.
6. pdf_job.py and the print Desk page: how jobs and files return to the user.
7. report.py and report toolbar script: the separate report path.
8. ai.py: the optional layout-generation service.
9. lint.py and CI: existing validation and its limits.

## Python navigation index

Top-level classes and functions are listed with their source line at review time.
Line numbers can change; search by symbol after future edits.

### [fibersoft/ai.py](../fibersoft/ai.py)

`_settings` (line 53), `_resolve_key` (line 61), `_model` (line 73), `_scrub` (line 78), `ai_status` (line 84), `save_ai_key` (line 98), `list_models` (line 116), `_clean_attachment` (line 286), `_fields_brief` (line 316), `_prompt` (line 345), `_hex` (line 377), `_number` (line 382), `_clean_style` (line 390), `_clean_settings` (line 426), `_clean_block` (line 446), `sanitize_definition` (line 481), `_generate` (line 535), `ai_format` (line 574).

### [fibersoft/api.py](../fibersoft/api.py)

`request_pdf` (line 20), `format_email` (line 47), `request_bulk_pdf` (line 78), `_fresh_render` (line 109), `list_formats` (line 147), `_default_template` (line 187), `_default_report_template` (line 214), `home_formats` (line 226), `list_companies` (line 308), `set_default_format` (line 317), `set_default_report_format` (line 372), `duplicate_format` (line 404), `delete_format` (line 434), `request_preview` (line 469), `get_job_result` (line 501), `enabled_doctypes` (line 511), `engine_diag` (line 519), `save_format` (line 592), `submit_feedback` (line 653), `list_snippets` (line 693), `save_snippet` (line 712), `delete_snippet` (line 737), `_validate_block_images` (line 744), `set_gallery` (line 761), `gallery_list` (line 778), `get_format` (line 798), `builder_reports` (line 839), `doctype_fields` (line 863), `doctype_link_fields` (line 882), `child_tables` (line 919), `builder_doctypes` (line 948), `builder_docs` (line 966), `builder_sample` (line 978), `_ensure_config_ready` (line 1058), `_require_manager` (line 1075), `_validate_image_srcs` (line 1080), `_activate_mapping` (line 1101), `_activate_report_mapping` (line 1115), `_authorize` (line 1136), `_key` (line 1150), `set_state` (line 1154), `_get_state` (line 1159).

### [fibersoft/assets.py](../fibersoft/assets.py)

`inline_images` (line 22), `_host_allowed` (line 58), `neutralize_remote` (line 66), `_safe_local_path` (line 79).

### [fibersoft/blocks.py](../fibersoft/blocks.py)

`_pf_css` (line 38), `page_dims` (line 52), `page_margin_x` (line 61), `_font_dir` (line 162), `_face` (line 166), `font_faces_css` (line 179), `fonts_in_use` (line 194), `base_css` (line 224), `_b_header_banner` (line 293), `_b_footer_banner` (line 297), `_b_title` (line 301), `_b_customer` (line 319), `_b_items` (line 335), `_b_totals` (line 361), `_b_payment_schedule` (line 381), `_b_terms` (line 402), `_b_signature` (line 412), `_b_spacer` (line 420), `_b_custom_html` (line 424), `default_blocks` (line 445), `render_blocks` (line 451), `_doc_fonts` (line 493), `font_stack` (line 499), `_label` (line 512), `_esc` (line 519), `_num` (line 523), `_fmt_num` (line 532), `_hexok` (line 543), `_field_value` (line 547), `_linked_field_value` (line 570), `_visible` (line 613), `_style_css` (line 632), `_e_heading` (line 706), `_e_text` (line 710), `_field_is_rich` (line 717), `_e_field` (line 725), `_e_image` (line 737), `_e_divider` (line 745), `_e_box` (line 752), `_cell_value` (line 761), `_list` (line 773), `_e_table` (line 778), `_e_spacer` (line 880), `_d_header_banner` (line 886), `_d_footer_banner` (line 892), `_d_title` (line 898), `_d_customer` (line 931), `_tbl_skin` (line 956), `_col_css` (line 1010), `_zebra_parts` (line 1032), `_d_items` (line 1042), `_dt_lines` (line 1138), `_dt_is_file` (line 1149), `_dt_line_css` (line 1154), `_dt_cell` (line 1171), `_d_datatable` (line 1212), `_d_totals` (line 1282), `_d_payment_schedule` (line 1312), `_d_terms` (line 1354), `_d_signature` (line 1366), `_zatca_tlv` (line 1381), `_qr_payload` (line 1411), `_e_qr` (line 1420), `_e_pagenum` (line 1444), `_report_ctx` (line 1456), `_d_report_title` (line 1461), `_d_report_filters` (line 1478), `_d_report_native` (line 1495), `_d_report_table` (line 1510), `_render_child` (line 1573), `_row_fit_widths` (line 1588), `_cell_css` (line 1607), `_d_row` (line 1643), `_branding_from_def` (line 1696), `collect_image_srcs` (line 1721), `collect_doc_image_srcs` (line 1744), `render_definition` (line 1792), `_absolute_page_html` (line 1840), `_flow_body_html` (line 1889), `_render_absolute` (line 1968), `watermark_page_html` (line 1977).

### [fibersoft/compose.py](../fibersoft/compose.py)

`compose_pdf` (line 26), `compose_report_pdf` (line 43), `_resolve` (line 75), `_margins_honored` (line 101), `clear_probe_cache` (line 135), `_finish` (line 144), `_watermark_text` (line 165), `_derive_region` (line 179), `_compose` (line 189).

### [fibersoft/config.py](../fibersoft/config.py)

`conf` (line 20).

### [fibersoft/lint.py](../fibersoft/lint.py)

`_num` (line 27), `_page` (line 36), `check_definition` (line 43), `lint_format` (line 128), `check_all` (line 138).

### [fibersoft/overrides.py](../fibersoft/overrides.py)

`_mapping` (line 24), `download_pdf` (line 61), `auto_attach_on_submit` (line 104), `_attach_pdf` (line 119).

### [fibersoft/pdf_job.py](../fibersoft/pdf_job.py)

`generate` (line 24), `generate_preview` (line 64), `_acquire_slot` (line 123), `_acquire` (line 140), `_release` (line 151), `generate_bulk` (line 160), `_merge` (line 204), `file_suffix` (line 219), `_save_private_file` (line 226), `cleanup_expired_files` (line 244).

### [fibersoft/render/base.py](../fibersoft/render/base.py)

`BaseRenderer` (line 9), `default_options` (line 14), `get_renderer` (line 25).

### [fibersoft/render/frappe_chrome_renderer.py](../fibersoft/render/frappe_chrome_renderer.py)

`_is_landscape_pdf` (line 30), `_land_state` (line 42), `_set_land_state` (line 49), `FrappeChromeRenderer` (line 56).

### [fibersoft/render/gotenberg_renderer.py](../fibersoft/render/gotenberg_renderer.py)

`GotenbergRenderer` (line 15).

### [fibersoft/render/playwright_renderer.py](../fibersoft/render/playwright_renderer.py)

`_find_chromium` (line 41), `PlaywrightRenderer` (line 61).

### [fibersoft/render_html.py](../fibersoft/render_html.py)

`render_html` (line 21), `_read_template` (line 53).

### [fibersoft/report.py](../fibersoft/report.py)

`ReportDoc` (line 34), `_reports_branding_on` (line 55), `_report_branding` (line 64), `_align_for` (line 99), `_normalize_columns` (line 103), `_fmt_value` (line 124), `_format_rows` (line 138), `_filter_summary` (line 157), `_company_from_filters` (line 168), `_check_report_perm` (line 172), `_build_report_doc` (line 183), `_report_mapping` (line 202), `_default_report_def` (line 217), `_lock` (line 248), `report_to_pdf` (line 257), `report_pdf` (line 290), `report_sample` (line 348), `_clear_messages` (line 391), `_guess_default_filters` (line 403).

### [fibersoft/resolver.py](../fibersoft/resolver.py)

`enabled_doctypes` (line 19), `resolve_branding` (line 29), `resolve_template` (line 52), `protect_standard_template` (line 85), `_conditions_match` (line 97), `_match` (line 107).

### [fibersoft/setup/install_browser.py](../fibersoft/setup/install_browser.py)

`ensure_chromium` (line 31).

### [fibersoft/setup/install_config.py](../fibersoft/setup/install_config.py)

`run` (line 106), `_integrity_check` (line 148), `ensure_config` (line 164), `_deferred_links` (line 187), `check_config` (line 196), `_ensure` (line 229), `_sync_fields` (line 257), `_perms` (line 271), `_seed` (line 276).
