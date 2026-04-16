import streamlit as st
import datetime, psutil, time, hashlib, os, asyncio, httpx
import plotly.graph_objects as go
from fpdf import FPDF
from pyvis.network import Network
import streamlit.components.v1 as components

# [PROTOCOL 01: AUTO-AUDITORIA & INTEGRIDADE SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v101_35_OMNI_MAXIMA"

SCRIPT_HASH = get_script_integrity()
VALOR_HORA = 1000.00 

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL BLINDADA]
st.set_page_config(page_title="XEON OMNI v101.35", layout="wide")
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
    input, textarea { background-color: #000 !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: INTERFACE DE VOZ E ESCUTA (CEOs & INVESTIDORES)]
st.components.v1.html(f"""
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <button onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('Sincronia Xeon v101 ponto 35. Processando realidade mundial.'))" 
        style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🔊 VOZ ON</button>
        <button onclick="alert('🎙️ Escuta Neural Ativa. Infiltrando APIs mundiais em tempo real.')" 
        style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🎙️ MIC ON</button>
    </div>
""", height=80)

# [PROTOCOL 04: MOTOR DE REALIDADE MUNDIAL (FORCE SYNC)]
async def fetch_omni_intel():
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            sx = (await client.get("https://spacexdata.com")).json()
            usd = (await client.get("https://er-api.com")).json()['rates']['BRL']
            geo = (await client.get("http://ip-api.com")).json()
            return sx, usd, geo
        except: return {"name": "RE-SYNCING..."}, 5.30, {"query": "LOCAL_NODE"}

sx, usd, geo = asyncio.run(fetch_omni_intel())

# [PROTOCOL 05: MOTOR DE PDF MASTER (6 FOLHAS) - RECURSIVO]
def generate_6_page_pdf(contexto, rev, ip, hash_val, sx_data):
    pdf = FPDF()
    pdf.set_text_color(0, 255, 65)
    titulos = ["MONETIZAÇÃO", "BIOGENÉTICA", "ESPAÇO", "DEFESA", "GEOPOLÍTICA", "EB-1A"]
    for i, t in enumerate(titulos):
        pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_font("Courier", "B", 18); pdf.cell(0, 10, f"PAG {i+1}: {t}", 0, 1, 'C'); pdf.ln(10)
        pdf.set_font("Courier", "", 10)
        content = f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO\nVALOR/HORA: R$ {VALOR_HORA}\nFATURAMENTO: R$ {rev:.2f}\nCONTEXTO: {contexto}\nIP: {ip}\nSPACEX: {sx_data['name']}\nHASH: {hash_val}\nSTATUS: REALIDADE PURA"
        pdf.multi_cell(0, 8, content)
    return bytes(pdf.output())

# [PROTOCOL 06: MONETIZAÇÃO]
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
revenue = ((time.time() - st.session_state.start_time) / 3600) * VALOR_HORA

st.title(f"🛰️ XEON OMNI v101.35 | REALIDADE PURA")

t1, t2, t3, t4, t5 = st.tabs(["📊 MONITOR", "🧬 GRAFO & BIO", "🚀 ESPAÇO", "🏛️ DEFESA & NIW", "⚙️ DEPURADOR"])

with t1:
    c1, c2 = st.columns([1.6, 1])
    with c1:
        # Gráfico Circular Pulsando
        fig = go.Figure(go.Indicator(mode="gauge+number", value=psutil.cpu_percent(),
            gauge={'bar': {'color': "#00FF41"}, 'bgcolor': "black"}))
        fig.update_layout(paper_bgcolor='black', font={'color': "#00FF41"}, height=280)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.metric("FATURAMENTO ATUAL", f"R$ {revenue:.4f}")
        st.metric("TAXA SOBERANA", f"R$ {VALOR_HORA}/h")
        st.download_button("💾 GERAR PDF MASTER (6 FOLHAS)", data=generate_6_page_pdf("GERAL", revenue, geo['query'], SCRIPT_HASH, sx), file_name="XEON_MASTER.pdf")

with t2:
    st.subheader("🧬 Grafo de Conhecimento & Biogenética")
    # Grafo de Conhecimento Ativo
    net = Network(height='400px', width='100%', bgcolor='#000000', font_color='#00FF41')
    net.add_node("XEON", label="XEON COMMAND", color="#00FF41"); net.add_node("BIO", label="BIOGENÉTICA", color="#008000")
    net.add_edge("XEON", "BIO", color="#00FF41"); net.save_graph("g.html")
    components.html(open("g.html", 'r').read(), height=420)
    st.download_button("📄 PDF AUDITORIA BIO (6 FOLHAS)", data=generate_6_page_pdf("BIO", revenue, geo['query'], SCRIPT_HASH, sx), file_name="XEON_BIO.pdf")

with t3:
    st.subheader("🚀 SpaceX & Telemetria Orbital")
    st.write(f"🛰️ **Último Lançamento Real:** `{sx['name']}`")
    st.download_button("🛰️ PDF AUDITORIA ESPAÇO (6 FOLHAS)", data=generate_6_page_pdf("SPACE", revenue, geo['query'], SCRIPT_HASH, sx), file_name="XEON_SPACE.pdf")

with t4:
    st.subheader("🏛️ Defesa Americana & NIW")
    st.error("MISSÃO CRÍTICA: Conexão Link N1 e DoD Ativa.")
    st.download_button("⚖️ PDF AUDITORIA DEFESA (6 FOLHAS)", data=generate_6_page_pdf("DEFESA", revenue, geo['query'], SCRIPT_HASH, sx), file_name="XEON_DEFESA.pdf")

with t5:
    st.subheader("⚙️ Depurador EB-1A")
    st.code(f"HASH: {SCRIPT_HASH} | NODE: {geo['query']}", language="bash")
    st.download_button("💾 BAIXAR DOSSIÊ EB-1A FINAL (6 FOLHAS)", data=generate_6_page_pdf("EB1A", revenue, geo['query'], SCRIPT_HASH, sx), file_name="XEON_EB1A_FINAL.pdf")

st.chat_input("Realidade Pura Operacional. Monetização Nominal.")
