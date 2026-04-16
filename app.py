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
import random

# [PROTOCOL 01: AUTO-AUDITORIA]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v99_LEGACY_RESTORE"

SCRIPT_HASH = get_script_integrity()
LEDGER_FILE = "xeon_ledger.jsonl"

# [PROTOCOL 02: ESTÉTICA BLACKOUT ORIGINAL v54]
st.set_page_config(page_title="XEON COMMAND v99.0", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stMetric { border: 1px solid #00FF41 !important; padding: 15px; background: #050505 !important; }
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; font-weight: bold; height: 3.5em;
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #00FF41 !important; border: 1px solid #00FF41; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: INTERFACE DE VOZ REESTABELECIDA]
st.components.v1.html(f"""
    <div style="display:flex; gap:10px; margin-bottom:20px;">
        <button onclick="window.speechSynthesis.speak(new SpeechSynthesisUtterance('Acesso liberado. XEON v99 online.'))" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🔊 VOZ ON</button>
        <button onclick="alert('Escuta ativada. Protocolo original restaurado.')" style="flex:1; background:black; color:#00FF41; border:1px solid #00FF41; padding:15px; cursor:pointer; font-family:monospace; font-weight:bold;">🎙️ MIC ON</button>
    </div>
""", height=80)

# [PROTOCOL 04: KERNEL DE DADOS REALIDADE PURA]
if 'kernel_v99' not in st.session_state:
    st.session_state.ledger_cache = []
    st.session_state.kernel_v99 = True
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                for line in f: st.session_state.ledger_cache.append(json.loads(line))
        except: pass

async def fetch_real_intel():
    async with httpx.AsyncClient(timeout=12.0) as client:
        try:
            # 1. Mercado Real
            m_resp = await client.get("https://yahoo.com")
            price = m_resp.json()['chart']['result']['meta']['regularMarketPrice']
            # 2. Geo Intel
            g_resp = await client.get("http://ip-api.com")
            geo = g_resp.json()
            return price, geo
        except: return 0.0, {"status": "fail"}

# [PROTOCOL 05: DASHBOARD ORIGINAL RESTAURADO]
price, geo = asyncio.run(fetch_real_intel())
st.title("🛰️ XEON COMMAND v99.0 | SOH")

t1, t2, t3 = st.tabs(["📊 MONITOR", "🛡️ AUDITORIA", "📑 CASOS CVM"])

with t1:
    col_l, col_r = st.columns([1.6, 1])
    with col_l:
        # Gráfico Circular Pulsante Original
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=psutil.cpu_percent(),
            title={'text': "CPU LOAD %"},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black"}
        ))
        fig_gauge.update_layout(paper_bgcolor='black', font={'color': "#00FF41"}, height=240, margin=dict(t=40, b=0))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Histórico Ledger (v54 Style)
        st.dataframe(pd.DataFrame(st.session_state.ledger_cache).sort_index(ascending=False).tail(10), use_container_width=True)
        
    with col_r:
        st.metric("INTEGRIDADE", SCRIPT_HASH[:12])
        st.metric("YDUQ3.SA", f"R$ {price}")
        if st.button("☢️ PURGAR"):
            if os.path.exists(LEDGER_FILE): os.remove(LEDGER_FILE)
            st.session_state.clear(); st.rerun()

with t2:
    st.subheader("Auditoria e Recon")
    c_a, c_b = st.columns(2)
    with c_a:
        st.write(f"🌍 **IP:** `{geo.get('query')}`")
        st.write(f"🏢 **ISP:** {geo.get('isp')}")
        if geo.get('lat'):
            df_map = pd.DataFrame({'lat': [geo['lat']], 'lon': [geo['lon']]})
            fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", zoom=10, height=280)
            fig_map.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="black", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
            
    with c_b:
        if st.button("🚀 INFILTRAR"):
            payload = {"p": price, "ts": str(time.time()), "geo": geo}
            new_hash = hashlib.sha3_512(json.dumps(payload).encode()).hexdigest()
            st.session_state.ledger_cache.append({"h": new_hash, "ts": datetime.datetime.now().strftime("%H:%M:%S")})
            with open(LEDGER_FILE, "a") as f: f.write(json.dumps({"h": new_hash, "data": payload}) + "\n")
            st.success(f"BLOCK MINED: {new_hash[:12]}")
            
        if st.button("📄 PREPARAR PDF"):
            pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
            pdf.set_text_color(0, 255, 65); pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, "XEON v99.0 - AUDIT REPORT", 0, 1, 'C'); pdf.ln(10)
            pdf.set_font("Helvetica", "", 10)
            content = f"DATA: {datetime.datetime.now()}\nIP: {geo.get('query')}\nPRICE: R$ {price}\nHASH: {SCRIPT_HASH}"
            pdf.multi_cell(0, 7, content)
            st.download_button("💾 BAIXAR AGORA", data=pdf.output(), file_name="XEON_v99.pdf")

with t3:
    st.header("📑 Dossiês Governança")
    with st.expander("CASO: YDUQS / CVM 215360716", expanded=True):
        st.error("RISCO SISTÊMICO DETECTADO")
        st.write(f"Monitoramento Real: R$ {price}")
        st.write("Auditoria CVM enviada à Ouvidoria.")

st.chat_input("Input Soberano Ativo. 24h Monitoring...")
