#!/bin/bash
# Script de setup pour Linux/Mac

echo "🚀 Setup AI Research Agent"
echo "================================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installant uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo ""
echo "📦 Création de l'environnement avec uv..."
uv venv

echo ""
echo "📥 Installation des dépendances..."
uv pip install -r requirements.txt

echo ""
echo "🔧 Configuration..."
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "⚠️  Éditez .env et ajoutez votre OPENAI_API_KEY"
fi

echo ""
echo "✅ Setup terminé!"
echo ""
echo "Prochaines étapes:"
echo "  1. Éditez .env avec votre clé API"
echo "  2. Activez l'env: source .venv/bin/activate"
echo "  3. CLI: python main.py --topic 'Votre sujet'"
echo "  4. Interface: streamlit run app.py"
