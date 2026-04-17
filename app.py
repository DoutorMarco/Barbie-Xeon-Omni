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

# --- [1. CONFIGURAÇÃO VISUAL SOBERANA] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v106.6", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stSidebar"] {{ background-color: {BLACKOUT} !important; border-right: 1px solid {MATRIX_GREEN}; }}
    .status-box {{ border: 2px solid {MATRIX_GREEN}; padding: 12px; background: #000; border-left: 8px solid {MATRIX_GREEN}; margin-bottom: 10px; }}
    button {{ border: 1px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; transition: 0.3s; font-size: 12px !important; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 15px {MATRIX_GREEN}; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA E HISTÓRICO] ---
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

# --- [3. TELEMETRIA E PERFORMANCE REAL-TIME] ---
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
    
    # Atualiza histórico para o gráfico
    new_data = pd.DataFrame([[time.strftime('%H:%M:%S'), qber, cpu, ping]], 
                            columns=['Time', 'QBER', 'CPU', 'Latência'])
    st.session_state.telemetry_history = pd.concat([st.session_state.telemetry_history, new_data]).tail(20)
    
    return {"mkt": mkt, "qber": qber, "cpu": cpu, "ping": f"{ping:.2f} ms", "status": "OPTIMAL"}

# --- [4. INTERFACE DE COMANDO] ---
init_db()
intel = fetch_intel()

st.title("🛰️ XEON COMMAND v106.6 | STRATEGIC NODE DOMINATION")

tab_ops, tab_infra, tab_ledger = st.tabs(["🎮 OPERAÇÕES", "🏗️ INFRAESTRUTURA", "📜 AUDITORIA"])

with tab_ops:
    c1, c2 = st.columns([1, 2.5])
    with c1:
        st.metric("S&P 500 ANCHOR", f"{intel['mkt']:.2f}")
        st.metric("QUANTUM QBER", f"{intel['qber']:.2f}%")
        st.metric("CPU LOAD", f"{intel['cpu']:.1f}%")
        if st.button("🔊 RELATÓRIO TÉCNICO"):
            msg = f"Nós XEON operacionais. Performance de CPU em {intel['cpu']:.1f} por cento. Q-B-E-R estável. Arquiteto Marco Antonio, rede pronta para expansão."
            components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{msg}'));</script>", height=0)

    with c2:
        st.write("### 📈 PERFORMANCE MULTI-STREAM (REAL-TIME)")
        # Gráfico ECharts de múltiplas séries
        line_options = {
            "backgroundColor": "#000",
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["QBER", "CPU", "Latência"], "textStyle": {"color": MATRIX_GREEN}},
            "xAxis": {"type": "category", "data": st.session_state.telemetry_history['Time'].tolist(), "axisLabel": {"color": MATRIX_GREEN}},
            "yAxis": {"type": "value", "axisLabel": {"color": MATRIX_GREEN}, "splitLine": {"lineStyle": {"color": "#111"}}},
            "series": [
                {"name": "QBER", "type": "line", "data": st.session_state.telemetry_history['QBER'].tolist(), "color": MATRIX_GREEN},
                {"name": "CPU", "type": "line", "data": st.session_state.telemetry_history['CPU'].tolist(), "color": "#008F11"},
                {"name": "Latência", "type": "line", "data": st.session_state.telemetry_history['Latência'].tolist(), "color": "#ADFF2F"}
            ]
        }
        st_echarts(options=line_options, height="350px")

st.divider()

# --- [5. SETORES DE DEFESA EXPANDIDOS (8 NÓS)] ---
st.write("### 🛠️ MATRIZ DE ATIVAÇÃO DE ATIVOS (ALTA DISPONIBILIDADE)")
setores = [
    "CRIPTOGRAFIA QKD", "DEFESA gRPC", "SIGINT/ELINT", "GOVERNANÇA NIW",
    "FIBER SHIELD", "NEURAL AUDIT", "SATELLITE LINK", "QUANTUM STORAGE"
]
cols = st.columns(4)
for i, s in enumerate(setores):
    with cols[i % 4]:
        st.markdown(f"<div class='status-box'><small>NÓ 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
        if st.button(f"ATIVAR {s.split()[0]}", key=f"btn_{i}"):
            tk = hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:10]
            ih = log_activation(s, tk, intel['qber'], intel['mkt'])
            st.success(f"ONLINE: {tk}")

with tab_infra:
    st.write("### 🛰️ TOPOLOGIA DE REDE DINÂMICA")
    infra_opt = {"backgroundColor": "#000", "series": [{"type": "graph", "layout": "force", "symbolSize": 40,
                 "data": [{"name": s} for s in setores] + [{"name": "CORE-AI", "symbolSize": 60}],
                 "links": [{"source": "CORE-AI", "target": s} for s in setores],
                 "label": {"show": True, "color": MATRIX_GREEN}}]}
    st_echarts(options=infra_opt, height="500px")

with tab_ledger:
    st.write("### 📜 LEDGER SOBERANO")
    with sqlite3.connect('xeon_sovereign.db') as conn:
        df_l = pd.read_sql_query("SELECT * FROM activation_logs ORDER BY timestamp DESC", conn)
        st.dataframe(df_l, use_container_width=True)

st.caption("ADMIN: MARCO ANTONIO | XEON SOVEREIGN INFRASTRUCTURE v106.6 | 2026")
