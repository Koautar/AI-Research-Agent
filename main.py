"""
Main CLI - Interface en ligne de commande
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Configure les logs
logger.remove()
logger.add(sys.stderr, format="<level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>")
logger.add("logs/research.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}", rotation="500 MB")

# Charge les variables d'environnement
load_dotenv()

from agents.researcher import run_full_research
from agents.writer import write_full_report
from tools.pdf_exporter import export_report
from agents.summarizer import Summarizer


def create_output_dirs():
    """Crée les répertoires de sortie"""
    Path("outputs/reports").mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    logger.info("✓ Répertoires créés")


def run_research_pipeline(topic: str, num_questions: int = 5, num_sources: int = 10, 
                         report_mode: str = "balanced", export_pdf: bool = False):
    """
    Exécute le pipeline complet de recherche.
    
    Args:
        topic: Le sujet de recherche
        num_questions: Nombre de questions de recherche
        num_sources: Nombre de sources à résumer
        report_mode: Mode de rapport (student/business/technical/balanced)
        export_pdf: Exporter en PDF
    """
    logger.info(f"🚀 Lancement du pipeline de recherche")
    logger.info(f"   Sujet: {topic}")
    logger.info(f"   Questions: {num_questions}, Sources: {num_sources}, Mode: {report_mode}")
    
    try:
        # Phase 1: Recherche
        logger.info("\n📊 Phase 1: Recherche et synthèse...")
        research_data = run_full_research(topic, num_questions, num_sources)
        
        # Phase 2: Rédaction du rapport
        logger.info("\n📝 Phase 2: Rédaction du rapport...")
        report = write_full_report(topic, research_data, report_mode)
        
        # Phase 3: Sauvegarde
        logger.info("\n💾 Phase 3: Sauvegarde...")
        
        # Fichier Markdown
        filename = topic.replace(" ", "_")[:30]
        markdown_path = f"outputs/reports/{filename}.md"
        
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.success(f"✓ Rapport Markdown: {markdown_path}")
        
        # Fichier PDF (optionnel)
        if export_pdf:
            pdf_path = f"outputs/reports/{filename}.pdf"
            export_report(markdown_path, pdf_path, title=topic)
            logger.success(f"✓ Rapport PDF: {pdf_path}")
        
        logger.success(f"\n✅ Pipeline complété avec succès!")
        logger.info(f"📂 Rapports disponibles dans: outputs/reports/")
        
        return {
            "markdown": markdown_path,
            "pdf": pdf_path if export_pdf else None,
            "report": report,
            "research_data": research_data
        }
    
    except Exception as e:
        logger.error(f"❌ Erreur dans le pipeline: {e}")
        raise


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description="AI Research Agent - Génère des rapports de recherche automatiques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py --topic "Machine Learning"
  python main.py --topic "Blockchain" --questions 7 --sources 15 --pdf
  python main.py --topic "Quantum Computing" --mode technical
        """
    )
    
    parser.add_argument(
        "--topic", "-t",
        type=str,
        required=True,
        help="Sujet de recherche"
    )
    parser.add_argument(
        "--questions", "-q",
        type=int,
        default=5,
        help="Nombre de questions de recherche (défaut: 5)"
    )
    parser.add_argument(
        "--sources", "-s",
        type=int,
        default=10,
        help="Nombre de sources à résumer (défaut: 10)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["student", "business", "technical", "balanced"],
        default="balanced",
        help="Mode de rapport (défaut: balanced)"
    )
    parser.add_argument(
        "--pdf", "-p",
        action="store_true",
        help="Exporter également en PDF"
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Mode debug"
    )
    
    args = parser.parse_args()
    
    # Vérifications
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("❌ OPENAI_API_KEY non configurée dans .env")
        sys.exit(1)
    
    # Créer les répertoires
    create_output_dirs()
    
    # Lancer le pipeline
    try:
        result = run_research_pipeline(
            topic=args.topic,
            num_questions=args.questions,
            num_sources=args.sources,
            report_mode=args.mode,
            export_pdf=args.pdf
        )
        
        print(f"\n{'='*60}")
        print(f"Rapport disponible à: {result['markdown']}")
        if result['pdf']:
            print(f"PDF disponible à: {result['pdf']}")
        print(f"{'='*60}")
    
    except KeyboardInterrupt:
        logger.warning("\n⚠ Interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
