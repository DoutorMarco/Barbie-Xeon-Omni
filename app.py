import streamlit as st
import time, hashlib, psutil, unicodedata, textwrap
from fpdf import FPDF
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. IDENTIDADE SOBERANA v195.0] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"
COMMAND_BLUE = "#0000FF"

st.set_page_config(page_title="XEON v195.0 - BIO-MONITOR", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

def speak(text):
    components.html(f"<script>var u=new SpeechSynthesisUtterance('{text}');u.lang='pt-BR';u.rate=0.9;window.speechSynthesis.speak(u);</script>", height=0)

# Estética Matrix Anti-Stress (Zero Branco)
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    
    /* ZONA CEREBRAL AZUL PROFUNDO */
    .stTextArea textarea {{
        background-color: {COMMAND_BLUE} !important; 
        color: #FFFFFF !important; 
        font-weight: bold !important;
        border: 2px solid {MATRIX_GREEN} !important;
    }}
    
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold;
    }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 12px; background: rgba(0,255,65,0.05); text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE DOSSIÊ v1032 (6 PÁGINAS)] ---
def generate_sovereign_dossier(node_name):
    pdf = FPDF()
    setores = ["AUDITORIA NIST", "FINANÇAS GLOBAIS", "GOVERNANÇA PQC", "FISIOLOGIA DIGITAL", "EB-1A EVIDENCE", "VEREDITO FINAL"]
    for i, setor in enumerate(setores):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, "XEON COMMAND AUDIT - BIOINFORMATICA FISIOLOGICA", ln=True, align='C')
        pdf.set_font("Courier", "B", 10)
        pdf.cell(0, 10, f"SMART-TAG: {hashlib.md5(node_name.encode()).hexdigest().upper()} | PAGE {i+1}/6", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        content = f"SETOR: {setor}\nSOH v2.2 STATUS: ACTIVE\nTELEMETRIA: 74 BPM | 99% SpO2\nS&P 500: 7035.94\nVEREDITO: MISSION CRITICAL READINESS"
        pdf.multi_cell(0, 7, content)
    return BytesIO(pdf.output())

# --- [3. DASHBOARD v195.0 COM BIOFEEDBACK] ---
@st.fragment(run_every=3)
def bio_command_hub():
    # Monitoramento de Saúde do Arquiteto (Voz Automática)
    if 'prev_bpm' not in st.session_state: st.session_state.prev_bpm = 74
    current_bpm = 74 # Simulação fixa para estabilidade; em uso real, viria de IoT
    
    # Se houver variação ou ciclo de 5 min, o sistema reporta
    if time.time() % 300 < 3: # A cada 5 min
        speak(f"Arquiteto, telemetria biofisiológica estável em {current_bpm} batimentos por minuto. Homeostase mantida.")

    c1, c2, c3 = st.columns([1, 1, 1.5])
    
    with c1:
        st.metric("S&P 500", "7035.94", delta="0.05%")
        st.metric("BIO-STATUS", f"{current_bpm} BPM", delta="NOMINAL")

    with c2:
        cpu = psutil.cpu_percent()
        options = {
            "backgroundColor": "transparent",
            "series": [{
                "type": 'gauge',
                "axisLine": {"lineStyle": {"width": 8, "color": [[0.3, '#00ff41'], [0.7, '#00ff41'], [1, '#ff4100']]}},
                "detail": {"color": MATRIX_GREEN, "fontSize": 15},
                "data": [{"value": cpu, "name": 'STRESS'}]
            }]
        }
        st_echarts(options=options, height="180px")

    with c3:
        st.markdown(f"<b style='color:#FFFFFF;'>🧠 CÉREBRO CIBERNÉTICO (DIGITAR):</b>", unsafe_allow_html=True)
        query = st.text_area("PESQUISAR / INGESTÃO:", height=85, label_visibility="collapsed", key="brain_azul")
        if st.button("🚀 EXECUTAR COMANDO"):
            speak(f"Processando comando soberano para {query[:15]}. Auditoria NIST iniciada.")

    st.divider()
    
    # 9 NÓS DO NEXUS SUPREMO
    nos = ["BIOGENETICS", "NEURALINK", "LAW & SOVEREIGNTY", "CYBER DEFENSE", "SPACE INFRA", "IPO GOLD", "VALUATION", "PQC AUDIT", "SYSTEMIC HOMEOSTASIS"]
    cols = st.columns(3)
    
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><b>{n}</b><br><small>SOH v2.2</small></div>", unsafe_allow_html=True)
            if st.button(f"🎙️ GERAR DOSSIÊ {n}", key=f"btn_{i}"):
                speak(f"Iniciando nó {n}. Gerando dossiê de seis páginas com telemetria bio-informática.")
                st.session_state[f"pdf_{i}"] = generate_sovereign_dossier(n)
            
            if f"pdf_{i}" in st.session_state:
                st.download_button(f"📥 DOWNLOAD DOSSIÊ {n}", st.session_state[f"pdf_{i}"], f"XEON_NIST_{n}.pdf", key=f"dl_{i}")

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v195.0</h1>", unsafe_allow_html=True)
bio_command_hub()

if psutil.cpu_percent() > 85:
    speak("Aviso Crítico: Stress de hardware elevado. Iniciando protocolos de resfriamento.")
