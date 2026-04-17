import streamlit as st
import time
import hashlib
import yfinance as yf
import random
import sqlite3
import pandas as pd
import os
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. FRONT-END SOBERANO - MATRIX BLACKOUT] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v107.1", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stSidebar"] {{ background-color: {BLACKOUT} !important; border-right: 1px solid {MATRIX_GREEN}; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; background: #000; border-radius: 2px; margin-bottom: 5px; min-height: 85px; }}
    button {{ border: 1px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border-radius: 12px !important; font-size: 10px !important; transition: 0.3s; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 15px {MATRIX_GREEN}; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 5px {MATRIX_GREEN}; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA OMNI-LINK] ---
def init_db():
    with sqlite3.connect('xeon_sovereign.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS activation_logs 
                     (timestamp TEXT, sector TEXT, token TEXT, qber REAL, mkt REAL, integrity_hash TEXT)''')

def log_activation(sector, token, qber, mkt):
    raw_data = f"{sector}{token}{qber}{mkt}"
    i_hash = hashlib.sha256(raw_data.encode()).hexdigest()[:16]
    with sqlite3.connect('xeon_sovereign.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO activation_logs VALUES (?,?,?,?,?,?)", 
                     (time.strftime('%H:%M:%S'), sector, token, qber, mkt, i_hash))
    return i_hash

# --- [3. MOTOR DE PDF (ESTABILIDADE TOTAL)] ---
def generate_encrypted_dossier(sector, token, intel, i_hash):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
    pdf.cell(0, 15, f"ENCRYPTED SOVEREIGN DOSSIER - {sector}", ln=True, align='C')
    pdf.ln(10)
    
    content = [
        f"NODE TOKEN: {token}",
        f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"INTEGRITY HASH: {i_hash}",
        f"S&P 500 REF: {intel['mkt']:.2f}",
        f"OMNI-LINK STATUS: ACTIVE",
        f"OPERATOR: ARQUITETO MARCO ANTONIO DO NASCIMENTO",
        "-"*45,
        "SISTEMA XEON v107.1 - BLINDAGEM OMNI-LINK ATIVA."
    ]
    
    pdf.set_font("Courier", "", 10)
    for line in content:
        pdf.cell(0, 8, line, ln=True)
    
    # Compatibilidade binária forçada
    try:
        return pdf.output(dest='S').encode('latin-1')
    except:
        return bytes(pdf.output())

# --- [4. TELEMETRIA E INTELIGÊNCIA] ---
@st.cache_data(ttl=3)
def fetch_intel():
    qber = random.uniform(1.0, 3.2)
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 5128.90
    return {"mkt": mkt, "qber": qber, "status": "ACTIVE"}

# --- [5. INTERFACE DE COMANDO] ---
init_db()
intel = fetch_intel()
setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE"]

with st.sidebar:
    st.markdown("### 🔥 COMANDO GLOBAL")
    if st.button("🚀 OMNI-ACTIVATION (ALL NODES)"):
        for s in setores:
            tk = hashlib.md5(f"{s}{time.time()}".encode()).hexdigest().upper()[:8]
            log_activation(s, tk, intel['qber'], intel['mkt'])
        st.success("OMNI-LINK ESTABELECIDO")
        # Alerta de voz
        msg = "Ativação Omni Link realizada. Todos os oito nós da rede Xeon foram integrados com sucesso. Soberania técnica confirmada."
        components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{msg}'));</script>", height=0)

# Dashboard Superior
c1, c2, c3 = st.columns(3)
with c1: st.metric("OMNI-LINK STATUS", "ESTÁVEL")
with c2: st.metric("QBER MÉDIO", f"{intel['qber']:.2f}%")
with c3: st.metric("S&P 500", f"{intel['mkt']:.2f}")

st.divider()

# --- [6. MATRIZ DE NÓS (8 MÓDULOS)] ---
cols = st.columns(4)
for i, s in enumerate(setores):
    with cols[i % 4]:
        st.markdown(f"<div class='status-box'><small>NÓ 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR + DOSSIÊ", key=f"btn_{i}"):
            tk = hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:8]
            ih = log_activation(s, tk, intel['qber'], intel['mkt'])
            pdf_data = generate_encrypted_dossier(s, tk, intel, ih)
            st.download_button("📥 DOSSIÊ", data=pdf_data, file_name=f"XEON_{tk}.pdf", key=f"dl_{i}")

st.divider()
st.caption(f"ARQUITETO: MARCO ANTONIO | XEON SOVEREIGN v107.1 | OMNI-LINK ACTIVE")
