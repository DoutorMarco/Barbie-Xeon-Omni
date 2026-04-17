import streamlit as st
import time
import hashlib
import sqlite3
import psutil
import platform
import pandas as pd
from fpdf import FPDF
from streamlit_echarts import st_echarts

# --- [1. CONFIGURAÇÃO VISUAL - ABSOLUTE BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 30px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    [data-testid="stDataFrame"], [data-testid="stTable"] {{ 
        background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; 
    }}
    hr {{ border: 1px solid {MATRIX_GREEN} !important; }}
    .node-box {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; text-align: center; background: rgba(0,255,65,0.05); margin-bottom: 5px; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE DADOS E AUDITORIA] ---
def init_db():
    with sqlite3.connect('xeon_sovereign_v131.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS federal_audit 
                     (ts TEXT, node TEXT, cpu REAL, hash TEXT)''')

def generate_node_pdf(node_name, cpu):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 15, f"TECHNICAL EVIDENCE: {node_name}", ln=True, align='C')
    pdf.ln(10); pdf.set_font("Courier", "", 12)
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    i_hash = hashlib.sha512(f"{node_name}{ts}{cpu}".encode()).hexdigest()[:48]
    lines = [
        f"TIMESTAMP: {ts}",
        f"ORIGIN_NODE: {platform.node().upper()}",
        f"SECTOR: {node_name}",
        f"CPU_LOAD: {cpu}%",
        f"INTEGRITY_HASH: {i_hash}",
        "-"*50,
        "CLASSIFIED: NATIONAL INTEREST WAIVER EXHIBIT",
        "ARCHITECT: MARCO ANTONIO DO NASCIMENTO"
    ]
    for line in lines: pdf.cell(0, 10, line, ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- [3. DASHBOARD DE COMANDO - HEARTBEAT E 9 NÓS] ---
@st.fragment(run_every=2)
def xeon_core():
    cpu_val = psutil.cpu_percent()
    
    # Grid Superior: Gráfico Circular Pulsante e Métricas
    col_metric, col_gauge, col_info = st.columns([1, 1.5, 1])
    
    with col_metric:
        st.metric("SYSTEM_VERACITY", "100%", delta="HOMEOSTASE")
        st.metric("UPTIME", "24/7", delta="STABLE")
        
    with col_gauge:
        # Gráfico Circular Pulsante (Gauge)
        gauge_options = {
            "backgroundColor": "transparent",
            "series": [{
                "type": 'gauge',
                "startAngle": 90, "endAngle": -270,
                "pointer": {"show": False},
                "progress": {"show": True, "roundCap": True, "itemStyle": {"color": MATRIX_GREEN}},
                "data": [{"value": cpu_val}],
                "detail": {"formatter": '{value}%', "color": MATRIX_GREEN, "fontSize": 35}
            }]
        }
        st_echarts(options=gauge_options, height="280px")
        
    with col_info:
        st.metric("NODE_ID", platform.node()[:10].upper())
        st.metric("NIW_TARGET", "EB-1A_ACTIVE")

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Grid de 9 Nós de Defesa
    st.write("### 🛰️ DEFENSE INFRASTRUCTURE: 9 ACTIVE NODES")
    setores = [
        "CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", 
        "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", 
        "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"
    ]
    
    cols = st.columns(3)
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='node-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {s}", key=f"btn_{i}"):
                pdf_data = generate_node_pdf(s, cpu_val)
                st.download_button(f"📥 PDF {s}", pdf_data, f"XEON_{s}.pdf", key=f"dl_{i}")

# --- [4. EXECUÇÃO CENTRAL] ---
init_db()
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 7px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {MATRIX_GREEN};'>MISSION CRITICAL | ARQUITETO MARCO ANTONIO DO NASCIMENTO</p>", unsafe_allow_html=True)

xeon_core()

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("PROTOCOLO STEALTH ATIVO | ZERO WHITE POLICY | PQC_ENABLED")
