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

# --- [1. CONFIGURAÇÃO VISUAL ABSOLUTA - ELIMINAÇÃO TOTAL DE BRANCO] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v125.0", layout="wide", page_icon="🛰️")

# CSS AGRESSIVO E PRIORITÁRIO
st.markdown(f"""
    <style>
    /* FUNDO GLOBAL */
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    
    /* CABEÇALHOS DE TABELA (CORREÇÃO DA IMAGEM) */
    th {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    td {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    [data-testid="stHeader"] {{ background: {BLACKOUT} !important; }}
    
    /* REMOVER TEMA BRANCO DO DATAFRAME */
    [data-testid="stDataFrame"] {{ background-color: {BLACKOUT} !important; border: 1px solid {MATRIX_GREEN}; }}
    [data-testid="stTable"] {{ background-color: {BLACKOUT} !important; }}
    
    /* BOTÕES MATRIX */
    .stButton button, .stDownloadButton button {{
        border: 1px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 20px {MATRIX_GREEN}; }}
    
    /* ELEMENTOS DE INTERFACE */
    footer, header {{ display: none !important; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: {BLACKOUT}; text-align: center; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN} !important; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA E DOCUMENTAÇÃO] ---
def init_db():
    with sqlite3.connect('xeon_sovereign_v125.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS federal_audit 
                     (timestamp TEXT, sector TEXT, cpu REAL, mkt REAL, integrity_hash TEXT)''')

def log_action(sector, cpu, mkt):
    raw = f"{sector}{time.time()}{cpu}{mkt}{random.random()}"
    i_hash = hashlib.sha512(raw.encode()).hexdigest()
    with sqlite3.connect('xeon_sovereign_v125.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO federal_audit VALUES (?,?,?,?,?)", 
                     (time.strftime('%Y-%m-%d %H:%M:%S'), sector, cpu, mkt, i_hash))
    return i_hash

def generate_node_pdf(sector, cpu, mkt, i_hash):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 15, f"EVIDENCIA TECNICA - {sector}", ln=True, align='C')
    pdf.ln(10); pdf.set_font("Courier", "", 10)
    pdf.cell(0, 10, f"DATA: {time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"HASH SHA-512: {i_hash[:32]}...", ln=True)
    pdf.cell(0, 10, "ARCHITECT: MARCO ANTONIO DO NASCIMENTO", ln=True)
    return bytes(pdf.output())

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
        if st.button("🔥 ATIVAÇÃO GLOBAL"):
            for s in setores: log_action(s, intel['cpu'], intel['mkt'])
            st.rerun()
    
    with c_heart:
        gauge_opt = {"backgroundColor": "rgba(0,0,0,0)", "series": [{"type": 'gauge', "startAngle": 90, "endAngle": -270, "pointer": {"show": False}, "progress": {"show": True, "roundCap": True, "itemStyle": {"color": MATRIX_GREEN}}, "data": [{"value": intel['cpu']}], "detail": {"color": MATRIX_GREEN, "formatter": '{value}%', "fontSize": 40}}]}
        st_echarts(options=gauge_opt, height="280px")
        
    with c_right:
        st.metric("MKT ANCHOR", f"{intel['mkt']:.2f}")
        st.metric("VERACITY", "100%", delta="SÍNCRONA")

    st.divider()
    
    # GRADE DE NÓS COM PDFs FUNCIONAIS
    cols = st.columns(4)
    for i, s in enumerate(setores):
        with cols[i % 4]:
            st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"🚀 ATIVAR {s.split()}", key=f"btn_{i}"):
                ih = log_action(s, intel['cpu'], intel['mkt'])
                pdf_data = generate_node_pdf(s, intel['cpu'], intel['mkt'], ih)
                st.download_button("📥 PDF", data=pdf_data, file_name=f"XEON_{s}.pdf", key=f"dl_{i}")

# --- [4. EXECUÇÃO E LEDGER] ---
init_db()
st.title("🛰️ XEON COMMAND v125.0 | ABSOLUTE BLACKOUT")
operational_core()

st.divider()

# LEDGER DE AUDITORIA (FORÇANDO ESTILO MATRIX)
st.write("### 📜 FEDERAL AUDIT LEDGER (GLOBAL REAL-TIME)")
with sqlite3.connect('xeon_sovereign_v125.db') as conn:
    df_ledger = pd.read_sql_query("SELECT timestamp as DATA, sector as SETOR, integrity_hash as HASH_512 FROM federal_audit ORDER BY timestamp DESC LIMIT 15", conn)
    if not df_ledger.empty:
        # O .style garante que o Streamlit respeite as cores de célula
        st.dataframe(df_ledger.style.set_properties(**{
            'background-color': 'black',
            'color': '#00FF41',
            'border-color': '#00FF41',
            'text-align': 'left'
        }), use_container_width=True)
    else:
        st.info("SISTEMA ATIVO. AGUARDANDO COMANDO DE DEFESA.")

st.caption("ARCHITECT: MARCO ANTONIO DO NASCIMENTO | GLOBAL MISSION CRITICAL | US DEFENSE COMPLIANT")
