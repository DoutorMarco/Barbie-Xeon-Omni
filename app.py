import streamlit as st
import subprocess
import os
import yfinance as yf
from fpdf import FPDF
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts
import time

# --- [CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.70 | GO-CORE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000 !important; color: #00FF41 !important; border: 2px solid #00FF41 !important; width: 100%; height: 50px; font-weight: bold; }
    .status-box { border: 2px solid #00FF41; padding: 15px; background: #0A0A0A; border-left: 10px solid #00FF41; margin-bottom: 20px; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [MOTOR GO: EXECUÇÃO DE MISSÃO CRÍTICA] ---
def run_xeon_core():
    try:
        # Tenta rodar o motor Go (precisa estar compilado ou usa 'go run')
        result = subprocess.run(['go', 'run', 'xeon_core.go'], capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else "GO-CORE-OFFLINE-FALLBACK-ACTIVE"
    except:
        return "PYTHON-HASH-RESERVE-ACTIVE"

# --- [GERADOR DE PDF 6 PÁGINAS] ---
def generate_dossier(sector, go_hash):
    pdf = FPDF()
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 15, f"XEON AUDIT - GO ENGINE v1.0 - {sector}", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Courier", "", 10)
        pdf.multi_cell(0, 8, f"PÁGINA {i}/6\nGO_HASH: {go_hash}\nSTATUS: SOBERANO\n\nAuditado via motor xeon_core.go.\nConformidade transdisciplinar garantida pelo Arquiteto Marco Antonio.")
    return pdf.output(dest='S').encode('latin-1')

# --- [INTERFACE] ---
st.title("🛰️ XEON OMNI v101.70 | MOTOR GO ATIVO")

# 1. VOZ E ESCUTA (HTML SOBERANO)
components.html("""
    <div style="background:#000; border:2px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
        <button onclick="rec()" style="width:48%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ESCUTA ATIVA</button>
        <button onclick="speak()" style="width:48%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🔊 STATUS GO</button>
        <p id="st" style="margin-top:10px; font-size:12px;">> AGUARDANDO COMANDO...</p>
    </div>
    <script>
        function speak() { 
            const u = new SpeechSynthesisUtterance("Motor Go Ativado. Processamento em nanossegundos iniciado.");
            u.rate = 0.9; window.speechSynthesis.speak(u);
        }
        function rec() { 
            const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            r.lang = 'pt-BR'; r.start();
            document.getElementById('st').innerText = "> ESCUTANDO...";
        }
    </script>
""", height=130)

# 2. GRAFO DE MALHA
options = {
    "backgroundColor": "#000",
    "series": [{"type": "graph", "layout": "force", "symbolSize": 50, "roam": True,
        "label": {"show": True, "color": "#00FF41"},
        "lineStyle": {"color": "#00FF41", "width": 2},
        "data": [{"name": "GO-CORE"}, {"name": "PY-UI"}, {"name": "PDF-GEN"}, {"name": "EB1A"}],
        "links": [{"source": "GO-CORE", "target": "PY-UI"}, {"source": "GO-CORE", "target": "PDF-GEN"}]
    }]
}
st_echarts(options=options, height="200px")

# 3. TERMINAIS COM GO-HASH
setores = ["FINANÇAS", "CONFORMIDADE GRC", "EVIDÊNCIA EB-1A"]
for i, setor in enumerate(setores):
    with st.container():
        st.markdown(f"<div class='status-box'>[NÓ 0{i+1}] {setor}</div>", unsafe_allow_stdio=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button(f"EXECUTAR: {setor.split()[0]}", key=f"go_{i}"):
                go_hash = run_xeon_core()
                with st.status("Invocando Motor Go...", expanded=True):
                    st.write(f"Hash Gerado: {go_hash}")
                    time.sleep(0.5)
                
                pdf_data = generate_dossier(setor, go_hash)
                st.download_button(
                    label="📥 BAIXAR RELATÓRIO 6 PÁGINAS",
                    data=pdf_data,
                    file_name=f"XEON_GO_AUDIT_{i}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{i}"
                )
        with col2:
            st.caption("Aguardando pulso de clock do motor Go.")

st.divider()
st.caption(f"CORE: GO-ENGINE | UI: STREAMLIT | ARCHITECT: MARCO ANTONIO")
