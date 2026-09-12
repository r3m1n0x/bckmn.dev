#!/usr/bin/env python3
"""Check built HTML, assets, RSS and publication boundaries without dependencies."""
import argparse
import base64
import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.styles = [], set(), []
        self.h1 = 0
        self.redirect = False
        self.noindex = False
        self.canonical = None
        self.active_elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "iframe", "form"):
            self.active_elements.append(tag)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "meta":
            self.redirect |= a.get("http-equiv", "").lower() == "refresh"
            self.noindex |= a.get("name") == "robots" and "noindex" in a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a["href"]
        if tag == "link" and a.get("rel") == "stylesheet":
            self.styles.append((a["href"], a.get("integrity")))
        for name in ("href", "src"):
            if name in a:
                self.links.append(a[name])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--preview", action="store_true")
    args = parser.parse_args()
    root = args.output.resolve()
    pages = {p: Page(p.read_text()) for p in root.rglob("*.html")}
    errors = []
    for required in ("index.html", "blog/index.html", "about/index.html", "imprint/index.html", "404.html", "index.xml", "sitemap.xml", "robots.txt", "CNAME"):
        if not (root / required).is_file():
            errors.append(f"Missing {required}")
    for path, page in pages.items():
        if not args.preview and page.active_elements:
            errors.append(f"{path}: active elements conflict with the static-site privacy notice: {page.active_elements}")
        if not page.redirect and page.h1 != 1:
            errors.append(f"{path}: expected one h1, got {page.h1}")
        if not args.preview and not page.redirect and path.name != "404.html":
            if page.noindex or not page.canonical:
                errors.append(f"{path}: production page is not indexable or has no canonical URL")
        for link in page.links:
            u = urlsplit(link)
            if u.scheme and u.scheme not in ("http", "https"):
                continue
            if u.netloc and u.hostname not in ("www.bckmn.dev", "bckmn.dev", "localhost", "127.0.0.1"):
                continue
            target = root / unquote(u.path).lstrip("/") if u.path.startswith("/") else path.parent / unquote(u.path)
            if not u.path:
                target = path
            if target.is_dir():
                target /= "index.html"
            target = target.resolve()
            if not target.exists():
                errors.append(f"{path}: broken link {link}")
            elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
                errors.append(f"{path}: missing anchor {link}")
        for href, integrity in page.styles:
            asset = root / urlsplit(href).path.lstrip("/")
            if asset.exists():
                actual = "sha256-" + base64.b64encode(hashlib.sha256(asset.read_bytes()).digest()).decode()
                if integrity != actual:
                    errors.append(f"{path}: stylesheet integrity mismatch")
    for path in root.rglob("*.xml"):
        ET.parse(path)
    feed = ET.parse(root / "index.xml").getroot()
    for item in feed.findall("channel/item"):
        if "/blog/" not in item.findtext("link", ""):
            errors.append("RSS contains a non-blog page")
    if not args.preview:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in (".html", ".xml"):
                text = path.read_text()
                if "following-a-dns-query" in text or "Local preview" in text or "hugo-profile.netlify.app" in text:
                    errors.append(f"{path}: preview or theme content in production output")
        if "Disallow: /" in (root / "robots.txt").read_text():
            errors.append("Production robots.txt blocks the site")
        if (root / "CNAME").read_text().strip() != "www.bckmn.dev":
            errors.append("Unexpected CNAME")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(pages)} HTML pages; internal links, anchors, CSS integrity, XML, RSS and publication checks")


if __name__ == "__main__":
    main()
