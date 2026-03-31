#!/usr/bin/env python3
"""
Script de comparaison visuelle des pages
Compare chaque page du site statique (localhost:5173) avec l'original WordPress
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime
import subprocess

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("⚠️  Playwright non installé. Installation...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)
    from playwright.async_api import async_playwright

ORIGINAL_SITE = "https://www.melaniezufferey.ch"
LOCAL_SITE = "http://localhost:5173"
OUTPUT_DIR = "www"
SCREENSHOTS_DIR = "comparison_screenshots"
REPORT_FILE = "comparison_report.json"

class VisualComparator:
    def __init__(self):
        self.screenshots_dir = Path(SCREENSHOTS_DIR)
        self.screenshots_dir.mkdir(exist_ok=True)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "original_site": ORIGINAL_SITE,
            "local_site": LOCAL_SITE,
            "pages": []
        }
        self.pages_to_compare = []

    def find_html_pages(self):
        """Trouve toutes les pages HTML du site statique"""
        print(f"\n🔍 Recherche des pages HTML dans {OUTPUT_DIR}...")

        html_files = list(Path(OUTPUT_DIR).rglob("*.html"))

        # Filtrer les fichiers système
        html_files = [
            f for f in html_files
            if f.name not in [".htaccess", "robots.txt"]
        ]

        # Convertir en URLs locales
        for html_file in sorted(html_files)[:20]:  # Limiter à 20 pages pour les tests
            relative_path = html_file.relative_to(OUTPUT_DIR)
            local_url = urljoin(LOCAL_SITE + "/", str(relative_path))
            original_url = urljoin(ORIGINAL_SITE + "/", str(relative_path))

            # Nettoyer les URLs
            if str(relative_path) == "index.html":
                local_url = LOCAL_SITE + "/"
                original_url = ORIGINAL_SITE + "/"
            else:
                local_url = local_url.replace("index.html", "")
                original_url = original_url.replace("index.html", "")

            self.pages_to_compare.append({
                "path": str(relative_path),
                "local_url": local_url,
                "original_url": original_url
            })

        print(f"✓ {len(self.pages_to_compare)} pages trouvées")
        return len(self.pages_to_compare) > 0

    async def take_screenshots(self, browser):
        """Prend des captures d'écran des pages"""
        print(f"\n📸 Capture des pages...")

        for i, page_info in enumerate(self.pages_to_compare, 1):
            print(f"  [{i}/{len(self.pages_to_compare)}] {page_info['path']}")

            page_result = {
                "path": page_info["path"],
                "local_url": page_info["local_url"],
                "original_url": page_info["original_url"],
                "screenshots": {},
                "comparison": {}
            }

            # Capture locale
            try:
                page = await browser.new_page()
                page.set_viewport_size({"width": 1280, "height": 1024})

                local_screenshot = self.screenshots_dir / f"{i:02d}_local.png"
                await page.goto(page_info["local_url"], wait_until="networkidle")
                await page.screenshot(path=str(local_screenshot), full_page=True)
                page_result["screenshots"]["local"] = str(local_screenshot)
                print(f"     ✓ Locale capturée")

                await page.close()
            except Exception as e:
                page_result["screenshots"]["local"] = None
                page_result["comparison"]["local_error"] = str(e)
                print(f"     ⚠️  Erreur locale: {e}")

            # Capture originale
            try:
                page = await browser.new_page()
                page.set_viewport_size({"width": 1280, "height": 1024})

                original_screenshot = self.screenshots_dir / f"{i:02d}_original.png"
                await page.goto(page_info["original_url"], wait_until="networkidle", timeout=30000)
                await page.screenshot(path=str(original_screenshot), full_page=True)
                page_result["screenshots"]["original"] = str(original_screenshot)
                print(f"     ✓ Originale capturée")

                await page.close()
            except Exception as e:
                page_result["screenshots"]["original"] = None
                page_result["comparison"]["original_error"] = str(e)
                print(f"     ⚠️  Erreur originale: {e}")

            self.results["pages"].append(page_result)

    async def compare_pages(self):
        """Compare les pages visuellement"""
        print(f"\n🔄 Comparaison des pages...")

        try:
            import subprocess
            from PIL import Image, ImageChops
        except ImportError:
            print("⚠️  Dépendances manquantes, installation...")
            subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], check=True)
            from PIL import Image, ImageChops

        for i, page_result in enumerate(self.results["pages"], 1):
            local_ss = page_result["screenshots"].get("local")
            original_ss = page_result["screenshots"].get("original")

            if local_ss and original_ss and Path(local_ss).exists() and Path(original_ss).exists():
                try:
                    local_img = Image.open(local_ss)
                    original_img = Image.open(original_ss)

                    # Redimensionner si nécessaire
                    if local_img.size != original_img.size:
                        page_result["comparison"]["size_match"] = False
                        page_result["comparison"]["local_size"] = local_img.size
                        page_result["comparison"]["original_size"] = original_img.size
                    else:
                        page_result["comparison"]["size_match"] = True

                    # Calculer la différence
                    diff = ImageChops.difference(local_img, original_img)
                    diff_stats = diff.getextrema()
                    page_result["comparison"]["diff_extrema"] = diff_stats

                    if max(diff_stats) == 0:
                        page_result["comparison"]["identical"] = True
                        print(f"  ✓ Page {i}: Identique")
                    else:
                        page_result["comparison"]["identical"] = False
                        print(f"  ⚠️  Page {i}: Différences détectées")

                except Exception as e:
                    page_result["comparison"]["error"] = str(e)
                    print(f"  ❌ Page {i}: Erreur de comparaison: {e}")

    def generate_report(self):
        """Génère un rapport HTML des comparaisons"""
        print(f"\n📋 Génération du rapport...")

        html_report = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Comparaison Visuelle</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-box {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #007bff;
        }
        .page-comparison {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 6px;
        }
        .page-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        .screenshot-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }
        .screenshot {
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
        }
        .screenshot img {
            width: 100%;
            height: auto;
            display: block;
        }
        .screenshot-label {
            background: #f0f0f0;
            padding: 8px;
            font-weight: bold;
            font-size: 12px;
        }
        .status {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .status.identical {
            background: #d4edda;
            color: #155724;
        }
        .status.different {
            background: #fff3cd;
            color: #856404;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
        }
        .urls {
            font-size: 12px;
            color: #666;
            margin: 10px 0;
        }
        .urls a {
            color: #007bff;
            text-decoration: none;
        }
        .urls a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rapport de Comparaison Visuelle</h1>
        <p><small>Généré le: """ + self.results["timestamp"] + """</small></p>

        <div class="summary">
            <div class="stat-box">
                <div><strong>Pages testées:</strong></div>
                <div>""" + str(len(self.results["pages"])) + """</div>
            </div>
            <div class="stat-box">
                <div><strong>Identiques:</strong></div>
                <div>""" + str(sum(1 for p in self.results["pages"] if p.get("comparison", {}).get("identical"))) + """</div>
            </div>
            <div class="stat-box">
                <div><strong>Différences:</strong></div>
                <div>""" + str(sum(1 for p in self.results["pages"] if not p.get("comparison", {}).get("identical") and "error" not in p.get("comparison", {}))) + """</div>
            </div>
            <div class="stat-box">
                <div><strong>Erreurs:</strong></div>
                <div>""" + str(sum(1 for p in self.results["pages"] if "error" in p.get("comparison", {}))) + """</div>
            </div>
        </div>

        <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
"""

        for i, page in enumerate(self.results["pages"], 1):
            comparison = page.get("comparison", {})
            is_identical = comparison.get("identical", False)
            has_error = "error" in comparison or "local_error" in comparison or "original_error" in comparison

            if is_identical:
                status_class = "identical"
                status_text = "✓ Identique"
            elif has_error:
                status_class = "error"
                status_text = "✗ Erreur"
            else:
                status_class = "different"
                status_text = "⚠ Différences"

            html_report += f"""
        <div class="page-comparison">
            <div class="page-title">Page {i}: {page['path']}</div>
            <div class="status {status_class}">{status_text}</div>

            <div class="urls">
                <div><strong>Locale:</strong> <a href="{page['local_url']}" target="_blank">{page['local_url']}</a></div>
                <div><strong>Originale:</strong> <a href="{page['original_url']}" target="_blank">{page['original_url']}</a></div>
            </div>
"""

            local_ss = page["screenshots"].get("local")
            original_ss = page["screenshots"].get("original")

            if local_ss or original_ss:
                html_report += '<div class="screenshot-container">'
                if local_ss:
                    html_report += f"""
                    <div class="screenshot">
                        <div class="screenshot-label">Site Statique Local</div>
                        <img src="{local_ss}" alt="Site local">
                    </div>
"""
                if original_ss:
                    html_report += f"""
                    <div class="screenshot">
                        <div class="screenshot-label">Site Original WordPress</div>
                        <img src="{original_ss}" alt="Site original">
                    </div>
"""
                html_report += "</div>"

            if comparison.get("error"):
                html_report += f'<p style="color: red;"><strong>Erreur:</strong> {comparison["error"]}</p>'

            html_report += "</div>"

        html_report += """
    </div>
</body>
</html>
"""

        report_path = Path("comparison_report.html")
        report_path.write_text(html_report)
        print(f"✓ Rapport HTML généré: {report_path}")

        # Sauvegarder aussi en JSON
        json_path = Path(REPORT_FILE)
        json_path.write_text(json.dumps(self.results, indent=2))
        print(f"✓ Rapport JSON généré: {json_path}")

    async def run(self):
        """Lance la comparaison complète"""
        if not self.find_html_pages():
            print("❌ Aucune page trouvée")
            return 1

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
            )

            try:
                await self.take_screenshots(browser)
                await self.compare_pages()
                self.generate_report()
                return 0
            finally:
                await browser.close()


async def main():
    print("=" * 60)
    print("COMPARAISON VISUELLE - WORDPRESS STATIQUE")
    print("=" * 60)

    comparator = VisualComparator()
    return await comparator.run()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
