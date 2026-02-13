# Déploiement de la Base de Données RAG avec Docker

Ce guide explique comment déployer la base de données pour le projet RAG avec Docker.

## Prérequis

- Docker et Docker Compose installés sur votre machine
- Python 3.x (pour le script d'insertion des fichiers)

## Démarrage rapide

### 1. Démarrer les conteneurs Docker

```bash
docker-compose up -d
```

Cette commande va :
- Créer et démarrer un conteneur MariaDB avec la base de données `ragbd`
- Créer et démarrer un conteneur phpMyAdmin pour l'interface web
- Initialiser automatiquement la base de données avec la structure des tables

### 2. Vérifier que les conteneurs sont démarrés

```bash
docker-compose ps
```

Vous devriez voir deux conteneurs en cours d'exécution :
- `ragbd-mariadb`
- `ragbd-phpmyadmin`

### 3. Insérer les fichiers PDF dans la base de données

Une fois les conteneurs démarrés, installez les dépendances Python et exécutez le script :

```bash
# Installer les dépendances
python -m pip install -r requirements.txt

# Insérer les fichiers
python insert_files_to_db.py
```

## Accès aux services

### phpMyAdmin (Interface Web)
- URL: http://localhost:8080
- Utilisateur: `root`
- Mot de passe: (aucun)

### MySQL/MariaDB (Connexion directe)
- Host: `localhost`
- Port: `3307` (3306 est utilisé par MySQL local)
- Base de données: `ragbdddd`
- Utilisateur: `root`
- Mot de passe: (aucun)

## Structure de la base de données

### Table `file`
Stocke les fichiers PDF et leurs métadonnées :
- `id`: Identifiant unique (AUTO_INCREMENT)
- `filename`: Nom du fichier
- `file`: Contenu binaire du fichier (LONGBLOB)
- `file_size`: Taille en octets
- `mime_type`: Type MIME (application/pdf, text/html, etc.)
- `date`: Date d'ajout
- `processed`: Indicateur de traitement (0/1)
- `processed_at`: Date de traitement
- `weaviate_object_id`: ID dans Weaviate (pour RAG)
- `chunk_count`: Nombre de chunks extraits
- `error_message`: Message d'erreur si traitement échoué

### Table `document_chunks`
Stocke les segments de texte extraits des documents :
- `id`: Identifiant unique
- `file_id`: Référence vers la table `file`
- `chunk_index`: Index du chunk dans le document
- `content`: Contenu textuel du chunk
- `page_number`: Numéro de page
- `char_count`: Nombre de caractères
- `weaviate_object_id`: ID dans Weaviate
- `created_at`: Date de création

## Commandes utiles

### Arrêter les conteneurs
```bash
docker-compose down
```

### Arrêter et supprimer les volumes (⚠️ supprime les données)
```bash
docker-compose down -v
```

### Voir les logs
```bash
# Logs de tous les services
docker-compose logs

# Logs de MariaDB uniquement
docker-compose logs mariadb

# Logs en temps réel
docker-compose logs -f
```

### Redémarrer les conteneurs
```bash
docker-compose restart
```

### Accéder au shell MySQL
```bash
docker-compose exec mariadb mysql -u root ragbdddd
```

## Configuration

Les paramètres de connexion peuvent être modifiés dans `docker-compose.yml` :

```yaml
environment:
  MYSQL_ROOT_PASSWORD:              # Mot de passe root (vide = pas de mot de passe)
  MYSQL_DATABASE: ragbdddd          # Nom de la base
  MYSQL_USER: root                  # Utilisateur
  MYSQL_PASSWORD:                   # Mot de passe utilisateur (vide = pas de mot de passe)
```

**⚠️ Important**: En production, configurez des mots de passe sécurisés!

## Dépannage

### Le conteneur ne démarre pas
1. Vérifiez que le port 3306 n'est pas déjà utilisé :
   ```bash
   netstat -an | findstr 3306
   ```
2. Vérifiez les logs :
   ```bash
   docker-compose logs mariadb
   ```

### Erreur de connexion au script Python
1. Assurez-vous que les conteneurs sont démarrés : `docker-compose ps`
2. Vérifiez que la base de données est initialisée (attendez quelques secondes après le démarrage)
3. Vérifiez les identifiants dans `insert_files_to_db.py`

### Les fichiers ne s'insèrent pas
1. Vérifiez que le dossier `bddfilesbeforechunks` existe et contient des fichiers
2. Vérifiez les logs du script Python
3. Vérifiez les permissions sur les fichiers

## Pour vos collaborateurs

Pour que vos collaborateurs utilisent la base de données :

1. **Partagez le projet** (via Git, etc.)
2. **Ils doivent avoir Docker installé**
3. **Ils exécutent** :
   ```bash
   docker-compose up -d
   pip install -r requirements.txt
   python insert_files_to_db.py
   ```

C'est tout ! La base de données sera prête à l'emploi.

## Sauvegarde et restauration

### Sauvegarder la base de données
```bash
docker-compose exec mariadb mysqldump -u root ragbdddd > backup.sql
```

### Restaurer la base de données
```bash
docker-compose exec -T mariadb mysql -u root ragbdddd < backup.sql
```
