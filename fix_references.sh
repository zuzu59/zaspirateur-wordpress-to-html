#!/bin/bash

# Script pour nettoyer les références à l'ancien site WordPress

echo "Nettoyage des références au site WordPress original..."

# 1. Remplacer les URLs absolues par des chemins relatifs
find www -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -exec sed -i \
    -e 's|https://www\.melaniezufferey\.ch/|/|g' \
    -e 's|http://www\.melaniezufferey\.ch/|/|g' \
    -e 's|https://melaniezufferey\.ch/|/|g' \
    -e 's|http://melaniezufferey\.ch/|/|g' \
    -e 's|//www\.melaniezufferey\.ch/|/|g' \
    {} \;

# 2. Remplacer les URLs encodées en URL (pour les feeds XML)
find www -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -exec sed -i \
    -e 's|https:%252F%252Fwww\.melaniezufferey\.ch|/|g' \
    -e 's|http:%252F%252Fwww\.melaniezufferey\.ch|/|g' \
    -e 's|%252F%252Fwww\.melaniezufferey\.ch|/|g' \
    {} \;

# 3. Nettoyage des références en double (// au lieu de /)
find www -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -exec sed -i \
    -e 's|href="//|href="/|g' \
    -e 's|src="//|src="/|g' \
    -e 's|url(//|url(/|g' \
    {} \;

# 4. Remplacer les références sans slash final
find www -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -exec sed -i \
    -e 's|https://www\.melaniezufferey\.ch\([^/]\)|/\1|g' \
    -e 's|http://www\.melaniezufferey\.ch\([^/]\)|/\1|g' \
    -e 's|https://melaniezufferey\.ch\([^/]\)|/\1|g' \
    -e 's|http://melaniezufferey\.ch\([^/]\)|/\1|g' \
    {} \;

echo "Nombre de références restantes:"
grep -r "melaniezufferey.ch" www/ --include="*.html" --include="*.css" --include="*.js" | wc -l

echo ""
echo "✅ Nettoyage terminé !"
