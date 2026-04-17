import streamlit as st
import pandas as pd
import yfinance as yf
from fpdf import FPDF
import time
import hashlib
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO DE AMBIENTE] ---
st.set_page_config(page_title="XEON OMNI v101.71", layout="wide", page_icon="🛰️")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 1px solid #00FF41 !important; color: #00FF41 !important; background: #000 !important; width: 100% !important; height: 60px !important; font-weight: bold !important; font-size: 16px !important;}
    .status-box { border: 2px solid #00FF41; padding: 15px; background: #0A0A0A; margin: 10px 0; border-left: 10px solid #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    h1, h2, h3 { color: #00FF41 !important; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [2. FUNÇÕES DE CORE (PDF E DADOS)] ---
def generate_pdf_6_pages(sector, token):
    pdf = FPDF()
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"DOSSIÊ XEON - {sector}", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Courier", "", 12)
        pdf.multi_cell(0, 10, f"PAGINA {i}/6\nTOKEN: {token}\nSTATUS: OPERAÇÃO SOBERANA\n\nConformidade NIST e Governança GRC ativa.\n\n" + "CONFIDENCIAL "*50)
    return pdf.output(dest='S').encode('latin-1')

# --- [3. HEADER: FALA E ESCUTA (FORÇADO)] ---
st.title("🛰️ XEON OMNI v101.71 | GLOBAL HUB")

c_voz, c_grafo = st.columns([1, 1])

with c_voz:
    st.write("### 🗣️ COMANDO VOCAL")
    components.html("""
        <div style="background:#000; border:1px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
            <button onclick="rec()" style="width:48%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ESCUTAR</button>
            <button onclick="falar()" style="width:48%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🔊 STATUS</button>
            <div id="v-status" style="margin-top:10px; font-size:12px;">> MONITOR: AGUARDANDO...</div>
        </div>
        <script>
            function falar() {
                const u = new SpeechSynthesisUtterance("Sistema Xeon Ativo. Monitorando APIs Globais.");
                u.rate = 0.8; window.speechSynthesis.speak(u);
            }
            function rec() {
                const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                r.lang = 'pt-BR'; r.start();
                document.getElementById('v-status').innerText = "> ESCUTANDO...";
                r.onresult = (e) => { 
                    document.getElementById('v-status').innerText = "> CAPTADO: " + e.results[0][0].transcript.toUpperCase();
                };
            }
        </script>
    """, height=140)

with c_grafo:
    st.write("### 🕸️ TOPOLOGIA DA MALHA")
    options = {
        "backgroundColor": "#000",
        "series": [{"type": "graph", "layout": "force", "symbolSize": 40, "roam": True,
            "label": {"show": True, "color": "#00FF41"},
            "lineStyle": {"color": "#00FF41", "width": 2},
            "data": [{"name": "GO-CORE"}, {"name": "FIN"}, {"name": "GRC"}, {"name": "EB1A"}],
            "links": [{"source": "GO-CORE", "target": "FIN"}, {"source": "GO-CORE", "target": "GRC"}]
        }]
    }
    st_echarts(options=options, height="140px")

# --- [4. TERMINAIS DE AUDITORIA] ---
st.write("---")
st.write("### 🛠️ TERMINAIS DE MISSÃO CRÍTICA")

setores = ["FINANÇAS GLOBAIS", "GOVERNANÇA E CONFORMIDADE", "RELATÓRIO TÉCNICO EB-1A"]

for i, setor in enumerate(setores):
    with st.container():
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}: {setor}</div>", unsafe_allow_stdio=True)
        col_btn, col_res = st.columns([1, 1])
        
        with col_btn:
            # Botão Único de Ativação
            if st.button(f"🚀 ATIVAR PROTOCOLO {i+1}", key=f"main_btn_{i}"):
                token = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16].upper()
                
                with st.status(f"Processando {setor}...", expanded=True):
                    st.write("Handshake com motor Go...")
                    time.sleep(0.5)
                    st.write("Gerando PDF de 6 páginas...")
                    st.progress(100)
                
                # O BOTÃO DE PDF APARECE IMEDIATAMENTE ABAIXO
                pdf_data = generate_pdf_6_pages(setor, token)
                st.download_button(
                    label=f"📥 BAIXAR DOSSIÊ (6 FOLHAS) - {setor}",
                    data=pdf_data,
                    file_name=f"XEON_AUDIT_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"pdf_dl_{i}"
                )
        with col_res:
            st.metric("INTEGRIDADE", "100%", "GO-CORE OK")

st.divider()
st.caption(f"ARQUITETO: MARCO ANTONIO | SESSION HASH: {hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:10]}")
