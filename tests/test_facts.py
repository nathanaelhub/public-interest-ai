"""Every figure on the page is in facts.json, the page says it, and its source still does."""

import html
import json
import re
import urllib.request
from functools import cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FACTS = json.loads((ROOT / "facts.json").read_text(encoding="utf-8"))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9$%/]", "", s.lower())


def page_text() -> str:
    raw = (ROOT / "index.html").read_text(encoding="utf-8")
    raw = re.sub(r"(?s)<(style|script)\b.*?</\1>", " ", raw)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


def test_the_page_says_every_fact():
    text = norm(page_text())
    for f in FACTS:
        assert norm(f["says"]) in text, f["says"]


def test_every_figure_on_the_page_is_in_facts_json():
    """Numbers in the page body (dates and the byline aside) must each come from a listed fact."""
    body = page_text().split("The projects", 1)[1].split("Not affiliated with Anthropic", 1)[0]
    listed = norm(" ".join(f["says"] for f in FACTS))
    for n in re.findall(r"\$?\d[\d,./]*%?", body):
        if re.fullmatch(r"20\d\d|1|October|\d", n):
            continue
        assert norm(n) in listed, f"{n} on the page isn't in facts.json"


@cache
def source(repo: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/nathanaelhub/{repo}/main/{path}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8")


@pytest.mark.live
@pytest.mark.parametrize("fact", FACTS, ids=[f["says"][:40] for f in FACTS])
def test_the_source_still_says_it(fact):
    assert fact["contains"] in source(fact["repo"], fact["path"])
