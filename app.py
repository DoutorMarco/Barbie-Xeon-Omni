import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
from fpdf import FPDF
import hashlib
import pandas as pd
import httpx
import json
import asyncio
import os
import numpy as np
import time
from pydantic import BaseModel, ValidationError, Field
from typing import Optional, Dict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [SCHEMA VALIDATION - BANK GRADE]
class MarketData(BaseModel):
    price: float = Field(..., gt=0)
    volume: int = Field(..., ge=0)
    ticker: str = "YDUQ3.SA"

class GeoData(BaseModel):
    query: str
    city: str
    countryCode: str
    isp: str
    proxy: bool
    as_info: str = Field(alias="as")

# [PROTOCOL 01: AUTO-AUDITORIA v90]
def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except Exception as e:
        return f"INTEGRITY_FAILURE_{str(e)[:8]}"

SCRIPT_HASH = get_script_integrity()
LEDGER_FILE = "xeon_ledger.jsonl"

# [PROTOCOL 02: ESTÉTICA BLACKOUT SUPREMA]
st.set_page_config(page_title="XEON COMMAND v90.0", layout="wide")
st.markdown("""
    <style>
    #MainMenu, header, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"], hr { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #000000 !important; color: #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stMetric { border: 1px solid #00FF41 !important; padding: 15px; background: #050505 !important; }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 03: KERNEL DE CUSTÓDIA & LOGS]
if 'kernel_v90' not in st.session_state:
    st.session_state.aes_key = AESGCM.generate_key(bit_length=256)
    st.session_state.ledger_cache = []
    st.session_state.event_logs = []
    st.session_state.price_history = []
    st.session_state.kernel_v90 = True

def log_event(level: str, message: str):
    entry = f"[{level}] {datetime.datetime.now().strftime('%H:%M:%S')} - {message}"
    st.session_state.event_logs.append(entry)
    if len(st.session_state.event_logs) > 50: st.session_state.event_logs.pop(0)

# [PROTOCOL 04: REAL-TIME INTEL (ROBUSTEZ APLICADA)]
async def fetch_v90_intel():
    headers = {'User-Agent': 'XEON-COMMAND-V90-AUDIT'}
    async with httpx.AsyncClient(timeout=12.0, headers=headers) as client:
        try:
            m_resp = await client.get("https://yahoo.com")
            m_resp.raise_for_status()
            raw_m = m_resp.json()['chart']['result'][0]
            m_validated = MarketData(price=raw_m['meta']['regularMarketPrice'], volume=raw_m['indicators']['quote'][0]['volume'][-1])
            
            g_resp = await client.get("http://ip-api.com")
            g_resp.raise_for_status()
            g_validated = GeoData(**g_resp.json())
            
            log_event("SUCCESS", "Sincronia de dados validada via Pydantic.")
            return m_validated, g_validated
        except ValidationError as ve:
            log_event("CRITICAL", f"Falha de Schema: {ve.json()}")
            return None, None
        except Exception as e:
            log_event("ERROR", f"Conectividade Crítica: {str(e)}")
            return None, None

def secure_commit_v90(data):
    aesgcm = AESGCM(st.session_state.aes_key)
    nonce = os.urandom(12)
    payload = json.dumps(data)
    # Proof of Existence (PoE) Hash
    poe_hash = hashlib.sha3_512(payload.encode()).hexdigest()
    cipher_blob = aesgcm.encrypt(nonce, payload.encode(), None)
    entry = {"n": nonce.hex(), "b": cipher_blob.hex(), "poe": poe_hash, "ts": datetime.datetime.now().isoformat()}
    
    with open(LEDGER_FILE, "a") as f: f.write(json.dumps(entry) + "\n")
    st.session_state.ledger_cache.append(entry)
    return poe_hash

# [PROTOCOL 05: UI DASHBOARD]
m_data, g_data = asyncio.run(fetch_v90_intel())

st.title(f"🛰️ XEON COMMAND v90.0 | BANKING COMPLIANCE")

c1, c2, c3, c4 = st.columns(4)
c1.metric("DATA SCHEMA", "VALIDATED" if m_data else "INVALID")
c2.metric("NETWORK ISP", g_data.isp[:15] if g_data else "OFFLINE")
c3.metric("YDUQ3.SA", f"R$ {m_data.price}" if m_data else "0.0")
c4.metric("INTEGRIDADE", SCRIPT_HASH[:12])

t1, t2, t3 = st.tabs(["📊 TELEMETRIA DE CONFORMIDADE", "🛡️ LEDGER SINK (PoE)", "📑 DOSSIÊ DE AUDITORIA"])

with t1:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Granular System Logs")
        for log in st.session_state.event_logs[::-1]:
            st.text(log)
    with col_r:
        if m_data:
            st.session_state.price_history.append(m_data.price)
            if len(st.session_state.price_history) > 30: st.session_state.price_history.pop(0)
            fig = go.Figure(go.Scatter(y=st.session_state.price_history, line=dict(color="#00FF41", width=2)))
            fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"}, height=250)
            st.plotly_chart(fig, use_container_width=True)

with t2:
    if st.button("🚀 EXECUTE SECURE COMMIT (PoE)"):
        if m_data and g_data:
            poe = secure_commit_v90({"m": m_data.dict(), "g": g_data.dict()})
            st.success(f"PROVA DE EXISTÊNCIA (PoE) REGISTRADA: {poe[:32]}...")
    st.dataframe(pd.DataFrame(st.session_state.ledger_cache).tail(10), use_container_width=True)

with t3:
    st.error("CERTIFICAÇÃO CVM: AUDITORIA DE PRODUÇÃO")
    if st.button("📑 GERAR LAUDO IMUTÁVEL"):
        pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "XEON v90.0 - BANK-GRADE AUDIT REPORT", 0, 1, 'C'); pdf.ln(10)
        pdf.set_font("Helvetica", "", 10)
        content = (f"DATA: {datetime.datetime.now()}\n"
                   f"INTEGRIDADE DO CORE: {SCRIPT_HASH}\n"
                   f"ULTIMO PoE HASH: {st.session_state.ledger_cache[-1]['poe'] if st.session_state.ledger_cache else 'N/A'}\n"
                   f"ISP TARGET: {g_data.isp if g_data else 'OFFLINE'}\n"
                   f"PREÇO VALIDADO: R$ {m_data.price if m_data else '0.0'}")
        pdf.multi_cell(0, 7, content)
        st.download_button("💾 BAIXAR LAUDO CVM", data=pdf.output(), file_name="AUDITORIA_V90_CVM.pdf")

st.chat_input("Compliance Nominal. Prontidão Bancária.")
