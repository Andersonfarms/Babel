# ==========================================
# PROJECT: BABEL // LANGUAGE TERMINAL V1.1
# Core Uplink Established: 2026-02-23
# Focus: Earth Standard, Indigenous, and Galactic Dialects
# ==========================================

import streamlit as st
import random
import time
from gtts import gTTS
import base64
import os
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Polyglot Prime", page_icon="🌍", layout="centered")

# --- CUSTOM UI STYLING ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FFFFFF; font-family: 'Arial Rounded MT Bold', sans-serif; }
    .xp-bar { background-color: #333; border-radius: 10px; height: 20px; width: 100%; margin-bottom: 20px; }
    .xp-fill { background-color: #00E676; height: 100%; border-radius: 10px; transition: width 0.5s ease-in-out; }
    .stButton>button { background-color: #2962FF; color: white; border-radius: 15px; font-weight: bold; height: 60px; width: 100%; font-size: 18px; border: none; }
    .stButton>button:hover { background-color: #0039CB; border: 2px solid white; }
    .vocab-card { background-color: #1E2129; padding: 30px; border-radius: 20px; text-align: center; border: 2px solid #333; margin-bottom: 20px;}
    .big-word { font-size: 40px; font-weight: bold; margin-bottom: 10px; color: #00E676;}
    .phonetic { font-size: 20px; color: #AAAAAA; font-style: italic; margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# --- STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'target_lang' not in st.session_state: st.session_state.target_lang = "Klingon"
if 'tier' not in st.session_state: st.session_state.tier = "Free"

# --- EXPANDED MULTI-VERSAL DATABASE ---
# Note: 'audio' is set to None for unsupported languages so the app doesn't crash.
import pandas as pd

# --- CLOUD DATABASE UPLINK ---
@st.cache_data(ttl=600) # Memorizes the sheet for 10 minutes for extreme speed
def load_cloud_database():
    sheet_id = "1TyURzmvrj_pxPQqonPA8nJuT0nw0QGQxrbznN7ooJyI"
    
    # Define our cloud sources by their Google Sheet 'gid'
    cloud_sources = {
    "Spanish": "0",
    "French": "1979626029",
    "Vulcan": "1706569588",
    "Hebrew": "2050849856",
    "Cherokee": "536791395"
}
    
    # We build the master database (keeping the Sci-Fi ones here for now)
    master_db = {
        "Spanish": [],
        "French": [],
        "Vulcan": [],
        "Hebrew":[],
        "Cherokee":[],
        "Klingon": [
            {"q": "nuqneH", "p": "(nook-NEKH)", "a": "What do you want? / Hello", "options": ["Goodbye", "What do you want? / Hello", "Honor", "Battle"], "audio": None},
            {"q": "Qapla'", "p": "(KAH-plah)", "a": "Success!", "options": ["Failure", "Success!", "Attack", "Defend"], "audio": None},
            {"q": "batlh", "p": "(baht-L)", "a": "Honor", "options": ["Honor", "Cowardice", "Sword", "Ship"], "audio": None}
        ],
        "High Valyrian": [
            {"q": "Rytsas", "p": "(RIT-sas)", "a": "Hello", "options": ["Goodbye", "Hello", "Dragon", "Fire"], "audio": None},
            {"q": "Dracarys", "p": "(drah-KAH-ris)", "a": "Dragonfire", "options": ["Fly", "Sword", "Dragonfire", "Blood"], "audio": None}
        ]
    }
    
    try:
        # Loop through both the Spanish and French tabs!
        for lang, gid in cloud_sources.items():
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
            df = pd.read_csv(url)
            
           # Set the correct Google Audio Accent or Disable for Sci-Fi
            if lang == "Spanish":
                audio_code = "es"
            elif lang == "French":
                audio_code = "fr"
            elif lang == "Hebrew":
                audio_code = "iw" # Modern Hebrew code
            else:
                audio_code = None # Disables audio for Vulcan, Klingon, and now Cherokee
            
            for index, row in df.iterrows():
                # Grab all the answers and shuffle them
                options = [str(row["Correct Translation"]), str(row["Wrong 1"]), str(row["Wrong 2"]), str(row["Wrong 3"])]
                random.shuffle(options)
                
                # Add the word to the specific language dictionary
                master_db[lang].append({
                    "q": str(row[lang]),
                    "script": str(row["Script"]) if "Script" in df.columns else None,
                    "p": str(row["Phonetic"]),
                    "a": str(row["Correct Translation"]),
                    "options": options,
                    "audio": audio_code
                })
    except Exception as e:
        st.error("⚠️ Cloud Database Uplink Failed. Check your Sheet IDs.")
        
    return master_db

VOCAB_DB = load_cloud_database()

# --- HYBRID AUDIO GENERATOR ---
def play_audio(text, lang_code):
    if lang_code is None:
        st.toast("⚠️ Audio telemetry unavailable for this dialect.", icon="🔇")
        return
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save("temp.mp3")
        with open("temp.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            
        # We use a unique ID (timestamp) to force the browser to re-render the audio tag
        unique_id = time.time()
        md = f"""
            <audio autoplay key="{unique_id}">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)
        os.remove("temp.mp3")
    except Exception as e:
        st.error(f"Audio uplink failed: {e}")

def load_new_question():
    st.session_state.current_q = random.choice(VOCAB_DB[st.session_state.target_lang])

if st.session_state.current_q is None:
    load_new_question()

# --- HEADER: GAMIFICATION ---
def get_rank(xp):
    if xp < 100: return "Novice"
    if xp < 500: return "Voyager"
    if xp < 1500: return "Prime Speaker"
    if xp < 5000: return "Polyglot"
    if xp < 10000: return "Universal Translator"
    return "Galactic Linguist"

c1, c2, c3 = st.columns([1, 2, 1])
current_rank = get_rank(st.session_state.xp) # Now the function is defined!

with c1:
    st.markdown(f"🔥 **Streak: {st.session_state.streak}**")
    st.markdown(f"🏆 **Rank: {current_rank}**")

with c2:
    # Calculate progress toward the next 100 XP milestone for the bar
    xp_percentage = min(100, (st.session_state.xp % 100))
    st.markdown(f'<div class="xp-bar"><div class="xp-fill" style="width: {xp_percentage}%;"></div></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f"⭐ **XP: {st.session_state.xp}**")

# --- MAIN LESSON UI ---
new_lang = st.selectbox("Select Target Language:", list(VOCAB_DB.keys()), index=list(VOCAB_DB.keys()).index(st.session_state.target_lang))
if new_lang != st.session_state.target_lang:
    st.session_state.target_lang = new_lang
    load_new_question()
    st.rerun()

q_data = st.session_state.current_q

# Logic to handle if a language has a 'Script' column
display_word = q_data["q"]
if "script" in q_data and q_data["script"] != "None":
        # Show Script (Aleph-bet) and Transliterated side-by-side
        display_word = f"{q_data['script']} ({q_data['q']})"

# Display the Word and Phonetic Spelling cleanly
st.markdown(f'''
        <div class="vocab-card">
            <div class="big-word">{display_word}</div>
            <div class="phonetic">{q_data["p"]}</div>
            <p>Select the correct translation:</p>
        </div>
''', unsafe_allow_html=True)
if st.button("🔊 Play Audio"):
    # Pass the main text to the audio engine. It will catch the 'None' and show a toast warning for Sci-Fi/Navajo.
    play_audio(q_data["q"], q_data["audio"])

st.write("")

# --- ANSWER LOGIC ---
cols = st.columns(2)
for i, option in enumerate(q_data["options"]):
    with cols[i % 2]:
        if st.button(option, key=f"btn_{i}"):
            if option == q_data["a"]:
                st.success(f"✅ Correct! '{q_data['q']}' means '{q_data['a']}'. +10 XP")
                st.session_state.xp += 10
                time.sleep(1.5)
                load_new_question()
                st.rerun()
            else:
                st.error("❌ Incorrect translation. Try again!")

st.divider()

# --- PAYWALL (V1 PREVIEW) ---
if st.session_state.tier == "Free":
    st.info("🔓 Free Tier (Limited to 20 phrases daily).")
    st.button("💎 UNLOCK FULL VERSAL DATABASE ($20 LIFETIME)", use_container_width=True)
