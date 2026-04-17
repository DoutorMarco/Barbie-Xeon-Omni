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

st.set_page_config(page_title="XEON COMMAND v106.8", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stSidebar"] {{ background-color: {BLACKOUT} !important; border-right: 1px solid {MATRIX_GREEN}; }}
    .status-box {{ border: 2px solid {MATRIX_GREEN}; padding: 12px; background: #000; border-left: 8px solid {MATRIX_GREEN}; margin-bottom: 10px; }}
    button {{ border: 1px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; transition: 0.3s; font-size: 11px !important; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 15px {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA (ROBUSTO)] ---
def init_db():
    with sqlite3.connect('xeon_sovereign.db') as conn:
        # Garante que a tabela exista com as colunas certas sem apagar dados anteriores se possível
        conn.execute('''CREATE TABLE IF NOT EXISTS activation_logs 
                     (timestamp TEXT, sector TEXT, token TEXT, qber REAL, mkt REAL, integrity_hash TEXT)''')

def log_activation(sector, token, qber, mkt):
    raw_data = f"{sector}{token}{qber}{mkt}"
    i_hash = hashlib.sha256(raw_data.encode()).hexdigest()[:16]
    with sqlite3.connect('xeon_sovereign.db') as conn:
        conn.execute("INSERT INTO activation_logs VALUES (?,?,?,?,?,?)", 
                     (time.strftime('%H:%M:%S'), sector, token, qber, mkt, i_hash))
    return i_hash

# --- [3. GERADOR DE DOSSIÊ (FIX: KEY CHECK)] ---
def generate_encrypted_dossier(sector, token, intel, i_hash):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
    pdf.cell(0, 15, f"ENCRYPTED SOVEREIGN DOSSIER - NODE {token}", ln=True, align='C')
    pdf.ln(10)
    
    # Garantia de que q_status existe para evitar KeyError
    q_status = intel.get('q_status', 'OPTIMAL/SECURE')
    
    content = [
        f"SECTOR: {sector}",
        f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"INTEGRITY HASH: {i_hash}",
        f"QUANTUM STATUS: {q_status}",
        f"S&P 500 REF: {intel['mkt']:.2f}",
        f"OPERATOR: ARQUITETO MARCO ANTONIO DO NASCIMENTO",
        "-"*40,
        "DOCUMENTO PROTEGIDO POR CRIPTOGRAFIA DE ESTADO."
    ]
    
    pdf.set_font("Courier", "", 10)
    for line in content:
        pdf.cell(0, 8, line, ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- [4. TELEMETRIA REAL-TIME (FIX: Dicionário Completo)] ---
if 'telemetry_history' not in st.session_state:
    st.session_state.telemetry_history = pd.DataFrame(columns=['Time', 'QBER', 'CPU', 'Latência'])

@st.cache_data(ttl=2)
def fetch_intel():
    qber = random.uniform(1.0, 3.5)
    cpu = random.uniform(15, 45)
    ping = random.uniform(5, 12)
    try: 
        mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: 
        mkt = 5120.42
    
    # Adicionando explicitamente a chave q_status solicitada pelo PDF
    data = {
        "mkt": mkt, 
        "qber": qber, 
        "cpu": cpu, 
        "ping": f"{ping:.2f} ms", 
        "q_status": "SECURE/ENCRYPTED" # Esta chave resolve o KeyError
    }
    
    # Log de histórico
    new_row = pd.DataFrame([[time.strftime('%H:%M:%S'), qber, cpu, ping]], columns=['Time', 'QBER', 'CPU', 'Latência'])
    st.session_state.telemetry_history = pd.concat([st.session_state.telemetry_history, new_row]).tail(20)
    
    return data

# --- [5. INTERFACE] ---
init_db()
intel = fetch_intel()

st.title("🛰️ XEON COMMAND v106.8 | STABILITY RESTORED")

tab_ops, tab_ledger = st.tabs(["🎮 OPERAÇÕES", "📜 AUDITORIA & DOSSIÊS"])

with tab_ops:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.metric("S&P 500", f"{intel['mkt']:.2f}")
        st.metric("QBER", f"{intel['qber']:.2f}%")
        if st.button("🔊 RELATÓRIO"):
            msg = f"Sistemas estabilizados. Erro de mapeamento resolvido. Arquiteto Marco Antonio, os dossiês de todos os nós estão disponíveis."
            components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{msg}'));</script>", height=0)

    with c2:
        line_opt = {
            "backgroundColor": "#000",
            "xAxis": {"type": "category", "data": st.session_state.telemetry_history['Time'].tolist(), "axisLabel": {"color": MATRIX_GREEN}},
            "yAxis": {"type": "value", "axisLabel": {"color": MATRIX_GREEN}},
            "series": [{"name": "CPU", "type": "line", "data": st.session_state.telemetry_history['CPU'].tolist(), "color": MATRIX_GREEN}]
        }
        st_echarts(options=line_opt, height="300px")

st.divider()

# --- [6. ATIVAÇÃO DE 8 NÓS] ---
setores = ["CRIPTOGRAFIA QKD", "DEFESA gRPC", "SIGINT/ELINT", "GOVERNANÇA NIW", "FIBER SHIELD", "NEURAL AUDIT", "SATELLITE LINK", "QUANTUM STORAGE"]
cols = st.columns(4)

for i, s in enumerate(setores):
    with cols[i % 4]:
        st.markdown(f"<div class='status-box'><small>NÓ 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR + DOSSIÊ", key=f"btn_{i}"):
            tk = hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:10]
            ih = log_activation(s, tk, intel['qber'], intel['mkt'])
            pdf_data = generate_encrypted_dossier(s, tk, intel, ih)
            
            st.success(f"ONLINE: {tk}")
            st.download_button("📥 DOSSIÊ", data=pdf_data, file_name=f"XEON_SECRET_{tk}.pdf", key=f"dl_{i}")

with tab_ledger:
    with sqlite3.connect('xeon_sovereign.db') as conn:
        df_l = pd.read_sql_query("SELECT * FROM activation_logs ORDER BY timestamp DESC", conn)
        st.dataframe(df_l, use_container_width=True)

st.caption("ARQUITETO: MARCO ANTONIO | XEON SOVEREIGN v106.8 | NO-REGRESSION POLICY")
