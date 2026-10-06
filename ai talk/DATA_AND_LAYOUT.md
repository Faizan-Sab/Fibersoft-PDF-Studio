# Data and layout reference

Reviewed against this checkout on 2026-10-05. Start with
[HOW_FIBERSOFT_WORKS.md](HOW_FIBERSOFT_WORKS.md) for the end-to-end flow.

## Database records

These DocTypes are created programmatically by
[setup/install_config.py](../fibersoft/setup/install_config.py). The normal hooks
create Custom DocTypes in the database; their absence as checked-in DocType JSON
directories is intentional in the current installation path.

| DocType | Main fields and responsibility |
| --- | --- |
| Fibersoft Settings | Unique company, banner attachments, colors, font, RTL, report-branding toggle; also contains some legacy/configuration fields not used by current renderer selection. |
| Fibersoft Template | Name, target kind, target DocType, report name, source type, visual JSON `definition`, legacy block rows, HTML body/Jinja path, standard/gallery flags, email subject/body. |
| Fibersoft Block | Child rows for the older block model: `block_type`, `label`, `content`. |
| Fibersoft Mapping | Target, template link, company scope, enabled flag, priority, behavior toggles, condition rows. |
| Fibersoft Mapping Condition | Child rows with fieldname, operator, and comparison value. |
| Fibersoft Snippet | Named reusable block JSON. Inserting a snippet copies it into a format. |
| Fibersoft AI Settings | Single record with encrypted Gemini key and model name. |

Template and snippet names use their label fields as document names. Non-child
configuration DocTypes are created with System Manager permissions. Child rows
inherit access through their parent.

Do not confuse the legacy `blocks` child table with the modern JSON
`definition.blocks` array. A seeded starter may use child rows without any visual
definition, whereas formats saved through the canvas use JSON.

## A small illustrative definition

This example shows the contract; it is not installed or runtime-tested as a template.

```json
{
  "name": "Simple Quotation",
  "layout": "absolute",
  "target_kind": "doctype",
  "target_doctype": "Quotation",
  "report_name": "",
  "page": {"orientation": "portrait", "margin_x": 14, "bg": "#FFFFFF"},
  "header": {"enabled": false, "height": 0, "margin": 0, "repeat": false},
  "footer": {"enabled": true, "height": 14, "margin": 4, "repeat": true},
  "branding": {
    "primary": "#1463FF", "navy": "#0C1322",
    "font": "Inter", "font_ar": "Cairo",
    "header_image": "none", "footer_image": "none"
  },
  "watermark": {"text": "", "color": "#0C1322", "opacity": 8, "size": 60},
  "blocks": [
    {
      "type": "field", "region": "body", "float": false,
      "pos": {"x": 14, "y": 10, "w": 182, "h": null},
      "settings": {"field": "name", "prefix": "Quotation: "},
      "style": {"size": 16, "weight": "700"}
    },
    {
      "type": "items", "region": "body", "float": false,
      "pos": {"x": 14, "y": 30, "w": 182, "h": null},
      "settings": {"cols": {"desc": true, "qty": true, "rate": true, "amount": true}},
      "style": {}
    },
    {
      "type": "pagenum", "region": "footer", "float": false,
      "pos": {"x": 140, "y": 287, "w": 56, "h": null},
      "settings": {"format": "Page {p} of {n}"},
      "style": {"size": 8, "align": "right"}
    }
  ]
}
```

The editor assigns temporary block IDs for selection and editing. `definition()`
removes them when exporting/saving. `loadDefinition()` assigns fresh IDs.

## Units and positioning

- Page and block coordinates, gaps, padding, and margins generally use millimeters.
- Text size uses points. Borders, corner radii, letter spacing, and table cell
  padding use pixels. Check the individual setting rather than assuming one unit.
- A4 portrait is 210 × 297 mm; landscape is 297 × 210 mm. `page_dims()` does not
  implement arbitrary page sizes despite some legacy page-size settings.
- Body side margin defaults to 14 mm and is clamped so at least 20 mm remains.
- Normal body blocks sort by `pos.y`; their `pos.x`, `pos.w`, and `pos.h` do not
  control the flowing wrapper. Use style width or a Row for side-by-side content.
- Header/footer coordinates use the whole page as their reference, not local
  band coordinates. A footer at y=287 is near the bottom of portrait A4.
- A floating body block uses fixed coordinates and can overlap flow. It is not
  the repeated header/footer mechanism.
- A fixed height in an absolute wrapper adds `overflow:hidden`; it can clip content.
- Body blocks receive 4 mm bottom spacing; nested row children receive 2 mm.
  Explicit `style.mb` can override that margin.

## Block vocabulary

The server dispatch table is `blocks.DEF_RENDERERS`. The browser mirrors the
rendering in `R` and default settings in `DSET` inside the builder HTML.

| Block | Purpose and main settings |
| --- | --- |
| `heading`, `text` | Escaped text from `settings.text`; typography is in `style`. |
| `field` | A document field, optional `prefix`, optional sanitized HTML rendering. |
| `image` | Uploaded site-file `src` and percentage width within its wrapper. |
| `divider` | Thickness, color, line style. |
| `box` | Sanitized HTML content. |
| `spacer` | Empty vertical space (`settings.height`). |
| `row` | One to four columns, gaps, fixed/auto widths, child blocks, per-cell styling. |
| `table` | Static rows and columns, optional field tokens, header/row/column styling. |
| `title` | Quotation-oriented title, optional Arabic subtitle and metadata table. |
| `customer` | Party name and sanitized address display. |
| `items` | Ready-made items table with quantity, rate, amount, description and optional photos. |
| `datatable` | Any child table, with editable columns made of stacked text/image lines. |
| `totals` | Subtotal, discount, tax rows and grand total. |
| `payment_schedule` | Payment terms, due dates, percentages and amounts. |
| `terms` | Pre-sanitized document terms and an optional heading. |
| `signature` | Signature line and label; it does not collect a digital signature. |
| `pagenum` | Replaces `{p}` and `{n}` using composition context. |
| `qr` | Inline SVG QR from fixed text, a field, or a ZATCA-style TLV payload. |
| `header_banner`, `footer_banner` | Branding images; modern composition synthesizes these from band settings. |
| `report_title`, `report_filters`, `report_table` | Display normalized report data. |
| `report_native` | Embeds the native report HTML for the wrapper path. |
| `custom_html` | Legacy block type; the modern dispatcher maps it to the box renderer. |

Not every server block appears in every palette or in the AI allowlist. A new block
needs coordinated changes in the browser, server, and possibly AI schema.

## Fields and tables

`_field_value()` formats a direct field and excludes fields with nonzero permlevel
when metadata is available. `_linked_field_value()` supports exactly one link hop,
such as `customer.email_id`. It checks Link/Dynamic Link metadata, permlevel-zero
fields, and target-DocType read permission. It is not a general expression evaluator.

A static table cell binds a field only when the **whole cell** is a token such as
`{name}` or `{customer.email_id}`. Text like `Invoice {name}` is not interpolated
by `_cell_value()`. Rich values in static table cells are reduced to plain text.
Field blocks can instead render sanitized rich HTML.

A Data Table reads `settings.table`, the child-table field on the document. Each
column has a label, width, alignment, vertical alignment, and `lines` array. Lines
can carry a field, text/image kind, size, weight, color, prefix/suffix, italic,
uppercase, duplicate suppression, and image dimensions. Empty values leave no gap.
Older `{field, label, width, align}` columns are normalized on read to one line.
Allowed child fields are filtered against metadata when available.

Rows use `settings.cells`, an array of arrays of child blocks. The server refuses
a Row nested inside another Row. `_row_fit_widths()` reserves space for auto
columns and scales fixed widths when necessary. `cellStyles` controls each
column's background, padding, alignment, border sides, and radius.

## Visibility, page numbers, and watermarks

Top-level `hidden: true` suppresses printing; `locked: true` is an editor interaction
flag, not a print-visibility flag. A `cond` object uses `{field, op, value}`.
Supported server comparisons are `=`, `!=`, `>`, `<`, `>=`, `<=`, `in`, and `like`.
Equality is numeric-aware; `in` splits a comma-separated string; `like` strips
percent signs and uses a case-insensitive substring match. No Python eval is used.

For dependable current/total page counts, put a top-level Page No block in a band.
Body rendering happens before total pages are known, and nested page numbers have
overlay-cache limitations described in [CODE_CAVEATS.md](CODE_CAVEATS.md).

Watermarks can have fixed text or ordered rules. The first matching rule provides
the text. The watermark is rendered separately and merged behind each page.

## Branding and assets

Company colors and banners come from `resolver.resolve_branding()`. A visual
definition overrides colors and selected fonts. For banner paths:

- Empty/missing value inherits the company banner.
- A nonempty uploaded file path overrides it.
- The literal string `"none"` suppresses it for that format.

`assets.inline_images()` maps file URLs to site public/private file directories,
checks resolved filesystem boundaries, and embeds image bytes as data URIs.
`neutralize_remote()` removes remaining image references and selected CSS fetches,
with Google Fonts hosts allowed. This is not complete network sandboxing.

The app bundles nine font families: Plus Jakarta Sans, Inter, Montserrat, Cairo,
Almarai, Tajawal, IBM Plex Sans Arabic, Noto Kufi Arabic, and Amiri. Used bundled
faces become base64 `@font-face` rules. Other supported Google font families may
still require remote access. Arabic text uses `branding.font_ar`, default Cairo;
a block can override it with `style.fontAr`.

QR encoding uses `pyqrcode` expected from the Frappe environment. The ZATCA mode
constructs five TLV values from seller/tax/date/total fields. That implementation
alone is not evidence of complete e-invoicing compliance or certified output.
