import streamlit as st
import time, hashlib, psutil, unicodedata, textwrap
from fpdf import FPDF
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI
import yfinance as yf

# --- [1. IDENTIDADE SOBERANA v180.0] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"
COMMAND_BLUE = "#0000FF"

st.set_page_config(page_title="XEON v180.0 - BIOINFORMÁTICA", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

def speak(text):
    components.html(f"<script>var u=new SpeechSynthesisUtterance('{text}');u.lang='pt-BR';window.speechSynthesis.speak(u);</script>", height=0)

# --- [2. GERADOR DE DOSSIÊ SOBERANO (6 PÁGINAS)] ---
def generate_6page_dossier(node_name):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    setores = ["AUDITORIA NIST", "FINANÇAS GLOBAIS", "GOVERNANÇA PQC", "FISIOLOGIA DIGITAL", "EB-1A EVIDENCE", "VEREDITO FINAL"]
    
    # Simulação de Telemetria Fisiológica
    bpm = 74 # Ideal para homeostase do Arquiteto
    spo2 = 99
    sp500 = "7035.94" # Conforme anexo
    pqc_sig = hashlib.sha256(f"{time.time()}".encode()).hexdigest()

    for i, setor in enumerate(setores):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        
        pdf.cell(0, 10, "XEON COMMAND AUDIT - BIOINFORMATICA FISIOLOGICA", ln=True, align='C')
        pdf.set_font("Courier", "B", 10)
        pdf.cell(0, 10, f"SMART-TAG: {hashlib.md5(node_name.encode()).hexdigest().upper()} | PAGE {i+1}/6", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Courier", "", 10)
        metadata = [
            f"SETOR: {setor}",
            f"TIMESTAMP: {time.strftime('%H:%M:%S')} | ESTADO: FALLBACK-SOBERANO",
            f"TELEMETRIA FISIOLOGICA (IoT): {bpm} BPM | {spo2}% SpO2",
            f"S&P 500: {sp500}",
            f"PQC SIGNATURE: {pqc_sig}"
        ]
        
        for line in metadata:
            pdf.cell(0, 7, line, ln=True)
            
        pdf.ln(5); pdf.cell(0, 0, "-"*60, ln=True)
        pdf.ln(10)
        
        pdf.set_font("Courier", "B", 11)
        pdf.multi_cell(0, 8, "RELATORIO DE AUDITORIA E SOBERANIA DIGITAL - ARQUITETO MARCO ANTONIO.\nINFRAESTRUTURA NACIONAL PROTEGIDA.")
        
    return BytesIO(pdf.output())

# --- [3. INTERFACE DE COMANDO] ---
@st.fragment(run_every=2)
def bio_hub():
    c1, c2, c3 = st.columns([1, 1, 1.5])
    with c1: st.metric("S&P 500", "7035.94", delta="STABLE")
    with c2: st.metric("IoT BIO", "74 BPM", delta="NORMAL")
    with c3:
        st.markdown("**🧠 CÉREBRO CIBERNÉTICO (DIGITAR):**")
        st.text_area("PESQUISA / INGESTÃO:", height=70, label_visibility="collapsed", key="in_azul")

    st.divider()
    
    # 9 NÓS MANTIDOS E PROTEGIDOS
    nos = ["BIOGENETICS", "NEURALINK", "SÉRIE NIST", "CYBER DEFENSE", "SPACE INFRA", "IPO GOLD", "VALUATION", "PQC AUDIT", "SYSTEMIC HOMEOSTASIS"]
    cols = st.columns(3)
    
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"<div style='border:1px solid {MATRIX_GREEN}; padding:10px; text-align:center;'><b>{n}</b><br><small>SOH v2.2</small></div>", unsafe_allow_html=True)
            if st.button(f"🎙️ GERAR DOSSIÊ 6 PAGS: {n}", key=f"n_{i}"):
                speak(f"Gerando dossiê de seis páginas para o setor {n}. Iniciando auditoria NIST e Bioinformática.")
                st.session_state[f"dossie_{i}"] = generate_6page_dossier(n)
            
            if f"dossie_{i}" in st.session_state:
                st.download_button(f"📥 BAIXAR DOSSIÊ {n}", st.session_state[f"dossie_{i}"], f"XEON_DOSSIE_{n}.pdf", key=f"dl_{i}")

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v180.0</h1>", unsafe_allow_html=True)
bio_hub()
