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

# --- [1. CONFIGURAÇÃO SOBERANA] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; text-align: center; margin-bottom: 5px; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF BLINDADO (CORREÇÃO DE ESPAÇO E UNICODE)] ---
def sanitize_text(text):
    if not text: return "N/A"
    # Remove caracteres que o FPDF não consegue renderizar no modo padrão
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')

def generate_dossier_fixed(node, cpu, ai_report):
    try:
        # Configuração de margens para evitar o erro de 'horizontal space'
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(left=15, top=15, right=15)
        pdf.add_page()
        
        # Fundo Preto
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(0, 0, 210, 297, 'F')
        
        # Cabeçalho
        pdf.set_text_color(0, 255, 65)
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, sanitize_text(f"EXHIBIT: {node}"), ln=True, align='C')
        pdf.ln(5)
        
        # Conteúdo Técnico
        pdf.set_font("Courier", "", 10)
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Sanitização rigorosa linha a linha
        report_safe = sanitize_text(ai_report)
        
        body = [
            f"TIMESTAMP: {ts}",
            f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
            f"SYSTEM_HOMEOSTASE: {100-(cpu*0.1):.2f}%",
            f"FEDERAL_HASH: {hashlib.md5(ts.encode()).hexdigest().upper()}",
            "-"*40,
            "GEN-AI ANALYSIS:",
            report_safe,
            "-"*40
        ]
        
        for line in body:
            # multi_cell com largura definida (0 = até a margem direita)
            pdf.multi_cell(w=0, h=7, txt=line, align='L')
            
        return pdf.output()
    except Exception as e:
        return f"Erro na geração do PDF: {str(e)}".encode('ascii')

# --- [3. DASHBOARD XEON] ---
@st.fragment(run_every=5)
def xeon_main():
    cpu_val = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1.5, 1])
    
    with c1:
        st.metric("STABILITY", "NOMINAL")
        try:
            val = yf.Ticker("USDBRL=X").history(period="1d")['Close'].iloc[-1]
            st.metric("USD/BRL", f"{val:.2f}")
        except: st.write("Market Offline")

    with c2:
        st_echarts(options={"backgroundColor": "transparent", "series": [{"type": 'gauge', "data": [{"value": cpu_val}], "detail": {"color": MATRIX_GREEN}}]}, height="200px")

    with c3:
        st.metric("NIW ELIGIBLE", "YES")
        if st.button("🧠 SCAN IA"):
            with st.status("Processando...", expanded=False) as s:
                if client:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Analise brevemente a estabilidade de {cpu_val}% para visto EB1A."}]
                    )
                    st.session_state.ai_report = res.choices.message.content
                    s.update(label="Concluído", state="complete")
                else:
                    st.session_state.ai_report = "IA Offline - Chave não encontrada."

    st.divider()

    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {s}", key=f"act_{i}"):
                st.session_state.active_node = s
            
            if st.session_state.get('active_node') == s:
                rep = st.session_state.get('ai_report', "Sem dados de IA.")
                pdf_data = generate_dossier_fixed(s, cpu_val, rep)
                st.download_button(label="📥 DOWNLOAD PDF", data=pdf_data, file_name=f"{s}.pdf", mime="application/pdf", key=f"dl_{i}")

# --- [4. FINALIZAÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_report' not in st.session_state: st.session_state.ai_report = ""
xeon_main()
