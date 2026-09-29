#!/usr/bin/env python3
"""Generate case-bulk: 300 pages plus sitemap.xml.

The sitemap is intentionally NOT referenced from the root sitemap.xml or
robots.txt; it is only reachable via its direct URL.

Run from anywhere: python3 case-bulk/generate.py
"""
from pathlib import Path

BASE = "https://corneldos.github.io/case-bulk"
COUNT = 300
LASTMOD = "2026-09-29"
OUT = Path(__file__).resolve().parent

PAGE = """<!DOCTYPE html>
<html lang="sv">
<head><meta charset="utf-8"><title>Case bulk: Sida {n}</title></head>
<body><h1>Case bulk: Sida {n}</h1><p>Sida {n} av {total} i case-bulk, bara nabar via direktlankad sitemap. <a href="/">Till start</a></p></body>
</html>
"""


def main():
    nums = [f"{i:03d}" for i in range(1, COUNT + 1)]
    for n in nums:
        (OUT / f"page-{n}.html").write_text(PAGE.format(n=n, total=COUNT), encoding="utf-8")
    urls = "".join(
        f"  <url><loc>{BASE}/page-{n}.html</loc><lastmod>{LASTMOD}</lastmod></url>\n" for n in nums
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
