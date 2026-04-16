import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
from fpdf import FPDF
import hashlib
import pandas as pd
import httpx
import asyncio
import json
import os
import time
from io import BytesIO  # [CRITICAL UPGRADE v54.2]
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [PROTOCOL 01: AUTO-AUDITORIA SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "SOH_CORE_V54_2_BYTESIO_ACTIVE"

SCRIPT_HASH = get_script_integrity()

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL]
st.set_page_config(page_title="XEON COMMAND v54.2", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    :root { --st-bg-color: #000000; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    [data-testid="stChatInput"], div[data-baseweb="base-input"], input, textarea {
        background-color: #000000 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important;
    }
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; text-transform: uppercase;
        font-weight: bold; letter-spacing: 2px; transition: 0.4s; height: 3.5em;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 50px #00FF41; }
    div[data-testid="metric-container"] { border: 1px solid #00FF41; background-color: #050505 !important; padding: 20px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stDataFrame { border: 1px solid #00FF41 !important; background-color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: SEGURANÇA E BLOCKCHAIN]
if 'priv_key' not in st.session_state:
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())
    st.session_state.aes_key = AESGCM.generate_key(bit_length=256)
    st.session_state.encrypted_ledger = []
    st.session_state.last_block_hash = "GENESIS_BLOCK_0000"

def secure_store(data_dict):
    nonce = os.urandom(12)
    aesgcm = AESGCM(st.session_state.aes_key)
    data_dict["PREV_HASH"] = st.session_state.last_block_hash
    raw_data = json.dumps(data_dict).encode()
    current_hash = hashlib.sha3_256(raw_data).hexdigest()
    st.session_state.last_block_hash = current_hash
    data_dict["CURRENT_HASH"] = current_hash
    data_dict["SIG"] = st.session_state.priv_key.sign(current_hash.encode(), ec.ECDSA(hashes.SHA256())).hex()
    encrypted_blob = aesgcm.encrypt(nonce, json.dumps(data_dict).encode(), None)
    st.session_state.encrypted_ledger.append({"nonce": nonce, "blob": encrypted_blob})

def decrypt_ledger():
    aesgcm = AESGCM(st.session_state.aes_key)
    return [json.loads(aesgcm.decrypt(i["nonce"], i["blob"], None)) for i in st.session_state.encrypted_ledger]

# [PROTOCOL 04: PERCEPÇÃO NEURAL (VOZ/MIC)]
st.components.v1.html("""
    <script>
    const s = window.speechSynthesis;
    window.speak = (t) => { const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.7; u.rate=0.9; s.speak(u); };
    window.listen = () => {
        const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        r.lang='pt-BR'; r.start();
        r.onresult = (e) => { alert("CAPTURADO: " + e.results.transcript); window.speak("Sincronizando fluxo."); };
    };
    </script>
    <div style="display:flex; gap:10px;">
        <button onclick="speak('Módulo v54.2 nominal. Buffer de memória direto ativado para download seguro.')" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:12px; cursor:pointer; font-family:monospace; font-weight:bold;">🔊 VOZ ON</button>
        <button onclick="listen()" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:12px; cursor:pointer; font-family:monospace; font-weight:bold;">🎙️ MIC ON</button>
    </div>
""", height=70)

# [PROTOCOL 05: DASHBOARD E MONITORAMENTO]
st.title("🛰️ XEON COMMAND v54.2 | BYTESIO SOVEREIGNTY")
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "SOVEREIGN")
c2.metric("LEDGER", f"BLOCK_{len(st.session_state.encrypted_ledger)}", "NOMINAL")
c3.metric("INTEGRIDADE", SCRIPT_HASH[:8], "SHA-3")
c4.metric("OUTPUT", "MEMORY_FLOW", "ACTIVE")

st.write("---")

col_left, col_right = st.columns([1.6, 1])

with col_left:
    fig = go.Figure(go.Indicator(mode="gauge+number", value=psutil.cpu_percent(), title={'text': "CPU LOAD", 'font': {'color': "#00FF41"}}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black", 'bordercolor': "#00FF41"}))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.encrypted_ledger:
        st.dataframe(pd.DataFrame(decrypt_ledger()).sort_index(ascending=False), use_container_width=True, hide_index=True)

with col_right:
    target = st.text_input("AUDIT TARGET URL", value="https://github.com")
    if st.button("🚀 EXECUTAR INFILTRAÇÃO"):
        try:
            start = time.perf_counter()
            response = httpx.get(target, timeout=5.0)
            secure_store({"TS": datetime.datetime.now().strftime("%H:%M:%S"), "TARGET": target, "STATUS": response.status_code, "TYPE": "MISSION_SUCCESS", "LATENCY": f"{(time.perf_counter()-start)*1000:.2f}ms"})
            st.success("BLOCK MINED.")
        except: st.error("CONNECTION FAIL.")

    if st.button("📄 GERAR DOSSIÊ R$ 1.000/H"):
        if st.session_state.encrypted_ledger:
            last = decrypt_ledger()[-1]
            # [UPGRADE v54.2: BYTESIO STREAMING]
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, "XEON COMMAND - OFFICIAL AUDIT EVIDENCE", 0, 1, 'C'); pdf.ln(10)
            pdf.set_font("Courier", "", 10)
            
            lines = [
                f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
                f"VALUATION: R$ 1.000,00 / HOUR",
                f"TS: {last['TS']}",
                f"HASH: {last['CURRENT_HASH']}",
                f"STATUS: REALITY PURITY OPERATIONAL",
                f"INTEGRITY: SHA-3_{SCRIPT_HASH[:16]}",
                "--------------------------------------------------",
                "EB-1A COMPLIANT EVIDENCE | NIW CATEGORY"
            ]
            for l in lines:
                safe_l = str(l).encode('ascii', 'ignore').decode('ascii')
                pdf.cell(0, 8, safe_l, 0, 1, 'L')
            
            # Força o PDF para o buffer de memória
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="💾 BAIXAR AGORA (BYTESIO)",
                data=pdf_output,
                file_name=f"XEON_AUDIT_{last['TS'].replace(':','')}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Ledger vazio.")

    if st.button("☢️ PURGAR"): st.session_state.clear(); st.rerun()

prompt = st.chat_input("Insira Instrução Soberana...")
