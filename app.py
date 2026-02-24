# ==========================================
# PROJECT: BABEL // LANGUAGE TERMINAL V1.0
# Core Uplink Established: 2026-02-23
# ==========================================

import streamlit as st
import random
import time
from gtts import gTTS
import base64

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
    .big-word { font-size: 48px; font-weight: bold; margin-bottom: 10px; color: #00E676;}
</style>
""", unsafe_allow_html=True)

# --- STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'current_q' not in st.session_state: st.session_state.current_q = None
if 'target_lang' not in st.session_state: st.session_state.target_lang = "Spanish"
if 'tier' not in st.session_state: st.session_state.tier = "Free"

# --- MOCK DATABASE (Will move to Google Sheets later) ---
VOCAB_DB = {
    "Spanish": [
        {"q": "El agua", "a": "The water", "options": ["The fire", "The water", "The earth", "The sky"], "audio": "es"},
        {"q": "La biblioteca", "a": "The library", "options": ["The bathroom", "The store", "The library", "The kitchen"], "audio": "es"},
        {"q": "Buenos días", "a": "Good morning", "options": ["Good night", "Hello", "Goodbye", "Good morning"], "audio": "es"}
    ],
    "Hebrew": [ # Adding a specific language as requested by the "more than Duolingo" premise
        {"q": "שָׁלוֹם (Shalom)", "a": "Peace / Hello", "options": ["Goodbye", "Peace / Hello", "Water", "Bread"], "audio": "iw"},
        {"q": "מַיִם (Mayim)", "a": "Water", "options": ["Fire", "Earth", "Water", "Sky"], "audio": "iw"}
    ]
}

# --- AUDIO GENERATOR ---
def play_audio(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

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
st.session_state.target_lang = st.selectbox("Select Language:", list(VOCAB_DB.keys()))

q_data = st.session_state.current_q

st.markdown(f'<div class="vocab-card"><div class="big-word">{q_data["q"]}</div><p>What does this mean?</p></div>', unsafe_allow_html=True)

if st.button("🔊 Play Pronunciation"):
    # Strip phonetic english if present (e.g. in Hebrew) for TTS
    tts_text = q_data["q"].split("(")[0].strip() if "(" in q_data["q"] else q_data["q"]
    play_audio(tts_text, q_data["audio"])

st.write("")

# --- ANSWER LOGIC ---
cols = st.columns(2)
for i, option in enumerate(q_data["options"]):
    with cols[i % 2]:
        if st.button(option, key=f"btn_{i}"):
            if option == q_data["a"]:
                st.success("✅ Correct! +10 XP")
                st.session_state.xp += 10
                time.sleep(1)
                load_new_question()
                st.rerun()
            else:
                st.error("❌ Incorrect. Try again!")

st.divider()

# --- PAYWALL (V1 PREVIEW) ---
if st.session_state.tier == "Free":
    st.info("🔓 You are on the Free Tier. (Limited to 20 daily words).")
    st.button("💎 UNLOCK FULL VERSION ($20 LIFETIME)", use_container_width=True)
