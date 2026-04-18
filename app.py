import streamlit as st
import time, hashlib, psutil, unicodedata, textwrap
from fpdf import FPDF
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. IDENTIDADE SOBERANA v240.0 - TOTAL MATRIX GREEN] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"
COMMAND_BLUE = "#0000FF" # Mantido apenas para a área de digitação cerebral

st.set_page_config(page_title="XEON v240.0 GLOBAL", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

def speak(text, lang='pt-BR'):
    components.html(f"<script>var u=new SpeechSynthesisUtterance('{text}');u.lang='{lang}';u.rate=0.9;window.speechSynthesis.speak(u);</script>", height=0)

# ESTÉTICA INEGOCIÁVEL: TUDO VERDE E PRETO
st.markdown(f"""
    <style>
    [data-testid="stHeader"], .stApp header, footer {{ display: none !important; }}
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; margin-top: -60px; }}
    
    /* CORREÇÃO DAS SELEÇÕES (SELECTBOX) - DE BRANCO PARA VERDE */
    div[data-baseweb="select"] > div {{
        background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important;
        border: 1px solid {MATRIX_GREEN} !important;
    }}
    div[data-baseweb="popover"] {{ background-color: {BLACKOUT} !important; }}
    div[role="option"] {{ color: {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important; }}

    /* CORREÇÃO DOS BOTÕES DE DOWNLOAD - DE AZUL/BRANCO PARA VERDE */
    .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; 
        background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important;
    }}

    .stTextArea textarea {{ background-color: {COMMAND_BLUE} !important; color: #FFFFFF !important; font-weight: bold !important; border: 2px solid {MATRIX_GREEN} !important; }}
    .stButton button {{ border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-weight: bold; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; background: rgba(0,255,65,0.05); text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. GERADOR DE DOSSIÊ GLOBAL (6 PÁGINAS)] ---
def generate_global_dossier(node_name, lang='EN'):
    pdf = FPDF()
    titles = {
        'PT': ["AUDITORIA NIST", "FINANÇAS GLOBAIS", "GOVERNANÇA PQC", "FISIOLOGIA DIGITAL", "EB-1A EVIDENCE", "VEREDITO FINAL"],
        'EN': ["NIST AUDIT", "GLOBAL FINANCE", "PQC GOVERNANCE", "DIGITAL PHYSIOLOGY", "EB-1A EVIDENCE", "FINAL VERDICT"],
        'ES': ["AUDITORÍA NIST", "FINANZAS GLOBALES", "GOBERNANZA PQC", "FISIOLOGÍA DIGITAL", "EVIDENCIA EB-1A", "VEREDICTO FINAL"]
    }
    selected_setores = titles.get(lang, titles['EN'])
    for i, setor in enumerate(selected_setores):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, "XEON COMMAND - GLOBAL AUDIT SOH v2.2", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        content = f"SECTOR: {setor}\nARCHITECT: MARCO ANTONIO DO NASCIMENTO\nRATE: $1,000/H | 74 BPM\nVERDICT: MISSION CRITICAL READINESS"
        pdf.multi_cell(0, 7, content)
    return BytesIO(pdf.output())

# --- [3. DASHBOARD v240.0] ---
@st.fragment(run_every=3)
def global_hub():
    c1, c2, c3 = st.columns([1, 1, 1.5])
    with c1:
        st.metric("RATE", "$1,000/H")
        st.metric("BIO", "74 BPM")
    with c2:
        cpu = psutil.cpu_percent()
        st_echarts(options={"backgroundColor":"transparent","series":[{"type":'gauge',"detail":{"fontSize":15},"data":[{"value":cpu}]}]}, height="180px")
    with c3:
        st.markdown("**🧠 CEREBRO CIBERNÉTICO:**")
        query = st.text_area("INGESTÃO:", height=85, label_visibility="collapsed", key="v240_azul")
        if st.button("🚀 PROCESSAR"): speak(f"Processando comando em malha verde.")

    st.divider()
    nos = ["BIOGENETICS", "NEURALINK", "SÉRIE NIST", "CYBER DEFENSE", "SPACE INFRA", "IPO GOLD", "VALUATION", "PQC AUDIT", "SYSTEMIC HOMEOSTASIS"]
    cols = st.columns(3)
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><b>{n}</b><br><small>GLOBAL SOH v2.2</small></div>", unsafe_allow_html=True)
            lang_pdf = st.selectbox(f"IDIOMA {i}", ["EN", "PT", "ES"], key=f"sel_{i}", label_visibility="collapsed")
            if st.button(f"🎙️ DOSSIÊ {n}", key=f"btn_{i}"):
                speak(f"Iniciando auditoria {n}.", 'pt-BR')
                st.session_state[f"pdf_{i}"] = generate_global_dossier(n, lang_pdf)
            if f"pdf_{i}" in st.session_state:
                st.download_button(f"📥 BAIXAR {lang_pdf}", st.session_state[f"pdf_{i}"], f"XEON_{lang_pdf}_{n}.pdf", key=f"dl_{i}")

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v240.0</h1>", unsafe_allow_html=True)
global_hub()
