#!/usr/bin/env python3
"""Check a static site: every local href/src/srcset in the HTML and every url() in the CSS
must point to a file in the repo, and every in-page #fragment must match an id.
Run from the repo root: python3 scripts/check_site.py. Exits 1 if anything is broken."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path.cwd()
SKIP = {".git", "node_modules", "scripts", ".github"}
ATTRS = {"href", "src", "srcset", "poster"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == "id" and value:
                self.ids.add(value)
            if name in ATTRS and value:
                parts = [p.strip().split()[0] for p in value.split(",") if p.strip()] if name == "srcset" else [value]
                self.refs += [(tag, name, p) for p in parts]


def local_target(base, ref):
    """Return (path, fragment) for a local reference, or None for external/special ones."""
    url = urlsplit(ref)
    if url.scheme or url.netloc or ref.startswith(("data:", "javascript:")):
        return None
    path = unquote(url.path)
    if not path:
        return base, url.fragment
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (base.parent / path)
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    return target, url.fragment


def files(pattern):
    return sorted(p for p in ROOT.rglob(pattern) if not SKIP & set(p.relative_to(ROOT).parts))


errors, pages = [], {}
for html in files("*.html"):
    page = Page()
    page.feed(html.read_text(encoding="utf-8"))
    pages[html.resolve()] = page
for html, page in pages.items():
    rel = html.relative_to(ROOT.resolve())
    for tag, attr, ref in page.refs:
        hit = local_target(html, ref)
        if hit is None:
            continue
        target, frag = hit
        if not target.exists():
            errors.append(f"{rel}: <{tag} {attr}=\"{ref}\"> -> missing {target.resolve().relative_to(ROOT.resolve())}")
        elif frag and target.resolve() == html and frag not in page.ids:
            errors.append(f"{rel}: <{tag} {attr}=\"{ref}\"> -> no element with id=\"{frag}\"")
for css in files("*.css"):
    for ref in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", css.read_text(encoding="utf-8")):
        hit = local_target(css, ref)
        if hit and not hit[0].exists():
            errors.append(f"{css.relative_to(ROOT)}: url({ref}) -> missing")

print(f"checked {len(pages)} HTML pages, {len(files('*.css'))} stylesheets: {len(errors)} broken")
for e in errors:
    print("  " + e)
sys.exit(1 if errors else 0)
