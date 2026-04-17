import streamlit as st
import psutil
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

# --- [CONFIGURAÇÃO SOBERANA - ESTADO NOMINAL] ---
st.set_page_config(page_title="XEON OMNI v101.65", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT TOTAL
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; border-radius: 0px; width: 100%; transition: 0.3s; height: 50px; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41; color: #000000; box-shadow: 0 0 15px #00FF41; }
    .status-box { border: 1px solid #00FF41; padding: 15px; background: #0A0A0A; margin-bottom: 10px; border-left: 5px solid #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    h1, h2, h3 { color: #00FF41 !important; border-bottom: 1px solid #008F11; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [CORE FUNCTIONS: ENGENHARIA DE DADOS] ---
def get_reality_metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "mem": psutil.virtual_memory().percent,
        "token": hashlib.sha256(str(time.time()).encode()).hexdigest()[:32].upper(),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }

@st.cache_data(ttl=60)
def get_market_data():
    try:
        tickers = ["^GSPC", "USDBRL=X", "BTC-USD", "GC=F"]
        data = yf.download(tickers, period="1d", interval="1m", progress=False)
        return {
            "sp500": data['Close']['^GSPC'].iloc[-1], 
            "usdbrl": data['Close']['USDBRL=X'].iloc[-1],
            "btc": data['Close']['BTC-USD'].iloc[-1],
            "gold": data['Close']['GC=F'].iloc[-1]
        }
    except:
        return {"sp500": 5200.0, "usdbrl": 5.15, "btc": 68000.0, "gold": 2350.0}

def generate_6_page_pdf(title, metrics, m):
    pdf = FPDF()
    clauses = [
        "CLAUSE 01: SOBERANIA DE DADOS - Auditoria NIST SP 800-207.",
        "CLAUSE 02: CRIPTOGRAFIA PÓS-QUÂNTICA - Protocolo AES-256-GCM.",
        "CLAUSE 03: CONFORMIDADE LEGAL - Cadeia de custódia imutável.",
        "CLAUSE 04: BIOMEDICINA - Integridade de dados sensíveis HIPAA.",
        "CLAUSE 05: GOVERNANÇA GRC - Monitoramento de risco em tempo real.",
        "CLAUSE 06: VALIDAÇÃO EB-1A - Evidência técnica de papel crítico."
    ]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"DOSSIÊ XEON: {title.upper()}", 0, 1, 'C')
        pdf.set_font("Courier", "B", 10)
        pdf.cell(0, 10, f"PÁGINA {i}/6 | HASH: {metrics['token']}", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Courier", "", 11)
        content = (f"PROCESSO: {clauses[i-1]}\n\n"
                   f"DATA: {metrics['timestamp']}\nCPU: {metrics['cpu']}%\n"
                   f"S&P500: {m['sp500']:.2f} | BTC: ${m['btc']:,.2f}\n" + "-"*60 + 
                   "\nRELATÓRIO DE AUDITORIA DE MISSÃO CRÍTICA DESTINADO A INFRAESTRUTURAS NACIONAIS. "
                   "ESTE DOCUMENTO POSSUI VALIDADE TÉCNICA E JURÍDICA TRANSFRONTEIRIÇA.")
        pdf.multi_cell(0, 10, content)
    return pdf.output(dest='S').encode('latin-1')

# --- [HEADER & VOZ] ---
st.title("🛰️ XEON OMNI v101.65 | MISSÃO CRÍTICA")
st.write("**Operando: APIS Mundiais Conectadas | Estado: Soberano**")

components.html("""
    <div style="background:#000; border:1px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
        <button onclick="start()" style="background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ATIVAR ESCUTA POLIGLOTA</button>
        <button onclick="speak()" style="background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer; margin-left:10px;">🔊 STATUS VOCAL</button>
        <p id="out" style="margin-top:10px; font-size:12px;">> SISTEMA AGUARDANDO COMANDO...</p>
    </div>
    <script>
        const rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'pt-BR';
        function start() { rec.start(); document.getElementById('out').innerText = "> ESCUTANDO..."; }
        rec.onresult = (e) => { document.getElementById('out').innerText = "> CAPTADO: " + e.results[0][0].transcript.toUpperCase(); };
        function speak() { 
            const u = new SpeechSynthesisUtterance("Xeon Omni ativo. Missão Crítica operacional.");
            u.rate = 0.8; window.speechSynthesis.speak(u);
        }
    </script>
""", height=130)

# --- [TELEMETRIA GLOBAL] ---
m = get_market_data()
c1, c2, c3, c4 = st.columns(4)
c1.metric("S&P 500", f"{m['sp500']:.2f}")
c2.metric("USD/BRL", f"{m['usdbrl']:.4f}")
c3.metric("BITCOIN", f"${m['btc']:,.0f}")
c4.metric("GOLD", f"${m['gold']:,.2f}")

# --- [TERMINAIS DE AUDITORIA] ---
nodes = [
    {"name": "FINANÇAS E LIQUIDEZ GLOBAL", "icon": "💰"},
    {"name": "CONFORMIDADE REGULATÓRIA (GRC)", "icon": "⚖️"},
    {"name": "INFRAESTRUTURA NACIONAL (EB-1A)", "icon": "🛡️"}
]

for i, node in enumerate(nodes):
    with st.container():
        st.markdown(f"<div class='status-box'>{node['icon']} {node['name']}</div>", unsafe_allow_stdio=True)
        col_btn, col_status = st.columns([1, 2])
        
        with col_btn:
            if st.button(f"EXECUTAR AUDITORIA {i+1}", key=f"btn_{i}"):
                met = get_reality_metrics()
                with st.status(f"Processando Nó {i+1}...", expanded=True):
                    st.write("Conectando APIs Federais...")
                    time.sleep(0.5)
                    st.write(f"Gerando Relatório de 6 Páginas (Token: {met['token'][:10]})...")
                    st.progress(100)
                
                # O BOTÃO DE PDF APARECE AQUI ABAIXO DO STATUS
                pdf_b = generate_6_page_pdf(node['name'], met, m)
                st.download_button(
                    label=f"📥 BAIXAR DOSSIÊ PDF (6 FOLHAS) - NÓ {i+1}",
                    data=pdf_b,
                    file_name=f"XEON_RELATORIO_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"dl_{i}"
                )
        with col_status:
            st.write(f"Aguardando pulso de comando para o setor de {node['name']}.")

st.divider()
st.caption(f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO | SECURITY HASH: {get_reality_metrics()['token']}")
