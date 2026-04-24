# Qu'est-ce que uv?

**uv** est un gestionnaire d'environnement et de dépendances Python ultra-rapide, écrit en Rust.

## Pourquoi uv au lieu de pip/venv?

| Aspect | pip/venv | uv |
|--------|----------|-----|
| Vitesse | Lent | **100x plus rapide** ⚡ |
| Mémoire | Élevée | **Très faible** 💾 |
| Installation | Complexe | **Simple** ✨ |
| Lock file | Non | **Oui** 🔒 |
| Cache | Basique | **Intelligent** 🧠 |

## Installation de uv

### Windows

**Option 1: Avec pip**
```powershell
pip install uv
```

**Option 2: Exécutable (Recommended)
```powershell
# Ouvrir PowerShell en Admin et lancer:
irm https://astral.sh/uv/install.ps1 | iex
```

**Option 3: Avec Scoop**
```powershell
scoop install uv
```

### Linux/Mac

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Utilisation basique

### Créer un environnement
```bash
uv venv
```
Cela crée `.venv/` automatiquement.

### Activer l'environnement
```powershell
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Installer des packages
```bash
# Installer depuis requirements.txt
uv pip install -r requirements.txt

# Installer un package
uv pip install requests

# Installer plusieurs
uv pip install requests numpy pandas
```

### Vérifier les packages
```bash
uv pip list
```

### Supprimer l'environnement
```bash
# Windows
rmdir /s .venv

# Linux/Mac
rm -rf .venv
```

## Commandes uv importantes

```bash
# Créer env
uv venv

# Installer deps
uv pip install package_name

# Activer env
.venv\Scripts\activate

# Désactiver
deactivate

# Afficher version
uv --version

# Aide
uv --help
```

## Fichier pyproject.toml (pour ce projet)

```toml
[project]
name = "ai-research-agent"
version = "0.1.0"
dependencies = [
    "streamlit>=1.28.0",
    "openai>=1.3.0",
    # ... autres packages
]
```

Avec uv, les deps du `pyproject.toml` sont installées directement:
```bash
uv pip install .
```

## Avantages uv pour ce projet

1. **Rapide** - Setup en secondes au lieu de minutes
2. **Fiable** - Résolutions correctes des dépendances
3. **Léger** - Peu de ressources utilisées
4. **Moderne** - Compatible avec les standards Python
5. **Production-ready** - Utilisé par les pros

## uv vs pip - Exemple

### Avec pip (lent)
```bash
python -m pip install -r requirements.txt
# ⏳ 2-5 minutes...
```

### Avec uv (rapide)
```bash
uv pip install -r requirements.txt
# ⚡ 10-30 secondes!
```

## Troubleshooting

### "Command uv not found"
```bash
# Réinstaller
pip install -U uv

# Ou utiliser le chemin complet
C:\Users\YourName\.local\bin\uv venv
```

### Permission denied
```bash
# Sur Linux/Mac, utiliser sudo
sudo uv pip install package
```

### "Poetry-like project detected"
Si vous avez un `pyproject.toml`:
```bash
uv sync  # Synchronise tout
```

## Ressources

- **Site officiel**: https://astral.sh/uv/
- **GitHub**: https://github.com/astral-sh/uv
- **Docs complètes**: https://docs.astral.sh/uv/

## ✨ Conclusion

uv est **plus rapide, plus simple, et plus fiable** que pip/venv.

Pour ce projet **AI Research Agent**, uv vous permet de:
- ✅ Setup 10x plus rapide
- ✅ Moins de bugs de dépendances
- ✅ Meilleure performance globale

**Recommandation**: Utilisez uv! 🚀
