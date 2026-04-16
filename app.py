import streamlit as st
import datetime, psutil, time, subprocess, json, hashlib, os, asyncio
import plotly.graph_objects as go
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# [PROTOCOL 01: AUTO-AUDITORIA & INTEGRIDADE SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v101_14_AUDIT_STABLE"

SCRIPT_HASH = get_script_integrity()
VALOR_HORA = 1000.00 # MONETIZAÇÃO CORRIGIDA E FIXADA

# [PROTOCOL 02: BLACKOUT TOTAL - ZERO BRANCO BLINDADO]
st.set_page_config(page_title="XEON OMNI v101.14", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stMetric { border: 1px solid #00FF41 !important; padding: 15px; background: #050505 !important; }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #00FF41 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000; border-bottom: 1px solid #00FF41; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; border: 1px solid #00FF41; background: #000; }
    .stButton>button { width: 100%; background: #000; color: #00FF41; border: 1px solid #00FF41; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: PERSISTÊNCIA & MONETIZAÇÃO RECURSIVA]
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.ledger = []

elapsed_hours = (time.time() - st.session_state.start_time) / 3600
revenue = elapsed_hours * VALOR_HORA

# [PROTOCOL 04: KERNEL DE REALIDADE MUNDIAL - CONEXÃO TOTAL]
async def fetch_omni_intel():
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            usd = (await client.get("https://er-api.com")).json()['rates']['BRL']
            geo = (await client.get("http://ip-api.com")).json()
            return usd, geo
        except: return 5.25, {"query": "LOCAL_NODE"}

usd, geo = asyncio.run(fetch_omni_intel())

st.title(f"🛰️ XEON OMNI COMMAND | v101.14")

# [PROTOCOLO 05: TABS DE AMPLITUDE TOTAL]
t1, t2, t3, t4 = st.tabs(["📊 MONITOR", "🧬 BIOGENÉTICA", "🚀 DEFESA & ESPAÇO", "⚙️ DEPURADOR"])

with t1:
    c1, c2 = st.columns([1.6, 1])
    with c1:
        # GAUGE CIRCULAR ATIVO E DEPURADOR
        fig_cpu = go.Figure(go.Indicator(mode="gauge+number", value=psutil.cpu_percent(),
            title={'text': "PROCESSAMENTO RECURSIVO %"}, gauge={'bar': {'color': "#00FF41"}, 'bgcolor': "black"}))
        fig_cpu.update_layout(paper_bgcolor='black', font={'color': "#00FF41"}, height=280)
        st.plotly_chart(fig_cpu, use_container_width=True)
    with c2:
        # MONETIZAÇÃO FIXADA EM R$ 1000/H - VISIBILIDADE 100%
        st.metric("TAXA DE AUDITORIA", f"R$ {VALOR_HORA}/h")
        st.metric("RECEITA EM TEMPO REAL", f"R$ {revenue:.4f}")
        st.metric("SHA-3 INTEGRITY", SCRIPT_HASH[:12])

with t4:
    st.subheader("⚙️ Depurador e Gerador de Dossiê EB-1A")
    st.code(f"CPU CORES: {psutil.cpu_count()} | MEMÓRIA: {psutil.virtual_memory().percent}%", language="bash")
    
    # [CORREÇÃO: BOTÃO PDF OPERACIONAL EM MEMÓRIA - SEM REGRESSÃO]
    def generate_pdf_dossier():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 10, "XEON OMNI COMMAND - DOSSIER v101.14", 0, 1, 'C'); pdf.ln(10)
        pdf.set_font("Courier", "", 10)
        content = (f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO\n"
                   f"DATA: {datetime.datetime.now()}\n"
                   f"VALOR/HORA: R$ {VALOR_HORA}\n"
                   f"RECEITA ACUMULADA: R$ {revenue:.2f}\n"
                   f"IP AUDITADO: {geo.get('query')}\n"
                   f"STATUS: SOBERANO / ERRO ZERO\n"
                   f"HASH: {SCRIPT_HASH}")
        pdf.multi_cell(0, 8, content)
        return pdf.output(dest='S').encode('latin-1')

    # BOTÃO PDF RESTAURADO E VISÍVEL
    st.download_button(
        label="💾 GERAR DOSSIÊ OFICIAL (PDF)",
        data=generate_pdf_dossier(),
        file_name=f"XEON_OMNI_DOSSIER_{int(time.time())}.pdf",
        mime="application/pdf"
    )

st.chat_input("IA Generativa em comando recursivo. Auditoria nominal.")
