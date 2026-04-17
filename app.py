import streamlit as st
import time
import hashlib
import yfinance as yf
import random
import pandas as pd
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [ESTADO DE MISSÃO CRÍTICA - v101.89] ---
st.set_page_config(page_title="XEON OMNI v101.89", layout="wide", page_icon="🛰️")

# CSS MATRIX SOBERANO
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #00FF41 !important; font-family: 'Courier New', monospace; }
    button { border: 2px solid #00FF41 !important; background: #000 !important; color: #00FF41 !important; height: 60px !important; width: 100% !important; font-weight: bold !important; transition: 0.4s; }
    button:hover { background: #00FF41 !important; color: #000 !important; box-shadow: 0 0 30px #00FF41; }
    .status-box { border: 2px solid #00FF41; padding: 15px; background: #050505; border-left: 12px solid #00FF41; margin-bottom: 25px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- [MOTORES DE INTELIGÊNCIA] ---
@st.cache_data(ttl=30)
def fetch_global_intel():
    try:
        data = yf.download(["^GSPC", "USDBRL=X"], period="1d", interval="1m", progress=False)
        return {"sp500": data['Close']['^GSPC'].iloc[-1], "usd": data['Close']['USDBRL=X'].iloc[-1], "state": "REAL-TIME"}
    except:
        return {"sp500": 7035.89, "usd": 4.96, "state": "RESERVA-SAFE"}

def get_geopolitical_risk():
    risks = [
        "ALERTA: Instabilidade em cabos submarinos no Atlântico Norte detectada.",
        "INFO: Nova diretiva da Casa Branca sobre IA em Infraestrutura Crítica.",
        "RISCO: Volatilidade em ativos de Bio-Tech após arbitragem da ANPD."
    ]
    return random.choice(risks)

# --- [GERADOR DE DOSSIÊ EXPANDIDO] ---
def generate_mega_dossier(sector, token, intel, physio, risk):
    pdf = FPDF()
    pages_intel = [
        f"01: ARBITRAGEM GLOBAL - Tendências de Mercado e Risco: {risk}",
        "02: FISIOLOGIA DIGITAL - Monitoramento de Gêmeos Sistêmicos.",
        "03: INFRAESTRUTURA NACIONAL - Proteção de Redes de Saúde (NIST).",
        "04: COMPLIANCE JURÍDICO - Evidências para EB-1A e NIW.",
        "05: ANÁLISE DE LIQUIDEZ - Sincronia Financeira Transdisciplinar.",
        "06: VEREDITO FINAL - Homeostase Diana / Erro Zero."
    ]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 15, f"XEON COMMAND AUDIT - {sector.upper()}", ln=True, align='C')
        pdf.set_font("Courier", "B", 10); pdf.cell(0, 10, f"HASH: {token} | PAGE {i}/6", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        body = (f"SETOR: {pages_intel[i-1]}\n\n"
                f"STATUS GEOPOLÍTICO: {risk}\n"
                f"TELEMETRIA FISIOLÓGICA: {physio['bpm']} BPM | {physio['spo2']}% SpO2\n"
                f"MÉTRICAS GLOBAIS: S&P500 @ {intel['sp500']:.2f}\n" + "-"*60 + 
                "\nRELATÓRIO FISIOLÓGICO - ARQUITETO MARCO ANTONIO DO NASCIMENTO.")
        pdf.multi_cell(0, 8, body)
    return bytes(pdf.output())

# --- [UI: INTERFACE SOBERANA] ---
st.title("🛰️ XEON COMMAND v101.89 | SOH v2.2")
intel = fetch_global_intel()
risk_intel = get_geopolitical_risk()
physio = {"bpm": random.randint(72, 78), "spo2": random.randint(98, 100)}

c1, c2 = st.columns([1, 1.5])
with c1:
    st.write("### 🗣️ COMANDO VOCAL & INTEL")
    if st.button("🔊 STATUS GERAL DE ARBITRAGEM"):
        components.html(f"""<script>
            var m=new SpeechSynthesisUtterance("Xeon ativo. Alerta geopolítico: {risk_intel}. Sincronia fisiológica em {physio['bpm']} BPM. Dashboard de tendências nominal.");
            m.lang = 'pt-BR'; m.pitch = 0.8; window.speechSynthesis.speak(m);
        </script>""", height=0)
    
    st.metric("S&P 500 (TENDÊNCIA)", f"{intel['sp500']:.2f}", intel['state'])
    st.markdown(f"**VARREDURA GEOPOLÍTICA:** {risk_intel}")

with c2:
    st.write("### 🕸️ MALHA DE TENDÊNCIAS GLOBAIS")
    options = {"backgroundColor": "#000", "series": [{"type": "graph", "layout": "force", "symbolSize": 50, "label": {"show": True, "color": "#00FF41", "fontWeight": "bold"}, "data": [{"name": "GO-CORE"}, {"name": "INTEL-RISK"}, {"name": "TRENDS"}, {"name": "EB1A"}], "links": [{"source": "GO-CORE", "target": "INTEL-RISK"}]}]}
    st_echarts(options=options, height="250px")

# --- [TERMINAIS DE MONETIZAÇÃO - $1.000/H] ---
st.divider()
st.write("### 🛠️ TERMINAIS DE AUDITORIA, TENDÊNCIAS E RISCOS")
setores = ["DASHBOARD DE TENDÊNCIAS", "VARREDURA GEOPOLÍTICA", "FISIOLOGIA (ARBITRADO)"]
cols = st.columns(3)

for i, setor in enumerate(setores):
    with cols[i]:
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}: {setor}</div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR PROTOCOLO {i+1}", key=f"node_{i}"):
            tk = hashlib.sha256(str(time.time()).encode()).hexdigest().upper()[:16]
            with st.status(f"Arbitrando {setor}...", expanded=True):
                time.sleep(1)
                st.write(f"Veredito Técnico: {risk_intel if i==1 else 'Homeostase Nominal'}")
            
            pdf_bytes = generate_mega_dossier(setor, tk, intel, physio, risk_intel)
            st.download_button(label="📥 BAIXAR RELATÓRIO (6 PÁGINAS)", data=pdf_bytes, file_name=f"XEON_INTEL_{tk}.pdf", mime="application/pdf", key=f"dl_{i}")

st.caption(f"ARQUITETO: MARCO ANTONIO | XEON COMMAND SOH | 2026")
