"""
Database Manager - Gestion de l'historique et du cache
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger

class DatabaseManager:
    """Gère la base de données SQLite"""
    
    def __init__(self, db_path: str = "database/history.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info(f"✓ Database initialized: {db_path}")
    
    def _init_database(self):
        """Initialise les tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des recherches
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                num_questions INTEGER,
                num_sources INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                report_path TEXT,
                status TEXT DEFAULT 'completed'
            )
        """)
        
        # Table des sources en cache
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                title TEXT,
                snippet TEXT,
                summary TEXT,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table des rapports générés
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id INTEGER,
                topic TEXT,
                content TEXT,
                mode TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (search_id) REFERENCES searches(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_search(self, topic: str, num_questions: int, num_sources: int, 
                    report_path: str) -> int:
        """Sauvegarde une recherche"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO searches (topic, num_questions, num_sources, report_path)
            VALUES (?, ?, ?, ?)
        """, (topic, num_questions, num_sources, report_path))
        
        search_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Search saved with ID: {search_id}")
        return search_id
    
    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """Récupère l'historique des recherches"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, topic, num_questions, num_sources, created_at, report_path
            FROM searches
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "topic": row[1],
                "num_questions": row[2],
                "num_sources": row[3],
                "created_at": row[4],
                "report_path": row[5]
            }
            for row in rows
        ]
    
    def cache_source(self, url: str, title: str, snippet: str, summary: str):
        """Met en cache une source"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO sources (url, title, snippet, summary)
                VALUES (?, ?, ?, ?)
            """, (url, title, snippet, summary))
            
            conn.commit()
            logger.debug(f"✓ Source cached: {url}")
        except Exception as e:
            logger.warning(f"⚠ Cache error: {e}")
        finally:
            conn.close()
    
    def get_cached_source(self, url: str) -> Optional[Dict]:
        """Récupère une source en cache"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT url, title, snippet, summary, cached_at
            FROM sources
            WHERE url = ?
        """, (url,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "url": row[0],
                "title": row[1],
                "snippet": row[2],
                "summary": row[3],
                "cached_at": row[4]
            }
        return None
    
    def clear_old_cache(self, days: int = 30):
        """Nettoie le cache ancien"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM sources
            WHERE cached_at < datetime('now', '-' || ? || ' days')
        """, (days,))
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"✓ {deleted} old sources deleted")
        return deleted


if __name__ == "__main__":
    # Test
    db = DatabaseManager()
    
    # Sauvegarde une recherche
    search_id = db.save_search("AI", 5, 10, "output.md")
    
    # Récupère l'historique
    history = db.get_search_history()
    print(f"✅ {len(history)} searches in history")
