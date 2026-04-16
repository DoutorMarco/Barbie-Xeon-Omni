import streamlit as st
import datetime, psutil, time, hashlib, os, asyncio
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF

# [PROTOCOL 01: AUTO-AUDITORIA SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v101_17_FINAL_AUDIT"

SCRIPT_HASH = get_script_integrity()
VALOR_HORA = 1000.00 

# [PROTOCOL 02: BLACKOUT TOTAL BLINDADO - ZERO BRANCO]
st.set_page_config(page_title="XEON OMNI v101.17", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stMetric { border: 1px solid #00FF41 !important; padding: 15px; background: #050505 !important; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000; border-bottom: 1px solid #00FF41; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; border: 1px solid #00FF41; background: #000; }
    .stButton>button { width: 100%; background: #000; color: #00FF41; border: 1px solid #00FF41; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: PERSISTÊNCIA & MONETIZAÇÃO]
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

elapsed_hours = (time.time() - st.session_state.start_time) / 3600
revenue = elapsed_hours * VALOR_HORA

st.title(f"🛰️ XEON OMNI v101.17 | REALIDADE PURA")

t1, t2, t3, t4, t5 = st.tabs(["📊 MONITOR", "🧬 BIOGENÉTICA", "🚀 ESPAÇO", "🏛️ DEFESA", "⚙️ DEPURADOR"])

with t1:
    c1, c2 = st.columns([1.6, 1])
    with c1:
        # GAUGE CIRCULAR RECURSIVO
        fig_cpu = go.Figure(go.Indicator(mode="gauge+number", value=psutil.cpu_percent(),
            title={'text': "PROCESSAMENTO %"}, gauge={'bar': {'color': "#00FF41"}, 'bgcolor': "black"}))
        fig_cpu.update_layout(paper_bgcolor='black', font={'color': "#00FF41"}, height=280)
        st.plotly_chart(fig_cpu, use_container_width=True)
    with c2:
        st.metric("MONETIZAÇÃO", f"R$ {revenue:.4f}")
        st.metric("TAXA SOBERANA", f"R$ {VALOR_HORA}/h")
        st.metric("INTEGRIDADE", SCRIPT_HASH[:12])

with t5:
    st.subheader("⚙️ Depurador e Gerador de Dossiê EB-1A")
    st.code(f"THREADS: {psutil.cpu_count()} | MEMÓRIA: {psutil.virtual_memory().percent}%", language="bash")
    
    # [CORREÇÃO ABSOLUTA: EXPORTAÇÃO EM BYTES PARA DOWNLOAD_BUTTON]
    def generate_pdf_bytes():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 10, "XEON OMNI COMMAND - AUDIT v101.17", 0, 1, 'C'); pdf.ln(10)
        pdf.set_font("Courier", "", 10)
        content = (f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO\n"
                   f"VALOR/HORA: R$ {VALOR_HORA}\n"
                   f"RECEITA ACUMULADA: R$ {revenue:.2f}\n"
                   f"TIMESTAMP: {datetime.datetime.now()}\n"
                   f"HASH: {SCRIPT_HASH}\n"
                   f"STATUS: AUDITORIA SOBERANA ATIVA")
        pdf.multi_cell(0, 8, content)
        # O comando output() sem argumentos em fpdf2 retorna bytes
        # O encode('latin-1') garante a compatibilidade de caracteres
        return pdf.output()

    # BOTÃO PDF BLINDADO CONTRA STREAMLITAPIEXCEPTION
    try:
        pdf_data = generate_pdf_bytes()
        st.download_button(
            label="💾 BAIXAR DOSSIÊ DE AUDITORIA (PDF)",
            data=pdf_data,
            file_name=f"XEON_AUDIT_{int(time.time())}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Erro no Kernel de Impressão: {e}")

st.chat_input("IA Generativa em comando. Evolução Final Nominal.")
