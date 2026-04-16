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

# [PROTOCOL 01: NEURAL-STUB FAILSAFE v96]
PYDANTIC_ACTIVE = False
try:
    from pydantic import BaseModel, ValidationError, Field
    PYDANTIC_ACTIVE = True
except ImportError:
    class BaseModel: 
        def __init__(self, **kwargs): self.__dict__.update(kwargs)
        def dict(self): return self.__dict__
    def Field(*args, **kwargs): return None

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

# [PROTOCOL 02: INTEGRIDADE & PERSISTÊNCIA DEFINITIVA]
VAULT_FILE = ".xeon_vault"
LEDGER_FILE = "xeon_ledger.jsonl"

def get_script_integrity():
    try:
        with open(__file__, "rb") as f: return hashlib.sha3_256(f.read()).hexdigest()
    except: return "XEON_v96_PERPETUAL_CUSTODY_CORE"

def load_or_create_vault():
    """Garante que a chave de criptografia persista entre reboots"""
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "rb") as f: return f.read()
    key = AESGCM.generate_key(bit_length=256)
    with open(VAULT_FILE, "wb") as f: f.write(key)
    return key

SCRIPT_HASH = get_script_integrity()
MASTER_KEY = load_or_create_vault()

# [SCHEMA VALIDATION]
class GeoIntel(BaseModel):
    query: str = "0.0.0.0"
    isp: str = "Unknown"
    lat: float = 0.0
    lon: float = 0.0
    as_info: str = ""

# [PROTOCOL 03: UI BLACKOUT SUPREMA]
st.set_page_config(page_title="XEON COMMAND v96.0", layout="wide")
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
        border: 1px solid #00FF41 !important; border-radius: 0px; font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# [PROTOCOL 04: KERNEL v96 - PERSISTENT VAULT]
if 'kernel_v96' not in st.session_state:
    st.session_state.priv_key = ec.generate_private_key(ec.SECP256R1())
    st.session_state.mfa_token = hashlib.sha256(MASTER_KEY).hexdigest()[:8].upper()
    st.session_state.mfa_auth = False
    st.session_state.ledger_cache = []
    st.session_state.kernel_v96 = True
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                for line in f: st.session_state.ledger_cache.append(json.loads(line))
        except: pass

if not st.session_state.mfa_auth:
    st.title("🛡️ XEON MFA - PERPETUAL KEY REQUIRED")
    st.warning(f"TOKEN DE SESSÃO: {st.session_state.mfa_token}")
    token = st.text_input("AUTENTICAÇÃO NEURAL", type="password")
    if st.button("DESBLOQUEAR ACESSO"):
        if token == st.session_state.mfa_token:
            st.session_state.mfa_auth = True
            st.rerun()
    st.stop()

# [PROTOCOL 05: RECOVERY-DRIVEN DATA INGESTION]
async def fetch_v96_intel():
    # Headers avançados para evitar 403 do Yahoo
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
        try:
            m_resp = await client.get("https://yahoo.com")
            m_resp.raise_for_status()
            price = m_resp.json()['chart']['result'][0]['meta']['regularMarketPrice']
            
            g_resp = await client.get("http://ip-api.com")
            geo_raw = g_resp.json()
            geo_validated = GeoIntel(query=geo_raw['query'], isp=geo_raw['isp'], lat=geo_raw['lat'], lon=geo_raw['lon'], as_info=geo_raw['as'])
            
            return price, geo_validated
        except Exception as e:
            return 0.0, None

def secure_commit_v96(data):
    aesgcm = AESGCM(MASTER_KEY)
    nonce = os.urandom(12)
    payload = json.dumps(data)
    new_hash = hashlib.sha3_512(payload.encode()).hexdigest()
    cipher_blob = aesgcm.encrypt(nonce, payload.encode(), None)
    entry = {"n": nonce.hex(), "b": cipher_blob.hex(), "poe": new_hash, "ts": datetime.datetime.now().isoformat()}
    with open(LEDGER_FILE, "a") as f: f.write(json.dumps(entry) + "\n")
    st.session_state.ledger_cache.append(entry)
    return new_hash

# [PROTOCOL 06: DASHBOARD]
price, geo = asyncio.run(fetch_v96_intel())

st.title(f"🛰️ XEON COMMAND v96.0 | PERPETUAL VAULT")

c1, c2, c3, c4 = st.columns(4)
c1.metric("VAULT STATE", "PERSISTENT", delta="KEY RECOVERABLE")
c2.metric("CORE HASH", SCRIPT_HASH[:12])
c3.metric("YDUQ3.SA", f"R$ {price}")
c4.metric("LEDGER SIZE", f"{len(st.session_state.ledger_cache)} BLKS")

t1, t2, t3 = st.tabs(["📊 TELEMETRIA DEFINITIVA", "🛡️ LEDGER CUSTODY", "📑 RELATÓRIO IMUTÁVEL"])

with t1:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Persistent Infrastructure Data")
        st.write(f"🏢 **ISP:** {geo.isp if geo else 'RECOVERY MODE'}")
        st.write(f"🌍 **IP:** {geo.query if geo else '0.0.0.0'}")
        st.write(f"🔒 **Vault Key Hash:** {hashlib.sha256(MASTER_KEY).hexdigest()[:16]}...")
    
    with col_r:
        st.subheader("Geospatial Intel")
        if geo and geo.lat != 0:
            df_map = pd.DataFrame({'lat': [geo.lat], 'lon': [geo.lon]})
            fig_map = px.scatter_mapbox(df_map, lat="lat", lon="lon", zoom=10, height=250)
            fig_map.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="black", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

with t2:
    if st.button("🚀 COMMIT PERPETUAL BLOCK"):
        if price > 0 and geo:
            poe = secure_commit_v96({"p": price, "g": geo.dict()})
            st.success(f"PROVA DE EXISTÊNCIA (PoE) PERSISTENTE: {poe[:32]}...")
    st.dataframe(pd.DataFrame(st.session_state.ledger_cache).tail(10), use_container_width=True)

with t3:
    st.error("LAUDO DE CUSTÓDIA PERPÉTUA: XEON v96")
    if st.button("📑 GERAR DOSSIÊ CRIPTOGRÁFICO"):
        pdf = FPDF(); pdf.add_page(); pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "XEON v96.0 - PERPETUAL AUDIT REPORT", 0, 1, 'C'); pdf.ln(10)
        content = (f"DATA: {datetime.datetime.now()}\n"
                   f"MASTER KEY HASH: {hashlib.sha256(MASTER_KEY).hexdigest()}\n"
                   f"TICKER: YDUQ3.SA (R$ {price})\n"
                   f"ISP: {geo.isp if geo else 'OFFLINE'}\n"
                   f"INTEGRIDADE CORE: {SCRIPT_HASH}")
        pdf.set_font("Helvetica", "", 10); pdf.multi_cell(0, 7, content)
        st.download_button("💾 DOWNLOAD CERTIFICADO", data=pdf.output(), file_name="XEON_v96_CUSTODY.pdf")

st.chat_input("Vault v96 Nominal. Custódia Ativa.")
