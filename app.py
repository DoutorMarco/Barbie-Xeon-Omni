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
    except: return "STABLE_SOH_NODE_V54_4_FULL"

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
        font-weight: bold; letter-spacing: 2px; transition: 0.4s; height: 3.5em; margin-bottom: 10px;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 50px #00FF41; }
    div[data-testid="metric-container"] { border: 1px solid #00FF41; background-color: #050505 !important; padding: 20px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    input { background-color: #0a0a0a !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; font-weight: bold; border: 1px solid #00FF41; padding: 10px 20px; }
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

# [PROTOCOL 04: PERCEPÇÃO NEURAL - BOTÕES TOPO]
st.components.v1.html("""
    <script>
    const s = window.speechSynthesis;
    window.speak = (t) => { const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.7; u.rate=0.9; s.speak(u); };
    window.listen = () => {
        const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        r.lang='pt-BR'; r.start();
        r.onresult = (e) => { alert("CAPTURADO: " + e.results.transcript); };
    };
    </script>
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <button onclick="speak('Protocolo de Recuperação Ativo. Sistema em Homeostase.')" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🔊 VOZ ON</button>
        <button onclick="listen()" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🎙️ MIC ON</button>
    </div>
""", height=80)

st.title("🛰️ XEON COMMAND v54.4 | SOH")

# [ESTRUTURA DE ABAS]
tab1, tab2, tab3 = st.tabs(["📊 MONITOR", "🛡️ AUDITORIA", "📑 CASOS CVM"])

with tab1:
    col_left, col_right = st.columns([1.6, 1])
    with col_left:
        cpu_val = psutil.cpu_percent()
        fig = go.Figure(go.Indicator(mode="gauge+number", value=cpu_val, title={'text': "CPU LOAD", 'font': {'color': "#00FF41"}}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black", 'bordercolor': "#00FF41"}))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        if st.session_state.encrypted_ledger:
            st.dataframe(pd.DataFrame(decrypt_ledger()).sort_index(ascending=False), use_container_width=True)
    with col_right:
        st.metric("SHA-3 INTEGRITY", SCRIPT_HASH[:12])
        if st.button("☢️ PURGAR TUDO"):
            st.session_state.clear()
            st.rerun()

with tab2:
    target = st.text_input("AUDIT TARGET", value="https://google.com")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🚀 INFILTRAR"):
            try:
                start = time.perf_counter()
                headers = {"User-Agent": "XEON-54.4"}
                with httpx.Client(timeout=10.0, verify=False) as client:
                    resp = client.get(target, headers=headers)
                    secure_store({"TS": datetime.datetime.now().strftime("%H:%M:%S"), "TARGET": target, "STATUS": resp.status_code, "LATENCY": f"{(time.perf_counter()-start)*1000:.2f}ms"})
                    st.success("BLOCK MINED")
                    st.rerun()
            except: st.error("FAIL")
            
    with c2:
        if st.button("📄 PREPARAR PDF"):
            if st.session_state.encrypted_ledger:
                last = decrypt_ledger()[-1]
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
                pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
                pdf.cell(0, 10, "XEON COMMAND AUDIT", 0, 1, 'C'); pdf.ln(10)
                pdf.set_font("Courier", "", 10)
                for k, v in last.items(): pdf.cell(0, 8, f"{k}: {v}", 0, 1, 'L')
                st.session_state.pdf_buffer = pdf.output(dest='S').encode('latin-1')
                st.success("PDF EM MEMÓRIA")
    
    with c3:
        if st.session_state.pdf_buffer:
            st.download_button("💾 BAIXAR PDF", data=st.session_state.pdf_buffer, file_name="XEON_AUDIT.pdf", mime="application/pdf")

with tab3:
    st.header("🛡️ Dossiê de Governança Corporativa")
    with st.expander("CASO: YDUQS / CVM 215360716", expanded=True):
        st.error("ALERTA: RISCO SISTÊMICO")
        st.write("Auditoria de falha em controles internos e fraude FIES/TCU.")
        st.info("Protocolo enviado à Ouvidoria da CVM.")

st.chat_input("Comando Soberano...")
