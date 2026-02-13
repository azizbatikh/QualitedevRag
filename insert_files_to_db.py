#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour insérer les fichiers PDF dans la base de données MySQL/MariaDB
À exécuter après que le conteneur Docker soit démarré
"""

import os
import pymysql
import mimetypes

# Configuration de la base de données
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,  # Port Docker (3306 est utilisé par MySQL local)
    'database': 'ragbdddd',
    'user': 'root',
    'password': '',
    'charset': 'utf8mb4'
}

# Chemin du dossier contenant les fichiers
FOLDER_PATH = r"bddfilesbeforechunks"

def get_mime_type(filename):
    """Détecte le type MIME du fichier"""
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        return mime_type
    elif filename.lower().endswith('.pdf'):
        return 'application/pdf'
    elif filename.lower().endswith('.html') or filename.lower().endswith('.htm'):
        return 'text/html'
    else:
        return 'application/octet-stream'

def insert_file(cursor, filename, file_path):
    """Insère un fichier dans la base de données"""
    try:
        # Lire le fichier en mode binaire
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        file_size = len(file_content)
        mime_type = get_mime_type(filename)
        
        # Préparer la requête SQL
        insert_query = """
        INSERT INTO `file` (`filename`, `file`, `file_size`, `mime_type`, `processed`)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # Exécuter l'insertion
        cursor.execute(insert_query, (filename, file_content, file_size, mime_type, 0))
        
        print(f"[OK] Fichier insere: {filename} ({file_size} octets, {mime_type})")
        return True
        
    except Exception as e:
        print(f"[ERREUR] Erreur avec {filename}: {e}")
        return False

def main():
    """Fonction principale"""
    connection = None
    try:
        # Connexion à la base de données
        print("Connexion à la base de données...")
        connection = pymysql.connect(**DB_CONFIG)
        
        if connection:
            cursor = connection.cursor()
            print("Connecte a la base de donnees!\n")
            
            # Vérifier si le dossier existe
            if not os.path.exists(FOLDER_PATH):
                print(f"[ERREUR] Le dossier '{FOLDER_PATH}' n'existe pas!")
                return
            
            # Parcourir tous les fichiers du dossier
            files = [f for f in os.listdir(FOLDER_PATH) 
                    if os.path.isfile(os.path.join(FOLDER_PATH, f))]
            
            if not files:
                print(f"[INFO] Aucun fichier trouve dans '{FOLDER_PATH}'")
                return
            
            print(f"Traitement de {len(files)} fichier(s)...\n")
            
            inserted_count = 0
            for filename in files:
                file_path = os.path.join(FOLDER_PATH, filename)
                if insert_file(cursor, filename, file_path):
                    inserted_count += 1
                connection.commit()  # Commit après chaque fichier
            
            print(f"\n[OK] {inserted_count}/{len(files)} fichier(s) insere(s) avec succes!")
            
            # Afficher un résumé
            cursor.execute("SELECT COUNT(*) FROM `file`")
            total_files = cursor.fetchone()[0]
            print(f"[INFO] Total de fichiers dans la base: {total_files}")
            
    except Exception as e:
        print(f"[ERREUR] Erreur de connexion MySQL: {e}")
        print("\nAssurez-vous que:")
        print("1. Le conteneur Docker est demarre (docker-compose up -d)")
        print("2. La base de donnees est initialisee")
        print("3. Les identifiants dans le script sont corrects")
        
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nConnexion fermee.")

if __name__ == "__main__":
    main()
