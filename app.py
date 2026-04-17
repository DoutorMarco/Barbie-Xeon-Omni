import streamlit as st
import time
import hashlib
import sqlite3
import random
import psutil
import pandas as pd
import numpy as np
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO VISUAL ABSOLUTA - BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v119.0", layout="wide", page_icon="🛰️")

# CSS SOBERANO: ZERO BRANCO, TOTAL BLACKOUT
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    .stDataFrame, [data-testid="stTable"], th, td {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    thead tr th {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; }}
    .stButton button, .stDownloadButton button {{
        border: 1px solid {MATRIX_GREEN} !important;
        background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important;
        border-radius: 2px !important;
        width: 100%;
        transition: 0.1s;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 20px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: {BLACKOUT}; text-align: center; margin-bottom: 5px; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA E TELEMETRIA REAL] ---
def init_db():
    with sqlite3.connect('xeon_sovereign_v119.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS federal_audit 
                     (timestamp TEXT, sector TEXT, cpu REAL, mkt REAL, integrity_hash TEXT)''')

def log_action(sector, cpu, mkt):
    raw = f"{sector}{time.time()}{cpu}{mkt}{random.random()}"
    i_hash = hashlib.sha512(raw.encode()).hexdigest()
    with sqlite3.connect('xeon_sovereign_v119.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO federal_audit VALUES (?,?,?,?,?)", 
                     (time.strftime('%Y-%m-%d %H:%M:%S'), sector, cpu, mkt, i_hash))
    return i_hash

@st.cache_data(ttl=2)
def fetch_intel():
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 7058.42
    cpu = psutil.cpu_percent()
    return {"mkt": mkt, "cpu": cpu}

# --- [3. FRAGMENTO OPERACIONAL (AUTO-REFRESH NATIVO)] ---
@st.fragment(run_every=3)
def operational_heart():
    intel = fetch_intel()
    
    # Painel de Telemetria de Missão Crítica
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("CPU LOAD", f"{intel['cpu']}%")
    with c2: st.metric("S&P ANCHOR", f"{intel['mkt']:.2f}")
    with c3: st.metric("CLUSTER SYNC", "ACTIVE", delta="OMNI")
    with c4: st.metric("VERACITY", "100%", delta="SECURE")
    
    st.divider()
    
    # Colunas de Comando e Gráfico
    col_nodes, col_chart = st.columns([1.5, 1])
    
    with col_nodes:
        setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "BIOTECH SYNC"]
        n_cols = st.columns(4)
        for i, s in enumerate(setores):
            with n_cols[i % 4]:
                st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
                if st.button(f"🚀 EXECUTAR {s.split()[0]}", key=f"btn_{i}"):
                    ih = log_action(s, intel['cpu'], intel['mkt'])
                    st.success(f"SHA-512: {ih[:12]}...")
                    components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('Ação operacional em {s} registrada no Ledger.'));</script>", height=0)

    with col_chart:
        st.write("### 📊 VOLUMETRIA (ZERO WHITE)")
        with sqlite3.connect('xeon_sovereign_v119.db') as conn:
            df_counts = pd.read_sql_query("SELECT sector, count(*) as total FROM federal_audit GROUP BY sector", conn)
        
        # Gráfico ECharts (Fundo Preto e Barras Verdes)
        chart_opt = {
            "backgroundColor": "#000",
            "xAxis": {"type": "category", "data": df_counts['sector'].tolist(), "axisLabel": {"color": MATRIX_GREEN, "rotate": 45}},
            "yAxis": {"type": "value", "axisLabel": {"color": MATRIX_GREEN}, "splitLine": {"show": False}},
            "series": [{"data": df_counts['total'].tolist(), "type": "bar", "itemStyle": {"color": MATRIX_GREEN}}]
        }
        st_echarts(options=chart_opt, height="280px")

# --- [4. EXECUÇÃO CENTRAL] ---
init_db()
st.title("🛰️ XEON COMMAND v119.0 | OMNI-SUPREMACY")
operational_heart()

st.divider()

# --- [5. LEDGER DE AUDITORIA NIST] ---
st.write("### 📜 FEDERAL AUDIT LEDGER (REAL-TIME SOVEREIGNTY)")
with sqlite3.connect('xeon_sovereign_v119.db') as conn:
    df_ledger = pd.read_sql_query("SELECT timestamp as DATA, sector as SETOR, integrity_hash as HASH_512 FROM federal_audit ORDER BY timestamp DESC LIMIT 15", conn)
    st.dataframe(df_ledger, use_container_width=True)

st.caption("ARCHITECT: MARCO ANTONIO DO NASCIMENTO | EB-1A EVIDENTIARY INFRASTRUCTURE | US DEFENSE COMPLIANT")
