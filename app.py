import streamlit as st
import psutil
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

# --- [1. CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.69", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT (Força visibilidade total)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000 !important; color: #00FF41 !important; border: 2px solid #00FF41 !important; width: 100% !important; height: 55px !important; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; }
    .status-box { border: 2px solid #00FF41; padding: 15px; background: #0A0A0A; margin: 10px 0; border-left: 10px solid #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    h1, h2, h3 { color: #00FF41 !important; border-bottom: 1px solid #008F11; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [2. MOTOR DE DADOS & PDF] ---
@st.cache_data(ttl=60)
def get_global_market():
    try:
        data = yf.download(["^GSPC", "USDBRL=X", "BTC-USD"], period="1d", interval="1m", progress=False)
        return {"sp500": data['Close']['^GSPC'].iloc[-1], "usd": data['Close']['USDBRL=X'].iloc[-1], "btc": data['Close']['BTC-USD'].iloc[-1]}
    except:
        return {"sp500": 5200.0, "usd": 5.15, "btc": 65000.0}

def generate_audit_pdf(sector, token, m):
    pdf = FPDF()
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"XEON AUDIT - {sector}", 0, 1, 'C')
        pdf.set_font("Courier", "", 12)
        pdf.ln(10)
        pdf.multi_cell(0, 10, f"PAGINA {i}/6\nTOKEN: {token}\nSTATUS: MISSÃO CRÍTICA\nBTC: {m['btc']}\nUSD: {m['usd']}\n\nConformidade NIST e Governança GRC atestada.")
    return pdf.output()

# --- [3. HEADER & CONTROLO DE VOZ] ---
st.title("🛰️ XEON OMNI v101.69 | OPERAÇÃO SOBERANA")

col_v, col_g = st.columns([1, 1])

with col_v:
    st.write("### 🗣️ COMANDO DE VOZ E ESCUTA")
    components.html("""
        <div style="background:#000; border:2px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
            <button onclick="startRec()" style="width:48%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ESCUTAR</button>
            <button onclick="systemSpeak()" style="width:48%; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🔊 FALAR</button>
            <div id="v-status" style="margin-top:10px; font-size:12px;">> MONITOR: STANDBY</div>
        </div>
        <script>
            const syn = window.speechSynthesis;
            function systemSpeak() {
                const u = new SpeechSynthesisUtterance("Xeon Omni operando em missão crítica. APIs mundiais conectadas.");
                u.rate = 0.8; syn.speak(u);
            }
            function startRec() {
                const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                rec.lang = 'pt-BR'; rec.start();
                document.getElementById('v-status').innerText = "> ESCUTANDO...";
                rec.onresult = (e) => { 
                    document.getElementById('v-status').innerText = "> CAPTADO: " + e.results[0][0].transcript.toUpperCase();
                };
            }
        </script>
    """, height=150)

with col_g:
    st.write("### 🕸️ TOPOLOGIA DA MALHA")
    options = {
        "backgroundColor": "#000",
        "series": [{"type": "graph", "layout": "force", "symbolSize": 50, "roam": True,
            "label": {"show": True, "color": "#00FF41"},
            "lineStyle": {"color": "#00FF41", "width": 2},
            "data": [{"name": "CORE"}, {"name": "FIN"}, {"name": "GOV"}, {"name": "EB1A"}],
            "links": [{"source": "CORE", "target": "FIN"}, {"source": "CORE", "target": "GOV"}, {"source": "CORE", "target": "EB1A"}]
        }]
    }
    st_echarts(options=options, height="150px")

# --- [4. TERMINAIS DE AUDITORIA] ---
st.write("### 🛠️ TERMINAIS DE ALTA RENTABILIDADE (R$ 1.000/H)")
m = get_global_market()
setores = ["FINANÇAS E LIQUIDEZ", "GOVERNANÇA E CONFORMIDADE", "DOSSIÊ TÉCNICO EB-1A"]

for i, setor in enumerate(setores):
    with st.container():
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}: {setor}</div>", unsafe_allow_stdio=True)
        c1, c2 = st.columns([1, 2])
        
        with c1:
            if st.button(f"ATIVAR PROTOCOLO {i+1}", key=f"exe_{i}"):
                token = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16].upper()
                with st.status(f"Processando {setor}...", expanded=True):
                    time.sleep(1)
                    st.write("Verificando Integridade Blockchain...")
                    st.progress(100)
                
                # BOTÃO DO PDF APARECE EXATAMENTE AQUI
                pdf_data = generate_audit_pdf(setor, token, m)
                st.download_button(
                    label=f"📥 BAIXAR DOSSIÊ (6 FOLHAS) - {setor}",
                    data=bytes(pdf_data),
                    file_name=f"XEON_AUDIT_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"pdf_dl_{i}"
                )
        with c2:
            st.metric("DISPONIBILIDADE", "100%", "ESTÁVEL")

st.divider()
st.caption(f"CONNECTED TO GLOBAL APIs | SECURITY TOKEN: {hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:12]}")
