# Sitemap-testsajt för Seoella

Statisk testsajt för att verifiera sitemap-discovery och crawl.

## Struktur / vad den testar

- `index.html` – startsida med `<link rel="sitemap">` i `<head>` (testar steg 3, head-discovery)
- `page-a..e.html` – 5 innehållssidor
- `robots.txt` – pekar ut `sitemap.xml` (testar robots-discovery)
- `sitemap.xml` – sitemap-INDEX som pekar på två under-sitemaps (testar index-följning)
- `sitemap-pages.xml` – 4 URL:er: `/`, page-a, page-b, page-c
- `sitemap-extra.xml` – 3 URL:er: page-d, page-e, OCH page-c igen (medveten dubblett)
- `.nojekyll` – så GitHub Pages serverar `.xml` rått utan Jekyll

## Rätt svar (facit)

Unika URL:er i sitemapen = **6**: `/`, page-a, page-b, page-c, page-d, page-e.
page-c finns i BÅDA under-sitemaps → cross-sitemap-dedup ska ge 6, inte 7.
Faktiska sidor på sajten = 6 (start + 5).

## Så här deployar du

1. Skapa ett nytt publikt repo på GitHub, t.ex. `sitemap-test`.
2. `./set-base.sh <användare>.github.io/sitemap-test`  (byter ut platshållaren)
3. Pusha alla filer till `main`.
4. Repo → Settings → Pages → Source: `main` / `/ (root)` → Save.
5. Vänta ~1 min. Sajten ligger på `https://<användare>.github.io/sitemap-test/`
6. Verifiera: öppna `.../sitemap.xml` i webbläsaren, den ska visa XML.

## Testfall du kan skapa sen (genom att ändra filerna)

- Lägg till fler `<url>` → se att estimat/crawl följer med
- Trasig XML i en under-sitemap → testar steg 2 (0 loc + warn)
- Ta bort `<head>`-länken → se att robots/guess ändå hittar den
- Ta bort robots-raden → se att head/guess ändå hittar den
