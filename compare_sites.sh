#!/bin/bash

# Script pour comparer le site statique avec le site WordPress original

ORIGINAL="https://www.melaniezufferey.ch/"
STATIC_DIR="www"

echo "Comparaison entre le site WordPress original et le site statique"
echo "================================================================"

# Vérifier que le dossier www existe
if [ ! -d "$STATIC_DIR" ]; then
    echo "ERREUR: Le dossier '$STATIC_DIR' n'existe pas. Exécutez d'abord download.sh"
    exit 1
fi

# Compter les fichiers téléchargés
FILE_COUNT=$(find "$STATIC_DIR" -type f | wc -l)
echo "Nombre de fichiers téléchargés: $FILE_COUNT"

# Taille totale
TOTAL_SIZE=$(du -sh "$STATIC_DIR" | cut -f1)
echo "Taille totale: $TOTAL_SIZE"

# Lister les types de fichiers
echo ""
echo "Types de fichiers:"
find "$STATIC_DIR" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20

# Vérifier les fichiers HTML
echo ""
echo "Fichiers HTML:"
find "$STATIC_DIR" -name "*.html" -o -name "*.htm" | head -20

# Vérifier les images
echo ""
echo "Images:"
find "$STATIC_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" -o -name "*.svg" -o -name "*.webp" \) | wc -l

# Vérifier les CSS
echo ""
echo "Fichiers CSS:"
find "$STATIC_DIR" -name "*.css" | wc -l

# Vérifier les JS
echo ""
echo "Fichiers JavaScript:"
find "$STATIC_DIR" -name "*.js" | wc -l

echo ""
echo "================================================================"
echo "Comparaison terminée."
echo "Pour une comparaison visuelle, ouvrez les deux sites dans un navigateur."