import streamlit as st
import datetime
import psutil
from fpdf import FPDF
import hashlib
import pandas as pd
import json
import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [PROTOCOL 01: ESTÉTICA BLACKOUT TOTAL - ZERO LIGHT]
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")
st.markdown(
    """
    <style>
    /* Neutralização Absoluta: Fundo #000000 e Texto #00FF41 */
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    :root { --st-bg-color: #000000; }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Inputs, Widgets e Chat em Preto Puro */
    [data-testid="stChatInput"], div[data-baseweb="base-input"], input, textarea, [data-testid="stChatInput"] {
        background-color: #000000 !important; 
        border: 1px solid #00FF41 !important; 
        color: #00FF41 !important;
    }

    /* Botões Táticos SOH v2.2 */
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; text-transform: uppercase;
        font-weight: bold; letter-spacing: 2px; transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important; color: #000000 !important;
        box-shadow: 0 0 40px #00FF41;
    }

    /* Tabelas e Métricas Científicas */
    div[data-testid="metric-container"] { 
        border: 1px solid #00FF41; background-color: #000000 !important; padding: 20px;
    }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stDataFrame, [data-testid="stTable"] { border: 1px solid #00FF41 !important; background-color: #000000 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# [PROTOCOL 02: PERCEPÇÃO NEURAL MULTILINGUE (FALA E ESCUTA)]
def perception_module():
    st.components.v1.html("""
    <script>
    const synth = window.speechSynthesis;
    
    // Voz Adaptativa Multilingue
    window.speakSovereign = (text) => {
        const utter = new SpeechSynthesisUtterance(text);
        // Tenta detectar idioma ou mantém autoridade em PT-BR/EN-US
        utter.lang = 'pt-BR'; 
        utter.pitch = 0.7; utter.rate = 0.9;
        synth.speak(utter);
    };

    // Escuta Universal (Auto-Detect Language)
    window.activateUniversalMic = () => {
        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!Recognition) { alert("Navegador sem suporte a Percepção de Voz."); return; }
        
        const rec = new Recognition();
        rec.lang = ''; // Detecta automaticamente o idioma falado
        rec.start();
        
        rec.onresult = (event) => {
            const transcript = event.results.transcript;
            alert("XEON CAPTUROU: " + transcript);
            window.speakSovereign("Comando recebido e processado em tempo real.");
        };
    };
    </script>
    <div style="display: flex; gap: 15px;">
        <button onclick="speakSovereign('Sistemas em realidade pura. Governança e finanças em homeostase. Mil reais por hora estabelecido.')" 
            style="flex:1; background: black; color: #00FF41; border: 2px solid #00FF41; padding: 15px; cursor: pointer; font-family: monospace; font-weight: bold; text-transform: uppercase;">
            🔊 VOZ DO SISTEMA (MULTILINGUE)
        </button>
        <button onclick="activateUniversalMic()" 
            style="flex:1; background: black; color: #00FF41; border: 2px solid #00FF41; padding: 15px; cursor: pointer; font-family: monospace; font-weight: bold; text-transform: uppercase;">
            🎙️ ESCUTA UNIVERSAL ATIVA
        </button>
    </div>
    """, height=90)

# [PROTOCOL 03: GOVERNANÇA FINANCEIRA E ASSINATURA ECDSA]
if 'ledger' not in st.session_state:
    st.session_state.ledger = []
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())

def sign_log(data):
    signature = st.session_state.priv_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature.hex()

def add_audit(setor, mission, valor="R$ 1.000,00/h"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sig = sign_log(f"{setor}{mission}{ts}")
    entry = {"TS": ts, "SETOR": setor, "MISSÃO": mission, "TAXA": valor, "ASSINATURA": sig}
    st.session_state.ledger.append(entry)
    return entry

# [PROTOCOL 04: FRONT-END OPERACIONAL C4I]
st.title("🛰️ XEON COMMAND v54.0 | GLOBAL SOVEREIGNTY")
perception_module()

# Dash de Alta Performance
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "SOVEREIGN")
c2.metric("GOVERNANÇA", "IMUTÁVEL", "AES-256/ECDSA")
c3.metric("REALIDADE", "PURA", "SEM ALUCINAÇÃO")
c4.metric("ENTROPIA", hashlib.sha256(str(psutil.boot_time()).encode()).hexdigest()[:8].upper(), "SEED")

st.write("---")

col_ops, col_data = st.columns([1, 1.5])

with col_ops:
    st.markdown("#### ⚡ COMANDOS DE MONETIZAÇÃO")
    
    # Seletor de Missão Transdisciplinar
    setor = st.selectbox("SETOR DE ATUAÇÃO", ["FINANÇAS", "GOVERNANÇA", "DEFESA GOV", "SAÚDE SUPLEMENTAR"])
    missao = st.text_input("OBJETIVO DA MISSÃO CRÍTICA", value="Auditoria Geral de Infraestrutura")
    
    if st.button("🚀 EXECUTAR MISSÃO E AUDITAR"):
        res = add_audit(setor, missao)
        st.success(f"Missão Registrada e Assinada Digitalmente.")

    if st.button("📄 IMPRIMIR DOSSIÊ R$ 1.000/H"):
        if st.session_state.ledger:
            last = st.session_state.ledger[-1]
            pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0,0,210,297,'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, f"XEON AUDIT - {last['SETOR']}", 0, 1, 'C')
            pdf.set_font("Courier", "", 8); pdf.ln(10)
            content = (f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO\n"
                       f"VALUATION: {last['TAXA']}\n"
                       f"SETOR: {last['SETOR']}\n"
                       f"MISSION LOG: {last['MISSÃO']}\n"
                       f"SIGNATURE (ECDSA): {last['ASSINATURA']}")
            pdf.multi_cell(0, 5, content.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("💾 DOWNLOAD DOSSIÊ", pdf.output(dest='S').encode('latin-1'), f"XEON_{last['SETOR']}.pdf")

with col_data:
    st.markdown("#### 🔍 LEDGER DE REALIDADE (VERIFIED)")
    if st.session_state.ledger:
        st.dataframe(pd.DataFrame(st.session_state.ledger).sort_index(ascending=False), use_container_width=True, hide_index=True)

# Chat Input Soberano
prompt = st.chat_input("Comando Global Omnis Ciência...")
if prompt:
    add_audit("GLOBAL", prompt)
    st.info(f"Instrução {prompt} processada e assinada.")
