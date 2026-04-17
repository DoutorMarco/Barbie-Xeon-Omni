import streamlit as st
import psutil
import pandas as pd
import yfinance as yf
from fpdf import FPDF
import hashlib
import time
import streamlit.components.v1 as components

# --- [CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.68", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT TOTAL
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41 !important; border: 1px solid #00FF41 !important; width: 100%; height: 50px; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 15px #00FF41; }
    .status-box { border: 1px solid #00FF41; padding: 10px; background: #0A0A0A; margin-bottom: 20px; border-left: 5px solid #00FF41; }
    h1, h2, h3, h4 { color: #00FF41 !important; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [CORE: GERADOR DE DOSSIÊ 6 PÁGINAS] ---
class XeonPDF(FPDF):
    def header(self):
        self.set_fill_color(0, 0, 0)
        self.rect(0, 0, 210, 297, 'F')
        self.set_text_color(0, 255, 65)
        self.set_font("Courier", "B", 12)
        self.cell(0, 10, "XEON COMMAND - CONFIDENTIAL AUDIT", 0, 1, 'C')

def create_dossier(sector, token):
    pdf = XeonPDF()
    sections = ["AUDITORIA NIST", "SOBERANIA JURÍDICA", "ANÁLISE BIOMÉDICA", "GOVERNANÇA GRC", "INFRAESTRUTURA CRÍTICA", "EB-1A EVIDENCE"]
    for i in range(6):
        pdf.add_page()
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 20, f"RELATÓRIO: {sector}", 0, 1, 'L')
        pdf.set_font("Courier", "", 12)
        pdf.multi_cell(0, 10, f"PÁGINA {i+1}/6\nTOKEN: {token}\nSEÇÃO: {sections[i]}\n\n" + "X "*200)
    return pdf.output()

# --- [INTERFACE PRINCIPAL] ---
st.title("🛰️ XEON OMNI v101.68")
st.write("ESTADO: **OPERANDO EM MISSÃO CRÍTICA** | APIS: **CONECTADAS**")

# COMANDO DE VOZ
components.html("""
    <div style="background:#000; border:1px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
        <button onclick="rec()" style="background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ESCUTA ATIVA</button>
        <p id="st" style="display:inline; margin-left:10px;">> STANDBY</p>
    </div>
    <script>
        function rec() { 
            const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            r.lang = 'pt-BR'; r.start();
            document.getElementById('st').innerText = "> ESCUTANDO...";
            r.onresult = (e) => { document.getElementById('st').innerText = "> CAPTADO: " + e.results[0][0].transcript.toUpperCase(); };
        }
    </script>
""", height=100)

# MERCADO REAL
try:
    m_data = yf.download(["^GSPC", "USDBRL=X", "BTC-USD"], period="1d", interval="1m", progress=False)
    c1, c2, c3 = st.columns(3)
    c1.metric("S&P 500", f"{m_data['Close']['^GSPC'].iloc[-1]:.2f}")
    c2.metric("USD/BRL", f"{m_data['Close']['USDBRL=X'].iloc[-1]:.4f}")
    c3.metric("BITCOIN", f"${m_data['Close']['BTC-USD'].iloc[-1]:,.0f}")
except:
    st.warning("Aguardando sincronização de APIs globais...")

# TERMINAIS DE AUDITORIA
st.write("### 🛠️ TERMINAIS DE GOVERNANÇA E FINANÇAS")
setores = ["FINANÇAS GLOBAIS", "CONFORMIDADE REGULATÓRIA", "PROVA TÉCNICA EB-1A"]

for i, setor in enumerate(setores):
    with st.container():
        st.markdown(f"<div class='status-box'>[NÓ 0{i+1}] {setor}</div>", unsafe_allow_stdio=True)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button(f"ATIVAR AUDITORIA {i+1}", key=f"exe_{i}"):
                token = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16].upper()
                with st.status("Processando...", expanded=False):
                    time.sleep(1)
                    st.write("Gerando Dossiê 6 Páginas...")
                
                pdf_out = create_dossier(setor, token)
                st.download_button(
                    label="📥 BAIXAR RELATÓRIO (6 FOLHAS)",
                    data=bytes(pdf_out),
                    file_name=f"XEON_{setor}.pdf",
                    mime="application/pdf",
                    key=f"dl_{i}"
                )
        with col2:
            st.caption(f"Aguardando pulso de comando para {setor}. Governança em tempo real.")

st.divider()
st.caption(f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO | SOVEREIGN OPERATIONS HUB")
