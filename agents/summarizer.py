"""
Summarizer Agent - Synthèse et agrégation des résumés
"""

import os
import json
from typing import Dict, List
from openai import OpenAI
from loguru import logger

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Summarizer:
    """Synthétise et agrège les résumés des sources"""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.summaries = {}
        self.synthesis = None
        
    def add_summary(self, url: str, summary: str, title: str = ""):
        """Ajoute un résumé"""
        self.summaries[url] = {
            "title": title,
            "summary": summary
        }
        logger.info(f"✓ Résumé ajouté: {title}")
    
    def add_summaries_dict(self, summaries_dict: Dict):
        """Ajoute plusieurs résumés depuis un dictionnaire"""
        for url, data in summaries_dict.items():
            self.add_summary(url, data['summary'], data.get('title', ''))
    
    def synthesize(self) -> str:
        """Synthétise tous les résumés en un document cohérent"""
        if not self.summaries:
            logger.warning("⚠ Aucun résumé à synthétiser")
            return ""
        
        logger.info(f"Synthèse de {len(self.summaries)} résumés")
        
        # Prépare le contenu pour la synthèse
        summaries_text = "\n\n".join([
            f"**{data['title']}**\n{data['summary']}"
            for data in self.summaries.values()
        ])
        
        try:
            prompt = f"""Tu es un expert en synthèse de contenu. Synthétise les résumés suivants sur "{self.topic}" 
            en un document cohérent et structuré.

Résumés:
{summaries_text}

Produis une synthèse qui:
1. Regroupe les thèmes communs
2. Identifie les points clés
3. Souligne les désaccords ou différences
4. Propose une conclusion d'ensemble
5. Reste objectif et basé sur les sources
"""
            
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                messages=[
                    {"role": "system", "content": "Tu es un expert en synthèse et analyse."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2000
            )
            
            self.synthesis = response.choices[0].message.content
            logger.success(f"✓ Synthèse générée ({len(self.synthesis)} caractères)")
            return self.synthesis
        
        except Exception as e:
            logger.error(f"Erreur lors de la synthèse: {e}")
            return ""
    
    def generate_key_insights(self) -> List[str]:
        """Extrait les insights clés"""
        if not self.summaries:
            return []
        
        logger.info("Extraction des insights clés")
        
        summaries_text = "\n\n".join([
            data['summary'] for data in self.summaries.values()
        ])
        
        try:
            prompt = f"""À partir de ces résumés sur "{self.topic}", 
            identifie les 5-7 insights clés les plus importants.

Résumés:
{summaries_text}

Retourne JSON:
{{
    "insights": [
        "Insight 1",
        "Insight 2",
        ...
    ]
}}
"""
            
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
                messages=[
                    {"role": "system", "content": "Tu identifies les insights clés."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            insights = result.get('insights', [])
            
            logger.success(f"✓ {len(insights)} insights identifiés")
            return insights
        
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction: {e}")
            return []
    
    def get_summary_report(self) -> Dict:
        """Génère un rapport de synthèse complet"""
        logger.info("Génération du rapport de synthèse")
        
        synthesis = self.synthesize()
        insights = self.generate_key_insights()
        
        report = {
            "topic": self.topic,
            "num_sources": len(self.summaries),
            "synthesis": synthesis,
            "key_insights": insights,
            "sources": [
                {
                    "title": data['title'],
                    "summary": data['summary']
                }
                for data in self.summaries.values()
            ]
        }
        
        return report


if __name__ == "__main__":
    # Test
    summarizer = Summarizer("Quantum Computing")
    
    # Ajoute quelques résumés de test
    summarizer.add_summary(
        "https://example1.com",
        "Quantum computing utilise les principes de la mécanique quantique...",
        "Introduction to Quantum Computing"
    )
    
    # Génère la synthèse
    synthesis = summarizer.synthesize()
    print(f"\n✅ Synthèse générée:")
    print(synthesis)
