# Copyright (c) 2026 Lumen Solutions (BSTC W.L.L). All rights reserved.
# SPDX-License-Identifier: LicenseRef-Lumen-Proprietary
# Proprietary and confidential. See license.txt. "LumenPDF" and "LumenPDF Studio" are
# trademarks of Lumen Solutions.
# Internal module id. NEVER rename this on a site that already has the app installed: Frappe
# registers the app by this id, so renamed code + an old registration = ModuleNotFoundError that
# wedges every bench command. A rename is only safe as a FRESH install of the new id
# (uninstall old → install new), which is exactly how this branch came to exist.
app_name = "fibersoft"
app_title = "Fibersoft PDF Studio"
app_publisher = "Fibersoft"
app_description = ("Visual print-format builder for Frappe/Fibersoft: design pixel-perfect branded "
                   "PDFs for documents AND reports with drag-and-drop blocks, ready-made templates, "
                   "multi-company branding and bilingual (EN/AR) support.")
app_email = ""
app_license = "Proprietary"
app_logo_url = "/assets/fibersoft/images/fibersoft-logo.svg"

# ---------------------------------------------------------------------------
# Client: a global script adds the "Download Branded PDF" button to every DocType
# that has an enabled Fibersoft Mapping (Phase 2); with no mappings it falls back to
# Quotation. See public/js/fibersoft_button.js.
# ---------------------------------------------------------------------------
app_include_js = [
    "/assets/fibersoft/js/fibersoft_button.js",
    # "Branded PDF" button in the Query Report view. A .bundle.js: bench build gives it a
    # content-hashed URL every deploy, so browsers can never serve a stale copy of it.
    "fibersoft_report_button.bundle.js",
]

# Standard Fibersoft templates are read-only (duplicate to edit).
# '*'.on_submit: auto-attach the branded PDF when the mapping's toggle is on (cheap no-op otherwise).
doc_events = {
    "Fibersoft Template": {
        "validate": "fibersoft.resolver.protect_standard_template",
    },
    "*": {
        "on_submit": "fibersoft.overrides.auto_attach_on_submit",
    },
}

# Replace ERPNext's native Print > PDF with the branded PDF for doctypes whose Fibersoft Mapping
# has 'Replace Print > PDF' enabled; everything else falls through to the native renderer.
override_whitelisted_methods = {
    "frappe.utils.print_format.download_pdf": "fibersoft.overrides.download_pdf",
    # Wrap the native Report > PDF in the branded header/footer when Settings.brand_reports is on.
    "frappe.utils.print_format.report_to_pdf": "fibersoft.report.report_to_pdf",
}

# Scheduler: clean up expired private render files.
scheduler_events = {
    "daily": [
        "fibersoft.pdf_job.cleanup_expired_files",
    ],
}

# After every deploy/migrate: (1) create/upgrade the Fibersoft config DocTypes (the format
# builder screens) as Custom DocTypes — no command needed; (2) make sure a Chromium is
# available for the Playwright engine. Both idempotent + non-fatal.
# Fresh install: after_migrate does NOT fire on `install-app`, so the config DocTypes would
# never be created and the builder would 500 with TableMissingError. ensure_config is idempotent,
# so running it here AND on every migrate is safe.
after_install = "fibersoft.setup.install_config.ensure_config"

after_migrate = [
    "fibersoft.setup.install_config.ensure_config",
    "fibersoft.compose.clear_probe_cache",  # engine behavior may change with a deploy
]
