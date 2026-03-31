#!/bin/bash

# Script pour installer et configurer Apache
# pour servir le site HTML statique

echo "Installation et configuration d'Apache..."

# Mettre à jour les paquets
apt-get update -qq

# Installer Apache
apt-get install -y -qq apache2

# Activer le module rewrite (souvent nécessaire pour les sites statiques)
a2enmod rewrite 2>/dev/null || true

# Créer le dossier du site
mkdir -p /var/www/melaniezufferey

# Copier les fichiers du site dans le dossier Apache
if [ -d "www" ]; then
    cp -r www/* /var/www/melaniezufferey/
    echo "Fichiers copiés dans /var/www/melaniezufferey/"
else
    echo "ERREUR: Le dossier 'www' n'existe pas. Exécutez d'abord download.sh"
    exit 1
fi

# Configurer les permissions
chown -R www-data:www-data /var/www/melaniezufferey
chmod -R 755 /var/www/melaniezufferey

# Créer la configuration du VirtualHost
cat > /etc/apache2/sites-available/melaniezufferey.conf << 'EOF'
<VirtualHost *:80>
    ServerName melaniezufferey.ch
    ServerAlias www.melaniezufferey.ch
    DocumentRoot /var/www/melaniezufferey

    <Directory /var/www/melaniezufferey>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/melaniezufferey-error.log
    CustomLog ${APACHE_LOG_DIR}/melaniezufferey-access.log combined
</VirtualHost>
EOF

# Activer le site
a2ensite melaniezufferey.conf

# Désactiver le site par défaut
a2dissite 000-default.conf 2>/dev/null || true

# Redémarrer Apache
systemctl restart apache2
systemctl enable apache2

echo "=========================================="
echo "Apache est installé et configuré !"
echo "Le site est accessible à l'adresse IPv4 du serveur"
echo "=========================================="

# Afficher l'adresse IP
echo "Adresse IP du serveur:"
hostname -I | awk '{print $1}'