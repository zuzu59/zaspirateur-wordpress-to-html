#!/bin/bash

# Script pour nettoyer toutes les références PHP et endpoints WordPress
# qui n'ont pas de sens sur un site HTML statique

echo "Nettoyage des références PHP et WordPress inutiles..."

# 1. Supprimer les liens pingback vers xmlrpc.php
find www -name "*.html" -exec sed -i \
    '/<link rel="pingback"/d' \
    {} \;

# 2. Supprimer les liens vers l'API REST wp-json
find www -name "*.html" -exec sed -i \
    '/<link rel="https:\/\/api\.w\.org\/"/d' \
    {} \;

# 3. Supprimer les liens alternate vers wp-json
find www -name "*.html" -exec sed -i \
    '/<link rel="alternate" title="JSON"/d' \
    {} \;

# 4. Supprimer les liens EditURI vers xmlrpc.php
find www -name "*.html" -exec sed -i \
    '/<link rel="EditURI"/d' \
    {} \;

# 5. Supprimer les références ajax_url au wp-admin
find www -name "*.html" -exec sed -i \
    's|"ajax_url":"/wp-admin/admin-ajax.php"|"ajax_url":"#"|g' \
    {} \;

# 6. Supprimer les scripts JavaScript pour les requêtes AJAX WordPress
find www -name "*.html" -exec sed -i \
    '/wp-admin\/admin-ajax/d' \
    {} \;

# 7. Supprimer les blocs de configuration prefetch qui incluent les patterns wp-*.php
find www -name "*.html" -exec sed -i \
    '/"prefetch":\[{/,/}]\)/s/"prefetch":\[{"source".*}})\]}//' \
    {} \;

echo ""
echo "Références supprimées:"
echo "- Pingback links (xmlrpc.php)"
echo "- REST API links (wp-json)"
echo "- AJAX references"
echo "- RSD links"
echo ""
echo "Nombre de fichiers .html traités: $(find www -name "*.html" | wc -l)"
echo "✅ Nettoyage terminé !"
