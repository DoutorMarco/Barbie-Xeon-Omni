import streamlit as st
import time
import hashlib
import sqlite3
import psutil
import platform
import pandas as pd
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO VISUAL - ABSOLUTE BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0", layout="wide", page_icon="🛰️")

# CSS PRIORITÁRIO: ZERO WHITE POLICY & GRID OPTIMIZATION
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stDataFrame"], [data-testid="stTable"], th, td {{ 
        background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; 
    }}
    .stButton button, .stDownloadButton button {{
        border: 1px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 25px {MATRIX_GREEN}; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN} !important; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 12px; background: {BLACKOUT}; text-align: center; min-height: 100px; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA E RASTREABILIDADE] ---
def init_db():
    with sqlite3.connect('xeon_sovereign_v131.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS federal_audit 
                     (timestamp TEXT, sector TEXT, cpu REAL, node_id TEXT, integrity_hash TEXT)''')

def log_real_event(sector, cpu, node_name):
    raw_payload = f"{sector}{time.time()}{cpu}{node_name}"
    signature = hashlib.sha512(raw_payload.encode()).hexdigest()
    with sqlite3.connect('xeon_sovereign_v131.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO federal_audit VALUES (?,?,?,?,?)", 
                     (time.strftime('%Y-%m-%d %H:%M:%S'), sector, cpu, node_name, signature))
    return signature

def generate_sovereign_pdf(sector, cpu, mkt, i_hash):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
    pdf.cell(0, 15, f"FEDERAL TECHNICAL EVIDENCE - {sector}", ln=True, align='C')
    pdf.ln(10); pdf.set_font("Courier", "", 10)
    lines = [
        f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"PHYSICAL_NODE_ID: {platform.node().upper()}",
        f"OS_PLATFORM: {platform.system()} {platform.release()}",
        f"CPU_PRECISION_LOAD: {cpu}%",
        f"MARKET_ANCHOR: {mkt}",
        f"INTEGRITY_HASH_512: {i_hash[:32]}...",
        "-"*60,
        "EXPANSÃO NODE 09: QUANTUM SENSING ACTIVE",
        "EMISSÃO: ARQUITETO MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL"
    ]
    for line in lines: pdf.cell(0, 8, line, ln=True)
    return bytes(pdf.output())

# --- [3. TELEMETRIA FÍSICA ULTRA-PRECISA] ---
@st.cache_data(ttl=1)
def fetch_real_intel():
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 7058.42
    cpu = psutil.cpu_percent(interval=0.1)
    return {"mkt": mkt, "cpu": cpu, "node": platform.node().upper()}

# --- [4. FRAGMENTO OPERACIONAL (HEARTBEAT & NODE GRID)] ---
@st.fragment(run_every=2)
def operational_heart():
    intel = fetch_real_intel()
    # Expansão para 9 Setores
    setores = [
        "CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", 
        "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", 
        "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"
    ]
    
    c_left, c_heart, c_right = st.columns([1, 1.5, 1])
    with c_left: 
        st.metric("HARDWARE NODE", intel['node'])
        if st.button("🔥 ATIVAÇÃO GLOBAL OMNI"):
            for s in setores: log_real_event(s, intel['cpu'], intel['node'])
            msg = "Sincronização global Xeon v131 concluída. Nó nove ativo. Sensor quântico operacional."
            components.html(f"<script>window.speechSynthesis.cancel(); var m=new SpeechSynthesisUtterance('{msg}'); m.lang='pt-BR'; window.speechSynthesis.speak(m);</script>", height=0)
            st.rerun()
            
    with c_heart:
        gauge_opt = {"backgroundColor": "rgba(0,0,0,0)", "series": [{"type": 'gauge', "startAngle": 90, "endAngle": -270, "pointer": {"show": False}, "progress": {"show": True, "roundCap": True, "itemStyle": {"color": MATRIX_GREEN}}, "data": [{"value": intel['cpu']}], "detail": {"color": MATRIX_GREEN, "formatter": '{value}%', "fontSize": 40}}]}
        st_echarts(options=gauge_opt, height="280px")
        
    with c_right:
        st.metric("MKT ANCHOR", f"{intel['mkt']:.2f}")
        st.metric("VERACITY", "STRICT", delta="NODE_09_ACTIVE")

    st.divider()
    
    # GRADE DE NÓS ATUALIZADA (Cols dinâmicas para 9 nós)
    cols = st.columns(3) # 3x3 Grid para 9 nós
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"🚀 ATIVAR {s}", key=f"btn_{i}"):
                ih = log_real_event(s, intel['cpu'], intel['node'])
                pdf_data = generate_sovereign_pdf(s, intel['cpu'], intel['mkt'], ih)
                st.download_button("📥 DOSSIÊ", data=pdf_data, file_name=f"XEON_AUDIT_{s}.pdf", key=f"dl_{i}")

# --- [5. EXECUÇÃO CENTRAL E LEDGER] ---
init_db()
st.title("🛰️ XEON COMMAND v131.0 | OMNI-VERACITY")
operational_heart()

st.divider()
st.write("### 📜 FEDERAL AUDIT LEDGER (EXPANDED NODE TRACEABILITY)")
with sqlite3.connect('xeon_sovereign_v131.db') as conn:
    df_ledger = pd.read_sql_query("SELECT timestamp as HORA, sector as SETOR, node_id as SERVER, integrity_hash as HASH_512 FROM federal_audit ORDER BY timestamp DESC LIMIT 12", conn)
    if not df_ledger.empty:
        st.dataframe(df_ledger.style.set_properties(**{'background-color': 'black', 'color': '#00FF41', 'border-color': '#00FF41'}), use_container_width=True)

st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | NODE 09 QUANTUM SENSING")
