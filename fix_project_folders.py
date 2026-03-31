#!/usr/bin/env python3
"""
Corrige les noms des dossiers de projets pour correspondre à leurs vraies pages
"""

import os
import shutil
from pathlib import Path

OUTPUT_DIR = "www/www.melaniezufferey.ch"

# Mapping correct basé sur les IDs de post et les titres réels
# Structure: old_folder → new_folder (avec le vrai contenu)
FOLDER_MAPPING = {
    'tinguely': 'ennéade',  # /tinguely/ contient "Ennéade"
    # Garder les autres comme ils sont car ils sont corrects
}

def fix_folder_names():
    """Renomme les dossiers pour matcher le contenu réel"""
    print("🔧 Correction des noms de dossiers de projets...")

    base_path = Path(OUTPUT_DIR)

    for old_name, new_name in FOLDER_MAPPING.items():
        old_path = base_path / old_name
        new_path = base_path / new_name

        if old_path.exists():
            # Si le nouveau dossier existe déjà, supprimer l'ancien
            if new_path.exists():
                print(f"  ⚠️  {new_name} existe déjà, suppression de {old_name}")
                shutil.rmtree(old_path)
            else:
                # Renommer le dossier
                os.rename(old_path, new_path)
                print(f"  ✓ {old_name} → {new_name}")
        else:
            print(f"  ⚠️  {old_name} n'existe pas")

def fix_links_to_renamed_folders():
    """Met à jour les liens dans tous les HTML"""
    print("\n🔗 Correction des liens vers les dossiers renommés...")

    files_fixed = 0
    base_path = Path(OUTPUT_DIR)

    for html_file in base_path.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        original = content

        # Remplacer les liens vers les anciens noms
        for old_name, new_name in FOLDER_MAPPING.items():
            content = content.replace(f'href="/{old_name}/', f'href="/{new_name}/')
            content = content.replace(f'href="../{old_name}/', f'href="../{new_name}/')

        if content != original:
            html_file.write_text(content, encoding='utf-8')
            files_fixed += 1

    print(f"  ✓ {files_fixed} fichiers HTML corrigés")

def verify_mapping():
    """Vérifie que le mapping est correct"""
    print("\n✓ Vérification du mapping...")

    base_path = Path(OUTPUT_DIR)

    for old_name, new_name in FOLDER_MAPPING.items():
        new_path = base_path / new_name
        if new_path.exists() and (new_path / "index.html").exists():
            title = ""
            try:
                content = (new_path / "index.html").read_text(encoding='utf-8', errors='ignore')
                import re
                match = re.search(r'<title>([^<]+)</title>', content)
                if match:
                    title = match.group(1).replace(' - Mélanie Zufferey', '')
            except:
                pass
            print(f"  ✓ /{new_name}/ → {title}")
        else:
            print(f"  ✗ /{new_name}/ → NOT FOUND")

if __name__ == "__main__":
    print("=" * 60)
    print("CORRECTION DES NOMS DE DOSSIERS DE PROJETS")
    print("=" * 60)

    fix_folder_names()
    fix_links_to_renamed_folders()
    verify_mapping()

    print("\n" + "=" * 60)
    print("✅ Correction terminée")
    print("=" * 60)
