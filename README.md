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

- **Rot-fallet** – `robots.txt` → `sitemap.xml` (index) → två under-sitemaps med
  en medveten dubblett. Facit: **6 unika URL:er**.
- **12 isolerade testfall** i egna undermappar (`case-*/`), var och en
  självständig med egen `robots.txt` och `index.html` så att den kan testas
  isolerat.

Full lista med URL:er att mata in och facit (förväntat antal unika URL:er /
beteende) finns i **[TESTFALL.md](TESTFALL.md)**.

## Not om robots.txt-isolering

Att varje undermapp har en egen `robots.txt` förutsätter att det testande
verktyget läser `robots.txt` **relativt inmatad sökväg**. Läser verktyget
`robots.txt` **enbart** på origin-roten gäller i stället rot-`robots.txt`, som
innehåller rot-fallets `Sitemap:`-rad plus case-8:s tre rader. (Samma not som i
[TESTFALL.md](TESTFALL.md).)

## Serving

`.nojekyll` i roten gör att GitHub Pages serverar `.xml`-filerna rått, utan
Jekyll-bearbetning.
