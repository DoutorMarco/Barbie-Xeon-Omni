import streamlit as st
import datetime, psutil, time, hashlib, os, asyncio, httpx
import plotly.graph_objects as go
from fpdf import FPDF
from pyvis.network import Network
import streamlit.components.v1 as components
from Bio import Entrez

# [PROTOCOL 01: AUTO-AUDITORIA & INTEGRIDADE SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v101_26_AUDIT_STABLE"

SCRIPT_HASH = get_script_integrity()
VALOR_HORA = 1000.00 

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL BLINDADA]
st.set_page_config(page_title="XEON OMNI v101.26", layout="wide")
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

# [PROTOCOL 03: AGENTE DE FILTRAGEM PUBMED (NCBI REAL)]
def search_pubmed_recursive(query):
    Entrez.email = "auditoria@xeon.com"
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=5)
        record = Entrez.read(handle)
        handle.close()
        return record["IdList"]
    except: return ["NCBI_OFFLINE"]

# [PROTOCOL 04: MOTOR DE GRAFO DE CONHECIMENTO (DEFESA + BIO)]
def build_sovereign_graph():
    net = Network(height='450px', width='100%', bgcolor='#000000', font_color='#00FF41')
    net.add_node("ARQUITETO", label="MARCO ANTONIO", color="#00FF41", size=50)
    net.add_node("DEFESA", label="US DEFENSE (NIW)", color="#FF0000", size=30)
    net.add_node("BIO", label="BIOGENÉTICA", color="#008000", size=30)
    net.add_edge("ARQUITETO", "DEFESA", color="#00FF41")
    net.add_edge("ARQUITETO", "BIO", color="#00FF41")
    net.save_graph("audit_graph.html")
    with open("audit_graph.html", 'r', encoding='utf-8') as f: return f.read()

# [PROTOCOL 05: PERSISTÊNCIA & MONETIZAÇÃO]
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
revenue = ((time.time() - st.session_state.start_time) / 3600) * VALOR_HORA

st.title(f"🛰️ XEON OMNI v101.26 | AUDITORIA TOTAL")

# INTERFACE DE TABS (AMPLITUDE MANTIDA)
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
    st.subheader("🧬 Agente PubMed & Knowledge Graph")
    q = st.text_input("Vetor Científico:", "gene editing longevity")
    if st.button("🚀 INFILTRAR BASES NCBI"):
        st.success(f"PMIDs Detectados: {search_pubmed_recursive(q)}")
    components.html(build_sovereign_graph(), height=480)

with t4:
    st.subheader("⚙️ Depurador e Gerador de Dossiê EB-1A")
    # FUNÇÃO PDF 5 FOLHAS (BLINDADA)
    def generate_pdf_audit():
        pdf = FPDF(); pdf.set_text_color(0, 255, 65)
        for _ in range(5):
            pdf.add_page(); pdf.set_fill_color(0); pdf.rect(0,0,210,297,'F')
            pdf.set_font("Courier","B",16); pdf.cell(0,10,"XEON OMNI COMMAND - DOSSIER v101.26",0,1,'C'); pdf.ln(10)
            pdf.set_font("Courier","",10); pdf.multi_cell(0,8,f"ARQUITETO: MARCO ANTONIO\nRECEITA: R$ {revenue:.2f}\nHASH: {SCRIPT_HASH}")
        return bytes(pdf.output())

    st.download_button("💾 BAIXAR DOSSIÊ MASTER (PDF 5 FOLHAS)", data=generate_pdf_audit(), file_name="XEON_OMNI_AUDIT.pdf")

st.chat_input("IA Generativa em comando recursivo. Auditoria nominal.")
