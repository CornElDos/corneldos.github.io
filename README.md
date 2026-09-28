# Sitemap-discovery testsajt

Testyta för ett SEO-verktygs **sitemap-discovery**, hostad på GitHub Pages på
origin-roten: `https://corneldos.github.io`.

Det här är en **ren testsajt utan riktigt innehåll** – sidorna och URL:erna finns
bara för att mata verktyget med kontrollerade fall.

## Vad som testas

Att verktygets sitemap-discovery:

- hittar sitemaps via alla tre vägar: `robots.txt` (`Sitemap:`-rad),
  `<head>` (`<link rel="sitemap">`) och gissade standardplatser
  (`/sitemap.xml`, `/sitemap_index.xml`, `/wp-sitemap.xml` m.fl.),
- följer sitemap-**index** ner till under-sitemaps (även nästlat),
- **deduplicerar** URL:er över flera sitemaps, och
- **inte blåser upp** antalet från trasig XML eller HTML-sidor som utger sig
  för att vara sitemaps.

## Struktur

- **Rot-fallet** – `robots.txt` → `sitemap.xml` (index) → tre under-sitemaps:
  `sitemap-pages.xml` (5), `sitemap-extra.xml` (6, varav page-c är en medveten
  dubblett) och `case-cap/sitemap.xml` (40). Facit för indexet: **50 unika**.
  Rot-`robots.txt` pekar dessutom ut case-8:s tre sitemaps (6 unika), så en körning
  på roten ger **56 unika** totalt.
  - `case-diff/` (3 sidor i `sitemap-extra.xml`) och `ny-sida-test.html`
    (i `sitemap-pages.xml`) är tillagda i efterhand för diff- och omskanningstest.
  - `case-cap/` (40 sidor) är till för att testa crawl-taket.
- **14 isolerade testfall** i egna undermappar (`case-*/`), var och en
  självständig med egen `robots.txt` och `index.html` så att den kan testas
  isolerat. Två av dem exponerar dedup-buggar: `case-multi-topsitemap-overlap/`
  (två fristående topp-sitemaps som delar en URL) och `case-inner-trailing-slash/`
  (URL-varianter av samma sida inuti en sitemap).
- **2 fristående sitemaps som matas in manuellt.** De ligger inte i robots.txt
  eller rot-indexet:
  - `case-gzip/sitemap.xml.gz` – statisk gzip-fil utan `Content-Encoding`, **3 unika**.
  - `case-big/sitemap.xml` – volymtest med 700 riktiga sidor, **700 unika**.

Full lista med URL:er att mata in och facit (förväntat antal unika URL:er /
beteende, samt rot-fallet uppdelat per sitemap) finns i **[TESTFALL.md](TESTFALL.md)**.

## Not om robots.txt-isolering

Att varje undermapp har en egen `robots.txt` förutsätter att det testande
verktyget läser `robots.txt` **relativt inmatad sökväg**. Läser verktyget
`robots.txt` **enbart** på origin-roten gäller i stället rot-`robots.txt`, som
innehåller rot-fallets `Sitemap:`-rad plus case-8:s tre rader. (Samma not som i
[TESTFALL.md](TESTFALL.md).)

## Serving

`.nojekyll` i roten gör att GitHub Pages serverar `.xml`-filerna rått, utan
Jekyll-bearbetning.
