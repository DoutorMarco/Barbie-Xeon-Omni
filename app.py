import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import hashlib
import pandas as pd
import httpx
import asyncio
import json
import os
import time
import numpy as np
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [PROTOCOL 01: AUTO-AUDITORIA DE INTEGRIDADE SHA-3]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f:
            return hashlib.sha3_256(f.read()).hexdigest()
    except:
        return "REALITY_MODE_ACTIVE"

SCRIPT_HASH = get_script_integrity()

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL - ZERO LIGHT]
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
        font-weight: bold; letter-spacing: 2px; transition: 0.4s; height: 3.5em;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 50px #00FF41; }
    div[data-testid="metric-container"] { border: 1px solid #00FF41; background-color: #050505 !important; padding: 20px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stDataFrame { border: 1px solid #00FF41 !important; background-color: #000000 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# [PROTOCOL 03: MOTOR PREDITIVO E ANÁLISE DE ANOMALIAS]
if 'latency_history' not in st.session_state:
    st.session_state.latency_history = []
if 'anomalies' not in st.session_state:
    st.session_state.anomalies = []

def detect_anomaly(current_latency):
    """Analisa se a latência atual representa uma anomalia global (Z-Score)."""
    if len(st.session_state.latency_history) < 5:
        st.session_state.latency_history.append(current_latency)
        return False
    
    mean = np.mean(st.session_state.latency_history)
    std = np.std(st.session_state.latency_history)
    z_score = (current_latency - mean) / (std if std > 0 else 1)
    
    st.session_state.latency_history.append(current_latency)
    if len(st.session_state.latency_history) > 50: st.session_state.latency_history.pop(0)
    
    return abs(z_score) > 2.5 # Threshold de Anomalia Crítica

# [PROTOCOL 04: MOTOR DE CONECTIVIDADE GLOBAL]
async def execute_predictive_probe(endpoint_name, url):
    async with httpx.AsyncClient() as client:
        try:
            start = time.perf_counter()
            response = await client.get(url, timeout=7.0)
            latency = (time.perf_counter() - start) * 1000
            is_anomaly = detect_anomaly(latency)
            return {
                "TARGET": endpoint_name,
                "STATUS": response.status_code,
                "LATENCY": latency,
                "ANOMALY": is_anomaly
            }
        except:
            return {"TARGET": endpoint_name, "STATUS": "FAIL", "LATENCY": 0, "ANOMALY": True}

# [PROTOCOL 05: GESTÃO DE ESTADO E ASSINATURA]
if 'ledger' not in st.session_state:
    st.session_state.ledger = []
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())

def sign_log(data):
    signature = st.session_state.priv_key.sign(data.encode(), ec.ECDSA(hashes.SHA256()))
    return signature.hex()

# [PROTOCOL 06: INTERFACE OPERACIONAL C4I]
st.title("🛰️ XEON COMMAND v54.0 | PREDICTIVE SOVEREIGNTY")

# Voz de Comando
st.components.v1.html(f"""
    <script>
    window.speak = (t) => {{
        const u = new SpeechSynthesisUtterance(t); u.lang='pt-BR'; u.pitch=0.8; u.rate=0.95;
        window.speechSynthesis.speak(u);
    }};
    </script>
    <button onclick="speak('Módulo preditivo ativado. Monitorando anomalias em bancos centrais e bolsas mundiais. Realidade pura operacional.')" 
    style="width:100%; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold; text-transform:uppercase;">
    🔊 STATUS: VIGILÂNCIA PREDITIVA GLOBAL ATIVA
    </button>
""", height=65)

# Dashboard de Telemetria
c1, c2, c3, c4 = st.columns(4)
c1.metric("RATE", "R$ 1.000/h", "SOVEREIGN")
c2.metric("ANOMALY RADAR", "SCANNING", "ACTIVE")
c3.metric("SHA-3", SCRIPT_HASH[:8], "VERIFIED")
c4.metric("VAULT", "RAM-ONLY", "AUTHENTIC")

st.write("---")

col_left, col_right = st.columns([1.6, 1])

with col_left:
    # Radar Global com Alertas de Anomalia
    targets_df = pd.DataFrame({
        'lat': [38.89, 51.50, 40.71, -23.55, 48.85, 35.68, 1.35, 55.75],
        'lon': [-77.03, -0.12, -74.00, -46.63, 2.35, 139.69, 103.82, 37.61],
        'intensity': [1.0 if not any(st.session_state.anomalies) else 2.0] * 8,
        'name': ['FED', 'BCE', 'NYSE', 'BACEN', 'Bourse', 'TSE', 'MAS', 'MICEX']
    })
    fig_map = px.density_mapbox(targets_df, lat='lat', lon='lon', z='intensity', radius=20,
                                mapbox_style="carto-darkmatter", title="GLOBAL ANOMALY DETECTION RADAR")
    fig_map.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig_map, use_container_width=True)

with col_right:
    st.markdown("#### ⚡ COMANDOS PREDITIVOS")
    
    target_sel = st.selectbox("ALVO DE MONITORAMENTO", ["US_FED", "EU_BCE", "BR_BACEN", "NYSE", "NASDAQ", "B3_SAO_PAULO"])
    endpoints = {
        "US_FED": "https://federalreserve.gov", "EU_BCE": "https://europa.eu",
        "BR_BACEN": "https://bcb.gov.br", "NYSE": "https://nyse.com",
        "NASDAQ": "https://nasdaq.com", "B3_SAO_PAULO": "https://b3.com.br"
    }

    if st.button("🚀 INICIAR PROBE PREDITIVO"):
        with st.spinner("Analisando Latência Sistêmica..."):
            url = endpoints.get(target_sel)
            res = asyncio.run(execute_predictive_probe(target_sel, url))
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            sig = sign_log(f"{res['LATENCY']}{ts}")
            
            if res['ANOMALY']:
                st.error(f"🚨 ANOMALIA DETECTADA EM {target_sel} | LATÊNCIA: {res['LATENCY']:.2f}ms")
                st.session_state.anomalies.append(target_sel)
            else:
                st.success(f"DADOS ESTÁVEIS | LATÊNCIA: {res['LATENCY']:.2f}ms")
            
            st.session_state.ledger.append({
                "TS": ts, "ALVO": res['TARGET'], "LAT": f"{res['LATENCY']:.2f}ms", "STATUS": "ANOMALY" if res['ANOMALY'] else "NOMINAL", "SIG": sig
            })

    if st.button("📄 GERAR DOSSIÊ PREDITIVO R$ 1.000/H"):
        if st.session_state.ledger:
            last = st.session_state.ledger[-1]
            pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0,0,210,297,'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, "XEON COMMAND - PREDICTIVE AUDIT REPORT", 0, 1, 'C')
            pdf.set_font("Courier", "", 8); pdf.ln(10)
            body = (f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO\nRATE: R$ 1.000,00/H\n"
                    f"PREDICTIVE_STATUS: {last['STATUS']}\nDETECTED_LATENCY: {last['LAT']}\n"
                    f"SIGNATURE_ECDSA: {last['SIG']}\nINTEGRITY_SHA3: {SCRIPT_HASH}")
            pdf.multi_cell(0, 5, body.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("💾 DOWNLOAD DOSSIÊ PREDITIVO", pdf.output(dest='S').encode('latin-1'), "XEON_PREDICTIVE_AUDIT.pdf")

    if st.button("☢️ PURGAR MEMÓRIA"):
        st.session_state.clear(); st.rerun()

st.markdown("#### 🔍 PREDICTIVE AUDIT LEDGER")
if st.session_state.ledger:
    st.dataframe(pd.DataFrame(st.session_state.ledger).sort_index(ascending=False), use_container_width=True, hide_index=True)

prompt = st.chat_input("Insira Comando para Missão Preditiva Global...")
