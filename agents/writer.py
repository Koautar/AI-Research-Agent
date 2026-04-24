"""
Writer Agent - Rédaction du rapport final
"""

import os
from typing import Dict, List
from openai import OpenAI
from loguru import logger

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ReportWriter:
    """Rédige le rapport final avec citations"""
    
    def __init__(self, topic: str, report_mode: str = "balanced"):
        """
        Initialise le rédacteur.
        
        Args:
            topic: Le sujet du rapport
            report_mode: Type de rapport ('student', 'business', 'technical', 'balanced')
        """
        self.topic = topic
        self.report_mode = report_mode
        self.data = {}
        self.report = None
        
    def load_data(self, data: Dict):
        """Charge les données de recherche"""
        self.data = data
        logger.info(f"✓ Données chargées: {len(data.get('summaries', {}))} sources")
    
    def _get_mode_prompt(self) -> str:
        """Retourne les instructions pour le mode de rapport"""
        modes = {
            "student": """Style académique, équilibré, avec citations appropriées. 
                         Inclut introduction, développement structuré, conclusion.""",
            "business": """Style professionnel, focus sur l'impact business et ROI. 
                          Inclut résumé exécutif, recommandations, chiffres clés.""",
            "technical": """Style technique, détails approfondis, terminologie spécialisée. 
                           Inclut mécanismes, architectures, implémentations.""",
            "balanced": """Style neutre et informatif, équilibre entre accessibilité et profondeur."""
        }
        return modes.get(self.report_mode, modes["balanced"])
    
    def generate_report(self) -> str:
        """Génère le rapport final en Markdown"""
        if not self.data:
            logger.warning("⚠ Aucune donnée chargée")
            return ""
        
        logger.info(f"Génération du rapport (mode: {self.report_mode})")
        
        summaries = self.data.get('summaries', {})
        plan = self.data.get('plan', {})
        
        # Prépare les sources
        sources_text = "\n\n".join([
            f"**{data['title']}** (Source: {url})\n{data['summary']}"
            for url, data in summaries.items()
        ])
        
        mode_instructions = self._get_mode_prompt()
        
        try:
            prompt = f"""Tu es un expert en rédaction de rapports de recherche.

Sujet: {self.topic}
Mode: {mode_instructions}

Sources de recherche:
{sources_text}

Rédige un rapport Markdown complet qui:
1. Commence par un titre H1
2. Inclut une introduction engageante
3. Développe le sujet avec sections H2 thématiques
4. Utilise les sources fournies avec citations [1], [2], etc.
5. Inclut une conclusion et perspectives
6. Termine avec une section "Références" listant les sources

Format Markdown strict avec:
- En-têtes clairs (# H1, ## H2, ### H3)
- Listes à puces et numérotées
- **gras** pour les concepts clés
- `code` pour les termes techniques
- Citations numérotées [1], [2], etc.

Rapport:
"""
            
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                messages=[
                    {"role": "system", "content": "Tu es un expert en rédaction de rapports académiques et professionnels."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            self.report = response.choices[0].message.content
            logger.success(f"✓ Rapport généré ({len(self.report)} caractères)")
            return self.report
        
        except Exception as e:
            logger.error(f"Erreur lors de la génération du rapport: {e}")
            return ""
    
    def add_references(self) -> str:
        """Ajoute une section références au rapport"""
        if not self.report:
            logger.warning("⚠ Aucun rapport à modifier")
            return self.report
        
        logger.info("Ajout des références")
        
        summaries = self.data.get('summaries', {})
        
        # Génère les références
        references_md = "\n## Références\n\n"
        for i, (url, data) in enumerate(summaries.items(), 1):
            references_md += f"[{i}] {data['title']}\n{url}\n\n"
        
        # Ajoute les références au rapport
        self.report = self.report.rstrip() + "\n\n" + references_md
        logger.success(f"✓ {len(summaries)} références ajoutées")
        return self.report
    
    def save_markdown(self, filepath: str):
        """Sauvegarde le rapport en Markdown"""
        if not self.report:
            logger.warning("⚠ Aucun rapport à sauvegarder")
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.report)
        
        logger.success(f"✓ Rapport sauvegardé: {filepath}")
    
    def get_report(self) -> str:
        """Retourne le rapport généré"""
        return self.report or ""


def write_full_report(topic: str, research_data: Dict, mode: str = "balanced") -> str:
    """
    Génère un rapport complet.
    
    Args:
        topic: Le sujet
        research_data: Les données de recherche
        mode: Le mode de rapport
    
    Returns:
        Le rapport Markdown
    """
    logger.info(f"📝 Rédaction du rapport final: {topic}")
    
    writer = ReportWriter(topic, mode)
    writer.load_data(research_data)
    report = writer.generate_report()
    writer.add_references()
    
    return writer.get_report()


if __name__ == "__main__":
    # Test
    topic = "Artificial Intelligence"
    test_data = {
        "summaries": {
            "https://example1.com": {
                "title": "What is AI?",
                "summary": "AI is intelligence exhibited by machines..."
            },
            "https://example2.com": {
                "title": "Future of AI",
                "summary": "AI will transform industries..."
            }
        }
    }
    
    report = write_full_report(topic, test_data, mode="balanced")
    print(f"\n✅ Rapport généré:\n{report[:500]}...")
