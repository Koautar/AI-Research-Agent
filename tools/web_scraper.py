"""
Web Scraper - Extraction et résumé du contenu web
"""

import os
import requests
from typing import Optional
from bs4 import BeautifulSoup
from openai import OpenAI
from loguru import logger

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def fetch_webpage(url: str, timeout: int = 10) -> Optional[str]:
    """
    Récupère le contenu textuel d'une page web.
    
    Args:
        url: L'URL à scraper
        timeout: Timeout en secondes
    
    Returns:
        Texte du contenu ou None si erreur
    """
    logger.info(f"Fetch: {url}")
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Parse le HTML
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Supprime les scripts et styles
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Extrait le texte
        text = soup.get_text(separator="\n", strip=True)
        text = "\n".join(line.strip() for line in text.split("\n") if line.strip())
        
        logger.success(f"✓ {len(text)} caractères extraits")
        return text[:5000]  # Limiter à 5000 caractères
    
    except requests.RequestException as e:
        logger.warning(f"⚠ Erreur lors du fetch: {e}")
        return None
    except Exception as e:
        logger.error(f"Erreur lors du parsing: {e}")
        return None


def summarize_source(url: str, title: str = "") -> Optional[str]:
    """
    Scrape une URL et génère un résumé avec OpenAI.
    
    Args:
        url: L'URL à résumer
        title: Titre optionnel de la source
    
    Returns:
        Résumé du contenu ou None
    """
    logger.info(f"Résumé de source: {url}")
    
    # Récupère le contenu
    content = fetch_webpage(url)
    if not content:
        logger.warning(f"⚠ Impossible de récupérer le contenu de {url}")
        return None
    
    # Génère le résumé
    try:
        prompt = f"""Résume ce contenu web de manière structurée et pertinente.

Titre: {title if title else "Sans titre"}
URL: {url}

Contenu:
{content}

Fournir un résumé:
1. En 3-4 phrases clés
2. Les points importants
3. Conclusions/insights
"""
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse et résumé de contenu."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        logger.success(f"✓ Résumé généré ({len(summary)} caractères)")
        return summary
    
    except Exception as e:
        logger.error(f"Erreur lors de la génération du résumé: {e}")
        return None


def extract_key_points(text: str, num_points: int = 5) -> list:
    """
    Extrait les points clés d'un texte avec OpenAI.
    
    Args:
        text: Le texte à analyser
        num_points: Nombre de points à extraire
    
    Returns:
        Liste des points clés
    """
    logger.info(f"Extraction de {num_points} points clés")
    
    try:
        prompt = f"""Extrait les {num_points} points clés de ce texte:

{text}

Retourne UNIQUEMENT une liste JSON des points:
[
    "Point 1",
    "Point 2",
    ...
]
"""
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            messages=[
                {"role": "system", "content": "Tu extrais les points clés des textes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        
        import json
        content = response.choices[0].message.content
        points = json.loads(content)
        logger.success(f"✓ {len(points)} points extraits")
        return points
    
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction: {e}")
        return []


if __name__ == "__main__":
    # Test avec une URL simple
    url = "https://en.wikipedia.org/wiki/Machine_learning"
    summary = summarize_source(url, "Wikipedia - Machine Learning")
    
    if summary:
        print(f"\n✅ Résumé de {url}:")
        print(summary)
