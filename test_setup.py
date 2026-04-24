#!/usr/bin/env python3
"""
Script de test - Vérifie l'installation et teste les composants
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    dependencies = {
        "streamlit": "Interface web",
        "openai": "API OpenAI",
        "requests": "Requêtes HTTP",
        "bs4": "Web scraping",
        "loguru": "Logging",
        "dotenv": "Variables d'environnement"
    }
    
    missing = []
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"  ✓ {module:<15} - {description}")
        except ImportError:
            print(f"  ✗ {module:<15} - {description} (MANQUANT)")
            missing.append(module)
    
    return len(missing) == 0


def check_env():
    """Vérifie la configuration .env"""
    print("\n🔑 Vérification de la configuration...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("  ✗ Fichier .env manquant")
        print("    → Créez un fichier .env en copiant .env.example")
        return False
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("  ✗ OPENAI_API_KEY non définie dans .env")
        return False
    
    print(f"  ✓ OPENAI_API_KEY configurée")
    print(f"  ✓ OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')}")
    
    return True


def check_directories():
    """Vérifie les répertoires"""
    print("\n📁 Vérification des répertoires...")
    
    dirs = ["outputs", "outputs/reports", "database", "logs", "agents", "tools"]
    
    for d in dirs:
        path = Path(d)
        if path.exists():
            print(f"  ✓ {d}/")
        else:
            print(f"  ⚠ Création de {d}/...")
            path.mkdir(parents=True, exist_ok=True)
    
    return True


def test_imports():
    """Teste l'import des modules"""
    print("\n🧪 Test d'import des modules...")
    
    modules = {
        "agents.planner": "Planner",
        "tools.web_search": "Web Search",
        "tools.web_scraper": "Web Scraper",
        "agents.researcher": "Researcher",
        "agents.summarizer": "Summarizer",
        "agents.writer": "Writer"
    }
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"  ✓ {name:<20} importé")
        except Exception as e:
            print(f"  ✗ {name:<20} erreur: {e}")
            return False
    
    return True


def test_quick():
    """Test rapide des fonctionnalités"""
    print("\n⚡ Test rapide...")
    
    try:
        from agents.planner import generate_research_questions
        
        print("  Génération de 3 questions de recherche...")
        questions = generate_research_questions("Test Topic", num_questions=3)
        
        if questions and len(questions) > 0:
            print(f"  ✓ {len(questions)} questions générées")
            for i, q in enumerate(questions[:2], 1):
                print(f"    {i}. {q[:50]}...")
            return True
        else:
            print("  ✗ Pas de questions générées")
            return False
    
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False


def main():
    """Lance les vérifications"""
    print("=" * 60)
    print("🔬 AI Research Agent - Test d'installation")
    print("=" * 60)
    
    results = {
        "Dependencies": check_dependencies(),
        "Environment": check_env(),
        "Directories": check_directories(),
        "Imports": test_imports(),
        "Quick Test": test_quick()
    }
    
    print("\n" + "=" * 60)
    print("📊 Résumé des vérifications:")
    print("=" * 60)
    
    for check, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ Tout est prêt!")
        print("\n📝 Prochaines étapes:")
        print("  1. CLI:       python main.py --topic 'Votre sujet'")
        print("  2. Interface: streamlit run app.py")
        print("=" * 60)
        return 0
    else:
        print("❌ Il y a des problèmes à résoudre")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
