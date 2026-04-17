import streamlit as st
import time
import hashlib
import yfinance as yf
import sqlite3
import pandas as pd
import psutil
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO VISUAL ABSOLUTA - BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v118.0", layout="wide", page_icon="🛰️")

# CSS para garantir o visual 100% PRETO e VERDE (ZERO BRANCO)
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    .stDataFrame, [data-testid="stTable"], th, td {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    thead tr th {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; }}
    .stButton button, .stDownloadButton button {{
        border: 1px solid {MATRIX_GREEN} !important;
        background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important;
        border-radius: 4px !important;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; }}
    [data-testid="stHeader"], footer {{ display: none; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: {BLACKOUT}; text-align: center; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA E TELEMETRIA REAL] ---
def init_db():
    with sqlite3.connect('xeon_sovereign_v118.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS federal_audit 
                     (timestamp TEXT, sector TEXT, cpu REAL, mkt REAL, integrity_hash TEXT)''')

def log_action(sector, cpu, mkt):
    raw = f"{sector}{time.time()}{cpu}{mkt}"
    i_hash = hashlib.sha512(raw.encode()).hexdigest()
    with sqlite3.connect('xeon_sovereign_v118.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO federal_audit VALUES (?,?,?,?,?)", 
                     (time.strftime('%H:%M:%S'), sector, cpu, mkt, i_hash))
    return i_hash

@st.cache_data(ttl=2)
def fetch_intel():
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 7058.42
    cpu = psutil.cpu_percent()
    return {"mkt": mkt, "cpu": cpu}

# --- [3. FRAGMENTO DE ATUALIZAÇÃO AUTOMÁTICA (SUBSTITUI O MÓDULO FALTANTE)] ---
@st.fragment(run_every=2)
def auto_update_core():
    intel = fetch_intel()
    
    # Painel de Telemetria
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("CPU REAL", f"{intel['cpu']}%")
    with c2: st.metric("S&P ANCHOR", f"{intel['mkt']:.2f}")
    with c3: st.metric("VERACITY", "STABLE")
    
    st.divider()
    
    # Grade de Nós e Gráfico
    col_n, col_c = st.columns([1.5, 1])
    
    with col_n:
        setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE"]
        n_cols = st.columns(4)
        for i, s in enumerate(setores):
            with n_cols[i % 4]:
                st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
                if st.button(f"🚀 ATIVAR {s}", key=f"btn_{i}"):
                    ih = log_action(s, intel['cpu'], intel['mkt'])
                    st.success(f"SIG: {ih[:8]}")

    with col_c:
        st.write("### 📊 RESUMO DE NÓS")
        with sqlite3.connect('xeon_sovereign_v118.db') as conn:
            df_counts = pd.read_sql_query("SELECT sector, count(*) as total FROM federal_audit GROUP BY sector", conn)
        
        chart_opt = {
            "backgroundColor": "#000",
            "xAxis": {"type": "category", "data": df_counts['sector'].tolist(), "axisLabel": {"color": MATRIX_GREEN, "rotate": 45}},
            "yAxis": {"type": "value", "axisLabel": {"color": MATRIX_GREEN}, "splitLine": {"show": False}},
            "series": [{"data": df_counts['total'].tolist(), "type": "bar", "itemStyle": {"color": MATRIX_GREEN}}]
        }
        st_echarts(options=chart_opt, height="280px")

# --- [4. INTERFACE FINAL] ---
init_db()
st.title("🛰️ XEON COMMAND v118.0 | OMNI-STABLE")
auto_update_core()

st.divider()
st.write("### 📜 LEDGER DE AUDITORIA (BLACKOUT MODE)")
with sqlite3.connect('xeon_sovereign_v118.db') as conn:
    df_ledger = pd.read_sql_query("SELECT timestamp as DATA, sector as SETOR, integrity_hash as HASH_512 FROM federal_audit ORDER BY timestamp DESC LIMIT 10", conn)
    st.dataframe(df_ledger, use_container_width=True)

st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | SOVEREIGN ARCHITECT | EB-1A EVIDENTIARY INFRASTRUCTURE")
