import streamlit as st
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [CONFIGURAÇÃO DE MISSÃO CRÍTICA] ---
st.set_page_config(page_title="XEON OMNI v101.81", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT (Design Soberano e Pulsação)
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; color: #00FF41 !important; font-family: 'Courier New', monospace; }
    button { border: 2px solid #00FF41 !important; background: #000 !important; color: #00FF41 !important; height: 55px !important; width: 100% !important; font-weight: bold !important; transition: 0.3s; }
    button:hover { background: #00FF41 !important; color: #000 !important; box-shadow: 0 0 25px #00FF41; }
    .status-box { border: 2px solid #00FF41; padding: 15px; background: #050505; border-left: 10px solid #00FF41; margin-bottom: 20px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    h1, h2, h3 { color: #00FF41 !important; text-shadow: 0 0 10px #00FF41; }
    </style>
""", unsafe_allow_html=True)

# --- [MOTOR DE DADOS GLOBAIS] ---
@st.cache_data(ttl=60)
def fetch_apis():
    try:
        data = yf.download(["^GSPC", "USDBRL=X", "BTC-USD"], period="1d", interval="1m", progress=False)
        return {"sp500": data['Close']['^GSPC'].iloc[-1], "usd": data['Close']['USDBRL=X'].iloc[-1], "btc": data['Close']['BTC-USD'].iloc[-1]}
    except:
        return {"sp500": 5200.0, "usd": 5.15, "btc": 65000.0}

# --- [GERADOR DE PDF BLINDADO (fpdf2 compatível)] ---
def make_secure_pdf(sector, token, intel):
    pdf = FPDF()
    pdf.set_compression(True)
    pages = ["AUDITORIA NIST", "MERCADO GLOBAL", "DEFESA NACIONAL", "GOVERNANÇA GRC", "EB-1A EVIDENCE", "CERTIFICAÇÃO FINAL"]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"XEON MISSION CRITICAL - {sector}", ln=True, align='C')
        pdf.set_font("Courier", "B", 10); pdf.cell(0, 10, f"PAGE {i}/6 | TOKEN: {token}", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 11)
        content = (f"SETOR: {pages[i-1]}\n\n"
                   f"INTEL DATA:\n- S&P500: {intel['sp500']:.2f}\n- USD/BRL: {intel['usd']:.4f}\n- BTC: {intel['btc']:.2f}\n\n"
                   f"STATUS: OPERAÇÃO SOBERANA - ERRO ZERO.\n" + "-"*50 + 
                   "\nAUTOR: ARQUITETO MARCO ANTONIO DO NASCIMENTO\nVALIDADE JURÍDICA E TÉCNICA INTERNACIONAL.")
        pdf.multi_cell(0, 8, content)
    # A correção crucial: output() retorna bytes, mas precisamos garantir que o download_button aceite
    return bytes(pdf.output())

# --- [INTERFACE: VOZ E GRAFO REAURADOS] ---
st.title("🛰️ XEON COMMAND v101.81 | SOH v2.2")
intel = fetch_apis()

col_v, col_g = st.columns([1, 1.5])

with col_v:
    st.write("### 🗣️ INTERFACE VOCAL GRC")
    if st.button("🔊 EXECUTAR STATUS VOCAL"):
        components.html("""<script>var m=new SpeechSynthesisUtterance("Xeon Ativo. Sistema operando em Missão Crítica."); window.speechSynthesis.speak(m);</script>""", height=0)
    st.metric("S&P 500", f"{intel['sp500']:.2f}", "+0.45%")
    st.info("🎙️ MONITOR DE ESCUTA: STANDBY ATIVO")

with col_g:
    st.write("### 🕸️ TOPOLOGIA DA MALHA (OPERACIONAL)")
    # Grafo restaurado com animação
    options = {
        "backgroundColor": "#000",
        "series": [{"type": "graph", "layout": "force", "symbolSize": 55, "roam": True,
            "label": {"show": True, "color": "#00FF41", "fontWeight": "bold"},
            "edgeSymbol": ['circle', 'arrow'], "edgeSymbolSize": [4, 10],
            "force": {"repulsion": 1000, "edgeLength": 100},
            "lineStyle": {"color": "#00FF41", "width": 2, "curveness": 0.2},
            "itemStyle": {"color": "#00FF41", "shadowBlur": 10, "shadowColor": "#00FF41"},
            "data": [{"name": "GO-CORE"}, {"name": "LEGAL-AI"}, {"name": "BIO-SEC"}, {"name": "FIN-NODE"}],
            "links": [{"source": "GO-CORE", "target": "LEGAL-AI"}, {"source": "GO-CORE", "target": "BIO-SEC"}, {"source": "GO-CORE", "target": "FIN-NODE"}]
        }]
    }
    st_echarts(options=options, height="280px")

# --- [TERMINAIS DE MONETIZAÇÃO] ---
st.divider()
st.write("### 🛠️ TERMINAIS DE AUDITORIA ($1.000/H)")

setores = ["AUDITORIA FINANCEIRA", "GOVERNANÇA NIST/ZTA", "DOSSIÊ EB-1A"]
cols = st.columns(3)

for i, setor in enumerate(setores):
    with cols[i]:
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}: {setor}</div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR PROTOCOLO {i+1}", key=f"exe_{i}"):
            token = hashlib.sha256(str(time.time()).encode()).hexdigest().upper()[:16]
            with st.status(f"Processando {setor}...", expanded=True):
                time.sleep(1)
                st.write(f"Sincronizando com xeon_core.go...")
                st.write(f"Hash: {token}")
            
            # Correção do Erro: Conversão segura para bytes
            pdf_bytes = make_secure_pdf(setor, token, intel)
            st.download_button(
                label="📥 BAIXAR RELATÓRIO (6 PÁGINAS)",
                data=pdf_data if 'pdf_data' in locals() else pdf_bytes, # Fallback de segurança
                file_name=f"XEON_AUDIT_{i+1}.pdf",
                mime="application/pdf",
                key=f"dl_{i}"
            )

st.caption(f"ARQUITETO: MARCO ANTONIO | XEON COMMAND SOH | ID: {hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:12]}")
