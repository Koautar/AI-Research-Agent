# 🗂️ Index du Projet - AI Research Agent

Bienvenue! Voici un guide complet de tous les fichiers et modules du projet.

## 📋 Guide de lecture par rôle

### 👤 Je suis utilisateur (je veux juste utiliser l'app)

1. **Lire en premier**: [GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md) ⭐
2. Puis: [README.md](README.md)
3. Essayer: `setup_windows.bat` ou `setup.sh`
4. Lancer: `streamlit run app.py`

### 👨‍💻 Je suis développeur (je veux modifier/étendre)

1. **Architecture**: [README.md](README.md) - Section "Architecture"
2. **Code**: `agents/` et `tools/` - Modules principaux
3. **Exemples**: [examples.py](examples.py) - Utilisation
4. **Configuration**: [config.py](config.py) - Paramètres

### 🏢 Je suis DevOps (je veux déployer)

1. **Docker**: [Dockerfile](Dockerfile) + [docker-compose.yml](docker-compose.yml)
2. **Config**: [.env.example](.env.example) - Variables
3. **Dépendances**: [pyproject.toml](pyproject.toml) et [requirements.txt](requirements.txt)

### 🤖 Je veux comprendre uv

→ [UV_GUIDE.md](UV_GUIDE.md) - Tout sur uv

---

## 📂 Structure complète

### 🎯 Fichiers racine

| Fichier | Type | Description |
|---------|------|-------------|
| **README.md** | 📚 Doc | Documentation complète |
| **GUIDE_DEMARRAGE.md** | 📚 Doc | Guide d'installation |
| **UV_GUIDE.md** | 📚 Doc | Guide uv (gestionnaire env) |
| **INDEX.md** | 📚 Doc | Ce fichier |
| **app.py** | 🎨 App | Interface Streamlit |
| **main.py** | 🖥️ CLI | Application ligne de commande |
| **config.py** | ⚙️ Config | Configuration centralisée |
| **examples.py** | 📖 Exemples | Exemples d'utilisation |
| **test_setup.py** | 🧪 Test | Vérification d'installation |
| **pyproject.toml** | 📦 Deps | Dépendances (uv) |
| **requirements.txt** | 📦 Deps | Dépendances (pip) |
| **.env.example** | ⚙️ Config | Template de configuration |
| **.gitignore** | 🔒 VCS | Fichiers ignorés par git |

### 📁 Dossiers

#### `agents/` - Modules de recherche

| Module | Classe/Fonction | Description |
|--------|-----------------|-------------|
| **planner.py** | `generate_research_questions()` | Génère les questions |
| | `generate_research_plan()` | Plan complet |
| **researcher.py** | `ResearchManager` | Orchestration |
| | `run_full_research()` | Pipeline complet |
| **summarizer.py** | `Summarizer` | Synthèse |
| | `synthesize()` | Crée synthèse |
| | `generate_key_insights()` | Insights clés |
| **writer.py** | `ReportWriter` | Rédaction rapport |
| | `write_full_report()` | Rapport final |

#### `tools/` - Outils utilitaires

| Module | Fonction | Description |
|--------|----------|-------------|
| **web_search.py** | `search_web()` | Recherche DuckDuckGo |
| | `search_web_parallel()` | Recherches parallèles |
| | `deduplicate_results()` | Enlève doublons |
| **web_scraper.py** | `fetch_webpage()` | Récupère page |
| | `summarize_source()` | Résume URL |
| | `extract_key_points()` | Points clés |
| **pdf_exporter.py** | `markdown_to_pdf()` | Markdown → PDF |
| | `export_report()` | Export rapport |

#### `database/` - Gestion données

| Module | Classe | Description |
|--------|--------|-------------|
| **manager.py** | `DatabaseManager` | SQLite manager |
| | `save_search()` | Sauve recherche |
| | `get_search_history()` | Historique |
| | `cache_source()` | Cache sources |

#### `outputs/` - Fichiers générés
```
outputs/
├── reports/    # Rapports Markdown/PDF
└── session.json # État session
```

#### `logs/` - Fichiers journaux
```
logs/
└── research.log  # Log principal
```

### ⚙️ Configuration

#### `.streamlit/config.toml`
Configuration Streamlit (thème, serveur, etc.)

#### `.env` / `.env.example`
- `OPENAI_API_KEY` - Clé API OpenAI (requis)
- `OPENAI_MODEL` - Modèle utilisé
- Variables optionnelles pour API tierces

### 🐳 Docker

| Fichier | Description |
|---------|-------------|
| **Dockerfile** | Image Docker |
| **docker-compose.yml** | Orchestration conteneur |

### 🚀 Scripts setup

| Script | OS | Description |
|--------|----|----|
| **setup.sh** | Linux/Mac | Installation auto |
| **setup_windows.bat** | Windows | Installation auto |
| **quickstart.sh** | Linux/Mac | Menu interactif |
| **quickstart_windows.bat** | Windows | Menu interactif |

---

## 🔄 Flux de l'application

### Vue d'ensemble
```
User Input (sujet)
    ↓
Planner (génère questions)
    ↓
WebSearch (recherche web)
    ↓
WebScraper (récupère contenu)
    ↓
Summarizer (résume sources)
    ↓
Writer (génère rapport)
    ↓
PDFExporter (export optionnel)
    ↓
Output (fichier Markdown/PDF)
```

### Flux détaillé du code

```python
# 1. Interface (app.py ou main.py)
topic = "Machine Learning"

# 2. Recherche (agents/researcher.py)
from agents.researcher import run_full_research
data = run_full_research(topic, num_questions=5)
# ├─ Planner: génère 5 questions
# ├─ WebSearch: cherche chaque question
# ├─ WebScraper: résume chaque URL
# └─ retourne data

# 3. Rapport (agents/writer.py)
from agents.writer import write_full_report
report = write_full_report(topic, data, mode="balanced")
# ├─ Synthétise les résumés
# ├─ Ajoute références
# └─ retourne Markdown

# 4. Export (tools/pdf_exporter.py)
from tools.pdf_exporter import markdown_to_pdf
pdf = markdown_to_pdf(report, "output.pdf")
```

---

## 🎯 Cas d'usage courants

### "Je veux juste tester rapidement"
```bash
cd ai-research-agent
setup_windows.bat       # ou setup.sh
streamlit run app.py
```
→ Puis dans le navigateur: http://localhost:8501

### "Je veux utiliser en CLI"
```bash
python main.py --topic "Blockchain" --questions 5 --sources 10 --pdf
```
→ Rapport sauvegardé dans `outputs/reports/`

### "Je veux intégrer dans mon code"
```python
from agents.researcher import run_full_research
from agents.writer import write_full_report

data = run_full_research("Topic", num_questions=5)
report = write_full_report("Topic", data)
```

### "Je veux déployer avec Docker"
```bash
docker-compose up
# Accessible sur http://localhost:8501
```

### "Je veux voir comment ça marche"
```bash
python examples.py
# Menu interactif avec 6 exemples
```

---

## 🔍 Recherche rapide

### Je cherche... [Comment trouver]

| Besoin | Fichier |
|--------|---------|
| Comment générer questions? | `agents/planner.py` |
| Comment faire recherche web? | `tools/web_search.py` |
| Comment résumer une URL? | `tools/web_scraper.py` |
| Comment générer rapport? | `agents/writer.py` |
| Comment exporter PDF? | `tools/pdf_exporter.py` |
| Comment gérer la DB? | `database/manager.py` |
| Comment configurer? | `config.py` ou `.env` |
| Comment lancer Streamlit? | `app.py` |
| Comment utiliser CLI? | `main.py` |
| Voir exemples? | `examples.py` |

---

## 📊 Phases de développement

### ✅ Phase 1 (Complète)
- Génération questions
- Recherche web
- Résumé sources
- Rapport Markdown
- CLI basique
- Web app Streamlit

### 🔄 Phase 2 (Prête)
- Citations/références
- Classement sources
- Modes rapports
- Détection sources faibles

### 🚀 Phase 3 (Infrastructure)
- Docker
- Export PDF
- Historique BD
- Interface raffinée

---

## 📚 Documentation par sujet

### Installation et setup
1. [GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md) - Installation complète
2. [UV_GUIDE.md](UV_GUIDE.md) - Gestionnaire environnement
3. [README.md](README.md) - Aperçu général

### Utilisation
1. [README.md](README.md) - "🚀 Utilisation rapide"
2. [examples.py](examples.py) - 6 exemples
3. [main.py](main.py) - Options CLI
4. [app.py](app.py) - Interface Web

### Développement
1. [agents/planner.py](agents/planner.py) - Questions
2. [agents/researcher.py](agents/researcher.py) - Orchestration
3. [tools/web_search.py](tools/web_search.py) - Recherche
4. [agents/writer.py](agents/writer.py) - Génération rapport

### Déploiement
1. [Dockerfile](Dockerfile) - Image Docker
2. [docker-compose.yml](docker-compose.yml) - Orchestration
3. [pyproject.toml](pyproject.toml) - Dépendances
4. [.env.example](.env.example) - Configuration

---

## 🆘 FAQ - Problèmes courants

**Q: Ça lance pas...**
→ Voir [GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md) section Troubleshooting

**Q: Comment changer le modèle?**
→ Éditer `.env`: `OPENAI_MODEL=gpt-3.5-turbo`

**Q: Comment utiliser ma propre API search?**
→ Modifier [tools/web_search.py](tools/web_search.py)

**Q: Peut-on sauvegarder l'historique?**
→ Oui! Voir [database/manager.py](database/manager.py)

**Q: Comment ajouter une nouvelle fonctionnalité?**
→ [README.md](README.md) - Section Architecture

---

## 📞 Support

| Question | Ressource |
|----------|-----------|
| Installer? | [GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md) |
| Utiliser? | [examples.py](examples.py) |
| Déboguer? | [test_setup.py](test_setup.py) |
| Étendre? | [agents/](agents/) et [tools/](tools/) |
| Déployer? | [docker-compose.yml](docker-compose.yml) |

---

**Dernière mise à jour**: 2024-04-24  
**Version**: 0.1.0 (Phase 1)  
**Statut**: ✅ Prêt pour utilisation
