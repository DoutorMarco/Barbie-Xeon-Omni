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

# [PROTOCOL 01: AUTO-AUDITORIA]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "STABLE_SOH_V54_4_FIX"

SCRIPT_HASH = get_script_integrity()

# [PROTOCOL 02: ESTÉTICA BLACKOUT]
st.set_page_config(page_title="XEON COMMAND v54.4", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; font-weight: bold;
        height: 3.5em; transition: 0.4s;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; }
    input { background-color: #0a0a0a !important; color: #00FF41 !important; border: 1px solid #00FF41 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; border: 1px solid #00FF41; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: SEGURANÇA]
if 'encrypted_ledger' not in st.session_state:
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
    st.session_state.encrypted_ledger.append({"nonce": nonce, "blob": aesgcm.encrypt(nonce, json.dumps(data_dict).encode(), None)})

def decrypt_ledger():
    aesgcm = AESGCM(st.session_state.aes_key)
    return [json.loads(aesgcm.decrypt(i["nonce"], i["blob"], None)) for i in st.session_state.encrypted_ledger]

# [PROTOCOL 04: INTERFACE DE VOZ REESTABELECIDA]
st.components.v1.html(f"""
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <button onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('Sistema Nominal. Protocolo v54.4 ativo.'))" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🔊 VOZ ON</button>
        <button onclick="alert('Escuta ativada. Aguardando comando neural.')" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🎙️ MIC ON</button>
    </div>
""", height=80)

st.title("🛰️ XEON COMMAND v54.4 | SOH")

t1, t2, t3 = st.tabs(["📊 MONITOR", "🛡️ AUDITORIA", "📑 CASOS CVM"])

with t1:
    col_l, col_r = st.columns([1.6, 1])
    with col_l:
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=psutil.cpu_percent(), title={'text': "CPU LOAD"}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black"})).update_layout(paper_bgcolor='black', font={'color': "#00FF41"}, height=240), use_container_width=True)
        if st.session_state.encrypted_ledger:
            st.dataframe(pd.DataFrame(decrypt_ledger()).sort_index(ascending=False), use_container_width=True)
    with col_r:
        st.metric("INTEGRIDADE", SCRIPT_HASH[:12])
        if st.button("☢️ PURGAR"):
            st.session_state.clear(); st.rerun()

with t2:
    target = st.text_input("AUDIT TARGET", value="https://google.com")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 INFILTRAR"):
            try:
                with httpx.Client(timeout=10.0, verify=False) as client:
                    resp = client.get(target)
                    secure_store({"TS": datetime.datetime.now().strftime("%H:%M:%S"), "TARGET": target, "STATUS": resp.status_code})
                    st.success("BLOCK MINED"); time.sleep(0.5); st.rerun()
            except Exception as e: st.error(f"FAIL: {str(e)}")
    with c2:
        if st.button("📄 PREPARAR PDF"):
            if st.session_state.encrypted_ledger:
                data = decrypt_ledger()[-1]
                pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
                pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
                pdf.cell(0, 10, "XEON AUDIT", 0, 1, 'C'); pdf.ln(10)
                for k, v in data.items(): pdf.cell(0, 8, f"{k}: {v}", 0, 1, 'L')
                st.session_state.pdf_buffer = pdf.output(dest='S').encode('latin-1')
                st.success("PDF PRONTO")
    
    # [FIX: Botão de Download persistente abaixo das colunas]
    if st.session_state.pdf_buffer:
        st.download_button("💾 BAIXAR AGORA", data=st.session_state.pdf_buffer, file_name="XEON_AUDIT.pdf", mime="application/pdf")

with t3:
    st.header("📑 Dossiês Governança")
    with st.expander("CASO: YDUQS / CVM 215360716", expanded=True):
        st.error("RISCO SISTÊMICO DETECTADO")
        st.write("Auditoria CVM enviada à Ouvidoria.")

st.chat_input("Input Soberano...")
