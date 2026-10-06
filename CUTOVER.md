# Fibersoft app rename

The application is now **Fibersoft PDF Studio**, with Python package/app id
`fibersoft`, module `Fibersoft`, and **Print with Fibersoft** buttons.

## Install the renamed application

Use the checkout containing these changes on a fresh Frappe site:

```sh
bench get-app fibersoft https://github.com/Faizan-Sab/Fibersoft-PDF-Studio.git --branch main
bench --site <new-site> install-app fibersoft
bench --site <new-site> migrate
bench --site <new-site> execute fibersoft.setup.install_config.check_config
```

The builder is `/app/fibersoft-builder`; the print page is `/app/fibersoft-print`.
Assets live under `/assets/fibersoft/`. The site creates Fibersoft Settings, Block,
Template, Snippet, Mapping Condition, Mapping and AI Settings DocTypes.

## Move an existing installation

**Do not replace an installed `lumenpdf` package with this renamed package and run
migrate.** Frappe stores installed app names, and an old registration with a missing
Python package can stop Bench commands with `ModuleNotFoundError`.

1. Keep the original checkout available to the original site. Back up its database,
   uploaded files and configuration before making installation changes.
2. Export saved document and report formats from the original builder using
   **File > Export as .json**. Record per-company settings, mapping priorities,
   conditions, enabled toggles, report defaults and saved snippets. Format export
   contains the format definition, not all these separate records.
3. Install `fibersoft` on a fresh site using the renamed checkout above. The rename
   does not automatically migrate the old DocType records or app registration.
4. Transfer the site's business data and uploaded files using your normal site
   migration process. Restore company branding, import formats with
   **File > Import from .json**, and recreate defaults, mappings and snippets.
5. Set your Gemini key/model in **Fibersoft AI Settings**. Configure your real
   support address as `fibersoft_feedback_email` if you use builder feedback.
6. Check a document print, a report print, PDF download, email attachment and the
   native print override on the new site before switching users to it.

The original site remains the fallback until the new site is verified. This local
source change does not run site migrations, uninstall apps, or alter any database.

## Configuration and browser preferences

New site configuration uses `fibersoft_*`. Engine and Gemini settings also read
previous `lumenpdf_*` and `brandpdf_*` keys as fallbacks; the new key takes priority.
Feedback uses only an explicitly configured `fibersoft_feedback_email`, so the
rebranded app does not send feedback to the original publisher by default.

When opened at the same browser origin, the builder copies the old draft and panel
preferences into `fibersoft_*` localStorage keys and removes the old keys after a
successful transfer. A draft does not move automatically to a different origin.

## Source and attribution

The Fibersoft source repository is
[Faizan-Sab/Fibersoft-PDF-Studio](https://github.com/Faizan-Sab/Fibersoft-PDF-Studio),
with `main` as its installation branch. A local app rename does not rename an
upstream repository or branch. CI checks renamed installations on pushes to any branch.

Original copyright, SPDX identifiers, licence and trademark notices remain as
source attribution. Bundled screenshots are historical references; capture new
Fibersoft screenshots before publishing a marketplace listing.

The previous cutover from `brandpdf` to `lumenpdf` is repository history. The
upstream tag `legacy/brandpdf-final` identifies the earlier implementation; it is
not a rollback procedure for the new Fibersoft installation.
