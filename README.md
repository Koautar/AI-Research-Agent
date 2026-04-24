# AI Research Agent

Un agent de recherche automatisé qui génère des rapports complets à partir d'un sujet d'intérêt.

## 🎯 Objectif

Transformer un sujet en rapport détaillé avec:
- Plan de recherche structuré
- Requêtes de recherche optimisées
- Résumés de sources fiables
- Rapport final avec citations
- Exports Markdown/PDF

## 🏗️ Architecture

```
User Topic
    ↓
Research Planner (génère questions)
    ↓
Web Search (recherche en ligne)
    ↓
Source Reader (scrape et analyse)
    ↓
Summarizer (résume le contenu)
    ↓
Report Writer (compile le rapport)
    ↓
Final Report (Markdown/PDF)
```

## 📦 Stack

- **Python 3.10+**
- **Streamlit** - Interface utilisateur
- **OpenAI API** - Génération et analyse
- **BeautifulSoup** - Web scraping
- **DuckDuckGo/TavILY** - Recherche web
- **SQLite** - Historique et cache
- **ReportLab** - Export PDF

## 🚀 Installation

### Avec `uv` (recommandé)

```bash
# Cloner/créer le projet
cd ai-research-agent

# Installer avec uv
uv sync

# Créer le .env
cp .env.example .env
# Éditer .env avec votre clé OpenAI
```

### Avec pip

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🔧 Configuration

1. Copier `.env.example` en `.env`
2. Ajouter votre `OPENAI_API_KEY`
3. (Optionnel) Configurer Tavily ou SerpAPI

## 📋 Phases de développement

### Phase 1 ✅ - Version simple
- [x] Structure du projet
- [ ] Générateur de questions de recherche
- [ ] Recherche web
- [ ] Résumé de sources
- [ ] Rapport Markdown

### Phase 2 - Version intelligente
- [ ] Citations et sources
- [ ] Classement des sources
- [ ] Modes de rapport (étudiant/business/technique)
- [ ] Détection sources faibles

### Phase 3 - Version production
- [ ] Interface Streamlit polishée
- [ ] Historique des recherches
- [ ] Export PDF
- [ ] Docker
- [ ] Screenshots et docs

## 💻 Utilisation rapide

```bash
# Lancer l'interface
streamlit run app.py

# Ou utiliser le script CLI
python main.py --topic "Machine Learning" --depth balanced
```

## 📁 Structure

```
ai-research-agent/
├── app.py                 # Interface Streamlit
├── main.py               # CLI principal
├── pyproject.toml        # Dépendances (uv)
├── .env                  # Configuration (gitignored)
├── README.md             # Ce fichier
│
├── agents/
│   ├── planner.py        # Générateur de questions
│   ├── researcher.py     # Gestionnaire de recherche
│   ├── summarizer.py     # Résumé de contenu
│   └── writer.py         # Rédacteur de rapport
│
├── tools/
│   ├── web_search.py     # Recherche web
│   ├── web_scraper.py    # Extraction de contenu
│   └── pdf_exporter.py   # Export PDF
│
├── database/
│   └── history.db        # Historique de recherches
│
└── outputs/
    └── reports/          # Rapports générés
```

## 🔌 Modules principaux

### `agents/planner.py`
```python
def generate_research_questions(topic: str) -> list[str]:
    """Génère 5 questions de recherche pertinentes"""
```

### `tools/web_search.py`
```python
def search_web(query: str, num_results: int = 5) -> list[dict]:
    """Recherche web et retourne résultats structurés"""
```

### `agents/summarizer.py`
```python
def summarize_source(url: str) -> str:
    """Scrape une URL et génère un résumé"""
```

### `agents/writer.py`
```python
def generate_report(summaries: dict) -> str:
    """Génère le rapport final en Markdown"""
```

## 📊 Format des résultats

### Recherche
```json
{
    "title": "...",
    "url": "...",
    "snippet": "...",
    "source": "DuckDuckGo|Tavily"
}
```

### Rapport
```
# Rapport: [Sujet]

## Vue d'ensemble
...

## Résumé des sources
...

## Conclusions
...

## Références
[1] Titre - URL
```

## 🛠️ Développement

```bash
# Formatter le code
black agents/ tools/ app.py main.py

# Linting
flake8 agents/ tools/ app.py main.py

# Tests (futur)
pytest tests/
```

## 📝 Prochaines étapes

- [ ] Implémenter le planner
- [ ] Ajouter web search
- [ ] Scraper et résumer
- [ ] Interface Streamlit
- [ ] Export PDF
- [ ] Historique DB

## 📄 Licence

MIT

---

**Créé avec ❤️ pour la recherche automatisée**
