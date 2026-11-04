# Public-interest projects built with Claude

One page connecting three public-interest projects: a Tennessee benefits screener, Nashville
Metro Council digests, and a workshop kit for nonprofit staff.

**Live:** https://nathanaelhub.github.io/public-interest-ai/

## How the page stays honest

Every figure on the page is listed in [`facts.json`](facts.json) with the repo and file it comes
from and the exact text there. Tests check three things:

- the page says every listed fact;
- every number on the page (outside dates) comes from a listed fact;
- **live:** each source file on GitHub still contains its text, so if a project's README changes
  a number, this page's tests fail until it's updated.

The site deploys only after all three pass.

```bash
uv sync
uv run pytest              # includes the live check (needs internet)
uv run pytest -m "not live"
```

## Stack

One static HTML file with inline CSS, light and dark themes, print styles; Python and pytest for
the checks; GitHub Pages.

Not affiliated with Anthropic. MIT license.
