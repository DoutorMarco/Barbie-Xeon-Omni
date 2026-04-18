import streamlit as st
import time, hashlib, psutil, unicodedata, textwrap
from fpdf import FPDF
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. IDENTIDADE BLACKOUT & VOX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v155.0", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

# Função de Voz (Vox Protocol)
def speak(text):
    components.html(f"""
        <script>
        var u = new SpeechSynthesisUtterance('{text}');
        u.lang = 'pt-BR';
        u.rate = 1.0;
        window.speechSynthesis.speak(u);
        </script>
    """, height=0)

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    input, textarea, [data-baseweb="select"] {{ 
        background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; 
        font-weight: bold !important; border: none !important; 
    }}
    .stButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; width: 100%; font-weight: bold; height: 45px;
    }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: rgba(0,255,65,0.05); text-align: center; }}
    .reprocessor {{ font-size: 0.6em; color: {MATRIX_GREEN}; opacity: 0.7; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. DASHBOARD v155.0 COM VOX ATIVA] ---
@st.fragment(run_every=2)
def xeon_sonic_core():
    cpu = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1, 1.5])
    
    with c1:
        st.metric("MONETIZAÇÃO", "$1,000/H")
        st.metric("STATUS", "VOX ACTIVE")
    
    with c2:
        options = {"backgroundColor": "transparent", "series": [{"type": 'gauge', "detail": {"color": MATRIX_GREEN, "fontSize": 12}, "data": [{"value": cpu, "name": 'CPU'}]}]}
        st_echarts(options=options, height="160px")

    with c3:
        st.markdown(f"<div style='background-color:{MATRIX_GREEN}; color:{BLACKOUT}; padding:5px; font-weight:bold;'>📥 INGESTAO VERDE / COMANDO DE VOZ:</div>", unsafe_allow_html=True)
        raw_input = st.text_area("DIGITE PARA PROCESSAR:", height=80, label_visibility="collapsed")
        if st.button("🚀 INGERIR DADOS"):
            speak(f"Arquiteto, iniciando processamento de {raw_input[:20]}")
            st.session_state.last_action = f"PROCESSADO: {hashlib.sha1(raw_input.encode()).hexdigest().upper()}"

    st.divider()
    
    # OS 9 NÓS COM REPROCESSADOR E VOX INDIVIDUAL
    nos = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NÓ 0{i+1}</small><br><b>{n}</b><div class='reprocessor'>HASH: {hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}</div></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {n}", key=f"btn_{i}"):
                speak(f"Nó {n} ativado. Gerando dossiê de missão crítica.")
                # Lógica de PDF simplificada para o exemplo
                st.success(f"Audit {n} Ready")

# --- [3. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v155.0</h1>", unsafe_allow_html=True)
xeon_sonic_core()

# Alerta de Stress Vocal
if psutil.cpu_percent() > 80:
    speak("Alerta Arquiteto: Carga de hardware elevada. Homeostase em risco.")
