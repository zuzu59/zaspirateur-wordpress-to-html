# Convertisseur WordPress → HTML Statique

**Projet**: Conversion du site WordPress en site HTML statique autonome
**Site source**: https://www.melaniezufferey.ch/
**Version**: zf260331.1116

## Objectif

Convertir un site WordPress dynamique en un site HTML statique pouvant être utilisé sans connexion Internet, y compris sur une clé USB.

---

## Démarrage Rapide

### Option 1: Exécuter tout automatiquement (recommandé)
```bash
bash run_all.sh
```

Ceci exécutera tous les scripts dans l'ordre:
1. ✅ Aspiration du site
2. ✅ Configuration Apache
3. ✅ Comparaison visuelle (optionnel)

### Option 2: Exécuter manuellement

#### Étape 1 - Aspirer le site
```bash
python3 scrape.py
```
Crée le dossier `www/` avec tous les fichiers du site statique.

#### Étape 2 - Configurer Apache
```bash
bash setup_apache.sh
```
Configure et démarre Apache sur le port 5173.
Accédez au site: http://localhost:5173

#### Étape 3 - Comparer les pages (optionnel)
```bash
python3 compare_visual.py
```
Prend des captures d'écran et génère un rapport de comparaison.

---

## Fichiers du Projet

| Fichier | Description |
|---------|-------------|
| `scrape.py` | Script Python pour aspirer le site WordPress |
| `setup_apache.sh` | Script Bash pour configurer Apache |
| `compare_visual.py` | Script Python pour comparer visuellement les pages |
| `run_all.sh` | Script principal (exécute tout) |
| `manuel.md` | **Manuel d'utilisation complet** |
| `README.md` | Ce fichier |

---

## Prérequis Système

- **OS**: Linux (Debian/Ubuntu) ou macOS
- **Python 3**: Version 3.6+
- **Connexion Internet**: Requise pendant l'aspiration
- **Accès administrateur**: Requis pour Apache (sudo)

### Installation automatique des dépendances
Les scripts installeront automatiquement:
- `wget` - Aspiration du site
- `apache2` - Serveur web
- Modules Python requis

---

## Processus Complet

### 1️⃣ Aspiration (5-10 minutes)
```bash
python3 scrape.py
```

**Résultat**:
- Dossier `www/` créé
- ~1000+ fichiers téléchargés (HTML, CSS, JS, images)
- Tous les liens corrigés pour fonctionner localement
- Fichier `.htaccess` créé pour la réécriture d'URLs

### 2️⃣ Serveur Web (< 1 minute)
```bash
bash setup_apache.sh
```

**Résultat**:
- Apache2 installé et configuré
- Port 5173 activé
- Site accessible à http://localhost:5173

**Arrêter le serveur**:
```bash
sudo systemctl stop apache2
```

### 3️⃣ Comparaison Visuelle (10-20 minutes)
```bash
python3 compare_visual.py
```

**Résultat**:
- `comparison_report.html` - Rapport visuel interactif
- `comparison_report.json` - Données en JSON
- `comparison_screenshots/` - Dossier avec captures d'écran

---

## Utilisation du Site Statique

### Sur le même ordinateur
```bash
# Le serveur est déjà en cours d'exécution
# Ouvrez: http://localhost:5173
```

### Sur le réseau local
```bash
# Découvrez votre IP
hostname -I

# Accédez depuis un autre ordinateur
# http://<votre-ip>:5173
```

### Sur une clé USB (hors ligne)
1. Copiez le dossier `www/` sur la clé USB
2. Transférez sur l'ordinateur cible
3. Configurez Apache pour pointer vers la clé
4. Accédez à http://localhost:5173

### Ouvrir directement en HTML
Aucun serveur requis:
```bash
open www/www.melaniezufferey.ch/index.html
```

---

## Documentation Complète

Pour le guide d'utilisation détaillé avec dépannage et FAQ:
👉 **Lisez [manuel.md](manuel.md)**

---

## Points Clés de Conversion

### ✅ Inclus dans la conversion
- ✓ Toutes les pages HTML
- ✓ Tous les stylesheets CSS
- ✓ Tous les scripts JavaScript
- ✓ Toutes les images
- ✓ Toutes les polices
- ✓ Tous les assets statiques
- ✓ Correction des URLs internes
- ✓ Support des répertoires sans index.html
- ✓ Caractères spéciaux (UTF-8)

### ⚠️ Limitations
- ✗ Contenu dynamique JavaScript (initial uniquement)
- ✗ Formulaires interactifs (statiques)
- ✗ Zones de commentaires (non fonctionnelles)
- ✗ Certains embeds externes (CDN, YouTube)
- ✗ Authentification (toutes les pages publiques)

---

## Dépannage Rapide

### Apache ne démarre pas
```bash
# Vérifier la syntaxe
sudo apache2ctl configtest

# Voir les erreurs
sudo tail -f /var/log/apache2/static-site-error.log

# Redémarrer
sudo systemctl restart apache2
```

### Le site ne s'affiche pas
```bash
# Vérifier qu'Apache est en cours
sudo systemctl status apache2

# Tester avec curl
curl http://localhost:5173
```

### Réaspirer le site
```bash
rm -rf www/
python3 scrape.py
```

---

## Logs et Rapports

| Fichier | Contenu |
|---------|---------|
| `/var/log/apache2/static-site-error.log` | Erreurs Apache |
| `/var/log/apache2/static-site-access.log` | Accès HTTP |
| `comparison_report.html` | Rapport visuel |
| `comparison_report.json` | Données brutes |

---

## Performances

| Étape | Durée | Remarques |
|-------|-------|----------|
| Aspiration | 5-10 min | Dépend de la connexion Internet |
| Configuration Apache | < 1 min | Très rapide |
| Comparaison | 10-20 min | Capture par capture |
| **Total** | **15-31 min** | Peut être parallélisé |

Le site statique servira les pages **100x plus vite** que l'original WordPress!

---

## Sécurité

⚠️ **Important**:
- Tous les fichiers sont publics (pas d'authentification)
- Les données sensibles en dur seront exposées
- À utiliser que pour l'archivage public

---

## Support

Pour plus d'informations détaillées:
- Lisez le [manuel.md](manuel.md) complet
- Consultez les logs Apache
- Vérifiez le rapport de comparaison HTML

---

**Créé**: 2026-03-31
**Statut**: ✅ Prêt à l'emploi
