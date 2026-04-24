#!/bin/bash
# quickstart_windows.bat - Démarrage rapide pour Windows

@echo off
setlocal enabledelayedexpansion

:menu
cls
echo.
echo 🎯 AI Research Agent - Menu principal
echo =====================================
echo.
echo 1. 🧪 Tester l'installation
echo 2. 🖥️  Lancer l'interface web
echo 3. 🔬 Lancer une recherche
echo 4. 📚 Voir les exemples
echo 5. 0️⃣  Quitter
echo.

set /p choice="Choisissez (1-5): "

if "%choice%"=="1" (
    python test_setup.py
    pause
    goto menu
)

if "%choice%"=="2" (
    streamlit run app.py
    goto menu
)

if "%choice%"=="3" (
    set /p topic="Sujet de recherche: "
    python main.py --topic "!topic!"
    pause
    goto menu
)

if "%choice%"=="4" (
    python examples.py
    pause
    goto menu
)

if "%choice%"=="5" (
    echo Au revoir! 👋
    exit /b 0
)

echo Option invalide
pause
goto menu
