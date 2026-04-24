# 🚀 QUICKSTART - 5 minutes chrono

## ⚡ Pour les pressés

### Sur Windows

```bash
# 1. Double-cliquez
setup_windows.bat

# 2. Éditez .env
# - Ajoutez votre OPENAI_API_KEY
# - Sauvegardez

# 3. Lancez
streamlit run app.py

# 4. Ouvrez
# http://localhost:8501

# 5. Entrez un sujet et cliquez "Démarrer"
```

### Sur Linux/Mac

```bash
# 1. Run setup
bash setup.sh

# 2. Éditez .env
nano .env  # ou votre éditeur
# Ajoutez OPENAI_API_KEY

# 3. Activez env
source .venv/bin/activate

# 4. Lancez
streamlit run app.py

# 5. Profitez!
```

## 📋 Qu'est-ce que j'ai?

Un **agent de recherche automatisé** qui:

1. Prend un sujet
2. Génère 5 questions
3. Cherche le web
4. Résume les résultats
5. Crée un rapport PDF
6. Tout en 5 minutes ⏱️

## 🔑 Clé API (requis une seule fois)

### Obtenir une clé OpenAI

1. Allez à: https://platform.openai.com/api-keys
2. Créez une clé
3. Copiez-la
4. Collez dans `.env`

```env
OPENAI_API_KEY=sk-your-key-here
```

## 🎯 Utilisation rapide

### Interface Web (Easiest)

```
Lancez → Entrez un sujet → Cliquez bouton → Attendez → Export
```

### Ligne de commande

```bash
python main.py --topic "Machine Learning"
```

### Avec options

```bash
python main.py \
  --topic "Blockchain" \
  --questions 7 \
  --sources 15 \
  --mode technical \
  --pdf
```

## 📊 Résultat

Rapport Markdown + PDF dans `outputs/reports/`

## 🎓 Voir des exemples

```bash
python examples.py
```

## 🧪 Vérifier que tout marche

```bash
python test_setup.py
```

## 🚨 Problème?

### "ModuleNotFoundError"
```bash
uv pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
1. Créez `.env` (copier `.env.example`)
2. Ajoutez votre clé

### "Port déjà utilisé"
```bash
streamlit run app.py --server.port 8502
```

## 📚 Docs complètes

- **Setup**: GUIDE_DEMARRAGE.md
- **Architecture**: ARCHITECTURE.md
- **Navigation**: INDEX.md
- **uv tool**: UV_GUIDE.md

## ✨ Fonctionnalités

- ✅ Recherche web parallèle
- ✅ Résumés AI
- ✅ Rapport Markdown
- ✅ Export PDF
- ✅ Historique DB
- ✅ CLI + Web UI
- ✅ Docker ready

## 🎉 Prêt?

```bash
# Windows
setup_windows.bat && echo "GO!"

# Linux/Mac
bash setup.sh && echo "GO!"
```

---

**5 minutes pour avoir un agent de recherche complet** 🚀

Aucune installation complexe. Aucun clonage. Juste du pur code.

**Bon research!** 🔬
