import streamlit as st
import time, hashlib, psutil, unicodedata, textwrap
from fpdf import FPDF
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. IDENTIDADE SOBERANA v230.0 - GLOBAL BLACKOUT] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"
COMMAND_BLUE = "#0000FF"

st.set_page_config(page_title="XEON v230.0 GLOBAL", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

def speak(text, lang='pt-BR'):
    # Detecta idioma para a voz automática
    components.html(f"<script>var u=new SpeechSynthesisUtterance('{text}');u.lang='{lang}';u.rate=0.9;window.speechSynthesis.speak(u);</script>", height=0)

st.markdown(f"""
    <style>
    [data-testid="stHeader"], .stApp header, footer {{ display: none !important; }}
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; margin-top: -60px; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 12px {MATRIX_GREEN}; }}
    .stTextArea textarea {{ background-color: {COMMAND_BLUE} !important; color: #FFFFFF !important; font-weight: bold !important; border: 2px solid {MATRIX_GREEN} !important; }}
    .stButton button {{ border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-weight: bold; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; background: rgba(0,255,65,0.05); text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. GERADOR DE DOSSIÊ MULTILINGUE (6 PÁGINAS)] ---
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
        header = "XEON COMMAND - SOVEREIGN GLOBAL AUDIT"
        pdf.cell(0, 10, header, ln=True, align='C')
        pdf.set_font("Courier", "B", 10)
        pdf.cell(0, 10, f"ID: {hashlib.sha256(node_name.encode()).hexdigest()[:12].upper()} | PAGE {i+1}/6", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        content = f"SECTOR: {setor}\nARCHITECT: MARCO ANTONIO DO NASCIMENTO\nRATE: $1,000/H | 74 BPM\nSTATUS: MISSION CRITICAL READINESS"
        pdf.multi_cell(0, 7, content)
    return BytesIO(pdf.output())

# --- [3. DASHBOARD GLOBAL v230.0] ---
@st.fragment(run_every=3)
def global_hub():
    c1, c2, c3 = st.columns([1, 1, 1.5])
    with c1:
        st.metric("GLOBAL RATE", "$1,000/H")
        st.metric("HOMEÓSTASE", "74 BPM")
    with c2:
        cpu = psutil.cpu_percent()
        st_echarts(options={"backgroundColor":"transparent","series":[{"type":'gauge',"axisLine":{"lineStyle":{"width":8,"color":[[0.3,'#00ff41'],[0.7,'#00ff41'],[1,'#ff4100']]}},"detail":{"color":MATRIX_GREEN,"fontSize":15},"data":[{"value":cpu,"name":'STRESS'}]}]}, height="180px")
    with c3:
        st.markdown(f"<b style='color:#FFFFFF;'>🌐 GLOBAL BRAIN / CEREBRO GLOBAL (PT/EN/ES):</b>", unsafe_allow_html=True)
        query = st.text_area("PESQUISA / SEARCH / BUSQUEDA:", height=85, label_visibility="collapsed", key="v230_azul")
        
        col_btns = st.columns(3)
        if col_btns[0].button("🚀 PT-BR"): speak(f"Processando em Português: {query[:10]}", 'pt-BR')
        if col_btns[1].button("🚀 EN-US"): speak(f"Processing in English: {query[:10]}", 'en-US')
        if col_btns[2].button("🚀 ES-ES"): speak(f"Procesando en Español: {query[:10]}", 'es-ES')

    st.divider()
    nos = ["BIOGENETICS", "NEURALINK", "SÉRIE NIST", "CYBER DEFENSE", "SPACE INFRA", "IPO GOLD", "VALUATION", "PQC AUDIT", "SYSTEMIC HOMEOSTASIS"]
    cols = st.columns(3)
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><b>{n}</b><br><small>GLOBAL SOH v2.2</small></div>", unsafe_allow_html=True)
            lang_pdf = st.selectbox(f"LANG {i}", ["EN", "PT", "ES"], key=f"sel_{i}", label_visibility="collapsed")
            if st.button(f"🎙️ DOSSIÊ {n}", key=f"btn_{i}"):
                speak(f"Generating dossier for node {n} in {lang_pdf}", 'en-US' if lang_pdf=='EN' else 'pt-BR')
                st.session_state[f"pdf_{i}"] = generate_global_dossier(n, lang_pdf)
            if f"pdf_{i}" in st.session_state:
                st.download_button(f"📥 DOWNLOAD {lang_pdf}", st.session_state[f"pdf_{i}"], f"XEON_{lang_pdf}_{n}.pdf", key=f"dl_{i}")

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v230.0</h1>", unsafe_allow_html=True)
global_hub()
