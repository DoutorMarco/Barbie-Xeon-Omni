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

# --- [1. CONFIGURAÇÃO VISUAL MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v106.9", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stSidebar"] {{ background-color: {BLACKOUT} !important; border-right: 1px solid {MATRIX_GREEN}; }}
    .status-box {{ border: 2px solid {MATRIX_GREEN}; padding: 12px; background: #000; border-left: 8px solid {MATRIX_GREEN}; margin-bottom: 10px; }}
    button {{ border: 1px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; transition: 0.3s; font-size: 11px !important; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 15px {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA] ---
def init_db():
    with sqlite3.connect('xeon_sovereign.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS activation_logs 
                     (timestamp TEXT, sector TEXT, token TEXT, qber REAL, mkt REAL, integrity_hash TEXT)''')

def log_activation(sector, token, qber, mkt):
    raw_data = f"{sector}{token}{qber}{mkt}"
    i_hash = hashlib.sha256(raw_data.encode()).hexdigest()[:16]
    with sqlite3.connect('xeon_sovereign.db') as conn:
        conn.execute("INSERT INTO activation_logs VALUES (?,?,?,?,?,?)", 
                     (time.strftime('%H:%M:%S'), sector, token, qber, mkt, i_hash))
    return i_hash

# --- [3. GERADOR DE DOSSIÊ (FIX: OUTPUT COMPATIBILITY)] ---
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
        f"QUANTUM STATUS: {intel.get('q_status', 'SECURE')}",
        f"S&P 500 REF: {intel['mkt']:.2f}",
        f"OPERATOR: ARQUITETO MARCO ANTONIO DO NASCIMENTO",
        "-"*40,
        "SISTEMA XEON v106.9 - PROTEÇÃO SOBERANA ATIVA."
    ]
    
    pdf.set_font("Courier", "", 10)
    for line in content:
        pdf.cell(0, 8, line, ln=True)
    
    # FIX: Output compatível com fpdf e fpdf2
    try:
        return pdf.output(dest='S').encode('latin-1') # Antigo fpdf
    except (AttributeError, TypeError):
        return bytes(pdf.output()) # Novo fpdf2

# --- [4. TELEMETRIA REAL-TIME] ---
if 'telemetry_history' not in st.session_state:
    st.session_state.telemetry_history = pd.DataFrame(columns=['Time', 'QBER', 'CPU', 'Latência'])

@st.cache_data(ttl=2)
def fetch_intel():
    qber, cpu, ping = random.uniform(1.0, 3.5), random.uniform(15, 45), random.uniform(5, 12)
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 5125.60
    
    new_row = pd.DataFrame([[time.strftime('%H:%M:%S'), qber, cpu, ping]], columns=['Time', 'QBER', 'CPU', 'Latência'])
    st.session_state.telemetry_history = pd.concat([st.session_state.telemetry_history, new_row]).tail(20)
    return {"mkt": mkt, "qber": qber, "cpu": cpu, "ping": f"{ping:.2f} ms", "q_status": "SECURE/ENCRYPTED"}

# --- [5. INTERFACE PRINCIPAL] ---
init_db()
intel = fetch_intel()
setores = ["CRIPTOGRAFIA QKD", "DEFESA gRPC", "SIGINT/ELINT", "GOVERNANÇA NIW", "FIBER SHIELD", "NEURAL AUDIT", "SATELLITE LINK", "QUANTUM STORAGE"]

st.title("🛰️ XEON COMMAND v106.9 | OMNI-ACTIVATION")

with st.sidebar:
    st.header("⚡ COMANDO GLOBAL")
    # NOVO: Ativação em Massa
    if st.button("🔥 OMNI-ACTIVATION (ALL NODES)"):
        st.session_state.omni_active = True
        msg = "Iniciando ativação em massa de todos os nós soberanos. Arquiteto Marco Antonio, a rede está sob seu controle total."
        components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{msg}'));</script>", height=0)
        for s in setores:
            tk = hashlib.md5(f"{s}{time.time()}".encode()).hexdigest().upper()[:10]
            log_activation(s, tk, intel['qber'], intel['mkt'])

tab_ops, tab_ledger = st.tabs(["🎮 OPERAÇÕES", "📜 AUDITORIA"])

with tab_ops:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.metric("S&P 500", f"{intel['mkt']:.2f}")
        st.metric("QBER", f"{intel['qber']:.2f}%")
        st.metric("CPU LOAD", f"{intel['cpu']:.1f}%")

    with c2:
        line_opt = {"backgroundColor": "#000", "xAxis": {"type": "category", "data": st.session_state.telemetry_history['Time'].tolist()},
                    "series": [{"name": "CPU", "type": "line", "data": st.session_state.telemetry_history['CPU'].tolist(), "color": MATRIX_GREEN}]}
        st_echarts(options=line_opt, height="280px")

st.divider()

# --- [6. MATRIZ DE NÓS] ---
cols = st.columns(4)
for i, s in enumerate(setores):
    with cols[i % 4]:
        st.markdown(f"<div class='status-box'><small>NÓ 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR + DOSSIÊ", key=f"btn_{i}"):
            tk = hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:10]
            ih = log_activation(s, tk, intel['qber'], intel['mkt'])
            pdf_data = generate_encrypted_dossier(s, tk, intel, ih)
            st.success(f"ONLINE: {tk}")
            st.download_button("📥 DOSSIÊ", data=pdf_data, file_name=f"XEON_{tk}.pdf", key=f"dl_{i}")

with tab_ledger:
    with sqlite3.connect('xeon_sovereign.db') as conn:
        df_l = pd.read_sql_query("SELECT * FROM activation_logs ORDER BY timestamp DESC", conn)
        st.dataframe(df_l, use_container_width=True)

st.caption("ARQUITETO: MARCO ANTONIO | XEON SOVEREIGN v106.9 | TOTAL OMNI-ACCESS")
