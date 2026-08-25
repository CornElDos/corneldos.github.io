#!/usr/bin/env bash
# Byter ut REPLACE_BASE mot din GitHub Pages-bas.
# Anvandning:  ./set-base.sh dittanvandarnamn.github.io/repo-namn
#   (utan https://, utan avslutande slash)
set -euo pipefail
if [ $# -ne 1 ]; then
  echo "Anvandning: ./set-base.sh <användare>.github.io/<repo>"
  exit 1
fi
BASE="$1"
for f in sitemap.xml sitemap-pages.xml sitemap-extra.xml robots.txt; do
  sed -i "s|REPLACE_BASE|$BASE|g" "$f"
  echo "uppdaterad: $f"
done
echo "Klart. Kontrollera med: grep -r '$BASE' ."
