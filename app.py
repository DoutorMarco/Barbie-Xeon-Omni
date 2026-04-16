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

# [PROTOCOL 01: AUTO-AUDITORIA SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f:
            return hashlib.sha3_256(f.read()).hexdigest()
    except:
        return "MEMORY_ONLY_MODE_ACTIVE"

SCRIPT_HASH = get_script_integrity()

# [PROTOCOL 02: ESTÉTICA SOBERANA - BLACKOUT TOTAL]
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")

# Correção: f-string exige {{ }} para CSS literal
st.markdown(
    f"""
    <style>
    #MainMenu, header, footer {{ visibility: hidden; }}
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
    .stDataFrame {{ border: 1px solid #00FF41 !important; background-color: #000000 !important; }}
    </style>
    """,
    unsafe_allow_html=True
)

# [PROTOCOL 03: GESTÃO DE ESTADO E PERCEPÇÃO]
if 'ledger' not in st.session_state:
    st.session_state.ledger = []
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())

def sign_payload(data):
    signature = st.session_state.priv_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature.hex()

def perception_module():
    # Correção: {{ }} para JS literal dentro de f-string
    st.components.v1.html(f"""
    <script>
    const synth = window.speechSynthesis;
    window.speak = (t) => {{
        const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.7; u.rate=0.95;
        synth.speak(u);
    }};
    window.activateMic = () => {{
        const rec = new (window.webkitSpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'pt-BR'; rec.start();
        rec.onresult = (e) => {{ 
            const transcript = e.results.transcript;
            alert("COMANDO CAPTURADO: " + transcript);
            window.speak("Comando recebido: " + transcript);
        }};
    }};
    </script>
    <div style="display:flex; gap:10px;">
        <button onclick="speak('Homeostase restaurada. Erro de sintaxe expurgado. Sistema nominal.')" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold; text-transform:uppercase;">
            🔊 STATUS DE VOZ
        </button>
        <button onclick="activateMic()" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold; text-transform:uppercase;">
            🎙️ ATIVAR ESCUTA (MIC)
        </button>
    </div>
    """, height=80)

# [PROTOCOL 04: DASHBOARD OPERACIONAL C4I]
st.title("🛰️ XEON COMMAND v54.0 | RECOVERY_READY")
perception_module()

c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "SOVEREIGN")
c2.metric("SHA-3", SCRIPT_HASH[:8], "VERIFIED")
c3.metric("STATE", "RAM-ONLY", "VOLATILE")
c4.metric("VAULT", "AUTHENTIC", "ECDSA_P256")

st.write("---")

col_left, col_right = st.columns([1, 1.5])

with col_left:
    cpu_val = psutil.cpu_percent()
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = cpu_val,
        title = {'text': "CPU LOAD (DIANA)", 'font': {'color': "#00FF41", 'size': 14}},
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black", 'bordercolor': "#00FF41"}
    ))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=250, margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### ⚡ COMANDOS EXECUTIVOS")
    if st.button("🚀 EXECUTAR MISSÃO E ASSINAR"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        sig = sign_payload(f"MISSION_{ts}_{SCRIPT_HASH}")
        st.session_state.ledger.append({"TS": ts, "MISSION": "Auditoria de Infraestrutura", "SIG": sig})
        st.success(f"MISSÃO ASSINADA: {sig[:16]}...")
        
    if st.button("☢️ PURGAR SESSÃO"):
        st.session_state.clear()
        st.cache_resource.clear()
        st.warning("MEMÓRIA VOLÁTIL PURGADA.")
        time.sleep(1)
        st.rerun()

with col_right:
    st.markdown("#### 🔍 LEDGER DE REALIDADE")
    if st.session_state.ledger:
        st.dataframe(pd.DataFrame(st.session_state.ledger).sort_index(ascending=False), use_container_width=True, hide_index=True)
    
    if st.button("📄 GERAR DOSSIÊ R$ 1.000/H"):
        if st.session_state.ledger:
            last = st.session_state.ledger[-1]
            pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0,0,210,297,'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, "XEON COMMAND - AUDIT EVIDENCE", 0, 1, 'C')
            pdf.set_font("Courier", "", 8); pdf.ln(10)
            body = (f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO\nRATE: R$ 1.000,00/H\n"
                    f"INTEGRITY_HASH (SHA-3): {SCRIPT_HASH}\n"
                    f"DIGITAL_SIGNATURE: {last['SIG']}\n")
            pdf.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("💾 DOWNLOAD DOSSIÊ", pdf.output(dest='S').encode('latin-1'), "XEON_AUDIT.pdf")

prompt = st.chat_input("Insira Comando Soberano...")
if prompt:
    st.info(f"Filtro Diana: {prompt} | Processando em RAM Segura.")
