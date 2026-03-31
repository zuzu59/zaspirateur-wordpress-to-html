#!/usr/bin/env python3
"""
Nettoyage INTELLIGENT du site WordPress
Supprime les références PHP sans détruire le contenu légitime
"""

import os
import re
from pathlib import Path

def clean_html_smart(filepath):
    """Nettoie un fichier HTML de manière chirurgicale"""

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_size = len(content)

    # 1. SUPPRESSION CHIRURGICALE DES RÉFÉRENCES PHP UNIQUEMENT

    # Supprimer les balises link pingback
    content = re.sub(r'<link\s+rel="pingback"[^>]*>', '', content)

    # Supprimer les balises link vers l'API REST (par URL)
    content = re.sub(r'<link[^>]*href="[^"]*wp-json[^"]*"[^>]*>', '', content)

    # Supprimer les balises link EditURI/RSD
    content = re.sub(r'<link[^>]*(EditURI|rsd)[^>]*>', '', content)

    # 2. REMPLACER LES URLs ABSOLUES (mais garder la structure)
    content = re.sub(r'https?://(?:www\.)?melaniezufferey\.ch', '', content)

    # 3. REMPLACER LES RÉFÉRENCES AUX ENDPOINTS SEULEMENT
    # Ne pas supprimer /wp-content/ (contient images et CSS!)
    # Supprimer seulement les références à /wp-admin/ et /wp-includes/

    # Remplacer ajax_url vers wp-admin
    content = re.sub(r'"ajax_url"\s*:\s*"[^"]*wp-admin[^"]*"', '"ajax_url":""', content)

    # 4. SUPPRIMER SEULEMENT LES VARIABLES INUTILES
    # Ne pas supprimer SiteParameters (c'est la config du site!)
    # Ne pas supprimer les blocs JSON-LD

    # Supprimer juste les variables analytics nuisibles
    content = re.sub(r'<script[^>]*>\s*var\s+SlimStatParams\s*=.*?</script>', '', content, flags=re.DOTALL)

    # 5. NETTOYER LES ATTRIBUTS HREF/SRC CASSÉS
    # Remplacer les href vers wp-admin par #
    content = re.sub(r'href="wp-admin/[^"]*"', 'href="#"', content)
    content = re.sub(r'src="wp-admin/[^"]*"', 'src="#"', content)

    # NE PAS TOUCHER à wp-content - c'est les images et CSS!

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return original_size - len(content)

# TRAITER TOUS LES FICHIERS HTML
print("=" * 70)
print("NETTOYAGE INTELLIGENT - CONSERVATION DU CONTENU")
print("=" * 70)
print()

html_count = 0
total_deleted = 0

for root, dirs, files in os.walk('www'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            deleted = clean_html_smart(filepath)
            total_deleted += deleted
            html_count += 1

print(f"✅ {html_count} fichiers HTML nettoyés")
print(f"✅ {total_deleted:,} bytes inutiles supprimés")
print()

# SUPPRIMER SEULEMENT LES RÉPERTOIRES VRAIMENT INUTILES
print("Suppression des répertoires API/Admin...")
dirs_to_remove = [
    'www/wp-json',      # API REST - pur PHP, pas de contenu utilisateur
    'www/wp-includes',  # Fichiers système PHP
]

for dirpath in dirs_to_remove:
    if os.path.exists(dirpath):
        import shutil
        shutil.rmtree(dirpath)
        print(f"✅ Supprimé: {dirpath}")

# GARDER wp-content - c'est critique!
if os.path.exists('www/wp-content'):
    print("✅ wp-content CONSERVÉ (images, CSS, thème)")
else:
    print("⚠️  wp-content n'existe pas")

print()
print("=" * 70)
print("RÉSULTATS")
print("=" * 70)
print()

# Statistiques finales
html_files = len([f for root, dirs, files in os.walk('www') for f in files if f.endswith('.html')])
css_files = len([f for root, dirs, files in os.walk('www') for f in files if f.endswith('.css')])
image_files = len([f for root, dirs, files in os.walk('www') for f in files if f.endswith(('.jpg', '.png', '.gif', '.svg', '.webp'))])
total_files = len([f for root, dirs, files in os.walk('www') for f in files])

print(f"Total fichiers: {total_files}")
print(f"  - HTML: {html_files} ✅")
print(f"  - CSS: {css_files} ✅")
print(f"  - Images: {image_files} ✅")
print()

# Vérifier qu'on a gardé le contenu critique
with open('www/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    index_content = f.read()

critical_checks = {
    '<nav': 'Navigation',
    '<main': 'Contenu principal',
    '<header': 'En-tête',
    '<footer': 'Pied de page',
    '<img': 'Images',
    '<script type="application/ld+json"': 'JSON-LD',
    'var SiteParameters': 'Configuration site',
}

print("Vérification du contenu:")
for elem, label in critical_checks.items():
    status = "✅" if elem in index_content else "❌"
    print(f"{status} {label}")

print()
print("=" * 70)
print("✅ NETTOYAGE INTELLIGENT TERMINÉ!")
print("=" * 70)
