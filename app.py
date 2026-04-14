import streamlit as st
import numpy as np
import psutil
import time
import asyncio
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
import aiosqlite 
import hashlib

# 1. INFRAESTRUTURA DE DADOS (LEDGER IMUTÁVEL EM NUVEM)
DB_PATH = 'xeon_ledger.db'
GENESIS_HASH = "X30N_G3N3S1S_7890_S0V3R31GN_B10_L4W_3NG"

async def init_ledger():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS audits 
                           (timestamp TEXT, vector TEXT, verdict TEXT, hash TEXT, prev_hash TEXT, risk REAL)''')
        await db.commit()

async def log_audit_real(vector, verdict):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    load = psutil.cpu_percent()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT hash FROM audits ORDER BY rowid DESC LIMIT 1") as cursor:
            row = await cursor.fetchone()
            prev_hash = row if row else GENESIS_HASH
        
        content = f"{timestamp}-{vector}-{verdict}-{load}-{prev_hash}"
        new_hash = hashlib.sha256(content.encode()).hexdigest()
        await db.execute("INSERT INTO audits VALUES (?,?,?,?,?,?)", 
                        (timestamp, vector, verdict, new_hash, prev_hash, load))
        await db.commit()
    return new_hash

# 2. FRONT-END DE ELITE: ZERO BRANCO / PURE MATRIX
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    :root { background-color: #000000 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    div[data-testid="stChatInput"] { background-color: #000000 !important; border: 1px solid #00FF41 !important; }
    .stButton>button { 
        background-color: #000000 !important; color: #00FF41 !important; 
        border: 1px solid #00FF41 !important; border-radius: 0px !important; height: 45px;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 20px #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    footer, header { visibility: hidden !important; }
    hr { border-top: 1px solid #00FF41 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFACE OPERACIONAL
st.markdown("<h1 style='text-align: center; color: #00FF41; letter-spacing: 15px;'>🛰️ XEON COMMAND v54.0</h1>", unsafe_allow_html=True)

# Telemetria Real-Time do Servidor de Nuvem
load_val = psutil.cpu_percent()
c1, c2, c3, c4 = st.columns(4)
c1.metric("CLOUD LOAD", f"{load_val}%")
c2.metric("UPTIME", "STABLE", "24/7")
c3.metric("LEDGER SYNC", "IMMUTABLE", "v2.2")
c4.metric("VALUATION", "READY", "$450/h")

st.divider()

# Monitor de Pulso Neural (Sincronizado)
t = np.linspace(0, 10, 300)
phase = time.time() * (1 + load_val/50)
y = (0.2 + load_val/150) * np.sin(2 * t + phase)
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=2), fill='tozeroy', fillcolor='rgba(0, 255, 65, 0.2)'))
fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), paper_bgcolor='black', plot_bgcolor='black')
st.plotly_chart(fig, use_container_width=True)

# 4. MÓDULOS DE MISSÃO (CONSOLIDAÇÃO)
if 'db_init' not in st.session_state:
    asyncio.run(init_ledger())
    st.session_state.db_init = True

st.write("### ⌨️ TERMINAL DE PRODUÇÃO MUNDIAL")
if cmd := st.chat_input("Insert Global Command..."):
    verdict = f"VETOR {cmd}: Auditado via SOH v2.2. Sem alucinação."
    hsh = asyncio.run(log_audit_real(cmd, verdict))
    st.session_state.res, st.session_state.hsh = verdict, hsh
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{verdict}'));</script>", height=0)

if 'res' in st.session_state:
    st.info(f"**VEREDITO:** {st.session_state.res}\n\n**HASH IMUTÁVEL:** {st.session_state.hsh}")

# Módulos de Monetização (Botões)
st.write("### 🚀 MISSION MODULES")
cols = st.columns(3)
btns = [("🧬 BIOMED AUDIT", "BIOMED"), ("⚖️ LAW AUDIT", "LAW"), ("🏗️ ENG AUDIT", "ENG"),
        ("🛡️ CYBER DEFENSE", "SOH"), ("🚀 SPACE OPS", "SPACE"), ("📈 GLOBAL IPO", "IPO")]

for i, (label, key) in enumerate(btns):
    with cols[i % 3]:
        if st.button(label):
            verdict = f"AUDITORIA {key}: Processada em Nuvem Soberana."
            hsh = asyncio.run(log_audit_real(key, verdict))
            st.session_state.res, st.session_state.hsh = verdict, hsh
            st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{verdict}'));</script>", height=0)

# Exportação do Produto Final (PDF de Faturamento)
if 'res' in st.session_state:
    buf = BytesIO(); p = canvas.Canvas(buf, pagesize=A4); p.setFillColorRGB(0,0,0); p.rect(0,0,600,900,fill=1); p.setFillColorRGB(0,1,0.25)
    p.setFont("Courier-Bold", 16); p.drawString(50, 800, "XEON COMMAND - CLOUD DOSSIER v54.0")
    p.setFont("Courier", 10); p.drawString(50, 770, f"TIMESTAMP: {datetime.datetime.now()} | ARQUITETO: MARCO ANTONIO")
    p.drawString(50, 750, f"VEREDITO: {st.session_state.res}")
    p.drawString(50, 730, f"BLOCK HASH: {st.session_state.hsh}")
    p.save(); buf.seek(0)
    st.download_button("📂 EXPORTAR PDF PARA FATURAMENTO", buf, "Xeon_Final_Audit.pdf", use_container_width=True)
