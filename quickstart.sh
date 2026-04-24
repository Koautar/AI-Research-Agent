#!/bin/bash
# Script de démarrage rapide

echo "🎯 AI Research Agent - Démarrage rapide"
echo "======================================"
echo ""
echo "Choisissez une option:"
echo "1. 🧪 Tester l'installation (setup.py)"
echo "2. 🖥️  Lancer l'interface web (Streamlit)"
echo "3. 🔬 Lancer une recherche (CLI)"
echo "4. 📊 Lancer avec Docker"
echo ""
read -p "Option (1-4): " choice

case $choice in
    1)
        python test_setup.py
        ;;
    2)
        streamlit run app.py
        ;;
    3)
        read -p "Sujet de recherche: " topic
        python main.py --topic "$topic"
        ;;
    4)
        docker-compose up
        ;;
    *)
        echo "Option invalide"
        ;;
esac
