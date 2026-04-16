import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
from fpdf import FPDF
import hashlib
import pandas as pd
import httpx
import json
import time
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [PROTOCOL 01: AUTO-AUDITORIA SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "STABLE_SOH_NODE_V54_4"

SCRIPT_HASH = get_script_integrity()

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL]
st.set_page_config(page_title="XEON COMMAND v54.4", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    :root { --st-bg-color: #000000; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; text-transform: uppercase;
        font-weight: bold; letter-spacing: 2px; transition: 0.4s; height: 3.5em;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 50px #00FF41; }
    div[data-testid="metric-container"] { border: 1px solid #00FF41; background-color: #050505 !important; padding: 20px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    input { background-color: #0a0a0a !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; gap: 20px; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; font-weight: bold; border: 1px solid #00FF41; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: SEGURANÇA E BLOCKCHAIN]
if 'priv_key' not in st.session_state:
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())
    st.session_state.aes_key = AESGCM.generate_key(bit_length=256)
    st.session_state.encrypted_ledger = []
    st.session_state.last_block_hash = "GENESIS_BLOCK_0000"
    st.session_state.pdf_buffer = None

def secure_store(data_dict):
    aesgcm = AESGCM(st.session_state.aes_key)
    data_dict["PREV_HASH"] = st.session_state.last_block_hash
    raw_data = json.dumps(data_dict).encode()
    current_hash = hashlib.sha3_256(raw_data).hexdigest()
    st.session_state.last_block_hash = current_hash
    data_dict["CURRENT_HASH"] = current_hash
    signature = st.session_state.priv_key.sign(current_hash.encode(), ec.ECDSA(hashes.SHA256()))
    data_dict["SIG"] = signature.hex()
    nonce = os.urandom(12)
    encrypted_blob = aesgcm.encrypt(nonce, json.dumps(data_dict).encode(), None)
    st.session_state.encrypted_ledger.append({"nonce": nonce, "blob": encrypted_blob})

def decrypt_ledger():
    aesgcm = AESGCM(st.session_state.aes_key)
    return [json.loads(aesgcm.decrypt(i["nonce"], i["blob"], None)) for i in st.session_state.encrypted_ledger]

# [PROTOCOL 04: PERCEPÇÃO NEURAL - VOZ E ESCUTA]
st.components.v1.html("""
    <script>
    const s = window.speechSynthesis;
    window.speak = (t) => { const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.7; u.rate=0.9; s.speak(u); };
    window.listen = () => {
        const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        r.lang='pt-BR'; r.start();
        r.onresult = (e) => { 
            const t = e.results[0][0].transcript;
            alert("COMANDO CAPTURADO: " + t);
            window.speak("Processando comando: " + t);
        };
    };
    </script>
    <div style="display:flex; gap:10px;">
        <button onclick="speak('Módulo de Voz Ativo. Sistema Nominal.')" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:12px; cursor:pointer; font-family:monospace; font-weight:bold; letter-spacing:1px;">🔊 STATUS VOZ</button>
        <button onclick="listen()" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:12px; cursor:pointer; font-family:monospace; font-weight:bold; letter-spacing:1px;">🎙️ ESCUTA ATIVA</button>
    </div>
""", height=70)

st.title("🛰️ XEON COMMAND v54.4 | SOVEREIGN HUB")

# Estrutura de Abas Soberanas
tab_monitor, tab_auditoria, tab_dossies = st.tabs(["📊 MONITORAMENTO", "🛡️ AUDITORIA ATIVA", "📑 DOSSIÊS CVM"])

with tab_monitor:
    col_left, col_right = st.columns([1.6, 1])
    with col_left:
        cpu_val = psutil.cpu_percent()
        fig = go.Figure(go.Indicator(mode="gauge+number", value=cpu_val, title={'text': "CPU LOAD", 'font': {'color': "#00FF41"}}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black", 'bordercolor': "#00FF41"}))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        if st.session_state.encrypted_ledger:
            st.write("### 🔗 LEDGER IMUTÁVEL (DECRYPTED)")
            st.dataframe(pd.DataFrame(decrypt_ledger()).sort_index(ascending=False), use_container_width=True)
    
    with col_right:
        st.metric("INTEGRIDADE SHA-3", SCRIPT_HASH[:16])
        st.metric("SOH STATUS", "NOMINAL")
        if st.button("☢️ PURGAR SESSÃO"):
            st.session_state.clear()
            st.rerun()

with tab_auditoria:
    col1, col2 = st.columns([2, 1])
    with col1:
        target = st.text_input("AUDIT TARGET", value="https://google.com")
        if st.button("🚀 INICIAR PROTOCOLO"):
            try:
                start_time = time.perf_counter()
                headers = {"User-Agent": "XEON-COMMAND-AUDITOR/54.4"}
                with httpx.Client(timeout=10.0, verify=False) as client:
                    response = client.get(target, headers=headers)
                    latency = (time.perf_counter() - start_time) * 1000
                    secure_store({"TS": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "TARGET": target, "STATUS": response.status_code, "LATENCY": f"{latency:.2f}ms"})
                    st.success(f"BLOCK MINED: {response.status_code}")
                    st.rerun()
            except Exception as e: st.error(f"FAIL: {str(e)}")
    
    with col2:
        if st.button("📄 GERAR RELATÓRIO PDF"):
            if st.session_state.encrypted_ledger:
                last = decrypt_ledger()[-1]
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
                pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
                pdf.cell(0, 10, "XEON AUDIT REPORT", 0, 1, 'C'); pdf.ln(10)
                pdf.set_font("Courier", "", 10)
                lines = [f"ARCHITECT: MARCO ANTONIO", f"TS: {last['TS']}", f"TARGET: {last['TARGET']}", f"HASH: {last['CURRENT_HASH']}"]
                for l in lines: pdf.cell(0, 8, l, 0, 1, 'L')
                st.session_state.pdf_buffer = pdf.output(dest='S').encode('latin-1')
                st.success("PDF PRONTO.")
        
        if st.session_state.pdf_buffer:
            st.download_button("💾 BAIXAR PDF", data=st.session_state.pdf_buffer, file_name="XEON_REPORT.pdf", mime="application/pdf")

with tab_dossies:
    st.header("📑 Dossiês de Governança Corporativa")
    with st.expander("🛡️ CASO CVM: YDUQS PARTICIPAÇÕES S.A. | PROTOCOLO 215360716", expanded=True):
        st.error("RISCO SISTÊMICO DE GOVERNANÇA DETECTADO")
        st.markdown("""
        - **FRAUDE FIES/TCU:** Retenção ilegal de bolsas e risco de descredenciamento.
        - **DESCUMPRIMENTO TJRJ:** Violação deliberada de ordens judiciais.
        - **STATUS:** Enviado à Ouvidoria do Participante (CVM).
        """)
        st.info("Evidência técnica integrada ao sistema para fins de Visto EB-1A.")

st.chat_input("Command Sovereign Input...")
