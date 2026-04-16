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
import subprocess # PROTOCOLO PARA CHAMAR O GO

# [PROTOCOL 01: AUTO-AUDITORIA & INTEGRIDADE]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v101_3_STABLE"

SCRIPT_HASH = get_script_integrity()
VALOR_HORA = 1000.00 

# [PROTOCOL: INTEGRAÇÃO COM MOTOR GO]
def get_go_engine_data():
    """Lê o resultado do hardware processado pelo arquivo xeon_core.go"""
    try:
        # Tenta compilar e rodar o arquivo Go que você criou no repositório
        result = subprocess.run(['go', 'run', 'xeon_core.go'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return "GO_ENGINE_OFFLINE"
    except:
        return "GO_NOT_FOUND"

# [PROTOCOL 02: BLACKOUT TOTAL - ZERO BRANCO]
st.set_page_config(page_title="XEON COMMAND v101.4", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    [data-testid="stDataFrame"], [data-testid="stTable"], .stTable, .stDataFrame {
        background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
    }
    .stMetric { border: 1px solid #00FF41 !important; padding: 15px; background: #050505 !important; }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #00FF41 !important; }
    .stButton>button {
        width: 100%; background-color: #000000 !important; color: #00FF41 !important;
        border: 1px solid #00FF41 !important; border-radius: 0px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: PERSISTÊNCIA & REALIDADE MUNDIAL]
LEDGER_LOG = "xeon_persistence.json"
if 'session_data' not in st.session_state:
    st.session_state.session_data = {"total_revenue": 0.0, "start_time": time.time()}
    st.session_state.ledger_cache = []

async def fetch_live_intel():
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            usd = (await client.get("https://er-api.com")).json()['rates']['BRL']
            return usd
        except: return 5.0

usd_brl = asyncio.run(fetch_live_intel())
elapsed_session = (time.time() - st.session_state.session_data["start_time"]) / 3600
current_revenue = elapsed_session * VALOR_HORA

# Captura dados do Motor Go (Ancoragem Hardware)
go_telemetry = get_go_engine_data()

st.title("🛰️ XEON COMMAND v101.4 | GO-POWERED")

t1, t2, t3 = st.tabs(["📊 MONITOR", "🛡️ AUDITORIA GO", "📑 EB-1A"])

with t1:
    col_l, col_r = st.columns([1.6, 1])
    with col_l:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=psutil.cpu_percent(),
            gauge={'axis': {'range': [None, 100], 'tickcolor': "#00FF41"}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black"}
        ))
        fig_gauge.update_layout(paper_bgcolor='black', font={'color': "#00FF41"}, height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col_r:
        st.metric("MONETIZAÇÃO", f"R$ {current_revenue:.4f}")
        st.metric("MOTOR GO STATUS", "ATIVO" if "CORE" in go_telemetry else "OFFLINE")

with t2:
    st.subheader("🛡️ Telemetria de Hardware (via Golang)")
    # EXIBE A SAÍDA REAL DO SEU ARQUIVO GO
    st.code(f"SAÍDA DO KERNEL GO:\n{go_telemetry}", language="bash")
    
    if st.button("🚀 EXECUTAR DEEP SCAN (GO)"):
        st.rerun()

with t3:
    st.header("📑 Dossiê Habilidade Extraordinária")
    st.success("Arquitetura Híbrida Python/Go para Proteção de Infraestrutura Crítica.")
    st.write(f"**Integridade SHA-3:** `{SCRIPT_HASH[:32]}`")
    st.write(f"**Câmbio Real:** R$ {usd_brl}")

st.chat_input("Operação v101.4 em Homeostase...")
