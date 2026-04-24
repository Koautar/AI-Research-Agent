# 📘 Guide de démarrage - AI Research Agent

## ⚡ Démarrage rapide

### Sur Windows

#### Option 1: Script automatique (Recommandé)
```bash
# Double-cliquez sur:
setup_windows.bat

# Puis:
quickstart_windows.bat
```

#### Option 2: Manuel avec uv
```powershell
# 1. Installer uv (si pas déjà installé)
pip install uv

# 2. Créer l'environnement
uv venv

# 3. Activer l'environnement
.venv\Scripts\activate

# 4. Installer les dépendances
uv pip install -r requirements.txt

# 5. Configurer .env
copy .env.example .env
# Puis éditez .env avec votre OPENAI_API_KEY
```

#### Option 3: Sans uv (pip standard)
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Sur Linux/Mac

```bash
# 1. Installer uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Setup
bash setup.sh

# 3. Activer l'environnement
source .venv/bin/activate

# 4. Configurer .env
cp .env.example .env
# Puis éditez .env avec votre OPENAI_API_KEY
```

## 🔑 Configuration - .env

Créez/éditez le fichier `.env`:

```env
# Required
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Optional
TAVILY_API_KEY=your-api-key
SERPAPI_API_KEY=your-api-key

# Settings
APP_DEBUG=False
MAX_SOURCES_PER_QUERY=5
RESEARCH_DEPTH=balanced
```

**Où obtenir vos clés:**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com (free tier available)
- SerpAPI: https://serpapi.com

## 🚀 Utilisation

### Option 1: Interface Web (Recommandée pour commencer)

```bash
# Activer l'env (si pas actif)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Lancer Streamlit
streamlit run app.py
```

Puis ouvrez: http://localhost:8501

### Option 2: Ligne de commande

```bash
# Recherche simple
python main.py --topic "Machine Learning"

# Recherche avancée avec options
python main.py \
  --topic "Blockchain" \
  --questions 7 \
  --sources 15 \
  --mode technical \
  --pdf
```

**Options CLI:**
```
--topic TEXT       Sujet de recherche (requis)
--questions INT    Nombre de questions (défaut: 5)
--sources INT      Nombre de sources (défaut: 10)
--mode TEXT        Mode: student/business/technical/balanced
--pdf              Exporter en PDF
--debug            Mode debug
```

### Option 3: Scripts Python

```python
from agents.researcher import run_full_research
from agents.writer import write_full_report

# Recherche complète
data = run_full_research("Machine Learning", num_questions=5)

# Rapport
report = write_full_report("Machine Learning", data, mode="balanced")

# Sauvegarde
with open("report.md", "w") as f:
    f.write(report)
```

## 🐳 Avec Docker

```bash
# 1. Configurer .env
copy .env.example .env
# Éditez avec votre clé

# 2. Lancer avec docker-compose
docker-compose up

# 3. Ouvrir
# http://localhost:8501
```

## 📊 Rapports générés

Les rapports sont sauvegardés dans: `outputs/reports/`

Formats:
- `.md` - Markdown (standard)
- `.pdf` - PDF (optionnel avec --pdf)

## 🧪 Vérification

Tester l'installation:
```bash
python test_setup.py
```

Voir les exemples:
```bash
python examples.py
```

## 📁 Structure après setup

```
ai-research-agent/
├── .venv/              # Environnement Python (créé)
├── outputs/            # Rapports générés
│   └── reports/
├── logs/               # Logs (créés)
├── database/           # SQLite (créé)
├── .env                # Configuration (copié de .example)
└── [tous les autres fichiers]
```

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
# Réinstaller les dépendances
uv pip install -r requirements.txt --force-reinstall
```

### "OPENAI_API_KEY not found"
- Créez/éditez `.env`
- Assurez-vous d'avoir copié la clé correcte

### Port 8501 déjà utilisé
```bash
# Utiliser un autre port
streamlit run app.py --server.port 8502
```

### DuckDuckGo search ne fonctionne pas
```bash
# Réinstaller duckduckgo-search
uv pip install duckduckgo-search --force-reinstall
```

## 📚 Ressources

- **Docs OpenAI**: https://platform.openai.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## 💡 Conseils

1. **Première recherche**: Commencez avec 3 questions et 5 sources
2. **Économiser les tokens**: DuckDuckGo est gratuit et suffisant
3. **Mode rapport**: "balanced" pour débuter, "technical" pour détails
4. **Historique**: Tous les rapports sont dans `outputs/reports/`

## 🎯 Prochaines étapes

Après le setup:
1. Essayez l'interface web
2. Testez le CLI
3. Générez votre premier rapport
4. Explorez les modes différents

## ❓ Questions?

- Check le README.md
- Voir examples.py
- Vérifier les logs: `logs/research.log`

---

**Bon research!** 🚀
