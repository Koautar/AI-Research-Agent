"""
Streamlit App - Interface interactive
"""

import streamlit as st
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Configure la page
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load env
load_dotenv()

# Import des modules
from agents.researcher import run_full_research
from agents.writer import write_full_report
from tools.pdf_exporter import markdown_to_pdf


def check_api_key():
    """Vérifie que la clé API est configurée"""
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OPENAI_API_KEY non configurée. Créez un fichier `.env` avec votre clé.")
        st.stop()


def save_session_state():
    """Sauvegarde l'état de la session"""
    session_file = Path("outputs/session.json")
    if "research_data" in st.session_state:
        with open(session_file, 'w') as f:
            json.dump({
                "topic": st.session_state.get("topic", ""),
                "num_questions": st.session_state.get("num_questions", 5),
                "num_sources": st.session_state.get("num_sources", 10),
            }, f)


def load_session_state():
    """Charge l'état de la session"""
    session_file = Path("outputs/session.json")
    if session_file.exists():
        with open(session_file, 'r') as f:
            return json.load(f)
    return {}


# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .progress-box {
        padding: 0.5rem;
        background-color: #e7f3ff;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Vérification API
check_api_key()

# Initialise la session
if "research_data" not in st.session_state:
    st.session_state.research_data = None
if "report" not in st.session_state:
    st.session_state.report = None
if "research_complete" not in st.session_state:
    st.session_state.research_complete = False


# Header
st.markdown("# 🔬 AI Research Agent")
st.markdown("Générez des rapports de recherche complets automatiquement")
st.divider()

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    topic = st.text_input(
        "📌 Sujet de recherche",
        placeholder="Ex: Machine Learning, Blockchain, ...",
        key="topic_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider(
            "Questions de recherche",
            min_value=1,
            max_value=10,
            value=5,
            key="num_questions_slider"
        )
    with col2:
        num_sources = st.slider(
            "Sources à résumer",
            min_value=1,
            max_value=20,
            value=10,
            key="num_sources_slider"
        )
    
    report_mode = st.selectbox(
        "📋 Mode de rapport",
        ["balanced", "student", "business", "technical"],
        help="Type de rapport à générer"
    )
    
    st.divider()
    
    # Bouton de lancement
    if st.button("🚀 Démarrer la recherche", use_container_width=True, type="primary"):
        if not topic:
            st.error("❌ Veuillez entrer un sujet")
        else:
            st.session_state.topic = topic
            st.session_state.num_questions = num_questions
            st.session_state.num_sources = num_sources
            st.session_state.report_mode = report_mode
            st.session_state.start_research = True
    
    st.divider()
    
    # Info
    st.info("""
    ℹ️ **Comment ça marche:**
    
    1. Entrez un sujet
    2. Configurez le nombre de questions
    3. Cliquez sur "Démarrer la recherche"
    4. L'agent génère un rapport complet
    5. Exportez en Markdown ou PDF
    """)


# Main content
if st.session_state.get("start_research"):
    st.session_state.start_research = False
    
    topic = st.session_state.topic
    num_questions = st.session_state.num_questions
    num_sources = st.session_state.num_sources
    report_mode = st.session_state.report_mode
    
    # Conteneurs pour l'affichage progressif
    status_container = st.container()
    progress_container = st.container()
    results_container = st.container()
    
    with status_container:
        st.markdown(f"### 🔍 Recherche en cours: {topic}")
        progress_bar = st.progress(0)
    
    try:
        # Phase 1: Recherche (0-60%)
        with progress_container:
            st.markdown('<div class="progress-box">Phase 1/3: Recherche et synthèse...</div>', unsafe_allow_html=True)
        
        progress_bar.progress(10)
        st.info("📊 Génération des questions de recherche...")
        
        research_data = run_full_research(topic, num_questions, num_sources)
        
        progress_bar.progress(60)
        st.success(f"✓ {len(research_data['summaries'])} sources résumées")
        
        # Phase 2: Rédaction (60-80%)
        with progress_container:
            st.markdown('<div class="progress-box">Phase 2/3: Rédaction du rapport...</div>', unsafe_allow_html=True)
        
        progress_bar.progress(70)
        report = write_full_report(topic, research_data, report_mode)
        
        progress_bar.progress(80)
        st.success("✓ Rapport généré")
        
        # Phase 3: Finalization (80-100%)
        with progress_container:
            st.markdown('<div class="progress-box">Phase 3/3: Finalization...</div>', unsafe_allow_html=True)
        
        progress_bar.progress(100)
        st.success("✅ Rapport complété!")
        
        # Sauvegarde la session
        st.session_state.research_data = research_data
        st.session_state.report = report
        st.session_state.research_complete = True
    
    except Exception as e:
        st.error(f"❌ Erreur lors de la recherche: {e}")
        st.session_state.research_complete = False


# Affichage des résultats
if st.session_state.research_complete and st.session_state.report:
    st.divider()
    
    # Tabs pour les résultats
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Rapport", "📊 Synthèse", "📚 Sources", "⬇️ Export"])
    
    with tab1:
        st.markdown("### Rapport complet")
        st.markdown(st.session_state.report)
    
    with tab2:
        st.markdown("### Synthèse des résultats")
        if "summaries" in st.session_state.research_data:
            for url, data in list(st.session_state.research_data["summaries"].items())[:5]:
                with st.expander(f"📌 {data['title']}"):
                    st.markdown(data['summary'])
                    st.caption(f"🔗 {url}")
    
    with tab3:
        st.markdown("### Sources trouvées")
        sources = st.session_state.research_data.get("search_results", {}).get("all", [])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.metric("Total sources", len(sources))
        
        for source in sources[:10]:
            with st.expander(f"🔗 {source['title']}"):
                st.markdown(f"**URL:** {source['url']}")
                st.markdown(f"**Snippet:** {source['snippet']}")
    
    with tab4:
        st.markdown("### Options d'export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export Markdown
            if st.button("📥 Télécharger Markdown", use_container_width=True):
                filename = st.session_state.topic.replace(" ", "_")[:30]
                st.download_button(
                    label="📄 Rapport Markdown",
                    data=st.session_state.report,
                    file_name=f"{filename}.md",
                    mime="text/markdown"
                )
        
        with col2:
            # Export PDF
            if st.button("📥 Générer PDF", use_container_width=True):
                try:
                    st.info("⏳ Génération du PDF...")
                    pdf_path = f"outputs/reports/{st.session_state.topic.replace(' ', '_')}.pdf"
                    
                    markdown_to_pdf(
                        st.session_state.report,
                        pdf_path,
                        title=st.session_state.topic
                    )
                    
                    with open(pdf_path, 'rb') as f:
                        st.download_button(
                            label="📄 Télécharger PDF",
                            data=f.read(),
                            file_name=f"{st.session_state.topic.replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                except Exception as e:
                    st.error(f"Erreur lors de la génération PDF: {e}")


# Footer
st.divider()
st.markdown("""
---
**AI Research Agent** | Généré automatiquement avec OpenAI GPT-4 | [Source Code](https://github.com)
""", unsafe_allow_html=True)
