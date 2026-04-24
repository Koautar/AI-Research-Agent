"""
Web Search Tool - Recherche web et récupération de résultats
"""

import os
from typing import List, Dict
from duckduckgo_search import DDGS
from loguru import logger


def search_web(query: str, num_results: int = 5, timeout: int = 10) -> List[Dict]:
    """
    Recherche le web avec DuckDuckGo.
    
    Args:
        query: La requête de recherche
        num_results: Nombre de résultats (défaut: 5)
        timeout: Timeout en secondes
    
    Returns:
        Liste de dictionnaires avec titre, URL, snippet
    """
    logger.info(f"Recherche web: {query}")
    
    try:
        ddgs = DDGS()
        results = []
        
        # Recherche web standard
        for result in ddgs.text(query, max_results=num_results, timelimit="y"):
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", ""),
                "source": "DuckDuckGo"
            })
        
        logger.success(f"✓ {len(results)} résultats trouvés")
        return results
    
    except Exception as e:
        logger.error(f"Erreur lors de la recherche: {e}")
        return []


def search_web_parallel(queries: List[str], num_results: int = 5) -> Dict[str, List[Dict]]:
    """
    Effectue plusieurs recherches web en parallèle.
    
    Args:
        queries: Liste des requêtes
        num_results: Résultats par requête
    
    Returns:
        Dict avec requête -> résultats
    """
    logger.info(f"Recherche parallèle: {len(queries)} requêtes")
    
    results = {}
    for query in queries:
        results[query] = search_web(query, num_results)
    
    return results


def deduplicate_results(results: List[Dict]) -> List[Dict]:
    """
    Déduplique les résultats de recherche.
    
    Args:
        results: Liste des résultats
    
    Returns:
        Résultats dédupliqués (basé sur l'URL)
    """
    seen_urls = set()
    unique_results = []
    
    for result in results:
        url = result.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    logger.info(f"Résultats dédupliqués: {len(results)} → {len(unique_results)}")
    return unique_results


if __name__ == "__main__":
    # Test
    query = "Machine Learning applications"
    results = search_web(query, num_results=5)
    
    print(f"\n✅ Résultats pour '{query}':")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   {result['snippet'][:100]}...")
