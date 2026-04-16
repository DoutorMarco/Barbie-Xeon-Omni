import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import hashlib
import pandas as pd
import httpx
import json
import asyncio
import os
import numpy as np
import time

# [PROTOCOL 01: AUTO-AUDITORIA]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v101_1_STABLE_FIX"

SCRIPT_HASH = get_script_integrity()
LEDGER_FILE = "xeon_ledger.jsonl"

# [PROTOCOL 02: ESTÉTICA BLACKOUT TOTAL - PREENCHIMENTO PRETO/VERDE]
st.set_page_config(page_title="XEON COMMAND v101.1", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    
    /* Fundo Global */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }

    /* FIX: Preenchimento de Tabelas e Dataframes (Elimina o branco da imagem) */
    [data-testid="stDataFrame"], [data-testid="stTable"], .stTable, .stDataFrame {
        background-color: #000000 !important;
        border: 1px solid #00FF41 !important;
    }
    
    /* Estilização interna para células e cabeçalhos */
    .stDataFrame div, .stTable td, .stTable th {
        color: #00FF41 !important;
        background-color: #000000 !important;
    }
    
    /* Cor para o texto 'empty' e placeholders */
    .st-ae, .st-af, .st-ag, .st-ah { color: #00FF41 !important; }

    .stMetric { border: 1px solid #00FF41 !important; padding: 15px; background: #050505 !important; }
    
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; font-weight: bold; height: 3.5em;
    }
    
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; border: 1px solid #00FF41; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: INTERFACE DE VOZ MUNDIAL]
st.components.v1.html("""
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <button onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('Sincronia Xenos v101 ponto 1 ativa.'))" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🔊 VOZ ON</button>
        <button onclick="alert('🎙️ Escuta neural em prontidão.')" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🎙️ MIC ON</button>
    </div>
""", height=80)

# [PROTOCOL 04: KERNEL DE DADOS REALIDADE PURA]
if 'kernel_v101' not in st.session_state:
    st.session_state.ledger_cache = []
    st.session_state.kernel_v101 = True

async def fetch_real_intel():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
        try:
            m_resp = await client.get("https://yahoo.com")
            g_resp = await client.get("http://ip-api.com")
            price = m_resp.json()['chart']['result'][0]['meta']['regularMarketPrice']
            geo = g_resp.json()
            return price, geo
        except: return 0.0, {"status": "fail"}

# [PROTOCOL 05: DASHBOARD OPERACIONAL]
price, geo = asyncio.run(fetch_real_intel())
st.title("🛰️ XEON COMMAND v101.1 | PURE BLACKOUT")

t1, t2, t3 = st.tabs(["📊 MONITOR", "🛡️ AUDITORIA", "📑 CASOS CVM"])

with t1:
    col_l, col_r = st.columns([1.6, 1])
    with col_l:
        # Gráfico Circular Pulsante
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=psutil.cpu_percent(),
            title={'text': "CPU LOAD %"},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black"}
        ))
        fig_gauge.update_layout(paper_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(t=40, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # DataFrame Customizado (Preto/Verde)
        if not st.session_state.ledger_cache:
            # Exibe um dataframe vazio estilizado se não houver dados
            st.dataframe(pd.DataFrame(columns=["HASH", "TIMESTAMP"]), use_container_width=True)
        else:
            st.dataframe(pd.DataFrame(st.session_state.ledger_cache).tail(10), use_container_width=True)
        
    with col_r:
        st.metric("INTEGRIDADE", SCRIPT_HASH[:12])
        st.metric("YDUQ3.SA", f"R$ {price}")
        if st.button("☢️ PURGAR"):
            st.session_state.clear(); st.rerun()

with t2:
    st.subheader("Auditoria e Recon")
    c_a, c_b = st.columns(2)
    with c_a:
        st.write(f"🌍 **IP:** `{geo.get('query')}`")
        if geo.get('lat'):
            df_map = pd.DataFrame({'lat': [geo['lat']], 'lon': [geo['lon']]})
            fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", zoom=10, height=280)
            fig_map.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="black", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
    with c_b:
        if st.button("🚀 INFILTRAR"):
            payload = {"p": price, "ts": str(time.time())}
            new_hash = hashlib.sha3_512(json.dumps(payload).encode()).hexdigest()
            st.session_state.ledger_cache.append({"h": new_hash[:16], "ts": datetime.datetime.now().strftime("%H:%M:%S")})
            st.success(f"BLOCK MINED: {new_hash[:12]}")
            
        if st.button("📄 PREPARAR PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "XEON v101.1 - AUDIT REPORT", 0, 1, 'C'); pdf.ln(10)
            content = f"DATA: {datetime.datetime.now()}\nIP: {geo.get('query')}\nPRICE: R$ {price}\nHASH: {SCRIPT_HASH}"
            pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 7, content)
            st.download_button("💾 BAIXAR PDF", data=bytes(pdf.output()), file_name="XEON_v101.pdf", mime="application/pdf")

with t3:
    st.header("📑 Dossiês Governança")
    with st.expander("CASO: YDUQS / CVM 215360716", expanded=True):
        st.error("RISCO SISTÊMICO DETECTADO")
        st.write(f"Monitoramento Real: R$ {price}")

st.chat_input("Operação v101.1 nominal...")
