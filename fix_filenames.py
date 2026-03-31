#!/usr/bin/env python3
"""
Corrige les noms de fichiers en enlevant les paramètres de query string
Exemple: file.css?ver=123.css → file.css
"""

import os
import re
from pathlib import Path

OUTPUT_DIR = "www/www.melaniezufferey.ch"

def clean_filenames():
    """Renomme les fichiers pour enlever les paramètres ?ver=..."""
    print("🔧 Nettoyage des noms de fichiers...")

    files_renamed = 0

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for filename in files:
            # Chercher les fichiers avec ?ver= dans le nom
            if "?" in filename:
                old_path = os.path.join(root, filename)

                # Extraire le vrai nom en enlevant ?ver=...
                # Exemple: style.css?ver=123.css → style.css
                new_filename = re.sub(r'\?ver=[\w\.]+', '', filename)
                new_filename = re.sub(r'%3F[^%]+%3D[\w\.]+', '', new_filename)

                new_path = os.path.join(root, new_filename)

                try:
                    if os.path.exists(new_path):
                        os.remove(old_path)
                        print(f"  ✗ {filename} (supprimé - doublon)")
                        files_renamed += 1
                    else:
                        os.rename(old_path, new_path)
                        print(f"  ✓ {filename} → {new_filename}")
                        files_renamed += 1
                except Exception as e:
                    print(f"  ⚠ Erreur avec {filename}: {e}")

    return files_renamed

def fix_html_links():
    """Met à jour les références dans les fichiers HTML"""
    print("\n🔗 Correction des liens HTML...")

    files_fixed = 0

    for html_file in Path(OUTPUT_DIR).rglob("*.html"):
        try:
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # Enlever ?ver=... des références
            content = re.sub(r'(["\'])(.*?)\?ver=[\w\.]+(["\'])', r'\1\2\3', content)
            content = re.sub(r'(["\'])(.*?)%3Fver=[\w\.%]+(["\'])', r'\1\2\3', content)

            if content != original_content:
                html_file.write_text(content, encoding='utf-8')
                files_fixed += 1
        except Exception as e:
            print(f"  ⚠ Erreur avec {html_file.name}: {e}")

    return files_fixed

def main():
    print("=" * 60)
    print("CORRECTION DES NOMS DE FICHIERS")
    print("=" * 60)

    renamed = clean_filenames()
    fixed = fix_html_links()

    print("\n" + "=" * 60)
    print(f"✅ {renamed} fichiers renommés")
    print(f"✅ {fixed} fichiers HTML corrigés")
    print("=" * 60)

if __name__ == "__main__":
    main()
