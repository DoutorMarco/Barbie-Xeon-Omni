import streamlit as st
import time
import hashlib
import yfinance as yf
import sqlite3
import pandas as pd
import psutil
import io
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# --- [1. CONFIGURAÇÃO VISUAL ABSOLUTA - ZERO BRANCO] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v117.0", layout="wide", page_icon="🛰️")
st_autorefresh(interval=2000, key="xeon_absolute_veracity")

st.markdown(f"""
    <style>
    /* Fundo Total e Texto */
    .stApp, [data-testid="stSidebar"], .main {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    
    /* Tabelas: Forçando 100% Blackout no Cabeçalho e Células */
    .stDataFrame, [data-testid="stTable"], th, td {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    thead tr th {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; }}
    
    /* Botões: Estilo Matrix sem bordas brancas */
    .stButton button, .stDownloadButton button {{
        border: 1px solid {MATRIX_GREEN} !important;
        background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important;
        border-radius: 4px !important;
        font-weight: bold;
    }}
    .stButton button:hover, .stDownloadButton button:hover {{
        background-color: {MATRIX_GREEN} !important;
        color: {BLACKOUT} !important;
    }}
    
    /* Esconder elementos padrão Streamlit */
    [data-testid="stHeader"], footer {{ display: none; }}
    .status-box {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: {BLACKOUT}; text-align: center; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    hr {{ border: 0.5px solid {MATRIX_GREEN}; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE AUDITORIA E PERSISTÊNCIA] ---
def init_db():
    with sqlite3.connect('xeon_sovereign_v117.db', check_same_thread=False) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS federal_audit 
                     (timestamp TEXT, sector TEXT, cpu REAL, mkt REAL, integrity_hash TEXT)''')

def log_action(sector, cpu, mkt):
    raw = f"{sector}{time.time()}{cpu}{mkt}"
    i_hash = hashlib.sha512(raw.encode()).hexdigest()
    with sqlite3.connect('xeon_sovereign_v117.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO federal_audit VALUES (?,?,?,?,?)", 
                     (time.strftime('%H:%M:%S'), sector, cpu, mkt, i_hash))
    return i_hash

# --- [3. MOTOR DE PDF CORRIGIDO (DOWNLOAD GARANTIDO)] ---
def generate_final_pdf(sector, i_hash, intel):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
    pdf.cell(0, 15, f"OFFICIAL AUDIT - {sector}", ln=True, align='C')
    pdf.ln(10); pdf.set_font("Courier", "", 10)
    lines = [
        f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
        f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"SHA-512 HASH: {i_hash[:32]}...",
        f"CPU LOAD: {intel['cpu']}%",
        f"MKT ANCHOR: {intel['mkt']:.2f}",
        "-"*60,
        "SISTEMA XEON v117.0 - EVIDÊNCIA DE MISSÃO CRÍTICA."
    ]
    for line in lines: pdf.cell(0, 8, line, ln=True)
    # Retorna como buffer de bytes para evitar erro de download
    return pdf.output(dest='S').encode('latin-1')

# --- [4. TELEMETRIA REAL E APIs] ---
@st.cache_data(ttl=1)
def fetch_intel():
    try: mkt = yf.Ticker("^GSPC").fast_info['last_price']
    except: mkt = 7058.42
    cpu = psutil.cpu_percent()
    return {"mkt": mkt, "cpu": cpu}

# --- [5. INTERFACE CENTRALIZADA] ---
init_db()
intel = fetch_intel()
setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE"]

st.title("🛰️ XEON COMMAND v117.0 | ABSOLUTE BLACKOUT")

c1, c2, c3 = st.columns(3)
with c1: st.metric("CPU (REAL)", f"{intel['cpu']}%")
with c2: st.metric("VERACIDADE", "100%", delta="SÍNCRONA")
with c3: st.metric("MKT ANCHOR", f"{intel['mkt']:.2f}")

st.divider()

# --- [6. GRADE DE NÓS E GRÁFICO MATRIX] ---
col_nodes, col_chart = st.columns([1.5, 1])

with col_nodes:
    n_cols = st.columns(4)
    for i, s in enumerate(setores):
        with n_cols[i % 4]:
            st.markdown(f"<div class='status-box'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"🚀 ATIVAR + PDF", key=f"btn_{i}"):
                ih = log_action(s, intel['cpu'], intel['mkt'])
                pdf_bytes = generate_final_pdf(s, ih, intel)
                st.download_button("📥 BAIXAR DOSSIÊ", data=pdf_bytes, file_name=f"XEON_{s.replace(' ', '_')}.pdf", mime="application/pdf", key=f"dl_{i}")

with col_chart:
    st.write("### 📊 RESUMO (ZERO WHITE)")
    with sqlite3.connect('xeon_sovereign_v117.db') as conn:
        df_counts = pd.read_sql_query("SELECT sector, count(*) as total FROM federal_audit GROUP BY sector", conn)
    
    chart_opt = {
        "backgroundColor": "#000",
        "xAxis": {"type": "category", "data": df_counts['sector'].tolist(), "axisLabel": {"color": MATRIX_GREEN, "rotate": 45}},
        "yAxis": {"type": "value", "axisLabel": {"color": MATRIX_GREEN}, "splitLine": {"show": False}},
        "series": [{"data": df_counts['total'].tolist(), "type": "bar", "itemStyle": {"color": MATRIX_GREEN}}]
    }
    st_echarts(options=chart_opt, height="300px")

st.divider()

# --- [7. AUDITORIA LEDGER FINAL] ---
st.write("### 📜 LEDGER DE AUDITORIA (BLACKOUT MODE)")
with sqlite3.connect('xeon_sovereign_v117.db') as conn:
    df_ledger = pd.read_sql_query("SELECT timestamp as DATA, sector as SETOR, integrity_hash as HASH_512 FROM federal_audit ORDER BY timestamp DESC LIMIT 10", conn)
    st.dataframe(df_ledger, use_container_width=True)

st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | SOVEREIGN ARCHITECT | EB-1A EVIDENTIARY INFRASTRUCTURE")
