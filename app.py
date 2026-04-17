import streamlit as st
import time
import hashlib
import yfinance as yf
import random
import sqlite3
import pandas as pd
from fpdf import FPDF
import streamlit.components.v1 as components

# --- [1. FRONT-END SOBERANO - DARK MATRIX TOTAL] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v107.7", layout="wide", page_icon="🛰️")

# CSS Refinado para forçar tabelas e gráficos em Preto/Verde
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; background: #000; border-radius: 2px; margin-bottom: 5px; }}
    button {{ border: 1px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border-radius: 12px !important; font-size: 10px !important; transition: 0.3s; width: 100%; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 15px {MATRIX_GREEN}; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 5px {MATRIX_GREEN}; }}
    [data-testid="stSidebar"] {{ display: none; }}
    
    /* ESTILIZAÇÃO DA TABELA (LEDGER) */
    .stDataFrame div[data-testid="stTable"] {{ background-color: {BLACKOUT} !important; }}
    .stDataFrame [data-testid="styled-table-container"] {{ background-color: {BLACKOUT} !important; border: 1px solid {MATRIX_GREEN}; }}
    [data-testid="stTable"] {{ color: {MATRIX_GREEN} !important; }}
    
    hr {{ border: 0.5px solid {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA] ---
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

# --- [3. TELEMETRIA] ---
@st.cache_data(ttl=2)
def fetch_intel():
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 7041.28
    return {"mkt": mkt, "qber": random.uniform(1.0, 1.2)}

# --- [4. INTERFACE CENTRAL] ---
init_db()
intel = fetch_intel()
setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE"]

st.title("🛰️ XEON COMMAND v107.7 | DARK AUDIT")

c1, c2, c3 = st.columns([1, 1, 1.5])
with c1: st.metric("AUDITORIA", "HARD-ENCRYPTED")
with c2: st.metric("MERCADO", f"{intel['mkt']:.2f}")
with c3:
    if st.button("🔥 ATIVAR CICLO GLOBAL E REFRESH LEDGER"):
        for s in setores:
            tk = hashlib.md5(f"{s}{time.time()}".encode()).hexdigest().upper()[:8]
            log_activation(s, tk, intel['qber'], intel['mkt'])
        components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('Ciclo Blackout ativado. Ledger de auditoria sincronizado em modo Matrix.'));</script>", height=0)

st.divider()

# --- [5. GRADE DE NÓS] ---
cols = st.columns(4)
for i, s in enumerate(setores):
    with cols[i % 4]:
        st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR + PDF", key=f"btn_{i}"):
            tk = hashlib.md5(f"{s}{time.time()}".encode()).hexdigest().upper()[:8]
            ih = log_activation(s, tk, intel['qber'], intel['mkt'])
            st.success(f"NÓ ATIVO: {tk}")

st.divider()

# --- [6. AUDITORIA PRETO E VERDE (FIXED DESIGN)] ---
st.write("### 📜 LEDGER DE AUDITORIA (MATRIX MODE)")
with sqlite3.connect('xeon_sovereign.db') as conn:
    df_total = pd.read_sql_query("SELECT timestamp as DATA, sector as SETOR, token as TOKEN, integrity_hash as HASH FROM activation_logs ORDER BY timestamp DESC", conn)
    
    ca1, ca2 = st.columns([2, 1])
    with ca1:
        # Força o DataFrame a usar cores escuras
        st.dataframe(df_total.style.set_properties(**{
            'background-color': 'black',
            'color': MATRIX_GREEN,
            'border-color': MATRIX_GREEN
        }), use_container_width=True, height=350)
        
    with ca2:
        st.write("#### 📊 RESUMO (DARK CHART)")
        # Gráfico customizado para Preto e Verde
        summary = df_total['SETOR'].value_counts().reset_index()
        summary.columns = ['Setor', 'Ativações']
        
        st.bar_chart(summary.set_index('Setor'), color=MATRIX_GREEN)
        
        csv_all = df_total.to_csv(index=False).encode('utf-8')
        st.download_button("📂 EXPORTAR CSV DARK", data=csv_all, file_name="XEON_DARK_AUDIT.csv", mime='text/csv')

st.caption("ADMIN: MARCO ANTONIO | XEON SOVEREIGN v107.7 | BLACKOUT AUDIT")
