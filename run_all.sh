#!/bin/bash
# Script principal - Exécute tout le processus de conversion
# Usage: bash run_all.sh

set -e

echo ""
echo "========================================="
echo "  CONVERTISSEUR WORDPRESS → HTML STATIQUE"
echo "========================================="
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
STEP_COUNT=0
TOTAL_STEPS=4

# Fonction pour afficher les étapes
print_step() {
    STEP_COUNT=$((STEP_COUNT + 1))
    echo ""
    echo -e "${YELLOW}▶ ÉTAPE $STEP_COUNT/$TOTAL_STEPS: $1${NC}"
    echo "========================================="
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Étape 1: Aspiration du site
print_step "ASPIRATION DU SITE WORDPRESS"
if python3 scrape.py; then
    print_success "Aspiration complétée"
else
    print_error "Erreur lors de l'aspiration"
    exit 1
fi

# Étape 2: Configuration Apache
print_step "CONFIGURATION ET DÉMARRAGE D'APACHE"
if bash setup_apache.sh; then
    print_success "Apache configuré et démarré"
else
    print_error "Erreur lors de la configuration d'Apache"
    exit 1
fi

# Demander si l'utilisateur veut faire la comparaison
echo ""
echo -e "${YELLOW}▶ Voulez-vous effectuer la comparaison visuelle des pages?${NC}"
echo "  Cela prendra environ 10-20 minutes..."
read -p "  (o/n): " -n 1 -r RESPONSE
echo ""

if [[ $RESPONSE =~ ^[Oo]$ ]]; then
    print_step "COMPARAISON VISUELLE DES PAGES"
    if python3 compare_visual.py; then
        print_success "Comparaison complétée"
        echo ""
        echo "  Rapport disponible: comparison_report.html"
    else
        print_error "Erreur lors de la comparaison"
        # Ne pas quitter, l'important est fait
    fi
else
    echo "  Comparaison ignorée"
fi

# Résumé final
echo ""
echo "========================================="
echo -e "${GREEN}✅ PROCESSUS TERMINÉ AVEC SUCCÈS${NC}"
echo "========================================="
echo ""
echo "🌐 Le site est maintenant disponible à:"
echo "   http://localhost:5173"
echo ""
echo "📂 Fichiers générés:"
echo "   • www/                 - Site HTML statique"
echo "   • manuel.md            - Guide d'utilisation complet"
echo ""
if [ -f "comparison_report.html" ]; then
    echo "📊 Rapport de comparaison:"
    echo "   • comparison_report.html"
    echo ""
fi
echo "Pour arrêter Apache: sudo systemctl stop apache2"
echo ""
