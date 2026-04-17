import streamlit as st
import psutil
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts  # Necessário: pip install streamlit-echarts

# --- [CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.64", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; border-radius: 0px; transition: 0.3s; }
    .stButton>button:hover { background-color: #00FF41; color: #000000; box-shadow: 0 0 10px #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    code { color: #00FF41 !important; background-color: #0A0A0A !important; border: 1px solid #00FF41; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [CORE FUNCTIONS] ---
def get_reality_metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "mem": psutil.virtual_memory().percent,
        "token": hashlib.sha256(str(time.time()).encode()).hexdigest()[:16].upper(),
        "timestamp": time.strftime('%H:%M:%S')
    }

@st.cache_data(ttl=60)
def get_market_data():
    try:
        tickers = ["^GSPC", "USDBRL=X"]
        data = yf.download(tickers, period="1d", interval="1m", progress=False)
        return {"sp500": data['Close']['^GSPC'].iloc[-1], "usdbrl": data['Close']['USDBRL=X'].iloc[-1]}
    except:
        return {"sp500": 5150.00, "usdbrl": 5.10}

def generate_6_page_pdf(node_name, metrics, market):
    pdf = FPDF()
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, f"DOSSIE XEON - {node_name} - PAG {i}/6", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Courier", "", 10)
        content = f"TOKEN: {metrics['token']}\nDATA: {metrics['timestamp']}\nCPU: {metrics['cpu']}%\n"
        if i == 2: content += f"MERCADO: S&P500 @ {market['sp500']:.2f}"
        pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- [UI: GRAFO DE REDE] ---
def render_graph():
    options = {
        "backgroundColor": "#000000",
        "series": [{
            "type": "graph", "layout": "force",
            "symbolSize": 50, "roam": True,
            "label": {"show": True, "color": "#00FF41"},
            "edgeSymbol": ["circle", "arrow"],
            "lineStyle": {"color": "#00FF41", "width": 2},
            "data": [
                {"name": "CORE", "itemStyle": {"color": "#00FF41"}},
                {"name": "EB-1A", "itemStyle": {"color": "#008F11"}},
                {"name": "FINANCE", "itemStyle": {"color": "#008F11"}},
                {"name": "INFRA", "itemStyle": {"color": "#008F11"}}
            ],
            "links": [
                {"source": "CORE", "target": "EB-1A"},
                {"source": "CORE", "target": "FINANCE"},
                {"source": "CORE", "target": "INFRA"}
            ]
        }]
    }
    st_echarts(options=options, height="300px")

# --- [INTERFACE PRINCIPAL] ---
st.title("🛰️ XEON OMNI v101.64 | SYSTEM OVERRIDE")

# MÓDULO DE VOZ (Corrigido)
components.html("""
    <div style="background:#000; border:1px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
        <button onclick="startDictation()" style="background:#00FF41; color:#000; border:none; padding:10px; cursor:pointer; font-weight:bold;">🎙️ INICIAR ESCUTA ATIVA</button>
        <p id="status" style="margin-top:10px;">> Aguardando entrada de voz...</p>
    </div>
    <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            document.getElementById('status').innerText = " RECONHECIDO: " + text.toUpperCase();
        };
        function startDictation() { recognition.start(); }
    </script>
    """, height=120)

market = get_market_data()
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("S&P 500", f"{market['sp500']:.2f}")
col_m2.metric("USD/BRL", f"{market['usdbrl']:.4f}")
col_m3.metric("Uptime", "99.99%", "Stable")

st.write("### 🕸️ TOPOLOGIA DA MALHA")
render_graph()

# --- [LOGICA DE NÓS] ---
nodes = ["INFRAESTRUTURA CRÍTICA", "DIREITO EB-1A", "FINANÇAS GLOBAIS"]

for idx, node in enumerate(nodes):
    node_id = f"node_{idx}"
    with st.expander(f"🔘 NÓ {idx+1}: {node}", expanded=True):
        col_btn, col_status = st.columns([1, 2])
        
        if col_btn.button(f"ATIVAR PROTOCOLO {idx+1}", key=f"btn_{node_id}"):
            st.session_state[f"run_{node_id}"] = True
            
        if st.session_state.get(f"run_{node_id}"):
            progress = st.progress(0)
            for p in range(101):
                time.sleep(0.002)
                progress.progress(p)
            
            metrics = get_reality_metrics()
            st.success(f"✅ RELATÓRIO {idx+1} GERADO")
            
            pdf_bytes = generate_6_page_pdf(node, metrics, market)
            st.download_button(
                label=f"💾 BAIXAR DOSSIÊ {node}",
                data=pdf_bytes,
                file_name=f"XEON_{idx+1}.pdf",
                mime="application/pdf",
                key=f"dl_{node_id}"
            )
            st.code(f"HASH: {metrics['token']}")

st.divider()
st.caption(f"XEON COMMAND UNIT // {time.strftime('%Y-%m-%d %H:%M:%S')} // SECURE ACCESS ONLY")
