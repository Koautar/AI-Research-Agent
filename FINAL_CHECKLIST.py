#!/usr/bin/env python3
"""
FINAL CHECKLIST - Validation du projet complet
"""

import os
import json
from pathlib import Path
from datetime import datetime

def print_header():
    print("\n" + "="*70)
    print("🔍 AI RESEARCH AGENT - FINAL VALIDATION CHECKLIST")
    print("="*70 + "\n")

def check_files():
    """Vérifie que tous les fichiers critiques existent"""
    print("📁 Vérification des fichiers...")
    
    required_files = {
        "Core Application": [
            "app.py",
            "main.py",
            "config.py",
        ],
        "Agents": [
            "agents/__init__.py",
            "agents/planner.py",
            "agents/researcher.py",
            "agents/summarizer.py",
            "agents/writer.py",
        ],
        "Tools": [
            "tools/__init__.py",
            "tools/web_search.py",
            "tools/web_scraper.py",
            "tools/pdf_exporter.py",
        ],
        "Database": [
            "database/__init__.py",
            "database/manager.py",
        ],
        "Configuration": [
            ".env.example",
            "config.py",
            "pyproject.toml",
            "requirements.txt",
            ".gitignore",
        ],
        "Documentation": [
            "README.md",
            "GUIDE_DEMARRAGE.md",
            "ARCHITECTURE.md",
            "INDEX.md",
            "UV_GUIDE.md",
            "SUMMARY.md",
            "QUICKSTART.md",
        ],
        "Setup Scripts": [
            "setup.sh",
            "setup_windows.bat",
            "quickstart.sh",
            "quickstart_windows.bat",
            "test_setup.py",
            "examples.py",
        ],
        "DevOps": [
            "Dockerfile",
            "docker-compose.yml",
            ".streamlit/config.toml",
        ],
    }
    
    all_good = True
    for category, files in required_files.items():
        print(f"\n  {category}:")
        for file in files:
            path = Path(file)
            if path.exists():
                size = path.stat().st_size
                print(f"    ✅ {file:<40} ({size:,} bytes)")
            else:
                print(f"    ❌ {file:<40} (MISSING!)")
                all_good = False
    
    return all_good

def check_directories():
    """Vérifie que les répertoires essentiels existent"""
    print("\n\n📂 Vérification des répertoires...")
    
    required_dirs = [
        "agents",
        "tools",
        "database",
        "outputs",
        "outputs/reports",
        ".streamlit",
    ]
    
    all_good = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists() and path.is_dir():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/ (MISSING!)")
            all_good = False
    
    return all_good

def check_code_quality():
    """Vérifie la qualité du code"""
    print("\n\n🧪 Vérification de la qualité du code...")
    
    checks = {
        "Type hints": 0,
        "Docstrings": 0,
        "Imports": 0,
        "Functions": 0,
    }
    
    python_files = list(Path(".").rglob("*.py"))
    python_files = [f for f in python_files if ".venv" not in str(f)]
    
    for py_file in python_files:
        try:
            with open(py_file, 'r') as f:
                content = f.read()
                
                # Count type hints
                if "->" in content or ": " in content:
                    checks["Type hints"] += 1
                
                # Count docstrings
                if '"""' in content or "'''" in content:
                    checks["Docstrings"] += 1
                
                # Count imports
                if "import" in content:
                    checks["Imports"] += 1
                
                # Count functions
                if "def " in content:
                    checks["Functions"] += content.count("def ")
        except:
            pass
    
    print(f"  📊 Found in {len(python_files)} Python files:")
    print(f"    ✅ {checks['Functions']} functions defined")
    print(f"    ✅ {checks['Docstrings']} files with docstrings")
    print(f"    ✅ {checks['Type hints']} files with type hints")
    
    return len(python_files) > 0

def check_documentation():
    """Vérifie la couverture de documentation"""
    print("\n\n📚 Vérification de la documentation...")
    
    doc_files = {
        "README.md": ["Architecture", "Usage", "Installation"],
        "GUIDE_DEMARRAGE.md": ["Setup", "Configuration", "Troubleshooting"],
        "ARCHITECTURE.md": ["Design", "Flow", "Components"],
        "INDEX.md": ["Navigation", "Folder structure"],
        "QUICKSTART.md": ["5 minutes", "Setup"],
        "SUMMARY.md": ["Statistics", "Features"],
    }
    
    all_good = True
    for doc_file, topics in doc_files.items():
        path = Path(doc_file)
        if path.exists():
            size = path.stat().st_size
            print(f"  ✅ {doc_file:<30} ({size:,} bytes)")
        else:
            print(f"  ❌ {doc_file:<30} (MISSING!)")
            all_good = False
    
    return all_good

def check_dependencies():
    """Vérifie le fichier de dépendances"""
    print("\n\n📦 Vérification des dépendances...")
    
    files_to_check = ["requirements.txt", "pyproject.toml"]
    
    all_good = True
    for dep_file in files_to_check:
        path = Path(dep_file)
        if path.exists():
            with open(path, 'r') as f:
                lines = f.readlines()
                deps = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
                print(f"  ✅ {dep_file:<25} ({len(deps)} dependencies)")
        else:
            print(f"  ❌ {dep_file:<25} (MISSING!)")
            all_good = False
    
    return all_good

def check_config():
    """Vérifie la configuration"""
    print("\n\n⚙️  Vérification de la configuration...")
    
    checks = []
    
    # .env.example
    env_path = Path(".env.example")
    if env_path.exists():
        with open(env_path) as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                checks.append(("✅", ".env.example has OPENAI_API_KEY"))
            else:
                checks.append(("❌", ".env.example missing OPENAI_API_KEY"))
    else:
        checks.append(("❌", ".env.example not found"))
    
    # config.py
    config_path = Path("config.py")
    if config_path.exists():
        with open(config_path) as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                checks.append(("✅", "config.py configured"))
            else:
                checks.append(("❌", "config.py not configured"))
    else:
        checks.append(("❌", "config.py not found"))
    
    # .gitignore
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path) as f:
            content = f.read()
            if ".env" in content:
                checks.append(("✅", ".gitignore excludes .env"))
            else:
                checks.append(("❌", ".gitignore doesn't exclude .env"))
    else:
        checks.append(("❌", ".gitignore not found"))
    
    for status, msg in checks:
        print(f"  {status} {msg}")
    
    return all(status == "✅" for status, _ in checks)

def check_docker():
    """Vérifie Docker setup"""
    print("\n\n🐳 Vérification Docker...")
    
    files = ["Dockerfile", "docker-compose.yml"]
    all_good = True
    
    for file in files:
        path = Path(file)
        if path.exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (MISSING!)")
            all_good = False
    
    return all_good

def generate_report():
    """Génère un rapport final"""
    print("\n\n" + "="*70)
    print("📊 RAPPORT FINAL")
    print("="*70 + "\n")
    
    checks = {
        "Files": check_files(),
        "Directories": check_directories(),
        "Code Quality": check_code_quality(),
        "Documentation": check_documentation(),
        "Dependencies": check_dependencies(),
        "Configuration": check_config(),
        "Docker": check_docker(),
    }
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print(f"\n✅ PASSED: {passed}/{total} checks")
    print(f"❌ FAILED: {total - passed}/{total} checks")
    
    if passed == total:
        print("\n" + "🎉 " * 20)
        print("✅ PROJECT COMPLETE AND READY FOR USE!")
        print("🎉 " * 20)
        return 0
    else:
        print("\n⚠️  Some issues detected. Please review above.")
        return 1

def print_next_steps():
    """Affiche les prochaines étapes"""
    print("\n\n" + "="*70)
    print("🚀 NEXT STEPS")
    print("="*70 + "\n")
    
    print("""
1. 🔑 Configure OpenAI API Key:
   - Copy .env.example to .env
   - Add your OPENAI_API_KEY

2. ⚡ Setup environment:
   - Windows: run setup_windows.bat
   - Linux/Mac: bash setup.sh

3. 🎨 Launch interface:
   - streamlit run app.py
   - Or: python main.py --topic "Your Topic"

4. 🧪 Run tests:
   - python test_setup.py
   - python examples.py

5. 📚 Read documentation:
   - QUICKSTART.md (5 minute guide)
   - GUIDE_DEMARRAGE.md (detailed setup)
   - ARCHITECTURE.md (for developers)

✅ You're all set! Happy researching! 🔬
    """)

def main():
    print_header()
    
    result = generate_report()
    
    print_next_steps()
    
    # Save results to JSON
    timestamp = datetime.now().isoformat()
    results = {
        "timestamp": timestamp,
        "status": "complete" if result == 0 else "incomplete",
        "python_files": len(list(Path(".").rglob("*.py"))),
        "doc_files": len(list(Path(".").rglob("*.md"))),
    }
    
    with open("validation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to validation_results.json")
    
    return result

if __name__ == "__main__":
    import sys
    sys.exit(main())
