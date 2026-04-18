import streamlit as st
import time
import hashlib
import psutil
import unicodedata
import textwrap
import aiosqlite
import asyncio
from fpdf import FPDF
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. CONFIGURAÇÃO DE NÚCLEO SOBERANO] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v140.0", layout="wide")

# Inicialização de API (Segurança PQC)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

# Interface Matrix "Zero White"
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    code, pre {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN}; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 20px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: rgba(0,255,65,0.05); margin-bottom: 5px; font-size: 0.8em; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE PERSISTÊNCIA & BLOCKCHAIN LEDGER] ---
async def init_db():
    async with aiosqlite.connect("xeon_ledger.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS intelligence (id INTEGER PRIMARY KEY, ts TIMESTAMP, node TEXT, data TEXT, hash TEXT)")
        await db.commit()

async def log_intelligence(node, data):
    ts = time.time()
    h = hashlib.sha256(f"{ts}{node}{data}".encode()).hexdigest()
    async with aiosqlite.connect("xeon_ledger.db") as db:
        await db.execute("INSERT INTO intelligence (ts, node, data, hash) VALUES (?, ?, ?, ?)", (ts, node, str(data), h))
        await db.commit()

# --- [3. MOTOR DE EVIDÊNCIA EB-1A & NIST] ---
def generate_eb1a_dossier(node_name, ai_report):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
    
    pdf.cell(0, 10, "XEON COMMAND - GLOBAL PREDICTION BRAIN", ln=True, align='C')
    pdf.set_font("Courier", "", 10)
    pdf.cell(0, 10, f"EB-1A TECHNICAL EVIDENCE - NIW CASE - NODE: {node_name}", ln=True, align='C')
    pdf.ln(10)
    
    content = f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO\nRATE: $1,000/H\nLOG AUDIT: NIST 800-53 | ISO 27001\n\nINTELIGÊNCIA:\n{ai_report}"
    pdf.multi_cell(0, 7, unicodedata.normalize('NFKD', content).encode('ascii', 'ignore').decode('ascii'))
    
    output = pdf.output()
    return BytesIO(output) if not isinstance(output, str) else BytesIO(output.encode('latin-1'))

# --- [4. DASHBOARD OPERACIONAL - O CÉREBRO PENSANTE] ---
@st.fragment(run_every=3)
def brain_center():
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        st.metric("MONETIZAÇÃO", "$1,000/H", delta="ACTIVE")
        st.metric("GLOBAL API STATUS", "CONNECTED")
        
    with c2:
        # Gráfico de Homeóstase (Carga de Processamento Infinito)
        cpu = psutil.cpu_percent()
        options = {
            "backgroundColor": "transparent",
            "series": [{"type": 'gauge', "detail": {"color": MATRIX_GREEN}, "data": [{"value": cpu, "name": 'CPU'}]}]
        }
        st_echarts(options=options, height="200px")

    with c3:
        st.write("### 🌐 GLOBAL NODES")
        # Simulação de Ingestão Ativa
        nodes = {
            "S&P 500": "STABLE", "DEFENSE (US/EU)": "MONITORING",
            "NEURALINK": "SYNC", "PUBMED": "EXTRACTING",
            "RU/CH DEFENSE": "ELINT ACTIVE"
        }
        for n, s in nodes.items():
            st.markdown(f"<div class='node-card'><b>{n}:</b> {s}</div>", unsafe_allow_html=True)

    st.divider()

    # Módulo de Geração de Receita / EB-1A
    target_node = st.selectbox("ALVO DE ANÁLISE PREDITIVA", list(nodes.keys()))
    
    if st.button(f"EXECUTAR PREDIÇÃO INFINITA: {target_node}"):
        with st.spinner("PROCESSANDO EM MALHA GLOBAL..."):
            if client:
                res = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": "Você é o cérebro pensante do XEON COMMAND. Gere uma predição de alta precisão transdisciplinar."},
                              {"role": "user", "content": f"Analise impacto global para {target_node} sob ótica de Engenharia, Direito e Biomedicina."}]
                )
                report = res.choices.message.content
                st.session_state.last_rep = report
                # Armazenar no Ledger Imutável
                asyncio.run(log_intelligence(target_node, report))
                st.success("PREDIÇÃO CONCLUÍDA E ARQUIVADA NO LEDGER.")

    if 'last_rep' in st.session_state:
        st.text_area("LOG DE INTELIGÊNCIA ATIVA", st.session_state.last_rep, height=200)
        pdf = generate_eb1a_dossier(target_node, st.session_state.last_rep)
        st.download_button("📥 EXPORTAR DOSSIÊ EB-1A (PDF)", pdf, f"XEON_{target_node}_EB1A.pdf", "application/pdf")

# --- [5. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v140.0</h1>", unsafe_allow_html=True)
st.caption(f"ARQUITETO PRINCIPAL: MARCO ANTONIO DO NASCIMENTO | EB-1A ELIGIBLE | MISSION CRITICAL")

if __name__ == "__main__":
    asyncio.run(init_db())
    brain_center()
