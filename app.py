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

# --- CONFIGURATION ---
st.set_page_config(page_title="Polyglot Pro", page_icon="🌍", layout="centered")

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
VOCAB_DB = {
    "Spanish": [
        {"q": "El agua", "p": "", "a": "The water", "options": ["The fire", "The water", "The earth", "The sky"], "audio": "es"},
        {"q": "Buenos días", "p": "", "a": "Good morning", "options": ["Good night", "Hello", "Goodbye", "Good morning"], "audio": "es"}
    ],
    "Hebrew": [
        {"q": "שָׁלוֹם", "p": "(Shalom)", "a": "Peace / Hello", "options": ["Goodbye", "Peace / Hello", "Water", "Bread"], "audio": "iw"},
        {"q": "מַיִם", "p": "(Mayim)", "a": "Water", "options": ["Fire", "Earth", "Water", "Sky"], "audio": "iw"}
    ],
    "Klingon": [
        {"q": "nuqneH", "p": "(nook-NEKH)", "a": "What do you want? / Hello", "options": ["Goodbye", "What do you want? / Hello", "Honor", "Battle"], "audio": None},
        {"q": "Qapla'", "p": "(KAH-plah)", "a": "Success!", "options": ["Failure", "Success!", "Attack", "Defend"], "audio": None},
        {"q": "batlh", "p": "(baht-L)", "a": "Honor", "options": ["Honor", "Cowardice", "Sword", "Ship"], "audio": None}
    ],
    "Vulcan": [
        {"q": "Dif-tor heh smusma", "p": "(Dif-tor heh smus-mah)", "a": "Live long and prosper", "options": ["Peace and long life", "Live long and prosper", "Logic dictates", "Fascinating"], "audio": None},
        {"q": "Cthia", "p": "(k-THEE-ah)", "a": "Logic / Reality", "options": ["Emotion", "Logic / Reality", "Science", "Mind Meld"], "audio": None}
    ],
    "Romulan": [
        {"q": "Jolan true", "p": "(jo-LAHN troo)", "a": "Hello / Peace be with you", "options": ["Attack now", "Hello / Peace be with you", "Victory", "Treachery"], "audio": None}
    ],
    "High Valyrian": [
        {"q": "Rytsas", "p": "(RIT-sas)", "a": "Hello", "options": ["Goodbye", "Hello", "Dragon", "Fire"], "audio": None},
        {"q": "Dracarys", "p": "(drah-KAH-ris)", "a": "Dragonfire", "options": ["Fly", "Sword", "Dragonfire", "Blood"], "audio": None}
    ],
    "Navajo (Diné Bizaad)": [
        {"q": "Yá'át'ééh", "p": "(Yah-ah-tay)", "a": "Hello / It is good", "options": ["Goodbye", "Water", "Hello / It is good", "Sun"], "audio": None},
        {"q": "Tó", "p": "(Toh)", "a": "Water", "options": ["Fire", "Earth", "Water", "Wind"], "audio": None}
    ]
}

# --- HYBRID AUDIO GENERATOR ---
def play_audio(text, lang_code):
    if lang_code is None:
        st.toast("⚠️ Audio telemetry unavailable for this dialect. Please read the phonetic spelling.", icon="🔇")
        return
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save("temp.mp3")
        with open("temp.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(md, unsafe_allow_html=True)
        os.remove("temp.mp3")
    except Exception as e:
        st.error("Audio uplink failed.")

def load_new_question():
    st.session_state.current_q = random.choice(VOCAB_DB[st.session_state.target_lang])

if st.session_state.current_q is None:
    load_new_question()

# --- HEADER: GAMIFICATION ---
c1, c2, c3 = st.columns([1, 2, 1])
with c1: st.markdown(f"🔥 **Streak: {st.session_state.streak}**")
with c2: 
    xp_percentage = min(100, (st.session_state.xp % 100))
    st.markdown(f'<div class="xp-bar"><div class="xp-fill" style="width: {xp_percentage}%;"></div></div>', unsafe_allow_html=True)
with c3: st.markdown(f"⭐ **XP: {st.session_state.xp}**")

st.divider()

# --- MAIN LESSON UI ---
new_lang = st.selectbox("Select Target Language:", list(VOCAB_DB.keys()), index=list(VOCAB_DB.keys()).index(st.session_state.target_lang))
if new_lang != st.session_state.target_lang:
    st.session_state.target_lang = new_lang
    load_new_question()
    st.rerun()

q_data = st.session_state.current_q

# Display the Word and Phonetic Spelling cleanly
st.markdown(f'''
<div class="vocab-card">
    <div class="big-word">{q_data["q"]}</div>
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
