#!/usr/bin/env python3
"""
Script de nettoyage agressif pour convertir un site WordPress en site HTML statique pur
"""

import os
import re
import json
from pathlib import Path

def clean_html_file(filepath):
    """Nettoie un fichier HTML de tous les artefacts WordPress"""

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_size = len(content)

    # 1. SUPPRIMER TOUS LES LIENS WORDPRESS
    # Pingback
    content = re.sub(r'<link\s+rel="pingback"[^>]*>', '', content)

    # API REST
    content = re.sub(r'<link[^>]*rel="https://api\.w\.org/"[^>]*>', '', content)
    content = re.sub(r'<link[^>]*href="[^"]*wp-json[^"]*"[^>]*>', '', content)

    # oEmbed
    content = re.sub(r'<link[^>]*oembed[^>]*>', '', content)

    # RSD
    content = re.sub(r'<link[^>]*EditURI[^>]*>', '', content)

    # 2. SUPPRIMER LES BLOCS SCRIPT JAVASCRIPT PROBLEMATIQUES
    # Variables wpcf7
    content = re.sub(r'<script[^>]*>var\s+wpcf7\s*=\s*\{[^}]*\};</script>', '', content)

    # Blocs JSON Schema Yoast avec wp-content
    content = re.sub(
        r'<script\s+type="application/ld\+json"[^>]*class="yoast-schema-graph"[^>]*>.*?</script>',
        '',
        content,
        flags=re.DOTALL
    )

    # 3. NETTOYER LES BALISES META PROBLEMATIQUES
    # Meta og:image pointant vers wp-content
    content = re.sub(r'<meta\s+property="og:image"[^>]*wp-content[^>]*>', '', content)

    # 4. REMPLACER LES URLS ABSOLUES
    # melaniezufferey.ch
    content = re.sub(r'https?://(?:www\.)?melaniezufferey\.ch/?', '/', content)
    content = re.sub(r'https?:%2F%2F(?:www\.)?melaniezufferey\.ch', '/', content)
    content = re.sub(r'https?:\\\\/\\\\/(?:www\.)?melaniezufferey\.ch', '/', content)

    # 5. NETTOYER LES REFERENCES WP-ADMIN ET WP-JSON
    # ajax_url
    content = re.sub(r'"ajax_url":\s*"[^"]*wp-admin[^"]*"', '"ajax_url":""', content)
    content = re.sub(r"'ajax_url':\s*'[^']*wp-admin[^']*'", "'ajax_url':''", content)

    # Blocs prefetch complexes
    content = re.sub(r'"prefetch":\s*\[\{[^}]*\}\]', '""', content)

    # 6. SUPPRIMER LES BLOCS STYLE AVEC VARIABLES CSS WORDPRESS
    # Variables --wp-*
    content = re.sub(r'--wp-[a-z\-]*:\s*[^;]*;?', '', content)
    content = re.sub(r'var\(--wp-[a-z\-]*\)', '', content)

    # 7. NETTOYER LES REFERENCES WP-CONTENT DANS LES ATTRIBUTS
    # data-guid
    content = re.sub(r'data-guid="[^"]*wp-content[^"]*"', 'data-guid=""', content)
    # data-path
    content = re.sub(r'data-path="[^"]*wp-content[^"]*"', 'data-path=""', content)
    # data-options avec thumbnail wp-content
    content = re.sub(
        r'data-options="([^"]*)(thumbnail:\s*[\'"])[^\'">]*wp-content[^\'">]*([\'"][^"]*)"',
        r'data-options="\1\2#\3"',
        content
    )

    # 8. SUPPRIMER LES BALISES LINK VERS WP-CONTENT
    content = re.sub(r'<link[^>]*href="[^"]*wp-content[^"]*"[^>]*>', '', content)

    # 9. SUPPRIMER LES SCRIPTS AVEC WP-CONTENT
    content = re.sub(r'<script[^>]*src="[^"]*wp-content[^"]*"[^>]*></script>', '', content)

    # 10. SUPPRIMER LES STYLES ID WORDPRESS
    content = re.sub(r"<style[^>]*id='wp-[^']*'[^>]*>[^<]*</style>", '', content)

    # 11. NETTOYER LES CHEMINS RELATIFS WP
    content = re.sub(r'href="wp-admin/[^"]*"', 'href="#"', content)
    content = re.sub(r"href='wp-admin/[^']*'", "href='#'", content)
    content = re.sub(r'href="wp-content/[^"]*"', 'href="#"', content)
    content = re.sub(r"href='wp-content/[^']*'", "href='#'", content)
    content = re.sub(r'href="wp-json/[^"]*"', 'href="#"', content)
    content = re.sub(r"href='wp-json/[^']*'", "href='#'", content)

    content = re.sub(r'src="wp-admin/[^"]*"', 'src="#"', content)
    content = re.sub(r"src='wp-admin/[^']*'", "src='#'", content)
    content = re.sub(r'src="wp-content/[^"]*"', 'src="#"', content)
    content = re.sub(r"src='wp-content/[^']*'", "src='#'", content)
    content = re.sub(r'src="wp-json/[^"]*"', 'src="#"', content)
    content = re.sub(r"src='wp-json/[^']*'", "src='#'", content)

    # 12. SUPPRIMER LES DOUBLES SLASHES AU DÉBUT
    content = re.sub(r'href="//(?!/)([^"]*)"', r'href="/\1"', content)
    content = re.sub(r"href='//(?!/)([^']*)'", r"href='/\1'", content)
    content = re.sub(r'src="//(?!/)([^"]*)"', r'src="/\1"', content)
    content = re.sub(r"src='//(?!/)([^']*)'", r"src='/\1'", content)

    # Écrire le fichier nettoyé
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    deleted_bytes = original_size - len(content)
    return deleted_bytes

# TRAITER TOUS LES FICHIERS
print("=" * 70)
print("NETTOYAGE AGRESSIF DES FICHIERS HTML")
print("=" * 70)
print()

html_count = 0
total_deleted = 0

for root, dirs, files in os.walk('www'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            deleted = clean_html_file(filepath)
            total_deleted += deleted
            html_count += 1
            print(f"✅ {filepath}")

print()
print(f"Traité: {html_count} fichiers HTML")
print(f"Supprimé: {total_deleted:,} bytes")
print()

# SUPPRIMER LES REPERTOIRES ENTIERS INUTILES
print("Suppression des répertoires WordPress...")
dirs_to_remove = ['wp-json', 'wp-content']
for dirname in dirs_to_remove:
    dirpath = os.path.join('www', dirname)
    if os.path.exists(dirpath):
        import shutil
        shutil.rmtree(dirpath)
        print(f"✅ Répertoire '{dirname}' supprimé")

print()
print("=" * 70)
print("✅ NETTOYAGE TERMINÉ!")
print("=" * 70)
