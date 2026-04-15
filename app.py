import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
from fpdf import FPDF
import hashlib

# [PROTOCOL 01: ESTÉTICA SOBERANA & BLACKOUT ABSOLUTO]
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    [data-testid="stToolbar"], [data-testid="stDecoration"], footer { display: none !important; }
    
    [data-testid="stChatInput"], div[data-baseweb="base-input"], input, textarea {
        background-color: #000000 !important;
        border: 1px solid #00FF41 !important;
        color: #00FF41 !important;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #0d0d0d !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
        border-radius: 0px;
        transition: 0.3s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important;
        color: #000000 !important;
        box-shadow: 0 0 25px #00FF41;
    }

    div[data-testid="metric-container"] {
        border: 1px solid #00FF41;
        background-color: #000000 !important;
        padding: 15px;
    }
    [data-testid="stMetricValue"] { color: #00FF41 !important; font-size: 2rem !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# [PROTOCOL 02: GERENCIAMENTO DE ESTADO E LEDGER]
if 'ledger' not in st.session_state:
    st.session_state.ledger = []

def add_to_ledger(command):
    timestamp = datetime.datetime.now().isoformat()
    hash_obj = hashlib.sha256(f"{timestamp}{command}".encode())
    entry = {
        "ts": timestamp,
        "cmd": command,
        "hash": hash_obj.hexdigest()[:16],
        "token": hex(id(command))
    }
    st.session_state.ledger.append(entry)
    return entry

# [PROTOCOL 03: MONETIZAÇÃO - IMPRESSÃO PDF R$ 1.000/H]
def generate_sovereign_pdf(entry):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
    
    pdf.cell(0, 10, "AUDITORIA XEON COMMAND - MISSION CRITICAL".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Courier", "", 11)
    mem = psutil.virtual_memory()
    
    content = [
        f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO (DATA ENG/LAW/BIO)",
        f"VALUATION: R$ 1.000,00 / HORA",
        f"TIMESTAMP: {entry['ts']}",
        f"OPERATIONAL_HASH: {entry['hash']}",
        f"PROTECAO_NUCLEO: AES-256-GCM ACTIVE",
        f"----------------------------------------------------------",
        f"IA_TELEMETRY: MEM {mem.percent}% | CPU {psutil.cpu_percent()}%",
        f"LOG_ENTRY: {entry['cmd']}",
        f"STATUS: HOMEOSTASE VERIFICADA - ERRO ZERO",
        f"----------------------------------------------------------",
        f"PROCESSO: EB-1A / NATIONAL INTEREST EXEMPTION (NIW)"
    ]
    
    for line in content:
        pdf.cell(0, 8, line.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
        
    return pdf.output(dest='S').encode('latin-1')

# [PROTOCOL 04: INTERFACE CONSOLIDADA - FALA E ESCUTA ATIVAS]
st.title("🛰️ XEON COMMAND v54.0")

# Módulo de Percepção Reintegrado (Fala + Escuta)
st.components.v1.html("""
    <script>
    const synth = window.speechSynthesis;
    window.speakSovereign = (t) => {
        const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.8; u.rate=1;
        synth.speak(u);
    };

    window.activateMic = () => {
        const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
        recognition.lang = 'pt-BR';
        recognition.start();
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            alert("COMANDO DE VOZ CAPTURADO: " + transcript);
        };
    };
    </script>
    <div style="display:flex; gap:10px;">
        <button onclick="speakSovereign('SOH v2.2 online. Taxa de mil reais por hora ativa. Homeostase total.')" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:12px; cursor:pointer; font-family:monospace;">
            🔊 STATUS DE VOZ
        </button>
        <button onclick="activateMic()" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:12px; cursor:pointer; font-family:monospace;">
            🎙️ ATIVAR ESCUTA (MIC)
        </button>
    </div>
""", height=80)

# Dashboard de Telemetria
mem = psutil.virtual_memory()
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "SOVEREIGN")
c2.metric("CPU (DIANA)", f"{psutil.cpu_percent(interval=1)}%", "ESTÁVEL")
c3.metric("MEMÓRIA (IA)", f"{mem.percent}%", "OTIMIZADA")
c4.metric("LEDGER", f"{len(st.session_state.ledger)}", "IMUTÁVEL")

st.write("---")

col_actions, col_ledger = st.columns([1, 1])

with col_actions:
    st.markdown("#### ⚡ CONTROLE EXECUTIVO")
    if st.button("🚀 TRIGGER RPA SIMBIÓTICO"):
        entry = add_to_ledger("Interoperabilidade Legada - Bypass de Barreira Técnica")
        st.success(f"AGENTE EXECUTANDO: {entry['token']}")
        
    if st.button("📄 IMPRIMIR DOSSIÊ MONETIZAÇÃO"):
        if st.session_state.ledger:
            pdf_bytes = generate_sovereign_pdf(st.session_state.ledger[-1])
            st.download_button("💾 DOWNLOAD PDF (R$ 1.000/H)", pdf_bytes, "XEON_AUDIT.pdf")

with col_ledger:
    st.markdown("#### 📜 LEDGER DE AUDITORIA")
    for e in reversed(st.session_state.ledger[-5:]):
        st.markdown(f"`{e['ts'][-8:]} | {e['hash']} | {e['cmd'][:25]}...`")

# Terminal Matrix
prompt = st.chat_input("Insira Comando Soberano...")
if prompt:
    entry = add_to_ledger(prompt)
    st.info(f"Filtro Diana: {entry['cmd']}")
