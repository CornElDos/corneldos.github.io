# TESTFALL – sitemap-discovery

Testyta för SEO-verktygets sitemap-discovery. Host: `https://corneldos.github.io`

Discovery-vägar som testas:
1. **robots** – `Sitemap:`-rad i `robots.txt`
2. **head** – `<link rel="sitemap">` i `<head>`
3. **guess** – gissad standardplats (`/sitemap.xml`, `/sitemap_index.xml`, `/wp-sitemap.xml` …)

## Antaganden (viktigt att veta vid testning)

- **Varje fall är självständigt** i sin egen mapp med en egen `robots.txt` och `index.html`,
  så att du kan mata in fallets URL isolerat. Detta förutsätter att verktyget hämtar
  `robots.txt` / gissar standardplatser **relativt den inmatade sökvägen**
  (t.ex. `…/case-guess-only/robots.txt` och `…/case-guess-only/sitemap.xml`).
  Läser ditt verktyg robots.txt **enbart** på origin-roten, så gäller i stället rot-`robots.txt`
  (se nedan) för robots-vägen.
- **Rot-`robots.txt`** innehåller rot-fallets `Sitemap:`-rad **plus** case-8:s tre rader
  (enligt spec – robots.txt måste ligga på roten). Rot-fallet är därför orört: matar du in
  roten hittas rot-sitemapen (6 unika) **och** case-8:s tre sitemaps (6 unika) via robots.
- Sidorna som `<loc>` pekar på behöver **inte** finnas som riktiga HTML-filer – discovery ska
  räkna sitemap-poster, inte crawla sidorna.

## Facit-tabell

| # | Fall | URL att mata in | Facit (unika URL:er / förväntat beteende) |
|---|------|-----------------|--------------------------------------------|
| 0 | root (befintligt) | `https://corneldos.github.io/` | **6** unika (`/`, page-a…e). page-c i båda under-sitemaps → dedup till 6. |
| 1 | robots-only | `https://corneldos.github.io/case-robots-only/` | **3** unika. Hittas **enbart** via robots (`karta-2024.xml`). Ingen head-länk, ej gissbart namn. |
| 2 | head-only | `https://corneldos.github.io/case-head-only/` | **3** unika. Hittas **enbart** via head-länk (`sitemap-huvud.xml`). robots saknar Sitemap-rad, ej gissbart namn. |
| 3 | guess-only | `https://corneldos.github.io/case-guess-only/` | **3** unika. Hittas **enbart** via gissad `/sitemap.xml`. Nämns ej i robots eller head. |
| 4 | broken-xml | `https://corneldos.github.io/case-broken-xml/` | **3** (`<loc>`-taggarna plockas trots oavslutad `<url>`-tagg). De **2** `<a href>`-decoyerna får **ALDRIG** räknas. Alt. acceptabelt: 0 + varning om verktyget avvisar hela filen – men aldrig 2/5. |
| 5 | html-as-sitemap | `https://corneldos.github.io/case-html-as-sitemap/` | **0**. `sitemap.xml` är egentligen en HTML 404-sida med 8 `<a>`. Ska behandlas som **ogiltig sitemap**, inte ge länkantalet (aldrig 8). |
| 6 | deep-index | `https://corneldos.github.io/case-deep-index/` | **5** unika. **3 nästlade index-nivåer**: `sitemap.xml` → `index-niva2.xml` → `index-niva3.xml` → (`blad-a.xml` 3 + `blad-b.xml` 2). |
| 7 | cross-dup | `https://corneldos.github.io/case-cross-dup/` | **6** unika. Ett index → `del-a.xml` (4) + `del-b.xml` (4), överlapp p3 & p4 → 8 listade, 6 unika. |
| 8 | multi-robots | `https://corneldos.github.io/case-multi-robots/` (eller roten) | **6** unika. 3 `Sitemap:`-rader (`sitemap-1/2/3.xml`), 2 URL var, alla distinkta → alla tre ska plockas. |
| 9 | trailing-slash | `https://corneldos.github.io/case-trailing-slash/` | **3** vid normalisering (`page-x` med/utan slash → 1; `page-y` blandad host-case → 1; `page-z`). Naivt utan normalisering: 5. Förväntat: **3**. |
| 10 | relative-loc | `https://corneldos.github.io/case-relative-loc/` | **Spec-brott** (spec kräver absoluta `<loc>`). Strikt verktyg → **0**; tolerant verktyg som resolvar mot sitemap-URL → **3**. Dokumentera vilket ditt gör. |
| 11 | large | `https://corneldos.github.io/case-large/` | **1000** unika. Volymtest att antalet stämmer. |
| 12 | empty-sitemap | `https://corneldos.github.io/case-empty-sitemap/` | **0**, **inget fel** (välformad `urlset` med 0 `<url>`). |
| 13 | multi-topsitemap-overlap | `https://corneldos.github.io/case-multi-topsitemap-overlap/` | **5** unika. TVÅ *fristående* topp-sitemaps (ej index): `sitemap-a.xml` (p1,p2,p3) + `sitemap-b.xml` (p3,p4,p5), delar p3 → naiv summa **6**, union **5**. Exponerar cross-sitemap-dubbelräkning (bugg #5) som ett *enda* index inte gör. |
| 14 | inner-trailing-slash | `https://corneldos.github.io/case-inner-trailing-slash/` | **3** unika efter normalisering (naiv **6**). En giltig sitemap där sido-URL:erna *inuti* har trailing-slash-, path-case- och host-case-varianter av samma sida. Testar normalisering av URL:erna inuti sitemapen (skilt från fil-URL:en). |

## Detaljer per fall

### 1. robots-only
- `case-robots-only/robots.txt` → `Sitemap: …/karta-2024.xml`
- `karta-2024.xml`: 3 `<loc>`. `index.html` saknar head-länk. Filnamnet är ej en gissad standardplats.

### 2. head-only
- `case-head-only/index.html` har `<link rel="sitemap" href="/case-head-only/sitemap-huvud.xml">`
- `robots.txt` finns men utan `Sitemap:`-rad. `sitemap-huvud.xml`: 3 `<loc>`.

### 3. guess-only
- `case-guess-only/sitemap.xml`: 3 `<loc>`. Varken robots eller head nämner den → endast gissning.

### 4. broken-xml
- `sitemap.xml`: 3 giltiga `<loc>` (`riktig-1..3`), sista `<url>` är **oavslutad** och `</urlset>` saknas → icke välformad.
- Innehåller dessutom 2 `<a href>`-decoyer (`lura-mig-1..2`) som **inte** är sitemap-poster.

### 5. html-as-sitemap
- `sitemap.xml` levererar HTML (404-landningssida), 8 `<a href>`, **0** `<loc>`.

### 6. deep-index
- Djup = **3 index-nivåer** innan blad: `sitemap.xml` → `index-niva2.xml` → `index-niva3.xml` → `blad-a.xml` (`djup-1..3`) + `blad-b.xml` (`djup-4..5`).

### 7. cross-dup
- `sitemap.xml` (index) → `del-a.xml` (p1–p4) + `del-b.xml` (p3–p6). Överlapp: p3, p4.

### 8. multi-robots
- Deklareras i **både** `case-multi-robots/robots.txt` och **rot-`robots.txt`**.
- `sitemap-1.xml` (a1,a2), `sitemap-2.xml` (b1,b2), `sitemap-3.xml` (c1,c2) – alla distinkta.

### 9. trailing-slash
- `sitemap.xml` rader: `…/page-x`, `…/page-x/`, `https://CornelDos.github.io/…/page-y`, `…/page-y`, `…/page-z`.
- Testar normalisering av trailing slash och host-case (host är skiftlägesokänslig).

### 10. relative-loc
- `<loc>` använder relativa URL:er: `/case-relative-loc/rel-1.html` (root-relativ), `rel-2.html` (dok-relativ), `../case-relative-loc/rel-3.html` (dot-relativ).
- Sitemap-spec kräver absoluta URL:er – detta testar hur verktyget hanterar spec-brott.

### 11. large
- `sitemap.xml` med 1000 genererade `<loc>` (`artikel-0001..1000.html`). Sidorna finns inte som filer.

### 12. empty-sitemap
- `sitemap.xml` = välformad `<urlset>` utan några `<url>`.

### 13. multi-topsitemap-overlap
- **Två fristående topp-sitemaps på samma nivå** (inget index): `sitemap-a.xml` (p1,p2,p3) och `sitemap-b.xml` (p3,p4,p5), delar `p3`.
- Båda pekas ut via `case-multi-topsitemap-overlap/robots.txt` (två `Sitemap:`-rader).
- Skiljer sig från fall 7: här sker överlappet mellan **två separat upptäckta topp-sitemaps**, inte inom ett index. Facit: union **5**, naiv summa **6**. Exponerar cross-sitemap-dubbelräkning (bugg #5).

### 14. inner-trailing-slash
- En enda giltig `sitemap.xml` där `<loc>`-URL:erna inuti har varianter av samma sida:
  - `produkt`: `/produkt`, `/produkt/` (trailing slash), `/Produkt` (path-case)
  - `artikel`: `https://CornelDos.github.io/…/artikel` + `…corneldos…/artikel` (host-case)
  - `om`: en unik
- 6 rader → **3** unika efter full normalisering (host-case + path-case + trailing slash). Testar normalisering av URL:erna **inuti** sitemapen, skilt från fil-URL:en.
- Not: host-case är alltid säkert att normalisera; path-case (`/Produkt`) är tekniskt signifikant per RFC, så ett strikt verktyg kan ge fler. Önskat facit: **3**.

---

**Summa förväntade unika (per isolerat fall):**
1→3, 2→3, 3→3, 4→3, 5→0, 6→5, 7→6, 8→6, 9→3, 10→0 *eller* 3, 11→1000, 12→0, 13→5, 14→3. Root→6.
