@echo off
echo ========================================
echo   Demarrage de la base de donnees RAG
echo ========================================
echo.

echo [1/3] Demarrage des conteneurs Docker...
docker-compose up -d

if %errorlevel% neq 0 (
    echo [ERREUR] Impossible de demarrer les conteneurs Docker
    echo Verifiez que Docker est installe et demarre
    pause
    exit /b 1
)

echo [OK] Conteneurs demarres
echo.
echo Attente de l'initialisation de la base de donnees (10 secondes)...
timeout /t 10 /nobreak >nul

echo.
echo [2/3] Installation des dependances Python...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer les dependances Python
    pause
    exit /b 1
)

echo.
echo [3/3] Insertion des fichiers dans la base de donnees...
python insert_files_to_db.py

echo.
echo ========================================
echo   Base de donnees prete!
echo ========================================
echo.
echo Acces aux services:
echo - phpMyAdmin: http://localhost:8080
echo - MySQL: localhost:3307
echo.
echo Utilisateur: root
echo Mot de passe: (aucun)
echo.
pause
