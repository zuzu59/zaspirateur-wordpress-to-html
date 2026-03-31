#!/usr/bin/env python3
"""
Corrige les liens dans la homepage pour qu'ils pointent vers le bon contenu
Basé sur: tmb-id-### + titre affiché
"""

import re
from pathlib import Path

OUTPUT_DIR = "www/www.melaniezufferey.ch"

# Mapping RÉEL basé sur le contenu réel trouvé
# Structure: post_id → correct_folder (basé sur le contenu real)
LINK_MAPPING = {
    # tmb-id-73103 → affiche "Grimpons!" → devrait aller à /73103-2/
    '73103': '73103-2',

    # tmb-id-359 → affiche "Ennéade" → devrait aller à /tinguely/
    # (359 actuallement va à /anguis/, ce qui est faux)
    # On va chercher: quels IDs correspondent à quels folders

    # tmb-id-281 → affiche ? → va à /73103-2/
    # Vérifier...
}

def analyze_homepage():
    """Analyse la homepage pour trouver le vrai mapping"""
    print("📊 Analyse de la homepage...")

    html_file = Path(OUTPUT_DIR) / "index.html"
    content = html_file.read_text(encoding='utf-8', errors='ignore')

    # Trouver tous les tmb-id-### avec leurs liens et titres
    pattern = r'tmb-id-(\d+).*?href="([^"]+)".*?<h2[^>]*>([^<]+)</h2>'

    mappings = []
    for match in re.finditer(pattern, content, re.DOTALL):
        post_id = match.group(1)
        link = match.group(2)
        title = match.group(3).strip()

        mappings.append({
            'post_id': post_id,
            'link': link,
            'title': title
        })

        print(f"  ID {post_id} → Link: {link} → Title: {title}")

    return mappings

def find_where_title_actually_is(title):
    """Trouve quel dossier contient ce titre"""
    base_path = Path(OUTPUT_DIR)

    for dir_path in base_path.iterdir():
        if not dir_path.is_dir():
            continue

        html_file = dir_path / "index.html"
        if html_file.exists():
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            if title in content:
                return dir_path.name

    return None

def fix_links():
    """Corrige les liens pour pointer vers le bon contenu"""
    print("\n🔧 Correction des liens...")

    html_file = Path(OUTPUT_DIR) / "index.html"
    content = html_file.read_text(encoding='utf-8', errors='ignore')
    original = content

    # Analyser les mappings
    mappings = analyze_homepage()

    # Pour chaque problème trouvé, déterminer le bon lien
    print("\n📋 Détermination des bons liens...")
    correct_mappings = {}

    for mapping in mappings:
        post_id = mapping['post_id']
        current_link = mapping['link']
        title = mapping['title']

        # Chercher où ce titre devrait réellement aller
        correct_folder = find_where_title_actually_is(title)

        if correct_folder and correct_folder != current_link.strip('/'):
            print(f"  ✓ ID {post_id} '{title}':")
            print(f"     Lien actuel: {current_link}")
            print(f"     Correct:     /{correct_folder}/")
            correct_mappings[current_link] = f"/{correct_folder}/"
        elif not correct_folder:
            print(f"  ⚠️  ID {post_id} '{title}': INTROUVABLE")
        else:
            print(f"  ✓ ID {post_id} '{title}': CORRECT")

    # Appliquer les corrections
    print("\n🔄 Application des corrections...")
    for old_link, new_link in correct_mappings.items():
        content = content.replace(f'href="{old_link}"', f'href="{new_link}"')
        print(f"  ✓ {old_link} → {new_link}")

    if content != original:
        html_file.write_text(content, encoding='utf-8')
        print(f"\n✅ Fichier index.html corrigé!")
    else:
        print(f"\n✅ Aucune correction nécessaire")

if __name__ == "__main__":
    print("=" * 70)
    print("CORRECTION DES LIENS DE LA HOMEPAGE")
    print("=" * 70)

    fix_links()

    print("\n" + "=" * 70)
