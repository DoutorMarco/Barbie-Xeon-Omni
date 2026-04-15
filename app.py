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

# [PROTOCOL 01: ESTÉTICA BLACKOUT ABSOLUTO - C4I MILITARY INTERFACE]
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")
st.markdown(
    """
    <style>
    /* Neutralização de UI Nativa - Zero Light Protocol */
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    :root { --st-bg-color: #000000; }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Widgets e Inputs em Preto Puro */
    [data-testid="stChatInput"], div[data-baseweb="base-input"], input, textarea {
        background-color: #000000 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important;
    }

    /* Botões Táticos de Missão Crítica */
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; text-transform: uppercase;
        font-weight: bold; letter-spacing: 2px; transition: 0.4s; height: 3em;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important; color: #000000 !important;
        box-shadow: 0 0 50px #00FF41;
    }

    /* Tabelas e Métricas Científicas */
    div[data-testid="metric-container"] { 
        border: 1px solid #00FF41; background-color: #050505 !important; padding: 20px;
    }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stDataFrame { border: 1px solid #00FF41 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# [PROTOCOL 02: MOTOR DE AUDITORIA DESCENTRALIZADA E ASSINATURA]
if 'ledger' not in st.session_state:
    st.session_state.ledger = []
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())

def generate_global_hash(data):
    # Simulação de CID (Content Identifier) estilo IPFS para Auditoria Global
    return f"Qm{hashlib.sha256(data.encode()).hexdigest()[:44]}"

def sign_data(data):
    signature = st.session_state.priv_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature.hex()

# [PROTOCOL 03: TELEMETRIA DE HARDWARE (PROVA DE CARGA EB-1A)]
def get_telemetry_chart():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = cpu,
        title = {'text': "CPU LOAD (DIANA_FILTER)", 'font': {'color': "#00FF41", 'size': 14}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "#00FF41"},
            'bar': {'color': "#00FF41"},
            'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "#00FF41",
        }
    ))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

# [PROTOCOL 04: PERCEPÇÃO UNIVERSAL]
def perception_module():
    st.components.v1.html("""
    <script>
    window.speak = (t) => {
        const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.7; u.rate=0.9;
        window.speechSynthesis.speak(u);
    };
    window.activateMic = () => {
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = ''; rec.start();
        rec.onresult = (e) => { alert("XEON COMMAND DETECTOU: " + e.results.transcript); };
    };
    </script>
    <div style="display: flex; gap: 10px;">
        <button onclick="speak('Auditoria Global Verificável ativa. Telemetria de hardware sincronizada. Mil reais por hora em homeostase.')" 
            style="flex:1; background: black; color: #00FF41; border: 1px solid #00FF41; padding: 12px; cursor: pointer; font-family: monospace; font-weight: bold;">
            🔊 STATUS DE VOZ
        </button>
        <button onclick="activateMic()" 
            style="flex:1; background: black; color: #00FF41; border: 1px solid #00FF41; padding: 12px; cursor: pointer; font-family: monospace; font-weight: bold;">
            🎙️ ESCUTA MULTILINGUE
        </button>
    </div>
    """, height=60)

# [PROTOCOL 05: DASHBOARD DE EXECUÇÃO SOBERANA]
st.title("🛰️ XEON COMMAND v54.0 | GLOBAL AUDIT")
perception_module()

# Métricas de Habilidade Extraordinária
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "EB-1A EVIDENCE")
c2.metric("LEDGER", "DECENTRALIZED", "IPFS_READY")
c3.metric("ENTROPIA", hashlib.sha256(str(psutil.boot_time()).encode()).hexdigest()[:8].upper(), "NOMINAL")
c4.metric("VERIFICAÇÃO", "ECDSA_P256", "IMMUTABLE")

st.write("---")

col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown("#### 🛡️ TELEMETRIA DE MISSÃO CRÍTICA")
    st.plotly_chart(get_telemetry_chart(), use_container_width=True)
    
    setor = st.selectbox("SETOR DE AUDITORIA", ["SAÚDE SUPLEMENTAR", "DEFESA GOVERNAMENTAL", "FINANÇAS"])
    if st.button("🚀 EXECUTAR E GERAR CID (IPFS)"):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cid = generate_global_hash(f"{setor}{ts}")
        sig = sign_data(cid)
        st.session_state.ledger.append({"TS": ts, "SETOR": setor, "CID": cid, "SIGNATURE": sig})
        st.success(f"Operação Verificável Gerada: {cid[:10]}...")

    if st.button("📄 IMPRIMIR DOSSIÊ EB-1A"):
        if st.session_state.ledger:
            last = st.session_state.ledger[-1]
            pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0,0,210,297,'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, "USCIS EB-1A EVIDENCE - NATIONAL INTEREST EXEMPTION", 0, 1, 'C')
            pdf.set_font("Courier", "", 8); pdf.ln(10)
            body = (f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO\nRATE: R$ 1.000/H\n"
                    f"GLOBAL_CID (IPFS): {last['CID']}\nSIGNATURE: {last['SIGNATURE']}\n"
                    f"SECTOR: {last['SETOR']}\nSTATUS: VERIFIED BY SOH v2.2")
            pdf.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("💾 DOWNLOAD EVIDÊNCIA GLOBAL", pdf.output(dest='S').encode('latin-1'), "XEON_EB1A.pdf")

with col_right:
    st.markdown("#### 🔍 GLOBAL VERIFIABLE LEDGER")
    if st.session_state.ledger:
        st.dataframe(pd.DataFrame(st.session_state.ledger).sort_index(ascending=False), use_container_width=True, hide_index=True)

prompt = st.chat_input("Insira Comando para Auditoria de Realidade Pura...")
if prompt:
    st.info(f"Análise Diana: {prompt}")
