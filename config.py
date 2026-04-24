"""
Configuration centralisée de l'application
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# Search APIs
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")

# App Settings
APP_DEBUG = os.getenv("APP_DEBUG", "False").lower() == "true"
MAX_SOURCES_PER_QUERY = int(os.getenv("MAX_SOURCES_PER_QUERY", "5"))
RESEARCH_DEPTH = os.getenv("RESEARCH_DEPTH", "balanced")

# Paths
REPORTS_DIR = "outputs/reports"
DATABASE_PATH = "database/history.db"
LOGS_DIR = "logs"

# Ensure directories exist
import os
for directory in [REPORTS_DIR, "database", LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)
