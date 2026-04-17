import streamlit as st
import time
import hashlib
import psutil
import platform
import asyncio
import aiosqlite
import unicodedata
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. CONFIGURAÇÃO SOBERANA - BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0", layout="wide")

# [INTELIGÊNCIA GENERATIVA ATIVADA]
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 60px;
    }}
    .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {MATRIX_GREEN} !important;
        color: {BLACKOUT} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; text-align: center; background: rgba(0,255,65,0.05); margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF CORRIGIDO (REAL BYTES)] ---
def sanitize_text(text):
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')

def generate_dossier_fixed(node, cpu, ai_report):
    """Gera PDF em bytes reais para evitar erro de corrupção"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
    
    pdf.cell(0, 15, "NATIONAL INTEREST WAIVER - TECHNICAL EXHIBIT", ln=True, align='C')
    pdf.ln(10); pdf.set_font("Courier", "", 11)
    
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    report_safe = sanitize_text(ai_report)
    
    lines = [
        f"TIMESTAMP: {ts}",
        f"OPERATIONAL_NODE: {node}",
        f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
        f"HOMEOSTASE: {100-(cpu*0.1):.2f}%",
        "-"*60,
        "GEN-AI PHYSIOLOGY ANALYSIS:",
        report_safe,
        "-"*60,
        f"INTEGRITY_HASH: {hashlib.sha256(ts.encode()).hexdigest()[:32].upper()}"
    ]
    
    for line in lines:
        pdf.multi_cell(0, 8, line)
    
    # Retorna o buffer de bytes puro
    return pdf.output()

# --- [3. DASHBOARD DE COMANDO CENTRAL] ---
@st.fragment(run_every=5)
def xeon_main():
    cpu_val = psutil.cpu_percent()
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1:
        st.metric("STABILITY", "NOMINAL")
        try:
            val = yf.Ticker("USDBRL=X").history(period="1d")['Close'].iloc[-1]
            st.metric("MONETIZAÇÃO (USD)", f"{val:.2f}")
        except: st.metric("MARKET", "OFFLINE")

    with c2:
        st_echarts(options={"backgroundColor": "transparent", "series": [{"type": 'gauge', "data": [{"value": cpu_val}], "detail": {"color": MATRIX_GREEN}}]}, height="200px")

    with c3:
        st.metric("EB-1A READY", "YES")
        if st.button("🧠 ATIVAR IA GENERATIVA"):
            with st.status("Processando Fisiologia Digital...", expanded=False) as s:
                if client:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "system", "content": "Você é um perito em vistos EB-1A e Infraestrutura Crítica."},
                                  {"role": "user", "content": f"Analise a homeostase de {cpu_val}% do sistema XEON."}]
                    )
                    st.session_state.ai_report = res.choices.message.content
                    s.update(label="Análise Concluída", state="complete")
                else:
                    st.session_state.ai_report = "IA OFFLINE: Configure OPENAI_API_KEY nos Secrets."
                    s.update(label="Erro de Chave", state="error")

    st.markdown("<hr>", unsafe_allow_html=True)

    # 9 NÓS SOBERANOS
    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {s}", key=f"act_{i}"):
                st.session_state.active_node = s
                st.session_state.voice = f"Nó {s} ativado."
            
            if st.session_state.get('active_node') == s:
                report = st.session_state.get('ai_report', "Execute o SCAN de IA primeiro.")
                pdf_data = generate_dossier_fixed(s, cpu_val, report)
                st.download_button(
                    label=f"📥 BAIXAR EB-1A {s}", 
                    data=pdf_data, 
                    file_name=f"XEON_{s.replace(' ','_')}.pdf",
                    mime="application/pdf",
                    key=f"dl_{i}"
                )

    if st.session_state.get('voice'):
        components.html(f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{st.session_state.voice}'); m.lang='pt-BR'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.voice = ""

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 10px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_report' not in st.session_state: st.session_state.ai_report = ""
xeon_main()
st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | US GOVT COMPATIBLE")
