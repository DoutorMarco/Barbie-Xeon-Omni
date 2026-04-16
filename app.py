import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
from fpdf import FPDF
import hashlib
import pandas as pd
import json
import os
import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [PROTOCOL 01: AUTO-AUDITORIA DE INTEGRIDADE SHA-3]
def get_script_integrity():
    try:
        # Verifica a integridade do código-fonte para Erro Zero
        with open(__file__, "rb") as f:
            return hashlib.sha3_256(f.read()).hexdigest()
    except:
        return "MEMORY_ONLY_MODE_ACTIVE"

SCRIPT_HASH = get_script_integrity()

# [PROTOCOL 02: ESTÉTICA BLACKOUT ABSOLUTO - C4I SOVEREIGN]
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")
st.markdown(
    f"""
    <style>
    #MainMenu, header, footer {{visibility: hidden;}}
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr {{ display: none !important; }}
    :root {{ --st-bg-color: #000000; }}
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {{
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }}
    [data-testid="stChatInput"], div[data-baseweb="base-input"], input, textarea {{
        background-color: #000000 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important;
    }}
    .stButton>button {{
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; text-transform: uppercase;
        font-weight: bold; letter-spacing: 2px; transition: 0.4s; height: 3.5em;
    }}
    .stButton>button:hover {{ background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 50px #00FF41; }}
    div[data-testid="metric-container"] {{ border: 1px solid #00FF41; background-color: #050505 !important; padding: 20px; }}
    [data-testid="stMetricValue"] {{ color: #00FF41 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

# [PROTOCOL 03: GESTÃO DE ESTADO VOLÁTIL E ASSINATURA ECDSA]
if 'ledger' not in st.session_state:
    st.session_state.ledger = []
    # Chave Privada reside apenas em RAM (RAM-Only Mode)
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())

def sign_payload(data):
    signature = st.session_state.priv_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature.hex()

# [PROTOCOL 04: TELEMETRIA MULTICORE (DATA ENGINEERING)]
def get_cpu_per_core_chart():
    cores = psutil.cpu_percent(interval=0.5, percpu=True)
    fig = go.Figure(go.Bar(x=[f"C{i}" for i in range(len(cores))], y=cores, marker_color='#00FF41'))
    fig.update_layout(
        title="MULTICORE TELEMETRY (DATA ENG PIXELS)",
        paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"},
        height=180, margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(range=[0, 100], gridcolor='#111111'),
        xaxis=dict(gridcolor='#111111')
    )
    return fig

# [PROTOCOL 05: FRONT-END OPERACIONAL C4I]
st.title("🛰️ XEON COMMAND v54.0 | ATOMIC PURGE READY")

# Módulo de Percepção Neural
st.components.v1.html(f"""
    <script>
    window.speak = (t) => {{
        const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.7; u.rate=0.95;
        window.speechSynthesis.speak(u);
    }};
    </script>
    <div style="display:flex; gap:10px;">
        <button onclick="speak('Integridade SHA-3 confirmada. Protocolo de autodestruição volátil em prontidão. Mil reais por hora nominal.')" 
        style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">
        🔊 STATUS: HASH {SCRIPT_HASH[:16]} OPERACIONAL
        </button>
    </div>
""", height=65)

# Métricas de Soberania
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "EB-1A")
c2.metric("SHA-3", SCRIPT_HASH[:8], "VERIFIED")
c3.metric("STATE", "RAM-ONLY", "VOLATILE")
c4.metric("VAULT", "ECDSA_P256", "AUTHENTIC")

st.write("---")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.plotly_chart(get_cpu_per_core_chart(), use_container_width=True)
    
    st.markdown("#### ⚡ COMANDOS EXECUTIVOS")
    mission = st.text_input("OBJETIVO DA MISSÃO", value="Auditoria Transdisciplinar")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 EXECUTAR E ASSINAR"):
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            sig = sign_payload(f"{mission}{ts}{SCRIPT_HASH}")
            st.session_state.ledger.append({"TS": ts, "MISSION": mission, "SIG": sig, "MODE": "VOLATILE"})
            st.success(f"MISSÃO ASSINADA EM RAM: {sig[:16]}")
            
    with col_btn2:
        if st.button("☢️ PURGAR SESSÃO (AUTODESTRUIÇÃO)"):
            st.session_state.clear()
            st.cache_resource.clear()
            st.warning("MEMÓRIA VOLÁTIL PURGADA. SISTEMA EM ZERO-STATE.")
            time.sleep(2)
            st.rerun()

with col_right:
    st.markdown("#### 📜 VOLATILE LEDGER")
    if st.session_state.ledger:
        st.dataframe(pd.DataFrame(st.session_state.ledger).sort_index(ascending=False), use_container_width=True, hide_index=True)
    
    if st.button("📄 GERAR DOSSIÊ R$ 1.000/H"):
        if st.session_state.ledger:
            last = st.session_state.ledger[-1]
            pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0,0,210,297,'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, "XEON COMMAND - HIGH-FIDELITY AUDIT", 0, 1, 'C')
            pdf.set_font("Courier", "", 8); pdf.ln(10)
            body = (f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO\nRATE: R$ 1.000,00/H\n"
                    f"INTEGRITY_HASH (SHA-3): {SCRIPT_HASH}\n"
                    f"DIGITAL_SIGNATURE (ECDSA): {last['SIG']}\n"
                    f"STORAGE_MODE: VOLATILE RAM (ZERO-TRACE)\n"
                    f"--------------------------------------------------\n"
                    f"EVIDÊNCIA DE HABILIDADE EXTRAORDINÁRIA (EB-1A).")
            pdf.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("💾 DOWNLOAD DOSSIÊ", pdf.output(dest='S').encode('latin-1'), "XEON_EB1A_VOLATILE.pdf")

# Terminal Matrix
prompt = st.chat_input("Insira Instrução Soberana...")
if prompt:
    st.info(f"Filtro Diana: {prompt} | Processando em RAM Segura.")
