import streamlit as st
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [CONFIGURAÇÃO DE MISSÃO CRÍTICA] ---
st.set_page_config(page_title="XEON OMNI v101.82", layout="wide", page_icon="🛰️")

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

# --- [MOTOR DE DADOS GLOBAIS COM FALLBACK (ERRO ZERO)] ---
def fetch_apis_resilient():
    try:
        # Puxa dados reais do S&P 500, USD/BRL e BTC
        data = yf.download(["^GSPC", "USDBRL=X", "BTC-USD"], period="1d", interval="1m", progress=False)
        # Se os dados vierem vazios, aciona fallback
        if data.empty or data['Close'].iloc[-1].isna().any():
             return {"sp500": 5240.15, "usd": 5.1245, "btc": 68450.20, "state": "FALLBACK-SAFE"}
        
        return {
            "sp500": data['Close']['^GSPC'].iloc[-1], 
            "usd": data['Close']['USDBRL=X'].iloc[-1], 
            "btc": data['Close']['BTC-USD'].iloc[-1],
            "state": "REAL-TIME"
        }
    except:
        return {"sp500": 5240.15, "usd": 5.1245, "btc": 68450.20, "state": "FALLBACK-SAFE"}

# --- [GERADOR DE PDF DE 6 PÁGINAS] ---
def make_secure_pdf(sector, token, intel):
    pdf = FPDF()
    pages = ["CONFORMIDADE NIST", "INTELIGÊNCIA DE MERCADO", "DEFESA CIBERNÉTICA", "GOVERNANÇA JURÍDICA", "EVIDÊNCIA EB-1A", "HOMEOSTASE FINAL"]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"XEON AUDIT - {sector}", ln=True, align='C')
        pdf.set_font("Courier", "B", 10); pdf.cell(0, 10, f"PAGE {i}/6 | TOKEN: {token}", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 11)
        content = (f"SETOR: {pages[i-1]}\n\n"
                   f"MÉTRICAS DO SISTEMA:\n- S&P500: {intel['sp500']:.2f}\n- USD/BRL: {intel['usd']:.4f}\n- BTC: {intel['btc']:.2f}\n\n"
                   f"ESTADO DO MOTOR: {intel['state']}\n" + "-"*50 + 
                   "\nAUTOR: ARQUITETO MARCO ANTONIO DO NASCIMENTO\nRELATÓRIO PARA PROTEÇÃO DE INFRAESTRUTURA CRÍTICA.")
        pdf.multi_cell(0, 8, content)
    return bytes(pdf.output())

# --- [INTERFACE PRINCIPAL] ---
st.title("🛰️ XEON COMMAND v101.82 | SOH v2.2")
intel = fetch_apis_resilient()

col_v, col_g = st.columns([1, 1.5])

with col_v:
    st.write("### 🗣️ INTERFACE VOCAL GRC")
    if st.button("🔊 EXECUTAR STATUS VOCAL"):
        components.html("""<script>var m = new SpeechSynthesisUtterance("Xeon Ativo. Monitorando APIs Mundiais."); window.speechSynthesis.speak(m);</script>""", height=0)
    
    # Métrica Resolvida (Fallback automático impede o "nan")
    st.metric("S&P 500 GLOBAL INDEX", f"{intel['sp500']:.2f}", f"STATE: {intel['state']}")
    
    # NOVO: BOTÃO DE RECALIBRAGEM
    if st.button("🔄 RECALIBRAR APIs GLOBAIS"):
        st.cache_data.clear()
        st.rerun()

with col_g:
    st.write("### 🕸️ TOPOLOGIA DA MALHA (OPERACIONAL)")
    options = {
        "backgroundColor": "#000",
        "series": [{"type": "graph", "layout": "force", "symbolSize": 55, "roam": True,
            "label": {"show": True, "color": "#00FF41", "fontWeight": "bold"},
            "force": {"repulsion": 1000},
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
        if st.button(f"🚀 ATIVAR NÓ 0{i+1}", key=f"exe_{i}"):
            token = hashlib.sha256(str(time.time()).encode()).hexdigest().upper()[:16]
            with st.status(f"Processando {setor}...", expanded=True):
                time.sleep(1)
                st.write(f"Hash: {token}")
            
            pdf_bytes = make_secure_pdf(setor, token, intel)
            st.download_button(
                label="📥 BAIXAR RELATÓRIO (6 PÁGINAS)",
                data=pdf_bytes,
                file_name=f"XEON_AUDIT_{i+1}.pdf",
                mime="application/pdf",
                key=f"dl_{i}"
            )

st.caption(f"ARQUITETO: MARCO ANTONIO | XEON COMMAND SOH | {time.strftime('%Y')}")
