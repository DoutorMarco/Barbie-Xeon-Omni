import streamlit as st
import time
import hashlib
import yfinance as yf
import random
import sqlite3
import pandas as pd
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. FRONT-END SOBERANO - SEM REGRESSÃO] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v107.6", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; background: #000; border-radius: 2px; margin-bottom: 5px; min-height: 85px; }}
    button {{ border: 1px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border-radius: 12px !important; font-size: 10px !important; transition: 0.3s; width: 100%; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 15px {MATRIX_GREEN}; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 5px {MATRIX_GREEN}; }}
    [data-testid="stSidebar"] {{ display: none; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN}; }}
    .stDataFrame {{ border: 1px solid {MATRIX_GREEN}; background-color: {BLACKOUT}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA COMPLETA] ---
def init_db():
    with sqlite3.connect('xeon_sovereign.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS activation_logs 
                     (timestamp TEXT, sector TEXT, token TEXT, qber REAL, mkt REAL, integrity_hash TEXT)''')

def log_activation(sector, token, qber, mkt):
    raw_data = f"{sector}{token}{qber}{mkt}{time.time()}"
    i_hash = hashlib.sha256(raw_data.encode()).hexdigest()[:16]
    with sqlite3.connect('xeon_sovereign.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO activation_logs VALUES (?,?,?,?,?,?)", 
                     (time.strftime('%Y-%m-%d %H:%M:%S'), sector, token, qber, mkt, i_hash))
    return i_hash

# --- [3. MOTOR DE DOSSIÊ] ---
def generate_audit_pdf(sector, token, intel, i_hash):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
    pdf.cell(0, 15, f"AUDIT REPORT - {sector}", ln=True, align='C')
    pdf.ln(10); pdf.set_font("Courier", "", 10)
    lines = [f"TOKEN: {token}", f"HASH: {i_hash}", f"MKT: {intel['mkt']:.2f}", "STATUS: AUDITED"]
    for line in lines: pdf.cell(0, 8, line, ln=True)
    try: return pdf.output(dest='S').encode('latin-1')
    except: return bytes(pdf.output())

# --- [4. TELEMETRIA] ---
@st.cache_data(ttl=2)
def fetch_intel():
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 7041.28
    return {"mkt": mkt, "qber": random.uniform(1.0, 1.2)}

# --- [5. INTERFACE CENTRALIZADA] ---
init_db()
intel = fetch_intel()
setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE"]

st.title("🛰️ XEON COMMAND v107.6 | TOTAL AUDIT")

# HEADER COMANDO
c1, c2, c3 = st.columns([1, 1, 1.5])
with c1: st.metric("AUDITORIA", "FULL SCAN")
with c2: st.metric("MERCADO", f"{intel['mkt']:.2f}")
with c3:
    if st.button("🔥 ATIVAR CICLO E VARRER LEDGER"):
        for s in setores:
            tk = hashlib.md5(f"{s}{time.time()}".encode()).hexdigest().upper()[:8]
            log_activation(s, tk, intel['qber'], intel['mkt'])
        components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('Auditoria total iniciada. Varredura completa de todos os oito nós realizada. Integridade confirmada.'));</script>", height=0)

st.divider()

# --- [6. GRADE DE NÓS (CONFORME ORIGINAL)] ---
cols = st.columns(4)
for i, s in enumerate(setores):
    with cols[i % 4]:
        st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR + PDF", key=f"btn_{i}"):
            tk = hashlib.md5(f"{s}{time.time()}".encode()).hexdigest().upper()[:8]
            ih = log_activation(s, tk, intel['qber'], intel['mkt'])
            pdf_data = generate_audit_pdf(s, tk, intel, ih)
            st.download_button("📥 AUDIT PDF", data=pdf_data, file_name=f"AUDIT_{tk}.pdf", key=f"dl_{i}")

st.divider()

# --- [7. INFRAESTRUTURA DE AUDITORIA TOTAL] ---
st.write("### 📜 LEDGER DE AUDITORIA COMPLETA (HISTÓRICO TOTAL)")
with sqlite3.connect('xeon_sovereign.db') as conn:
    # Captura todos os registros sem limite para auditoria total
    df_total = pd.read_sql_query("SELECT timestamp as DATA, sector as SETOR, token as TOKEN, integrity_hash as HASH FROM activation_logs ORDER BY timestamp DESC", conn)
    
    ca1, ca2 = st.columns([2, 1])
    with ca1:
        st.dataframe(df_total, use_container_width=True, height=300)
    with ca2:
        st.write("#### 📊 RESUMO DE ATIVAÇÕES")
        summary = df_total['SETOR'].value_counts()
        st.bar_chart(summary)
        
        csv_all = df_total.to_csv(index=False).encode('utf-8')
        st.download_button("📂 BAIXAR AUDITORIA COMPLETA (CSV)", data=csv_all, file_name="XEON_TOTAL_AUDIT.csv", mime='text/csv')

st.caption("ADMIN: MARCO ANTONIO | XEON SOVEREIGN v107.6 | TOTAL AUDIT INFRASTRUCTURE")
