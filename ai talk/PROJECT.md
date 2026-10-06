# Project context

For the detailed source review, read [HOW_FIBERSOFT_WORKS.md](HOW_FIBERSOFT_WORKS.md).
The full inventory is in [FILE_MAP.md](FILE_MAP.md), and implementation caveats
are in [CODE_CAVEATS.md](CODE_CAVEATS.md). Local version: **1.8.0**.

## Overview

Fibersoft PDF Studio is a visual print-format builder for Frappe / ERPNext. It provides
document and report layouts, PDF rendering, branding, and a Gemini design copilot.
This summary is based on repository files inspected on 2026-10-05; consult the
source before relying on implementation details.

## Source map

| Location | What to look for |
| --- | --- |
| [README.md](../README.md) | Features, installation, requirements, and usage |
| [pyproject.toml](../pyproject.toml) | Python packaging and optional dependencies |
| [fibersoft/](../fibersoft/) | Frappe application package |
| [api.py](../fibersoft/api.py) | Application API |
| [ai.py](../fibersoft/ai.py) | AI design copilot implementation |
| [blocks.py](../fibersoft/blocks.py) | Layout blocks |
| [compose.py](../fibersoft/compose.py) | PDF composition |
| [render/](../fibersoft/render/) | PDF rendering engines |
| [public/builder/index.html](../fibersoft/public/builder/index.html) | Builder frontend |
| [fibersoft/page/](../fibersoft/fibersoft/page/) | Frappe builder and print pages |
| [setup/install_config.py](../fibersoft/setup/install_config.py) | Configuration installation |
| [CI workflow](../.github/workflows/ci.yml) | Bench installation and smoke checks |
| [PUBLISHING.md](../PUBLISHING.md) | Publishing documentation |
| [CUTOVER.md](../CUTOVER.md) | Cutover documentation |

## Environment and compatibility

- Package metadata requires Python 3.10 or later and Frappe 14 through 16.
- The inspected CI workflow covers Frappe 15 and 16.
- This is a Frappe app; full runtime validation needs a configured Bench and site.
- The default PDF engine uses the host's PDF infrastructure. Other engine options
  and fallback behavior are described in the root README.
- License and trademark terms are in [license.txt](../license.txt) and
  [TRADEMARKS.md](../TRADEMARKS.md).

## Validation reference

For Python syntax checks, from the repository root:

```sh
python -m compileall -q fibersoft
```

The following checks are used by CI and require an installed app and configured
test site. Run them from the Bench directory, replacing `<test-site>`:

```sh
bench --site <test-site> execute fibersoft.setup.install_config.check_config
bench --site <test-site> execute fibersoft.lint.check_all --kwargs "{'strict': True}"
```

Syntax checks do not prove runtime behavior. For builder or rendering changes,
also exercise the changed flow and inspect the resulting PDF in the relevant
test environment. Report any checks that could not be run.
