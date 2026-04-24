#!/bin/bash
# setup_windows.bat - Script d'installation pour Windows

@echo off
setlocal enabledelayedexpansion

echo.
echo 🚀 Setup AI Research Agent pour Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou non accessible
    echo Veuillez installer Python 3.10+ depuis https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python trouvé

REM Install uv
echo.
echo 📦 Installation de uv...
pip install uv

echo.
echo 🔧 Création de l'environnement avec uv...
uv venv

echo.
echo 📥 Installation des dépendances...
uv pip install -r requirements.txt

REM Create .env
if not exist .env (
    echo.
    echo 📝 Création du fichier .env...
    copy .env.example .env
    echo ⚠️  Éditez .env et ajoutez votre OPENAI_API_KEY
) else (
    echo ✓ Fichier .env trouvé
)

echo.
echo ✅ Setup terminé!
echo.
echo Prochaines étapes:
echo   1. Éditez .env avec votre clé API
echo   2. Activez l'env: .venv\Scripts\activate
echo   3. CLI: python main.py --topic "Votre sujet"
echo   4. Interface: streamlit run app.py
echo.
pause
