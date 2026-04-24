"""
Planner Agent - Génère des questions de recherche pertinentes
"""

import os
import json
from typing import List
from openai import OpenAI
from loguru import logger

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_research_questions(topic: str, num_questions: int = 5) -> List[str]:
    """
    Génère des questions de recherche pertinentes pour un sujet.
    
    Args:
        topic: Le sujet de recherche
        num_questions: Nombre de questions à générer (défaut: 5)
    
    Returns:
        Liste des questions de recherche générées
    """
    logger.info(f"Génération de questions pour: {topic}")
    
    prompt = f"""Tu es un expert en recherche. Pour le sujet suivant, génère {num_questions} questions de recherche 
    détaillées, pertinentes et progressives (du général au spécifique).
    
    Sujet: {topic}
    
    Retourne UNIQUEMENT un JSON valide avec cette structure:
    {{
        "questions": [
            "Question 1?",
            "Question 2?",
            ...
        ]
    }}
    
    Les questions doivent:
    - Couvrir différents aspects du sujet
    - Être progressives et complémentaires
    - Être optimisées pour la recherche web
    """
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview"),
            messages=[
                {"role": "system", "content": "Tu es un expert en recherche et analyse."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse la réponse JSON
        content = response.choices[0].message.content
        result = json.loads(content)
        questions = result.get("questions", [])
        
        logger.success(f"✓ {len(questions)} questions générées")
        return questions
    
    except Exception as e:
        logger.error(f"Erreur lors de la génération des questions: {e}")
        # Retourner des questions par défaut
        return [
            f"Qu'est-ce que {topic}?",
            f"Comment {topic} fonctionne?",
            f"Pourquoi {topic} est important?",
            f"Quels sont les défis liés à {topic}?",
            f"Quels sont les développements récents en {topic}?"
        ]


def generate_research_plan(topic: str, num_questions: int = 5) -> dict:
    """
    Génère un plan de recherche complet pour un sujet.
    
    Args:
        topic: Le sujet de recherche
        num_questions: Nombre de questions à générer
    
    Returns:
        Dict contenant le plan de recherche
    """
    logger.info(f"Génération du plan de recherche pour: {topic}")
    
    questions = generate_research_questions(topic, num_questions)
    
    plan = {
        "topic": topic,
        "num_sources": 5 * num_questions,
        "research_phases": [
            "Contextualisation générale",
            "Aspects techniques",
            "Implications pratiques",
            "Développements récents",
            "Perspectives futures"
        ],
        "questions": questions,
        "search_queries": questions  # Les questions servent aussi de requêtes
    }
    
    logger.success(f"✓ Plan de recherche généré avec {len(questions)} questions")
    return plan


if __name__ == "__main__":
    # Test
    topic = "Machine Learning et Intelligence Artificielle"
    questions = generate_research_questions(topic)
    print("\n✅ Questions générées:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
