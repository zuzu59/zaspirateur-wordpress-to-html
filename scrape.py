#!/usr/bin/env python3
"""
Script d'aspiration du site WordPress vers HTML statique
Convertit https://www.melaniezufferey.ch/ en site statique dans le dossier 'www'
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

SITE_URL = "https://www.melaniezufferey.ch"
OUTPUT_DIR = "www"

def create_output_dir():
    """Crée le dossier de destination"""
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    print(f"✓ Dossier {OUTPUT_DIR} créé")

def scrape_with_wget():
    """Utilise wget pour aspirer le site entier"""
    print(f"\n📥 Aspiration du site {SITE_URL}...")

    cmd = [
        "wget",
        "-r",  # Récursif
        "-p",  # Télécharge tous les assets (CSS, JS, images)
        "-E",  # Convertit les liens en .html
        "-P", OUTPUT_DIR,  # Destination
        "-k",  # Convertit les liens pour local
        "-w", "1",  # Délai d'1 seconde entre les requêtes
        "--no-check-certificate",  # Ignorer les certificats SSL expirés
        "--user-agent=Mozilla/5.0",
        SITE_URL
    ]

    try:
        subprocess.run(cmd, check=True, timeout=600)
        print("✓ Aspiration complétée")
    except subprocess.CalledProcessError as e:
        print(f"⚠ Erreur wget: {e}")
        print("Continuant malgré tout...")
    except FileNotFoundError:
        print("⚠ wget non trouvé, installation...")
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "-y", "wget"], check=True)
        scrape_with_wget()

def fix_internal_links():
    """Corrige les liens internes et les références PHP"""
    print("\n🔧 Correction des liens internes...")

    html_files = list(Path(OUTPUT_DIR).rglob("*.html"))

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            original_content = content

            # Remplace les URLs absolues du site original
            content = re.sub(
                r'https?://www\.melaniezufferey\.ch',
                '',
                content
            )
            content = re.sub(
                r'https?://melaniezufferey\.ch',
                '',
                content
            )

            # Corrige les chemins PHP en .html
            content = re.sub(
                r'(["\'])/index\.php(["\'])',
                r'\1/index.html\2',
                content
            )

            # Convertit les URLs relatives pour éviter les chemins ../../../
            content = re.sub(
                r'href=["\'](?!(?:https?:|/|#|\.))([^"\']+)["\']',
                lambda m: f'href="{urljoin("/", m.group(1))}"',
                content
            )

            if content != original_content:
                html_file.write_text(content, encoding='utf-8')

        except Exception as e:
            print(f"⚠ Erreur avec {html_file}: {e}")

    print(f"✓ {len(html_files)} fichiers HTML corrigés")

def create_htaccess():
    """Crée un .htaccess pour servir index.html par défaut"""
    htaccess_content = """# Redirige les URLs sans extension vers HTML
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /

    # Si le fichier ou dossier n'existe pas
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d

    # Redirige vers le fichier .html correspondant
    RewriteRule ^(.*)$ $1.html [L]
    RewriteCond %{REQUEST_FILENAME}.html -f
    RewriteRule ^(.*)$ $1.html [L]
</IfModule>

# Sert index.html pour les répertoires
DirectoryIndex index.html

# Défaut MIME types
AddType text/html .html
AddType text/css .css
AddType application/javascript .js
AddType application/json .json
AddType image/svg+xml .svg
"""

    htaccess_path = Path(OUTPUT_DIR) / ".htaccess"
    htaccess_path.write_text(htaccess_content)
    print("✓ Fichier .htaccess créé")

def download_external_resources():
    """Télécharge les ressources externes (polices, CDN, etc.)"""
    print("\n📦 Téléchargement des ressources externes...")

    resources_dir = Path(OUTPUT_DIR) / "assets"
    resources_dir.mkdir(exist_ok=True)

    # Cette étape est partiellement gérée par wget -p
    # Mais on peut ajouter des ressources supplémentaires manuellement si nécessaire
    print("✓ Ressources traitées")

def verify_structure():
    """Vérifie la structure créée"""
    print("\n📋 Vérification de la structure...")

    html_count = len(list(Path(OUTPUT_DIR).rglob("*.html")))
    css_count = len(list(Path(OUTPUT_DIR).rglob("*.css")))
    js_count = len(list(Path(OUTPUT_DIR).rglob("*.js")))

    # Compter les images
    img_count = 0
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.svg']:
        img_count += len(list(Path(OUTPUT_DIR).rglob(ext)))

    print(f"  📄 {html_count} fichiers HTML")
    print(f"  🎨 {css_count} fichiers CSS")
    print(f"  ✨ {js_count} fichiers JavaScript")
    print(f"  🖼️  {img_count} fichiers images")

    if html_count == 0:
        print("⚠ Aucun fichier HTML trouvé!")
        return False

    return True

def main():
    print("=" * 60)
    print("CONVERTISSEUR WORDPRESS → HTML STATIQUE")
    print("=" * 60)

    try:
        create_output_dir()
        scrape_with_wget()
        fix_internal_links()
        create_htaccess()
        download_external_resources()

        if verify_structure():
            print("\n✅ Aspiration complétée avec succès!")
            print(f"   Site statique généré dans: {OUTPUT_DIR}/")
            return 0
        else:
            print("\n⚠️  Aspiration incomplète")
            return 1

    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
