
import streamlit as st
import pandas as pd
import yfinance as yf
from fpdf import FPDF
import time
import hashlib
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [CONFIGURAÇÃO SOBERANA - LIMPEZA DE LOGS] ---
st.set_page_config(page_title="XEON OMNI v101.73", layout="wide")

# Forçando o Blackout Matrix via CSS estável
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 1px solid #00FF41 !important; color: #00FF41 !important; background: #000 !important; width: 100%; height: 50px; font-weight: bold; }
    .status-box { border: 2px solid #00FF41; padding: 15px; background: #0A0A0A; margin-bottom: 20px; border-left: 10px solid #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [GERADOR DE PDF DE 6 PÁGINAS (v2)] ---
def generate_xeon_pdf(sector, token):
    pdf = FPDF()
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65)
        # Correção do erro de fonte do log
        pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 15, f"XEON AUDIT DOSSIER - {sector}", 0, 1, 'C')
        pdf.set_font("Courier", "", 10)
        pdf.ln(10)
        pdf.multi_cell(0, 8, f"PAGINA {i}/6\nTOKEN: {token}\nSTATUS: MISSION CRITICAL\n\nEste documento atesta a conformidade NIST/ZTA e governança transdisciplinar.")
    return pdf.output(dest='S').encode('latin-1')

# --- [INTERFACE: VOZ E GRAFO] ---
st.title("🛰️ XEON OMNI | MISSION CRITICAL")

col_v, col_g = st.columns(2)

with col_v:
    st.write("### 🗣️ COMANDO VOCAL")
    # Versão atualizada do componente de HTML
    components.html("""
        <div style="background:#000; border:1px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
            <button onclick="rec()" style="width:45%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ESCUTAR</button>
            <button onclick="speak()" style="width:45%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer; margin-left:5%;">🔊 STATUS</button>
            <p id="st" style="margin-top:10px; font-size:12px;">> MONITOR: STANDBY</p>
        </div>
        <script>
            function speak() {
                const u = new SpeechSynthesisUtterance("Xeon Omni Ativo. Missão Crítica Nominal.");
                u.rate = 0.8; window.speechSynthesis.speak(u);
            }
            function rec() {
                const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                r.lang = 'pt-BR'; r.start();
                document.getElementById('st').innerText = "> ESCUTANDO...";
                r.onresult = (e) => { document.getElementById('st').innerText = "> CAPTADO: " + e.results.transcript.toUpperCase(); };
            }
        </script>
    """, height=150)

with col_g:
    st.write("### 🕸️ TOPOLOGIA DA MALHA")
    options = {
        "backgroundColor": "#000",
        "series": [{"type": "graph", "layout": "force", "symbolSize": 40, "roam": True,
            "label": {"show": True, "color": "#00FF41"},
            "lineStyle": {"color": "#00FF41", "width": 2},
            "data": [{"name": "GO-CORE"}, {"name": "LEGAL"}, {"name": "BIO"}, {"name": "FIN"}],
            "links": [{"source": "GO-CORE", "target": "LEGAL"}, {"source": "GO-CORE", "target": "FIN"}]
        }]
    }
    st_echarts(options=options, height="150px")

# --- [TERMINAIS DE AUDITORIA] ---
st.divider()
setores = ["FINANÇAS GLOBAIS", "GOVERNANÇA NIST/ZTA", "PROVA TÉCNICA EB-1A"]

for i, setor in enumerate(setores):
    with st.container():
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}: {setor}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button(f"ATIVAR NÓ 0{i+1}", key=f"btn_{i}"):
                tk = hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:16]
                with st.status(f"Gerando Dossiê {setor}...", expanded=True):
                    time.sleep(1)
                    st.write(f"Hash de Integridade: {tk}")
                    st.progress(100)
                
                pdf_data = generate_xeon_pdf(setor, tk)
                st.download_button(
                    label=f"📥 BAIXAR PDF (6 FOLHAS) - {setor.split()[0]}",
                    data=pdf_data,
                    file_name=f"XEON_AUDIT_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"dl_{i}"
                )
        with c2:
            st.metric("SITUACIONAL", "ESTÁVEL", "GO-CORE OK")

st.caption(f"ARQUITETO: MARCO ANTONIO | SESSION: {hashlib.sha1(str(time.time()).encode()).hexdigest()[:10].upper()}")
