"""
Example - Exemples d'utilisation du AI Research Agent
"""

from agents.researcher import ResearchManager
from agents.writer import ReportWriter
from tools.pdf_exporter import markdown_to_pdf
import os
from dotenv import load_dotenv

# Charger .env
load_dotenv()


def example_1_simple_research():
    """Exemple 1 - Recherche simple"""
    print("=" * 60)
    print("Exemple 1: Recherche simple")
    print("=" * 60)
    
    topic = "Machine Learning en 2024"
    
    # Crée un gestionnaire de recherche
    manager = ResearchManager(topic, num_questions=3)
    
    # Étape 1: Plan
    plan = manager.generate_plan()
    print(f"\n📋 Plan généré:")
    for i, q in enumerate(plan['questions'], 1):
        print(f"  {i}. {q}")
    
    # Étape 2: Recherche
    print(f"\n🔍 Recherche en cours...")
    results = manager.execute_searches(num_results=5)
    print(f"✓ {len(results['all'])} sources trouvées")
    
    # Étape 3: Résumés
    print(f"\n📚 Résumé des sources...")
    summaries = manager.summarize_sources(limit=5)
    print(f"✓ {len(summaries)} sources résumées")
    
    # Retourne les données
    return manager.get_research_data()


def example_2_full_pipeline():
    """Exemple 2 - Pipeline complet avec rapport"""
    print("\n" + "=" * 60)
    print("Exemple 2: Pipeline complet")
    print("=" * 60)
    
    topic = "Intelligence Artificielle générative"
    
    # Recherche
    manager = ResearchManager(topic, num_questions=5)
    manager.generate_plan()
    manager.execute_searches(num_results=5)
    manager.summarize_sources(limit=10)
    research_data = manager.get_research_data()
    
    # Rapport
    writer = ReportWriter(topic, report_mode="balanced")
    writer.load_data(research_data)
    report = writer.generate_report()
    writer.add_references()
    
    print(f"\n📄 Rapport généré ({len(report)} caractères)")
    print("\nPremiers 500 caractères:")
    print(report[:500])
    
    # Sauvegarde
    filename = f"outputs/reports/{topic.replace(' ', '_')}.md"
    writer.save_markdown(filename)
    print(f"\n✓ Rapport sauvegardé: {filename}")
    
    return report, research_data


def example_3_custom_summaries():
    """Exemple 3 - Résumés personnalisés"""
    print("\n" + "=" * 60)
    print("Exemple 3: Synthèse personnalisée")
    print("=" * 60)
    
    from agents.summarizer import Summarizer
    
    topic = "Quantum Computing"
    summarizer = Summarizer(topic)
    
    # Ajoute des résumés personnalisés
    summarizer.add_summary(
        "https://example1.com",
        "Quantum computing utilise les qubits et la superposition...",
        "Introduction to Quantum Computing"
    )
    summarizer.add_summary(
        "https://example2.com",
        "Les applications pratiques incluent la cryptographie...",
        "Quantum Computing Applications"
    )
    
    # Génère la synthèse
    synthesis = summarizer.synthesize()
    print(f"\n📝 Synthèse ({len(synthesis)} caractères):")
    print(synthesis[:300])
    
    # Insights
    insights = summarizer.generate_key_insights()
    print(f"\n💡 Insights clés:")
    for insight in insights:
        print(f"  • {insight}")


def example_4_export_pdf():
    """Exemple 4 - Export en PDF"""
    print("\n" + "=" * 60)
    print("Exemple 4: Export PDF")
    print("=" * 60)
    
    markdown_content = """# Sample Report

## Introduction

This is a sample research report on Machine Learning.

### Key Points

1. Machine Learning is revolutionizing AI
2. Deep Learning has shown great promise
3. Transformers are state-of-the-art

## Conclusion

The future of ML is bright.

## References

[1] Example Source 1
[2] Example Source 2
"""
    
    pdf_path = "outputs/reports/sample_report.pdf"
    result = markdown_to_pdf(markdown_content, pdf_path, title="Sample Report")
    
    if result:
        print(f"✓ PDF généré: {result}")
    else:
        print("✗ Erreur lors de la génération du PDF")


def example_5_cli_style():
    """Exemple 5 - Utilisation CLI"""
    print("\n" + "=" * 60)
    print("Exemple 5: Utilisation CLI")
    print("=" * 60)
    
    print("""
# Utilisation CLI:

# Recherche simple
python main.py --topic "Machine Learning"

# Recherche avancée
python main.py --topic "Blockchain" \\
  --questions 7 \\
  --sources 15 \\
  --mode technical \\
  --pdf

# Options:
  --topic TEXT         Sujet de recherche
  --questions INT      Nombre de questions (défaut: 5)
  --sources INT        Nombre de sources (défaut: 10)
  --mode TEXT          Mode: student/business/technical/balanced
  --pdf                Exporter en PDF
  --debug              Mode debug
""")


def example_6_streamlit_app():
    """Exemple 6 - Utilisation Streamlit"""
    print("\n" + "=" * 60)
    print("Exemple 6: Interface Streamlit")
    print("=" * 60)
    
    print("""
# Lancer l'interface web:

streamlit run app.py

# Ensuite:
1. Entrez un sujet
2. Configurez les paramètres
3. Cliquez sur "Démarrer la recherche"
4. Consultez le rapport
5. Exportez en Markdown/PDF

# URL par défaut: http://localhost:8501
""")


def main():
    """Exécute les exemples"""
    
    # Vérif API
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY non configurée")
        print("   Créez un fichier .env avec votre clé")
        return
    
    print("""
🔬 AI Research Agent - Exemples d'utilisation
===============================================

Cet script montre comment utiliser le AI Research Agent
dans différents contextes.

IMPORTANT: Les exemples 1-4 vont appeler OpenAI API.
Assurez-vous d'avoir configuré OPENAI_API_KEY dans .env

Menu:
1. Recherche simple
2. Pipeline complet
3. Synthèse personnalisée
4. Export PDF
5. Utilisation CLI
6. Interface Streamlit
0. Quitter
    """)
    
    choice = input("\nChoisissez (0-6): ").strip()
    
    try:
        if choice == "1":
            data = example_1_simple_research()
        elif choice == "2":
            report, data = example_2_full_pipeline()
        elif choice == "3":
            example_3_custom_summaries()
        elif choice == "4":
            example_4_export_pdf()
        elif choice == "5":
            example_5_cli_style()
        elif choice == "6":
            example_6_streamlit_app()
        elif choice == "0":
            print("Au revoir! 👋")
        else:
            print("Option invalide")
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrompu")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    main()
