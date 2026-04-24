# 🏗️ Architecture Technique - AI Research Agent

## 1️⃣ Vue d'ensemble du système

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
├──────────────────────────┬──────────────────────────────────────┤
│   Streamlit App (app.py) │        CLI (main.py)                │
│                          │                                      │
│  • Web interface         │  • Argument parsing                 │
│  • Real-time progress    │  • Batch processing                │
│  • Report viewer         │  • Script automation               │
│  • Export tools          │                                      │
└──────────────────┬───────┴────────────────┬─────────────────────┘
                   │                        │
              Calls│                        │
                   ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESEARCH PIPELINE                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Planner (agents/planner.py)                                │
│     └─ Generates 5 research questions                          │
│                                                                  │
│  2. Researcher (agents/researcher.py)                          │
│     ├─ WebSearch (tools/web_search.py)                        │
│     │  └─ DuckDuckGo parallel searches                        │
│     ├─ WebScraper (tools/web_scraper.py)                     │
│     │  └─ Fetch + summarize URLs                             │
│     └─ Returns deduplicated results                           │
│                                                                  │
│  3. Summarizer (agents/summarizer.py)                          │
│     ├─ Synthesizes all summaries                              │
│     ├─ Extracts key insights                                  │
│     └─ Generates synthesis text                               │
│                                                                  │
│  4. Writer (agents/writer.py)                                  │
│     ├─ Generates full report (Markdown)                       │
│     ├─ Supports multiple modes (student/business/etc)         │
│     └─ Adds citations and references                          │
│                                                                  │
│  5. Exporter (tools/pdf_exporter.py)                           │
│     └─ Optional: Markdown to PDF conversion                   │
│                                                                  │
└──────────────────────┬────────────────────────────────────────┘
                       │
                 Stores│
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA PERSISTENCE                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Database (database/manager.py)                                │
│  ├─ SQLite: history.db                                        │
│  ├─ Searches table (topic, questions, sources)               │
│  ├─ Sources table (url, title, snippet, summary)             │
│  └─ Reports table (content, mode, metadata)                  │
│                                                                  │
│  File System                                                    │
│  ├─ outputs/reports/  → Generated Markdown/PDF               │
│  ├─ logs/             → research.log                         │
│  └─ .env              → Configuration                        │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

## 2️⃣ Flux de données détaillé

### Flux: Utilisateur → Rapport

```
┌──────────────────────────┐
│  User Input (topic)      │
│  + Configuration         │
└────────────┬─────────────┘
             │
             ▼
    ┌────────────────────┐
    │  ResearchManager   │
    │  __init__(topic)   │
    └────────┬───────────┘
             │
             ├─ generate_plan()
             │  └─ Calls: planner.generate_research_questions()
             │     └─ OpenAI: Creates 5 questions
             │        └─ Returns: list[str]
             │
             ├─ execute_searches()
             │  ├─ Calls: web_search.search_web_parallel()
             │  │  └─ DuckDuckGo: For each question
             │  │     └─ Returns: list[dict] with title, url, snippet
             │  │
             │  └─ Calls: web_search.deduplicate_results()
             │     └─ Removes duplicate URLs
             │        └─ Returns: unique sources list
             │
             ├─ summarize_sources()
             │  └─ For each source:
             │     ├─ Calls: web_scraper.fetch_webpage()
             │     │  └─ BeautifulSoup: Extracts text
             │     │     └─ Returns: str (up to 5000 chars)
             │     │
             │     └─ Calls: web_scraper.summarize_source()
             │        └─ OpenAI: Summarizes content
             │           └─ Returns: summary text
             │
             └─ Returns: dict with all research data
                
                ▼
    ┌────────────────────────┐
    │  ReportWriter          │
    │  write_full_report()   │
    └────────┬───────────────┘
             │
             ├─ Calls: Summarizer.synthesize()
             │  └─ OpenAI: Creates synthesis
             │
             ├─ Generates Markdown report
             │  └─ OpenAI: Full report generation
             │
             └─ add_references()
                └─ Appends sources section
                   └─ Returns: Markdown string
                
                ▼
    ┌───────────────────────────┐
    │  Save Report              │
    └────────┬──────────────────┘
             │
             ├─ Save Markdown
             │  └─ outputs/reports/{topic}.md
             │
             ├─ Save to Database
             │  └─ database/manager.py::save_search()
             │
             └─ Optional: Export to PDF
                └─ pdf_exporter.markdown_to_pdf()
                   └─ ReportLab: Converts to PDF
                      └─ outputs/reports/{topic}.pdf
```

## 3️⃣ Modules et responsabilités

### `agents/planner.py` - Génération de questions

**Interface:**
```python
def generate_research_questions(topic: str, num_questions: int = 5) -> list[str]
def generate_research_plan(topic: str) -> dict
```

**Responsabilités:**
- Analyse le sujet
- Génère questions complémentaires et progressives
- Crée un plan de recherche structuré

**Dépendances:**
- OpenAI API
- loguru (logging)

### `tools/web_search.py` - Recherche web

**Interface:**
```python
def search_web(query: str, num_results: int = 5) -> list[dict]
def search_web_parallel(queries: list[str]) -> dict[str, list[dict]]
def deduplicate_results(results: list[dict]) -> list[dict]
```

**Responsabilités:**
- Effectue des recherches
- Déduplique les résultats
- Retourne structure: {title, url, snippet, source}

**Dépendances:**
- DuckDuckGo API
- loguru (logging)

### `tools/web_scraper.py` - Extraction de contenu

**Interface:**
```python
def fetch_webpage(url: str, timeout: int = 10) -> str
def summarize_source(url: str, title: str = "") -> str
def extract_key_points(text: str, num_points: int = 5) -> list
```

**Responsabilités:**
- Récupère contenu des pages
- Résume avec IA
- Extrait points clés

**Dépendances:**
- BeautifulSoup
- OpenAI API
- requests

### `agents/researcher.py` - Orchestration

**Interface:**
```python
class ResearchManager:
    def generate_plan(self) -> dict
    def execute_searches(self) -> dict
    def summarize_sources(self) -> dict
    def get_research_data(self) -> dict
    def export_json(self, filepath: str)
```

**Responsabilités:**
- Orchestre tout le pipeline
- Gère l'état de recherche
- Exporte les données

**Dépendances:**
- planner, web_search, web_scraper
- loguru

### `agents/summarizer.py` - Synthèse

**Interface:**
```python
class Summarizer:
    def add_summary(self, url: str, summary: str, title: str)
    def synthesize(self) -> str
    def generate_key_insights(self) -> list[str]
    def get_summary_report(self) -> dict
```

**Responsabilités:**
- Agrège les résumés
- Crée synthèse cohérente
- Extrait insights clés

**Dépendances:**
- OpenAI API
- loguru

### `agents/writer.py` - Génération rapport

**Interface:**
```python
class ReportWriter:
    def load_data(self, data: dict)
    def generate_report(self) -> str
    def add_references(self) -> str
    def save_markdown(self, filepath: str)
    def get_report(self) -> str
```

**Responsabilités:**
- Génère rapport structuré
- Supporte plusieurs modes
- Ajoute citations

**Dépendances:**
- OpenAI API
- loguru

### `tools/pdf_exporter.py` - Export PDF

**Interface:**
```python
def markdown_to_pdf(content: str, output_path: str) -> str
def export_report(markdown_path: str, pdf_path: str) -> str
```

**Responsabilités:**
- Convertit Markdown en PDF
- Formate correctement
- Gère styles et images

**Dépendances:**
- ReportLab
- loguru

### `database/manager.py` - Persistance

**Interface:**
```python
class DatabaseManager:
    def save_search(self, topic: str, num_questions, num_sources) -> int
    def get_search_history(self, limit: int = 10) -> list[dict]
    def cache_source(self, url, title, snippet, summary)
    def get_cached_source(self, url) -> dict
    def clear_old_cache(self, days: int = 30)
```

**Responsabilités:**
- Gère base de données SQLite
- Cache les sources
- Historique des recherches

**Dépendances:**
- sqlite3
- loguru

## 4️⃣ Flux de contrôle: App.py

```
app.py (Streamlit Interface)
│
├─ Session initialization
│  ├─ research_data = None
│  ├─ report = None
│  └─ research_complete = False
│
├─ Sidebar Configuration
│  ├─ Input: topic
│  ├─ Slider: num_questions (1-10)
│  ├─ Slider: num_sources (1-20)
│  ├─ Select: report_mode
│  └─ Button: "Start Research"
│
├─ Main Content
│  │
│  ├─ IF "Start Research" clicked:
│  │  │
│  │  ├─ Progress bar (0%)
│  │  ├─ Call: run_full_research()
│  │  │  └─ Progress (10-60%)
│  │  │
│  │  ├─ Call: write_full_report()
│  │  │  └─ Progress (60-80%)
│  │  │
│  │  ├─ Save results to session_state
│  │  ├─ Progress bar (100%)
│  │  └─ research_complete = True
│  │
│  └─ IF research_complete:
│     │
│     ├─ Tab 1: Full Report
│     │  └─ Display: st.markdown(report)
│     │
│     ├─ Tab 2: Synthesis
│     │  └─ Display: List of summaries
│     │
│     ├─ Tab 3: Sources
│     │  └─ Display: Found sources
│     │
│     └─ Tab 4: Export
│        ├─ Button: Download Markdown
│        │  └─ st.download_button(report.md)
│        │
│        └─ Button: Export PDF
│           └─ pdf_exporter.markdown_to_pdf()
│              └─ st.download_button(report.pdf)
│
└─ Footer
   └─ Info and links
```

## 5️⃣ Flux de contrôle: Main.py (CLI)

```
main.py
│
├─ argparse: Parse arguments
│  ├─ --topic (required)
│  ├─ --questions (default: 5)
│  ├─ --sources (default: 10)
│  ├─ --mode (default: balanced)
│  ├─ --pdf (optional flag)
│  └─ --debug (optional flag)
│
├─ Validation
│  ├─ Check OPENAI_API_KEY
│  ├─ Create directories
│  └─ Setup logging
│
├─ Pipeline execution
│  ├─ Call: run_full_research(topic, num_q, num_s)
│  │  └─ Phase 1: Generates plan, searches, summarizes
│  │     └─ Returns: research_data dict
│  │
│  ├─ Call: write_full_report(topic, data, mode)
│  │  └─ Phase 2: Generates report
│  │     └─ Returns: Markdown string
│  │
│  ├─ Save to file
│  │  ├─ outputs/reports/{topic}.md
│  │  └─ database: save_search()
│  │
│  └─ IF --pdf flag:
│     └─ Call: pdf_exporter.markdown_to_pdf()
│        └─ outputs/reports/{topic}.pdf
│
└─ Display results
   └─ Print file paths and summary
```

## 6️⃣ Configuration et variables d'environnement

### Hiérarchie de configuration

```
1. .env file (highest priority)
   └─ Environment variables loaded via python-dotenv

2. config.py
   └─ Reads from .env and provides defaults

3. Function arguments (lowest priority)
   └─ Used when config not specified
```

### Variables clés

```
OPENAI_API_KEY          # Required - OpenAI API key
OPENAI_MODEL           # Optional - Model name
TAVILY_API_KEY         # Optional - Alternative search
SERPAPI_API_KEY        # Optional - Alternative search
APP_DEBUG              # Optional - Debug mode
MAX_SOURCES_PER_QUERY  # Optional - Search limit
RESEARCH_DEPTH         # Optional - Research mode
```

## 7️⃣ Gestion des dépendances

### Dépendances principales

```
├─ streamlit (UI)
├─ openai (LLM)
├─ requests (HTTP)
├─ beautifulsoup4 (scraping)
├─ duckduckgo-search (web search)
├─ python-dotenv (config)
├─ loguru (logging)
├─ reportlab (PDF)
└─ markdown (formatting)
```

### Versions compatibles

- Python 3.10+
- OpenAI API v1.3.0+
- Streamlit 1.28.0+

## 8️⃣ Patterns et best practices

### Design Pattern: Manager Pattern
```python
# ResearchManager orchestre tout
manager = ResearchManager(topic)
manager.generate_plan()
manager.execute_searches()
manager.summarize_sources()
data = manager.get_research_data()
```

### Pattern: Strategy Pattern
```python
# Writer supporte plusieurs stratégies
writer = ReportWriter(topic, mode="student")  # ou business, technical
report = writer.generate_report()
```

### Pattern: Factory-like
```python
# run_full_research crée et orchestre les composants
data = run_full_research(topic)
# Crée ResearchManager, SearchEngine, Scraper, Summarizer internalement
```

## 9️⃣ Performance et optimisation

### Optimisations actuelles
- ✅ Parallel DuckDuckGo searches
- ✅ Result deduplication
- ✅ URL content caching (database)
- ✅ Lazy loading in Streamlit

### Possibilités futures
- [ ] Asynchronous HTTP requests
- [ ] LRU cache for API responses
- [ ] Batch processing for large topics
- [ ] Vector embeddings for better relevance

## 🔟 Évolutivité

### Ajouter une nouvelle source de recherche

1. Créer fonction dans `tools/web_search.py`:
```python
def search_custom_api(query: str) -> list[dict]:
    # Implement API call
    return results
```

2. Modifier `search_web_parallel()` pour utiliser:
```python
if use_custom:
    results.extend(search_custom_api(query))
```

### Ajouter un nouveau mode de rapport

1. Modifier `agents/writer.py`:
```python
def _get_mode_prompt(self) -> str:
    modes = {
        # ... existing modes
        "custom": "Your custom instructions..."
    }
```

2. Mode automatiquement disponible dans CLI et UI

## 📋 Checklist de qualité

- ✅ Type hints on all functions
- ✅ Docstrings on all modules
- ✅ Error handling with try/except
- ✅ Logging with loguru
- ✅ Configuration management
- ✅ Modular design
- ✅ No hardcoded values
- ✅ Environment variables for secrets

---

**Architecture Version**: 1.0  
**Last Updated**: 2024-04-24  
**Maintainer**: AI Research Team
