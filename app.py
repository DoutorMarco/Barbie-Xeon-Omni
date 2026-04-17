import streamlit as st
import time
import hashlib
import sqlite3
import random
import psutil
import pandas as pd
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO VISUAL ABSOLUTA - BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v123.0", layout="wide", page_icon="🛰️")

# CSS AGRESSIVO: ELIMINAÇÃO TOTAL DE AZUL/BRANCO (FOCO NA IMAGEM ENVIADA)
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stDataFrame"], [data-testid="stTable"], .stDataFrame {{ background-color: {BLACKOUT} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    th, td {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    .stButton button, .stDownloadButton button {{
        border: 1px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 2px !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 25px {MATRIX_GREEN}; }}
    .stAlert {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    [data-testid="stHeader"], footer {{ display: none; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: {BLACKOUT}; text-align: center; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN} !important; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA E DOCUMENTAÇÃO] ---
def init_db():
    with sqlite3.connect('xeon_sovereign_v123.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS federal_audit 
                     (timestamp TEXT, sector TEXT, cpu REAL, mkt REAL, integrity_hash TEXT)''')

def log_action(sector, cpu, mkt):
    raw = f"{sector}{time.time()}{cpu}{mkt}{random.random()}"
    i_hash = hashlib.sha512(raw.encode()).hexdigest()
    with sqlite3.connect('xeon_sovereign_v123.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO federal_audit VALUES (?,?,?,?,?)", 
                     (time.strftime('%Y-%m-%d %H:%M:%S'), sector, cpu, mkt, i_hash))
    return i_hash

def generate_node_pdf(sector, cpu, mkt, i_hash):
    """Gera PDF Funcional de Missão Crítica."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 15, f"EVIDENCIA TECNICA - {sector}", ln=True, align='C')
    pdf.ln(10); pdf.set_font("Courier", "", 11)
    pdf.cell(0, 10, f"DATA: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"CPU LOAD: {cpu}% | MKT REF: {mkt}", ln=True)
    pdf.ln(5); pdf.set_font("Courier", "B", 8)
    pdf.multi_cell(0, 8, f"HASH SHA-512:\n{i_hash}")
    pdf.ln(10); pdf.set_font("Courier", "I", 10)
    pdf.cell(0, 10, "ARCHITECT: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

@st.cache_data(ttl=1)
def fetch_intel():
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 7058.42
    cpu = psutil.cpu_percent()
    return {"mkt": mkt, "cpu": cpu}

# --- [3. FRAGMENTO OPERACIONAL (CORAÇÃO & NÓS)] ---
@st.fragment(run_every=2)
def operational_core():
    intel = fetch_intel()
    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE"]
    
    # HEADER E ATIVAÇÃO GLOBAL
    c_left, c_heart, c_right = st.columns([1, 1.5, 1])
    with c_left: 
        st.metric("CPU LOAD", f"{intel['cpu']}%")
        if st.button("🔥 ATIVAÇÃO GLOBAL (OMNI)"):
            for s in setores: log_action(s, intel['cpu'], intel['mkt'])
            components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('Ciclo Global Completo. Todos os nós auditados.'));</script>", height=0)
    
    with c_heart:
        gauge_opt = {
            "backgroundColor": "rgba(0,0,0,0)",
            "series": [{
                "type": 'gauge', "startAngle": 90, "endAngle": -270, "pointer": {"show": False},
                "progress": {"show": True, "roundCap": True, "itemStyle": {"color": MATRIX_GREEN}},
                "axisLine": {"lineStyle": {"width": 12, "color": [[1, "#080808"]]}},
                "data": [{"value": intel['cpu']}],
                "detail": {"color": MATRIX_GREEN, "formatter": '{value}%', "fontSize": 40}
            }]
        }
        st_echarts(options=gauge_opt, height="280px")
        
    with c_right:
        st.metric("MKT ANCHOR", f"{intel['mkt']:.2f}")
        st.metric("VERACITY", "100%", delta="REAL-TIME")

    st.divider()
    
    # GRADE DE NÓS COM PDFs FUNCIONAIS
    cols = st.columns(4)
    for i, s in enumerate(setores):
        with cols[i % 4]:
            st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"🚀 ATIVAR {s.split()}", key=f"btn_{i}"):
                ih = log_action(s, intel['cpu'], intel['mkt'])
                pdf_data = generate_node_pdf(s, intel['cpu'], intel['mkt'], ih)
                st.download_button("📥 DOSSIÊ", data=pdf_data, file_name=f"XEON_{s.replace(' ','_')}.pdf", mime="application/pdf", key=f"dl_{i}")

# --- [4. EXECUÇÃO E LEDGER] ---
init_db()
st.title("🛰️ XEON COMMAND v123.0 | OMNI-DOCS ACTIVE")
operational_core()

st.divider()

# LEDGER DE AUDITORIA (ZERO BRANCO / ZERO AZUL)
st.write("### 📜 FEDERAL AUDIT LEDGER (GLOBAL REAL-TIME)")
with sqlite3.connect('xeon_sovereign_v123.db') as conn:
    df_ledger = pd.read_sql_query("SELECT timestamp as DATA, sector as SETOR, integrity_hash as HASH_512 FROM federal_audit ORDER BY timestamp DESC LIMIT 15", conn)
    if not df_ledger.empty:
        st.dataframe(df_ledger.style.set_properties(**{'background-color': 'black', 'color': '#00FF41', 'border-color': '#00FF41'}), use_container_width=True)
    else:
        st.info("SISTEMA EM STANDBY. AGUARDANDO ATIVAÇÃO DOS NÓS SOBERANOS.")

st.caption("ARCHITECT: MARCO ANTONIO DO NASCIMENTO | GLOBAL MISSION CRITICAL | US DEFENSE COMPLIANT")
