# Manuel d'Utilisation - Convertisseur WordPress → HTML Statique

## Objectif

Ce projet convertit un site WordPress dynamique en un site HTML statique pouvant être utilisé sans connexion Internet sur une clé USB.

**Site source:** https://www.melaniezufferey.ch/
**Destination:** Dossier `www/` (site HTML statique)

---

## Architecture du Projet

```
zaspirateur-wordpress-to-html/
├── scrape.py              # Aspiration du site WordPress
├── setup_apache.sh        # Configuration Apache
├── compare_visual.py      # Comparaison visuelle des pages
├── manuel.md              # Ce fichier
├── www/                   # Dossier généré avec le site statique
├── comparison_screenshots/# Captures d'écran des comparaisons
├── comparison_report.html # Rapport de comparaison visuelle
└── comparison_report.json # Données de comparaison en JSON
```

---

## Prérequis

### Système d'exploitation
- Linux (Debian/Ubuntu) ou macOS
- Accès administrateur (sudo)

### Logiciels requis
Les scripts installeront automatiquement les dépendances manquantes:
- `python3` (avec pip)
- `wget`
- `apache2`
- Modules Python: `requests`, `beautifulsoup4`, `playwright`, `Pillow`

### Connexion Internet
Une connexion Internet est requise PENDANT l'aspiration du site.

---

## Étape 1: Aspiration du Site WordPress

### Commande
```bash
python3 scrape.py
```

### Ce que fait ce script

1. **Crée le dossier `www/`** - Destination de l'aspiration
2. **Télécharge le site** avec `wget`:
   - Toutes les pages HTML
   - Tous les fichiers CSS
   - Tous les fichiers JavaScript
   - Toutes les images (JPG, PNG, GIF, SVG, etc.)
   - Tous les assets (polices, vidéos, etc.)
3. **Corrige les liens internes**:
   - Remplace `https://www.melaniezufferey.ch` par des chemins relatifs
   - Convertit les URLs PHP en `.html`
   - Rend tous les chemins indépendants de la racine
4. **Crée un fichier `.htaccess`** pour la configuration serveur
5. **Vérifie la structure** - Affiche les statistiques

### Résultat
```
✅ Aspiration complétée avec succès!
   Site statique généré dans: www/
```

### Durée
- **5-10 minutes** selon la taille du site et la vitesse Internet
- Le script ajoute des délais entre les requêtes pour respecter le serveur

### Problèmes courants

**Erreur: "wget non trouvé"**
- Le script l'installera automatiquement

**Connexion interrompue**
- Relancez `python3 scrape.py` - il reprendra où il s'est arrêté

**Aucun fichier HTML généré**
- Vérifiez votre connexion Internet
- Vérifiez que le site est accessible: `curl https://www.melaniezufferey.ch`

---

## Étape 2: Configuration et Démarrage d'Apache

### Commande
```bash
bash setup_apache.sh
```

### Ce que fait ce script

1. **Vérifie que le dossier `www/` existe**
2. **Installe Apache2** (si nécessaire)
3. **Active les modules requis**:
   - `mod_rewrite` - Réécriture d'URLs
   - `mod_headers` - Gestion des en-têtes
   - `mod_mime` - Types MIME
   - `mod_dir` - Gestion des répertoires
4. **Crée une configuration Apache** pour le port 5173
5. **Vérifie la syntaxe** de la configuration
6. **Démarre le serveur** Apache

### Résultat
```
✅ CONFIGURATION COMPLÉTÉE
🌐 Serveur disponible sur:
   http://localhost:5173
   http://127.0.0.1:5173
   http://192.168.x.x:5173  (IP locale)
```

### Accès au site

Ouvrez un navigateur et allez à:
- `http://localhost:5173`
- Ou `http://127.0.0.1:5173`
- Ou l'adresse IP locale affichée

### Arrêter le serveur
```bash
sudo systemctl stop apache2
```

### Redémarrer le serveur
```bash
sudo systemctl restart apache2
```

### Vérifier l'état
```bash
sudo systemctl status apache2
```

### Configuration Apache

Le fichier de configuration créé est:
`/etc/apache2/sites-available/static-site.conf`

Il contient:
- **DocumentRoot**: Pointe vers le dossier `www/`
- **Port**: 5173
- **Réécriture d'URLs**: Convertit `/page` en `/page.html`
- **Index par défaut**: Sert `index.html` pour les répertoires
- **Types MIME**: Configuration correcte pour CSS, JS, JSON, SVG, etc.

---

## Étape 3: Comparaison Visuelle des Pages

### Commande
```bash
python3 compare_visual.py
```

### Prérequis
- Le serveur Apache doit être en cours d'exécution (voir Étape 2)
- Le site original doit être accessible en ligne

### Ce que fait ce script

1. **Trouve toutes les pages HTML** du site statique
2. **Prend des captures d'écran** de chaque page:
   - Version locale (localhost:5173)
   - Version originale (melaniezufferey.ch)
3. **Compare les images**:
   - Détecte les différences de taille
   - Détecte les différences visuelles
4. **Génère un rapport HTML** avec comparaison côte à côte

### Résultat
Deux fichiers sont générés:

1. **`comparison_report.html`** - Rapport visuel interactif
   - Ouvrez dans un navigateur
   - Voir côte à côte les 2 versions
   - État de chaque page (✓ Identique, ⚠ Différences, ✗ Erreur)

2. **`comparison_report.json`** - Données brutes
   - Métadonnées de comparaison
   - Tailles d'images
   - Détails des différences

3. **`comparison_screenshots/`** - Dossier avec les captures
   - `01_local.png` - Site statique
   - `01_original.png` - Site original
   - Etc.

### Durée
- **10-20 minutes** selon le nombre de pages
- Prend une capture tous les ~30 secondes pour éviter les abus

### Problèmes courants

**Erreur: "Connection refused" pour localhost:5173**
- Vérifiez que Apache est en cours d'exécution: `sudo systemctl status apache2`
- Relancez Apache: `sudo systemctl restart apache2`

**Erreur: "Page WordPress inaccessible"**
- Vérifiez votre connexion Internet
- Le site original peut avoir un firewall

**Captures blanches ou vides**
- Attendez plus longtemps pour le chargement
- Augmentez `wait_until="networkidle"` dans le script

---

## Étape 4: Utilisation du Site Statique

### Sur le même ordinateur
```bash
# Lancez Apache (si pas déjà en cours)
sudo systemctl start apache2

# Ouvrez dans le navigateur
# http://localhost:5173
```

### Sur un autre ordinateur (même réseau)
```bash
# Découvrez votre IP locale
hostname -I

# Ouvrez dans le navigateur du nouvel ordinateur
# http://<votre-ip>:5173
```

### Sur une clé USB (sans connexion Internet)
1. **Copiez le dossier `www/`** sur la clé USB
2. **Transférez sur l'ordinateur cible**
3. **Configurez Apache** en pointant vers le dossier de la clé
4. **Accédez au site** via `http://localhost:5173`

---

## Dépannage

### Le site ne s'affiche pas
1. Vérifiez qu'Apache est en cours d'exécution
   ```bash
   sudo systemctl status apache2
   ```
2. Vérifiez les logs
   ```bash
   sudo tail -f /var/log/apache2/static-site-error.log
   ```
3. Testez avec curl
   ```bash
   curl http://localhost:5173
   ```

### Les styles CSS ne s'appliquent pas
- Les fichiers CSS doivent être dans `www/www.melaniezufferey.ch/` (structure créée par wget)
- Vérifiez que les chemins CSS sont corrects dans les fichiers HTML
- Ouvrez les Outils de développement (F12) pour voir les erreurs

### Les JavaScript ne fonctionnent pas
- Vérifiez que les fichiers `.js` existent dans `www/`
- Vérifiez que les chemins sont corrects
- Vérifiez la console (F12) pour les erreurs

### Les images ne s'affichent pas
- Vérifiez que les images existent dans `www/`
- Vérifiez les chemins dans le HTML
- Vérifiez les logs Apache

### Réaspirer le site
```bash
# Supprimez l'ancien site
rm -rf www/

# Relancez l'aspiration
python3 scrape.py
```

---

## Scripts Disponibles

### `scrape.py`
- **Usage**: `python3 scrape.py`
- **Résultat**: Dossier `www/` avec le site statique
- **Durée**: 5-10 minutes
- **Peut être relancé**: Oui (ajoute aux fichiers existants)

### `setup_apache.sh`
- **Usage**: `bash setup_apache.sh`
- **Résultat**: Apache2 configuré et démarré sur le port 5173
- **Prérequis**: Avoir d'abord exécuté `scrape.py`
- **Accès**: http://localhost:5173

### `compare_visual.py`
- **Usage**: `python3 compare_visual.py`
- **Résultat**: Rapports HTML et JSON de comparaison
- **Prérequis**: Apache en cours d'exécution, site original accessible
- **Durée**: 10-20 minutes

---

## Limitations et Considérations

### Contenu dynamique
- Les éléments JavaScript qui modifient le DOM seront capturés dans leur état initial
- Les formulaires interactifs seront statiques
- Les zones de commentaires ne seront pas fonctionnelles

### Contenu externe
- Certains assets externes (CDN, Google Fonts) seront téléchargés localement
- Certains embed externes (vidéos YouTube, cartes) peuvent ne pas fonctionner
- Les compteurs et analytics ne fonctionneront pas

### Performance
- Le site statique sera **beaucoup plus rapide** que l'original
- Pas d'appels PHP ou base de données
- Peut être servi sur HTTP simple

### Sécurité
- Les informations sensibles en dur dans le JavaScript seront exposées
- Aucune authentification requise pour accéder au site
- À utiliser que pour l'archivage public

### Limite de taille
- Aucune limite théorique
- Performance limitée par la RAM disponible
- Vitesse d'écriture disque

---

## Maintenance

### Mettre à jour le site
```bash
# Supprimez l'ancien site
rm -rf www/

# Réexécutez l'aspiration
python3 scrape.py

# Redémarrez Apache
sudo systemctl restart apache2

# Optionnel: recomparez
python3 compare_visual.py
```

### Archiver le site
```bash
# Créez une archive
tar -czf wordpress-statique-backup.tar.gz www/

# Ou un ZIP
zip -r wordpress-statique-backup.zip www/
```

### Supprimer le site
```bash
# Arrêtez Apache
sudo systemctl stop apache2

# Supprimez le dossier
rm -rf www/

# Optionnel: supprimez la configuration
sudo rm /etc/apache2/sites-available/static-site.conf
sudo a2dissite static-site.conf
sudo systemctl restart apache2
```

---

## Questions Fréquemment Posées

### Q: Puis-je utiliser ce site sans Apache?
**R**: Oui! Les fichiers HTML statiques peuvent être ouverts directement:
```bash
# Ouvrir dans le navigateur par défaut
open www/www.melaniezufferey.ch/index.html
# Ou sur Linux
xdg-open www/www.melaniezufferey.ch/index.html
```

### Q: Puis-je servir sur HTTPS?
**R**: Oui, avec un certificat SSL. Modifiez `/etc/apache2/sites-available/static-site.conf` et ajoutez:
```apache
SSLEngine on
SSLCertificateFile /path/to/cert.pem
SSLCertificateKeyFile /path/to/key.pem
```

### Q: Puis-je changer le port 5173?
**R**: Oui, modifiez `setup_apache.sh` ligne 5: `PORT=XXXX` et relancez le script.

### Q: Combien de temps ça prend?
**R**:
- Aspiration: 5-10 min
- Configuration Apache: < 1 min
- Comparaison: 10-20 min
- **Total: 15-31 minutes**

### Q: Le site fonctionne-t-il hors ligne?
**R**: Oui, une fois généré, le site fonctionne complètement sans Internet.

---

## Support

- Consultez les logs Apache: `sudo tail -f /var/log/apache2/static-site-error.log`
- Vérifiez la configuration: `sudo apache2ctl configtest`
- Lisez les rapports de comparaison: `comparison_report.html`

---

**Version**: 1.0
**Dernière mise à jour**: 2026-03-31
**Auteur**: Script automatisé
