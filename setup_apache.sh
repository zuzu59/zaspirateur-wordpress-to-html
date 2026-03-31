#!/bin/bash
# Script d'installation et configuration d'Apache sur le port 5173
# Sert le site HTML statique du dossier 'www'

set -e

PORT=5173
OUTPUT_DIR="www"
APACHE_CONFIG="/etc/apache2/sites-available/static-site.conf"
APACHE_ENABLE_DIR="/etc/apache2/sites-enabled"

echo "========================================"
echo "CONFIGURATION APACHE POUR SITE STATIQUE"
echo "========================================"

# Vérifier que le dossier www existe
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "❌ Erreur: Dossier '$OUTPUT_DIR' non trouvé"
    echo "   Veuillez d'abord exécuter: python3 scrape.py"
    exit 1
fi

echo "✓ Dossier $OUTPUT_DIR trouvé"

# Vérifier et installer Apache2
if ! command -v apache2 &> /dev/null; then
    echo "📥 Installation d'Apache2..."
    apt-get update
    apt-get install -y apache2 apache2-utils
else
    echo "✓ Apache2 déjà installé"
fi

# Activer les modules nécessaires
echo "🔧 Activation des modules Apache..."
a2enmod rewrite
a2enmod headers
a2enmod mime
a2enmod dir

# Créer la configuration du site
echo "📝 Création de la configuration pour le port $PORT..."

SITE_ROOT=$(pwd)
CONFIG_CONTENT="<VirtualHost *:$PORT>
    ServerName localhost
    ServerAdmin admin@localhost

    DocumentRoot $SITE_ROOT/$OUTPUT_DIR

    <Directory $SITE_ROOT/$OUTPUT_DIR>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted

        # Serve index.html for directories
        DirectoryIndex index.html

        # Enable .htaccess rules
        <IfModule mod_rewrite.c>
            RewriteEngine On
            RewriteBase /

            # If the request is not for an existing file
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteCond %{REQUEST_FILENAME} !-d

            # Rewrite to HTML file if it exists
            RewriteCond %{REQUEST_FILENAME}.html -f
            RewriteRule ^(.*)$ \$1.html [L]
        </IfModule>

        # Proper MIME types
        AddType text/html .html
        AddType text/css .css
        AddType application/javascript .js
        AddType application/json .json
        AddType image/svg+xml .svg
        AddCharset UTF-8 .html .css .js
    </Directory>

    # Logging
    ErrorLog \${APACHE_LOG_DIR}/static-site-error.log
    CustomLog \${APACHE_LOG_DIR}/static-site-access.log combined
</VirtualHost>"

# Écrire la configuration
sudo tee "$APACHE_CONFIG" > /dev/null <<< "$CONFIG_CONTENT"
echo "✓ Configuration créée"

# Activer le site
echo "⚡ Activation du site..."
sudo a2ensite static-site.conf

# Vérifier la syntaxe
echo "✓ Vérification de la syntaxe Apache..."
sudo apache2ctl configtest

# Ajouter le port à la configuration d'écoute
if ! grep -q "Listen $PORT" /etc/apache2/ports.conf; then
    echo "Listen $PORT" | sudo tee -a /etc/apache2/ports.conf
    echo "✓ Port $PORT ajouté à la configuration"
fi

# Redémarrer Apache
echo "🚀 Redémarrage d'Apache..."
sudo systemctl restart apache2

# Attendre qu'Apache démarre
sleep 2

# Vérifier que le service est actif
if sudo systemctl is-active --quiet apache2; then
    echo "✓ Apache2 est actif"
else
    echo "⚠️  Apache2 n'est pas actif"
    sudo systemctl status apache2
    exit 1
fi

# Afficher l'adresse IP locale
echo ""
echo "========================================"
echo "✅ CONFIGURATION COMPLÉTÉE"
echo "========================================"

LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "🌐 Serveur disponible sur:"
echo "   http://localhost:$PORT"
echo "   http://127.0.0.1:$PORT"
echo "   http://$LOCAL_IP:$PORT"
echo ""
echo "📂 Racine du site: $SITE_ROOT/$OUTPUT_DIR"
echo ""
echo "Pour arrêter le serveur:"
echo "   sudo systemctl stop apache2"
echo ""
echo "Pour vérifier l'état:"
echo "   sudo systemctl status apache2"
echo ""
