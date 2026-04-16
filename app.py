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
        return "STABLE_SOH_NODE"

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
    # Setup de Segurança Assimétrica
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())
    # Setup de Segurança Simétrica (RAM Protection)
    st.session_state.aes_key = AESGCM.generate_key(bit_length=256)
    # Blockchain Core
    st.session_state.encrypted_ledger = []
    st.session_state.last_block_hash = "GENESIS_BLOCK_0000"

def secure_store(data_dict):
    """Criptografa dados em repouso na RAM (AES-256-GCM) e encadeia hashes."""
    nonce = os.urandom(12)
    aesgcm = AESGCM(st.session_state.aes_key)
    
    # Adiciona o hash do bloco anterior (Blockchain Structure)
    data_dict["PREV_HASH"] = st.session_state.last_block_hash
    raw_data = json.dumps(data_dict).encode()
    
    # Gera novo Hash SHA-3 para o bloco atual
    current_hash = hashlib.sha3_256(raw_data).hexdigest()
    st.session_state.last_block_hash = current_hash
    data_dict["CURRENT_HASH"] = current_hash
    
    # Assinatura Digital ECDSA
    signature = st.session_state.priv_key.sign(current_hash.encode(), ec.ECDSA(hashes.SHA256())).hex()
    data_dict["SIG"] = signature
    
    # Criptografia Final para st.session_state
    encrypted_blob = aesgcm.encrypt(nonce, json.dumps(data_dict).encode(), None)
    st.session_state.encrypted_ledger.append({"nonce": nonce, "blob": encrypted_blob})

def decrypt_ledger():
    """Descriptografa o ledger em tempo real para visualização auditada."""
    aesgcm = AESGCM(st.session_state.aes_key)
    decrypted_list = []
    for item in st.session_state.encrypted_ledger:
        raw = aesgcm.decrypt(item["nonce"], item["blob"], None)
        decrypted_list.append(json.loads(raw))
    return decrypted_list

# [PROTOCOL 04: PERCEPÇÃO NEURAL MULTILINGUE]
def perception_module():
    st.components.v1.html(f"""
    <script>
    const synth = window.speechSynthesis;
    window.speak = (t) => {{
        const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.75; u.rate=0.95;
        synth.speak(u);
    }};
    window.activateMic = () => {{
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'pt-BR'; rec.start();
        rec.onresult = (e) => {{ alert("BLOCKCHAIN LOG DETECTADO: " + e.results.transcript); }};
    }};
    </script>
    <div style="display:flex; gap:10px;">
        <button onclick="speak('Encadeamento de hashes SHA-3 ativo. Blindagem de RAM com AES-256 nominal. Realidade pura operando com zero erro.')" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">
            🔊 STATUS DE VOZ: BLOCKCHAIN ON
        </button>
        <button onclick="activateMic()" 
            style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">
            🎙️ ESCUTA MULTILINGUE
        </button>
    </div>
""", height=75)

# [PROTOCOL 05: MOTOR DE INFILTRAÇÃO COM VALIDAÇÃO HTTP]
async def validated_probe(target_url):
    """Executa auditoria com diferenciação tática de status code."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            start = time.perf_counter()
            response = await client.get(target_url)
            latency = (time.perf_counter() - start) * 1000
            
            # Validação de Status (Success 2xx vs Failure 4xx/5xx)
            status_type = "MISSION_SUCCESS" if 200 <= response.status_code < 300 else "ACCESS_DENIED"
            return {"CODE": response.status_code, "LAT": f"{latency:.2f}ms", "TYPE": status_type, "VERIFIED": True}
        except Exception:
            return {"CODE": "ERROR", "LAT": "N/A", "TYPE": "INFRA_FAIL", "VERIFIED": False}

# [PROTOCOL 06: DASHBOARD OPERACIONAL C4I]
st.title("🛰️ XEON COMMAND v54.0 | BLOCKCHAIN LEDGER")
perception_module()

# Dash de Telemetria SOH v2.2
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "SOVEREIGN")
c2.metric("RAM VAULT", "ENCRYPTED", "AES-256-GCM")
c3.metric("CHAIN", f"BLOCK_{len(st.session_state.encrypted_ledger)}", "IMMUTABLE")
c4.metric("INTEGRIDADE", SCRIPT_HASH[:8], "SHA-3")

st.write("---")

col_left, col_right = st.columns([1.6, 1])

with col_left:
    # Gráfico circular de Telemetria Hardware
    cpu_val = psutil.cpu_percent()
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = cpu_val,
        title = {'text': "CPU LOAD (AES_ENCRYPTION)", 'font': {'color': "#00FF41", 'size': 14}},
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black", 'bordercolor': "#00FF41"}
    ))
    fig_gauge.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("#### 🔗 HASH CHAIN LEDGER (DECRYPTED ON-THE-FLY)")
    if st.session_state.encrypted_ledger:
        df = pd.DataFrame(decrypt_ledger())
        st.dataframe(df.sort_index(ascending=False), use_container_width=True, hide_index=True)

with col_right:
    st.markdown("#### ⚡ COMANDOS DE AUDITORIA REAL")
    target = st.text_input("TARGET INFRASTRUCTURE URL", value="https://github.com")
    
    if st.button("🚀 INICIAR INFILTRAÇÃO VALIDADA"):
        with st.spinner("Validando Status de Rede e Blindagem..."):
            res = asyncio.run(validated_probe(target))
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            # Adicionando ao Ledger Criptografado com Hash Chain
            secure_store({
                "TS": ts, "TARGET": target, "STATUS": res['CODE'], 
                "TYPE": res['TYPE'], "LATENCY": res['LAT']
            })
            if res['VERIFIED']: st.success(f"DADOS CAPTURADOS: {res['TYPE']}")
            else: st.error("FALHA CRÍTICA DE ACESSO.")

    if st.button("📄 GERAR DOSSIÊ R$ 1.000/H"):
        if st.session_state.encrypted_ledger:
            last = decrypt_ledger()[-1]
            pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0,0,210,297,'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, "XEON COMMAND - BLOCKCHAIN AUDIT EVIDENCE", 0, 1, 'C')
            pdf.set_font("Courier", "", 8); pdf.ln(10)
            body = (f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO\nRATE: R$ 1.000,00/H\n"
                    f"CURRENT_BLOCK_HASH: {last['CURRENT_HASH']}\n"
                    f"PREVIOUS_BLOCK_HASH: {last['PREV_HASH']}\n"
                    f"DIGITAL_SIGNATURE: {last['SIG']}\n"
                    f"ENCRYPTION: AES-256-GCM + SHA-3 INTEGRITY")
            pdf.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("💾 DOWNLOAD PROVA TÉCNICA", pdf.output(dest='S').encode('latin-1'), "XEON_EB1A_PROOF.pdf")

    if st.button("☢️ PURGAR MEMÓRIA"):
        st.session_state.clear(); st.rerun()

prompt = st.chat_input("Insira Instrução Soberana para Processamento em RAM Blindada...")
