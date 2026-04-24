"""
Researcher Agent - Orchestration de la recherche complète
"""

import json
from typing import Dict, List
from loguru import logger

from agents.planner import generate_research_plan
from tools.web_search import search_web_parallel, deduplicate_results
from tools.web_scraper import summarize_source


class ResearchManager:
    """Orchestrateur principal de la recherche"""
    
    def __init__(self, topic: str, num_questions: int = 5):
        self.topic = topic
        self.num_questions = num_questions
        self.plan = None
        self.search_results = {}
        self.summaries = {}
        
    def generate_plan(self) -> Dict:
        """Génère le plan de recherche"""
        logger.info(f"Génération du plan pour: {self.topic}")
        self.plan = generate_research_plan(self.topic, self.num_questions)
        return self.plan
    
    def execute_searches(self, num_results: int = 5) -> Dict[str, List[Dict]]:
        """Exécute les recherches pour toutes les questions"""
        if not self.plan:
            self.generate_plan()
        
        logger.info(f"Exécution de {len(self.plan['questions'])} recherches")
        queries = self.plan['questions']
        
        # Recherche parallèle (simulée)
        all_results = search_web_parallel(queries, num_results)
        
        # Déduplique tous les résultats
        all_urls_results = []
        for query, results in all_results.items():
            all_urls_results.extend(results)
        
        unique_results = deduplicate_results(all_urls_results)
        
        self.search_results = {
            "by_query": all_results,
            "all": unique_results
        }
        
        logger.success(f"✓ {len(unique_results)} sources uniques trouvées")
        return self.search_results
    
    def summarize_sources(self, limit: int = 10) -> Dict:
        """Résume les sources trouvées"""
        logger.info(f"Résumé des sources (limite: {limit})")
        
        if not self.search_results:
            self.execute_searches()
        
        sources = self.search_results.get("all", [])[:limit]
        
        for i, source in enumerate(sources, 1):
            logger.info(f"Résumé {i}/{len(sources)}: {source['title']}")
            
            summary = summarize_source(
                source['url'],
                source['title']
            )
            
            if summary:
                self.summaries[source['url']] = {
                    "title": source['title'],
                    "url": source['url'],
                    "summary": summary,
                    "snippet": source.get('snippet', '')
                }
        
        logger.success(f"✓ {len(self.summaries)} sources résumées")
        return self.summaries
    
    def get_research_data(self) -> Dict:
        """Retourne toutes les données de recherche"""
        return {
            "topic": self.topic,
            "plan": self.plan,
            "search_results": self.search_results,
            "summaries": self.summaries
        }
    
    def export_json(self, filepath: str):
        """Exporte les résultats en JSON"""
        data = self.get_research_data()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.success(f"✓ Données exportées vers {filepath}")


def run_full_research(topic: str, num_questions: int = 5, limit_sources: int = 10) -> Dict:
    """
    Exécute une recherche complète.
    
    Args:
        topic: Le sujet de recherche
        num_questions: Nombre de questions à générer
        limit_sources: Nombre de sources à résumer
    
    Returns:
        Toutes les données de recherche
    """
    logger.info(f"🔍 Lancement recherche complète: {topic}")
    
    manager = ResearchManager(topic, num_questions)
    manager.generate_plan()
    manager.execute_searches(num_results=5)
    manager.summarize_sources(limit=limit_sources)
    
    return manager.get_research_data()


if __name__ == "__main__":
    # Test
    topic = "Blockchain et Crypto-monnaies"
    data = run_full_research(topic, num_questions=3, limit_sources=5)
    
    print("\n✅ Recherche complète exécutée!")
    print(f"Plan: {len(data['plan']['questions'])} questions")
    print(f"Résultats: {len(data['search_results']['all'])} sources")
    print(f"Résumés: {len(data['summaries'])} résumés")
