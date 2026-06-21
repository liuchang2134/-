#!/usr/bin/env python3
"""Small respectful crawler for barbybar.top.

The crawler stays on the same host, skips fragments and non-page links,
rate-limits requests, and writes raw HTML plus extracted text for review.
It uses only the Python standard library so it can run in this workspace
without installing requests/BeautifulSoup.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from collections import deque
from dataclasses import dataclass, asdict
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser


DEFAULT_START = "https://barbybar.top/index.html"
DEFAULT_USER_AGENT = "KarthusLiuLearningCrawler/1.0 (+local study archive)"
SKIP_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".css",
    ".js",
    ".mjs",
    ".json",
    ".pdf",
    ".zip",
    ".rar",
    ".7z",
    ".mp3",
    ".mp4",
    ".webm",
    ".woff",
    ".woff2",
    ".ttf",
}
ROBOTS_CACHE: dict[str, RobotFileParser | None] = {}


@dataclass
class PageRecord:
    url: str
    status: int
    title: str
    description: str
    html_file: str
    text_file: str
    text_chars: int
    links: list[str]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.description = ""
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
            return
        if tag == "title":
            self._in_title = True
            return
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
            return
        if tag == "meta" and attr.get("name", "").lower() == "description":
            self.description = attr.get("content", "").strip()
            return
        if tag in {"p", "div", "section", "article", "header", "footer", "li", "br", "h1", "h2", "h3", "h4", "h5"}:
            self.text_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._skip_depth and tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth -= 1
            return
        if tag == "title":
            self._in_title = False
        if tag in {"p", "div", "section", "article", "li", "h1", "h2", "h3", "h4", "h5"}:
            self.text_parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self.title_parts.append(text)
        self.text_parts.append(text)

    @property
    def title(self) -> str:
        return clean_text(" ".join(self.title_parts))

    @property
    def text(self) -> str:
        return clean_text(" ".join(self.text_parts))


def clean_text(value: str) -> str:
    value = unescape(value)
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n\s+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def normalize_url(url: str) -> str:
    url, _fragment = urldefrag(url)
    parsed = urlparse(url)
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path or "/"
    if path == "/":
        path = "/index.html"
    return urlunparse((scheme, netloc, path, "", parsed.query, ""))


def same_host(url: str, host: str) -> bool:
    return urlparse(url).netloc.lower() == host.lower()


def looks_like_page(url: str) -> bool:
    path = urlparse(url).path.lower()
    suffix = Path(path).suffix
    return not suffix or suffix in {".html", ".htm", ".php"} or suffix not in SKIP_EXTENSIONS


def safe_name(url: str) -> str:
    parsed = urlparse(url)
    raw = f"{parsed.path or '/index.html'}?{parsed.query}" if parsed.query else (parsed.path or "/index.html")
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", raw.strip("/")) or "index.html"
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{slug}_{digest}"


def fetch(url: str, user_agent: str, timeout: int) -> tuple[int, bytes, str]:
    request = Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"})
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("content-type", "")
        return response.status, response.read(), content_type


def decode_html(data: bytes, content_type: str) -> str:
    match = re.search(r"charset=([\w.-]+)", content_type, re.I)
    encodings = [match.group(1)] if match else []
    encodings.extend(["utf-8", "gb18030", "latin-1"])
    for encoding in encodings:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", "ignore")


def allowed_by_robots(url: str, user_agent: str) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    if robots_url in ROBOTS_CACHE:
        parser = ROBOTS_CACHE[robots_url]
        return True if parser is None else parser.can_fetch(user_agent, url)
    parser = RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except Exception:
        ROBOTS_CACHE[robots_url] = None
        return True
    ROBOTS_CACHE[robots_url] = parser
    return parser.can_fetch(user_agent, url)


def extract_links(base_url: str, hrefs: Iterable[str], host: str) -> list[str]:
    found: list[str] = []
    for href in hrefs:
        href = href.strip()
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        url = normalize_url(urljoin(base_url, href))
        if same_host(url, host) and looks_like_page(url):
            found.append(url)
    return sorted(set(found))


def crawl(start_url: str, out_dir: Path, max_pages: int, delay: float, timeout: int, user_agent: str) -> list[PageRecord]:
    start_url = normalize_url(start_url)
    host = urlparse(start_url).netloc
    html_dir = out_dir / "html"
    text_dir = out_dir / "text"
    html_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    queue: deque[str] = deque([start_url])
    seen: set[str] = set()
    records: list[PageRecord] = []

    while queue and len(records) < max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)

        if not allowed_by_robots(url, user_agent):
            print(f"SKIP robots {url}")
            continue

        print(f"GET {url}")
        try:
            status, data, content_type = fetch(url, user_agent, timeout)
        except HTTPError as exc:
            print(f"ERR {exc.code} {url}")
            continue
        except URLError as exc:
            print(f"ERR {exc.reason} {url}")
            continue

        if "html" not in content_type.lower() and data[:100].lower().find(b"<html") == -1:
            print(f"SKIP non-html {content_type} {url}")
            continue

        html = decode_html(data, content_type)
        parser = PageParser()
        parser.feed(html)
        links = extract_links(url, parser.links, host)

        for link in links:
            if link not in seen:
                queue.append(link)

        name = safe_name(url)
        html_path = html_dir / f"{name}.html"
        text_path = text_dir / f"{name}.txt"
        html_path.write_text(html, encoding="utf-8")
        text_path.write_text(parser.text, encoding="utf-8")

        records.append(
            PageRecord(
                url=url,
                status=status,
                title=parser.title,
                description=clean_text(parser.description),
                html_file=str(html_path.relative_to(out_dir)),
                text_file=str(text_path.relative_to(out_dir)),
                text_chars=len(parser.text),
                links=links,
            )
        )

        time.sleep(delay)

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl public pages from barbybar.top into local files.")
    parser.add_argument("--start", default=DEFAULT_START, help="Start URL")
    parser.add_argument("--out", default="materials/barbybar_crawl", help="Output directory")
    parser.add_argument("--max-pages", type=int, default=80, help="Maximum HTML pages to fetch")
    parser.add_argument("--delay", type=float, default=0.8, help="Delay between requests in seconds")
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="Crawler user agent")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    records = crawl(args.start, out_dir, args.max_pages, args.delay, args.timeout, args.user_agent)

    index = {
        "start": normalize_url(args.start),
        "page_count": len(records),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages": [asdict(record) for record in records],
    }
    (out_dir / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "pages.md").write_text(render_markdown(records), encoding="utf-8")
    print(f"\nSaved {len(records)} pages to {out_dir}")


def render_markdown(records: list[PageRecord]) -> str:
    lines = ["# barbybar.top crawl", ""]
    for i, record in enumerate(records, 1):
        lines.extend(
            [
                f"## {i}. {record.title or record.url}",
                "",
                f"- URL: {record.url}",
                f"- Status: {record.status}",
                f"- Text chars: {record.text_chars}",
                f"- HTML: {record.html_file}",
                f"- Text: {record.text_file}",
            ]
        )
        if record.description:
            lines.append(f"- Description: {record.description}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
