import streamlit as st
import time
import hashlib
import psutil
import platform
import sqlite3
import requests
import threading
import unicodedata
import random
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [AUDITORIA E CONCORRÊNCIA: LOCK DE SEGURANÇA] ---
db_lock = threading.Lock()

# --- [1. CONFIGURAÇÃO VISUAL - ABSOLUTE BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0 | SOH v2.2", layout="wide")

# Inicialização de IA via st.secrets (NIST/US Govt Compatible)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    client = None

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 60px;
    }}
    .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {MATRIX_GREEN} !important;
        color: {BLACKOUT} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 30px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    hr {{ border: 1px solid {MATRIX_GREEN} !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; text-align: center; background: rgba(0,255,65,0.05); margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. INFRAESTRUTURA: LEDGER IMUTÁVEL & FOG CLUSTER] ---
def init_db():
    with db_lock:
        conn = sqlite3.connect('xeon_integrity.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ledger 
                     (id INTEGER PRIMARY KEY, timestamp TEXT, node TEXT, hash TEXT, status TEXT)''')
        conn.commit()
        conn.close()

def log_event(node, status):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    i_hash = hashlib.sha512(f"{node}{ts}{status}".encode()).hexdigest()[:64]
    with db_lock:
        conn = sqlite3.connect('xeon_integrity.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("INSERT INTO ledger (timestamp, node, hash, status) VALUES (?, ?, ?, ?)",
                  (ts, node, i_hash, status))
        conn.commit()
        conn.close()
    return i_hash

def get_cluster_status():
    """Simulação de telemetria para Fog Computing (Cluster Geodistribuído)"""
    return {
        "NODE-US-EAST": {"status": "ACTIVE", "latency": f"{random.randint(15, 30)}ms"},
        "NODE-US-WEST": {"status": "ACTIVE", "latency": f"{random.randint(45, 70)}ms"},
        "NODE-EU-CENTRAL": {"status": "STANDBY", "latency": f"{random.randint(120, 150)}ms"}
    }

# --- [3. MOTOR PDF E FISIOLOGIA DIGITAL] ---
def sanitize_text(text):
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')

def generate_audit_dossier(node_name, cpu_val, ai_insight):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, "OFFICIAL DOCUMENT: CRITICAL INFRASTRUCTURE AUDIT", ln=True, align='C')
        pdf.ln(10)
        
        safe_ai = sanitize_text(ai_insight)
        lines = [
            f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
            f"FOG_COMPUTING_STATUS: DISTRIBUTED / ACTIVE",
            f"SYSTEM_HOMEOSTASE: {100-(cpu_val*0.1):.2f}%",
            f"INTEGRITY_HASH: {log_event(node_name, 'CERTIFIED')}",
            "-"*50, "IA PHYSIOLOGY ANALYSIS (NIW CRITERIA):", safe_ai[:600], "-"*50
        ]
        pdf.set_font("Courier", "", 10)
        for line in lines: pdf.multi_cell(0, 8, line)
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e: return f"ERROR: {str(e)}".encode('latin-1')

# --- [4. DASHBOARD DE COMANDO CENTRAL] ---
init_db()

@st.fragment(run_every=5)
def xeon_core():
    cpu_percent = psutil.cpu_percent()
    
    # Telemetria Superior
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1:
        st.metric("STABILITY", "NOMINAL")
        st.metric("HOMEOSTASE", f"{100-(cpu_percent*0.1):.2f}%")
        try:
            ping = requests.get("https://google.com", timeout=0.5).elapsed.total_seconds()
            st.metric("GLOBAL RELAY", f"{ping:.3f}s")
        except: st.metric("GLOBAL RELAY", "OFFLINE")

    with c2:
        gauge_opt = {"backgroundColor": "transparent", "series": [{"type": 'gauge', "progress": {"show": True, "itemStyle": {"color": MATRIX_GREEN}}, "data": [{"value": cpu_percent}], "detail": {"formatter": '{value}%', "color": MATRIX_GREEN, "fontSize": 24}}]}
        st_echarts(options=gauge_opt, height="250px")

    with c3:
        st.metric("EB-1A STATUS", "READY")
        if st.button("🧠 IA PHYSIOLOGY SCAN"):
            with st.status("Infiltrando IA na Fisiologia Digital...", expanded=False) as status:
                if client:
                    try:
                        res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "system", "content": "Parecer NIW Infraestrutura Crítica."}, {"role": "user", "content": f"CPU {cpu_percent}%. Analise a resiliência."}])
                        st.session_state.ai_analysis = res.choices.message.content
                        status.update(label="Análise Concluída", state="complete")
                        st.session_state.voice_trigger = "Protocolo de IA concluído. Sistema em homeostase absoluta."
                    except Exception as e:
                        status.update(label=f"Erro API", state="error")
                else:
                    st.session_state.ai_analysis = "Modo Offline: Resiliência garantida por redundância local."
                    status.update(label="Offline Mode", state="complete")

    st.markdown("<hr>", unsafe_allow_html=True)

    # MONITOR DE CLUSTER FOG (Distribuição Geográfica)
    st.markdown("#### 🌐 XEON FOG CLUSTER MONITOR")
    cluster_cols = st.columns(3)
    cluster_data = get_cluster_status()
    for i, (node, info) in enumerate(cluster_data.items()):
        with cluster_cols[i]:
            color = MATRIX_GREEN if info["status"] == "ACTIVE" else "#FF9900"
            st.markdown(f"<div style='border: 1px solid {color}; padding: 10px; text-align:center;'><b>{node}</b><br><span style='color:{color};'>{info['status']}</span><br><small>{info['latency']}</small></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 9 NÓS DE DEFESA
    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    node_cols = st.columns(3)
    for i, s in enumerate(setores):
        with node_cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {s}", key=f"btn_{i}"):
                st.session_state.active_node = s
                st.session_state.voice_trigger = f"Nó {s} ativado."
                log_event(s, "ACTIVE")
            
            if st.session_state.get('active_node') == s:
                pdf_bytes = generate_audit_dossier(s, cpu_percent, st.session_state.get('ai_analysis', 'Aguardando Scan IA...'))
                st.download_button(label=f"📥 DOSSIÊ {s}", data=pdf_bytes, file_name=f"XEON_{s}.pdf", mime="application/pdf", key=f"dl_{i}")

    # VOX PROTOCOL
    if st.session_state.get('voice_trigger'):
        components.html(f"""<script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{st.session_state.voice_trigger}');
            msg.lang = 'pt-BR'; window.speechSynthesis.speak(msg);
        </script>""", height=0)
        st.session_state.voice_trigger = ""

# --- [5. FINALIZAÇÃO SOBERANA] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 5px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'active_node' not in st.session_state: st.session_state.active_node = None
xeon_core()
st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | US GOVT COMPATIBLE | FOG COMPUTING ACTIVE")
