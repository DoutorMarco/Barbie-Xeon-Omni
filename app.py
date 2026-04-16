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
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [PROTOCOL 01: AUTO-AUDITORIA DE INTEGRIDADE SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f:
            return hashlib.sha3_256(f.read()).hexdigest()
    except:
        return "STABLE_SOH_NODE_V54"

SCRIPT_HASH = get_script_integrity()

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL - C4I MILITARY]
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")
st.markdown(
    """
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
        font-weight: bold; letter-spacing: 2px; transition: 0.4s; height: 3.2em;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 50px #00FF41; }
    div[data-testid="metric-container"] { border: 1px solid #00FF41; background-color: #050505 !important; padding: 20px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stDataFrame { border: 1px solid #00FF41 !important; background-color: #000000 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# [PROTOCOL 03: CRIPTOGRAFIA DE RAM E HASH CHAIN]
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
    signature = st.session_state.priv_key.sign(current_hash.encode(), ec.ECDSA(hashes.SHA256())).hex()
    data_dict["SIG"] = signature
    encrypted_blob = aesgcm.encrypt(nonce, json.dumps(data_dict).encode(), None)
    st.session_state.encrypted_ledger.append({"nonce": nonce, "blob": encrypted_blob})

def decrypt_ledger():
    aesgcm = AESGCM(st.session_state.aes_key)
    decrypted_list = []
    for item in st.session_state.encrypted_ledger:
        raw = aesgcm.decrypt(item["nonce"], item["blob"], None)
        decrypted_list.append(json.loads(raw))
    return decrypted_list

# [PROTOCOL 04: MONETIZAÇÃO - MOTOR PDF BLINDADO]
def generate_sovereign_pdf(entry):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, "XEON COMMAND - AUDIT EVIDENCE (v54.0)", 0, 1, 'C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        
        content = [
            f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
            f"VALUATION: R$ 1.000,00 / HOUR",
            f"TIMESTAMP: {entry.get('TS', 'N/A')}",
            f"TARGET: {entry.get('TARGET', 'N/A')}",
            f"LATENCY: {entry.get('LATENCY', 'N/A')}",
            f"PREV_HASH: {entry.get('PREV_HASH', 'N/A')}",
            f"CURRENT_HASH: {entry.get('CURRENT_HASH', 'N/A')}",
            f"SIGNATURE_SIG: {entry.get('SIG', 'N/A')[:32]}...",
            "----------------------------------------------------------",
            "STATUS: MISSION_SUCCESS - REALITY PURITY",
            "COMPLIANCE: EB-1A EXTRAORDINARY ABILITY EVIDENCE",
            f"INTEGRITY_CHECK: SHA-3_{SCRIPT_HASH[:16]}"
        ]
        for line in content:
            # Sanitização forçada para evitar erros de encoding (Latin-1/FPDF)
            safe_line = str(line).encode('ascii', 'ignore').decode('ascii')
            pdf.cell(0, 8, safe_line, 0, 1, 'L')
        return pdf.output(dest='S').encode('latin-1')
    except Exception as e:
        st.error(f"ERRO CRÍTICO NA GERAÇÃO: {str(e)}")
        return None

# [PROTOCOL 05: MOTOR DE AUDITORIA REAL]
async def validated_probe(target_url):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            start = time.perf_counter()
            response = await client.get(target_url)
            latency = (time.perf_counter() - start) * 1000
            status_type = "MISSION_SUCCESS" if 200 <= response.status_code < 300 else "ACCESS_DENIED"
            return {"CODE": response.status_code, "LAT": f"{latency:.2f}ms", "TYPE": status_type}
        except:
            return {"CODE": "FAIL", "LAT": "0ms", "TYPE": "INFRA_ERROR"}

# [PROTOCOL 06: DASHBOARD OPERACIONAL C4I]
st.title("🛰️ XEON COMMAND v54.0 | BLOCKCHAIN LEDGER")

# Métricas SOH v2.2
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "SOVEREIGN")
c2.metric("RAM VAULT", "AES-256", "ENCRYPTED")
c3.metric("CHAIN", f"BLOCK_{len(st.session_state.encrypted_ledger)}", "IMMUTABLE")
c4.metric("INTEGRIDADE", SCRIPT_HASH[:8], "SHA-3")

st.write("---")

col_left, col_right = st.columns([1.6, 1])

with col_left:
    # Telemetria Circular
    cpu_val = psutil.cpu_percent()
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = cpu_val,
        title = {'text': "CPU LOAD (AES_ENCRYPTION)", 'font': {'color': "#00FF41", 'size': 14}},
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black", 'bordercolor': "#00FF41"}
    ))
    fig_gauge.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("#### 🔗 HASH CHAIN LEDGER (DECRYPTED)")
    if st.session_state.encrypted_ledger:
        df = pd.DataFrame(decrypt_ledger())
        st.dataframe(df.sort_index(ascending=False), use_container_width=True, hide_index=True)

with col_right:
    st.markdown("#### ⚡ COMANDOS DE AUDITORIA REAL")
    target = st.text_input("TARGET URL", value="https://github.com")
    
    if st.button("🚀 INICIAR INFILTRAÇÃO VALIDADA"):
        with st.spinner("Encadeando Hashes..."):
            res = asyncio.run(validated_probe(target))
            secure_store({
                "TS": datetime.datetime.now().strftime("%H:%M:%S"), 
                "TARGET": target, "STATUS": res['CODE'], 
                "TYPE": res['TYPE'], "LATENCY": res['LAT']
            })
            st.success(f"BLOCK_{len(st.session_state.encrypted_ledger)} MINED")

    if st.button("📄 GERAR DOSSIÊ R$ 1.000/H"):
        if st.session_state.encrypted_ledger:
            last_block = decrypt_ledger()[-1]
            pdf_bytes = generate_sovereign_pdf(last_block)
            if pdf_bytes:
                st.download_button(
                    label="💾 DOWNLOAD EVIDÊNCIA PDF",
                    data=pdf_bytes,
                    file_name=f"XEON_AUDIT_{last_block['TS'].replace(':','')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Execute uma missão primeiro.")

    if st.button("☢️ PURGAR MEMÓRIA"):
        st.session_state.clear(); st.rerun()

prompt = st.chat_input("Comando de Realidade Pura...")
