# ==========================================
# PROJECT: BABEL // LANGUAGE TERMINAL V1.2
# Core Uplink Established: 2026-02-23
# Focus: Earth Standard, Indigenous, and Galactic Dialects
#Created by NyssaFire Gaming and Anderson Farms
# ==========================================

import streamlit as st
import pandas as pd
import random
from supabase import create_client, Client

# --- CONFIG & SUPABASE CONNECTION ---
st.set_page_config(page_title="Babel Language App", page_icon="🌍", layout="wide")

@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# --- UI LABELS (SUPABASE) ---
@st.cache_data(ttl=600)
def load_languages():
    try:
        response = supabase.table("app_labels").select("*").execute()
        labels_df = pd.DataFrame(response.data)
        if not labels_df.empty:
            return labels_df.set_index('label_key').to_dict('index')
        return {}
    except Exception as e:
        st.error(f"Supabase connection error: {e}")
        return {}

labels = load_languages()

def get_ui_text(label_key, default_text=""):
    """Fetches text from Supabase, prioritizing the 'preferred_name' column if it exists."""
    label_data = labels.get(label_key, {})
    # This automatically uses your preferred naming conventions if you added them to the database
    return label_data.get('preferred_name') or label_data.get('english_text') or default_text

# Custom styling
st.markdown("""
<style>
.phonetic { font-size: 20px; color: #AAAAAA; font-style: italic; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# --- STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'target_lang' not in st.session_state: st.session_state.target_lang = "Klingon"
if 'tier' not in st.session_state: st.session_state.tier = "Free"

# --- CLOUD DATABASE UPLINK (Google Sheets for Vocab) ---
@st.cache_data(ttl=600)
def load_cloud_database():
    sheet_id = "1TyURzmvrj_pxPQqonPA8nJuT0nw0QGQxrbznN7ooJyI"
    cloud_sources = {
        "Spanish": "0",
        "French": "1979626029",
        "Vulcan": "1706569588",
        "Hebrew": "2050849856",
        "Cherokee": "536791395",
        "Klingon": "226168764",
        "High Valyrian": "23375132",
    }
    
    master_db = {lang: [] for lang in cloud_sources}
    
    try:
        for lang, gid in cloud_sources.items():
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
            df = pd.read_csv(url)
            
            if lang == "Spanish": audio_code = "es"
            elif lang == "French": audio_code = "fr"
            elif lang == "Hebrew": audio_code = "iw"
            else: audio_code = None
            
            for index, row in df.iterrows():
                options = [
                    str(row.get("Correct Translation", "")),
                    str(row.get("Wrong 1", "")),
                    str(row.get("Wrong 2", "")),
                    str(row.get("Wrong 3", ""))
                ]
                random.shuffle(options)
                
                master_db[lang].append({
                    "q": str(row.get(lang, "")),
                    "script": str(row.get("
