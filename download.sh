#!/bin/bash

# Script pour aspirer le site WordPress
# https://www.melaniezufferey.ch/

SITE="https://www.melaniezufferey.ch/"
OUTPUT_DIR="www"

echo "Aspiration du site $SITE dans le dossier $OUTPUT_DIR..."

# Créer le dossier www s'il n'existe pas
mkdir -p "$OUTPUT_DIR"

# Télécharger le site avec wget
# -r: récursif
# -k: convertir les liens
# -np: ne pas remonter dans les répertoires parents
# -nH: pas de création de répertoire hostname
# -E: ajustement des extensions
# -p: télécharger tous les fichiers nécessaires pour afficher la page
# -q: mode silencieux
# --cut-dirs: coupe les répertoires
# -l 10: profondeur de récursion

wget --mirror \
     --convert-links \
     --no-parent \
     --no-host-directories \
     --adjust-extension \
     --page-requisites \
     --execute robots=off \
     --no-check-certificate \
     --quiet \
     --level=10 \
     -P "$OUTPUT_DIR" \
     "$SITE"

echo "Aspiration terminée !"
echo "Le site est disponible dans le dossier $OUTPUT_DIR"