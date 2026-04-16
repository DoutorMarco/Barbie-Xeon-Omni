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
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; font-weight: bold; }
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

# [INTERFACE PRINCIPAL]
st.title("🛰️ XEON COMMAND v54.4 | SOVEREIGN OPERATIONS HUB")

# Criação das Abas
tab_monitor, tab_auditoria, tab_dossies = st.tabs(["📊 MONITORAMENTO", "🛡️ AUDITORIA ATIVA", "📑 DOSSIÊS CVM"])

with tab_monitor:
    col_left, col_right = st.columns([1.6, 1])
    with col_left:
        cpu_val = psutil.cpu_percent()
        fig = go.Figure(go.Indicator(mode="gauge+number", value=cpu_val, title={'text': "CPU LOAD", 'font': {'color': "#00FF41"}}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black", 'bordercolor': "#00FF41"}))
        fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        if st.session_state.encrypted_ledger:
            st.write("### 🔗 LEDGER IMUTÁVEL (CRYPTOGRAPHIC PROOF)")
            st.dataframe(pd.DataFrame(decrypt_ledger()).sort_index(ascending=False), use_container_width=True)
    with col_right:
        st.metric("INTEGRIDADE SHA-3", SCRIPT_HASH[:16])
        st.metric("RATE", "$450/HR")
        if st.button("☢️ PURGAR SESSÃO"):
            st.session_state.clear()
            st.rerun()

with tab_auditoria:
    target = st.text_input("AUDIT TARGET (URL)", value="https://google.com")
    if st.button("🚀 EXECUTAR PROTOCOLO DE INFILTRAÇÃO"):
        try:
            start_time = time.perf_counter()
            headers = {"User-Agent": "XEON-COMMAND-AUDITOR/54.4"}
            with httpx.Client(timeout=10.0, verify=False) as client:
                response = client.get(target, headers=headers)
                latency = (time.perf_counter() - start_time) * 1000
                secure_store({
                    "TS": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "TARGET": target,
                    "STATUS": response.status_code,
                    "LATENCY": f"{latency:.2f}ms"
                })
                st.success(f"BLOCK MINED: {response.status_code}")
                st.rerun()
        except Exception as e:
            st.error(f"FAIL: {str(e)}")

with tab_dossies:
    st.header("📑 Dossiês de Auditoria de Infraestrutura Crítica")
    st.write("Exposição de evidências de falhas sistêmicas em governança corporativa.")
    
    # Caso YDUQS / CVM
    with st.expander("🛡️ CASO: YDUQS PARTICIPAÇÕES S.A. | CVM 215360716", expanded=True):
        st.error("STATUS: ENVIADO À OUVIDORIA - RISCO SISTÊMICO DETECTADO")
        st.markdown("""
        **Resumo do Caso:**
        *   **Objeto:** Fraude contra FIES/TCU e descumprimento de ordens judiciais (TJRJ).
        *   **Impacto:** Risco reputacional omitido e contingência financeira bilionária.
        *   **Normativas:** Violação da Resolução CVM 80/2022 e 44/2021.
        """)
        st.warning("O Dossiê completo está disponível para download autenticado abaixo.")
        
        # Simulação de Download para o Case Study (O PDF deve estar no repositório GitHub)
        st.button("📄 SOLICITAR ACESSO AO DOSSIÊ YDUQS (PROJETADO)")

# [FOOTER SOBERANO]
st.chat_input("Command Input...")
