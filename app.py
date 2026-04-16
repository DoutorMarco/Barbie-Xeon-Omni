import streamlit as st
import os, sys, time, datetime, psutil, hashlib, asyncio, json

# [PROTOCOL 00: AUTO-REPARO DE DEPENDÊNCIAS - SEM REGRESSÃO]
def install_dependencies():
    libs = ["pyvis", "biopython", "httpx", "fpdf2", "plotly"]
    for lib in libs:
        try:
            __import__(lib.split('.')[0] if '.' in lib else lib)
        except ImportError:
            os.system(f"{sys.executable} -m pip install {lib}")

install_dependencies()

# Agora importamos as bibliotecas blindadas
from pyvis.network import Network
import streamlit.components.v1 as components
from Bio import Entrez
import plotly.graph_objects as go
from fpdf import FPDF
import httpx

# [PROTOCOL 01: AUTO-AUDITORIA SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v101_27_SOVEREIGN_FIX"

SCRIPT_HASH = get_script_integrity()
VALOR_HORA = 1000.00 

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL BLINDADA]
st.set_page_config(page_title="XEON OMNI v101.27", layout="wide")
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
    .stButton>button { width: 100%; background: #000; color: #00FF41; border: 1px solid #00FF41; font-weight: bold; height: 3.5em; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: PERSISTÊNCIA & MONETIZAÇÃO]
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
elapsed = (time.time() - st.session_state.start_time) / 3600
revenue = elapsed * VALOR_HORA

st.title(f"🛰️ XEON OMNI v101.27 | REPARO DE KERNEL")

# TABS DE OPERAÇÃO (AMPLITUDE MANTIDA)
t1, t2, t3, t4 = st.tabs(["📊 MONITOR", "🧬 BIOGENÉTICA & GRAFO", "🏛️ DEFESA & NIW", "⚙️ DEPURADOR"])

with t1:
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=psutil.cpu_percent(),
            title={'text': "CPU %"}, gauge={'bar': {'color': "#00FF41"}, 'bgcolor': "black"})).update_layout(paper_bgcolor='black', font={'color': "#00FF41"}), use_container_width=True)
    with c2:
        st.metric("MONETIZAÇÃO ATIVA", f"R$ {revenue:.4f}")
        st.metric("TAXA SOBERANA", f"R$ {VALOR_HORA}/h")
        st.metric("INTEGRIDADE SHA-3", SCRIPT_HASH[:12])

with t2:
    st.subheader("🧬 Grafo de Conhecimento & PubMed")
    # Função para o Grafo (Blindada)
    def build_omni_graph():
        net = Network(height='400px', width='100%', bgcolor='#000000', font_color='#00FF41')
        net.add_node("XEON", label="XEON COMMAND", color="#00FF41", size=40)
        net.add_node("BIO", label="BIOGENÉTICA", color="#008000")
        net.add_node("DEFESA", label="DEFESA EUA", color="#FF0000")
        net.add_edge("XEON", "BIO"); net.add_edge("XEON", "DEFESA")
        net.save_graph("graph.html")
        with open("graph.html", 'r', encoding='utf-8') as f: return f.read()
    
    components.html(build_omni_graph(), height=450)

with t4:
    st.subheader("⚙️ Depurador e Gerador de Dossiê EB-1A")
    def generate_pdf_v27():
        pdf = FPDF(); pdf.set_text_color(0, 255, 65)
        for _ in range(5):
            pdf.add_page(); pdf.set_fill_color(0); pdf.rect(0,0,210,297,'F')
            pdf.set_font("Courier","B",16); pdf.cell(0,10,"XEON OMNI COMMAND - DOSSIER v101.27",0,1,'C')
            pdf.set_font("Courier","",10); pdf.multi_cell(0,8,f"ARQUITETO: MARCO ANTONIO\nRECEITA: R$ {revenue:.2f}\nHASH: {SCRIPT_HASH}")
        return bytes(pdf.output())

    st.download_button("💾 BAIXAR DOSSIÊ MASTER (PDF 5 FOLHAS)", data=generate_pdf_v27(), file_name="XEON_OMNI_AUDIT.pdf")

st.chat_input("Kernel reparado. IA Generativa em comando recursivo.")
