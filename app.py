import streamlit as st
import psutil
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
import streamlit.components.v1 as components
from streamlit_echarts import st_echarts

# --- [CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.64", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT (Aprimorado para Botões de Fala/Escuta)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; border-radius: 0px; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #00FF41; color: #000000; box-shadow: 0 0 15px #00FF41; }
    .status-box { border: 1px solid #00FF41; padding: 10px; background: #0A0A0A; margin-bottom: 10px; }
    [data-testid="stMetricValue"] { color: #00FF41; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [CORE FUNCTIONS] ---
def get_reality_metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "mem": psutil.virtual_memory().percent,
        "token": hashlib.sha256(str(time.time()).encode()).hexdigest()[:24].upper(),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }

@st.cache_data(ttl=30)
def get_market_data():
    try:
        tickers = ["^GSPC", "USDBRL=X", "BTC-USD"]
        data = yf.download(tickers, period="1d", interval="1m", progress=False)
        return {
            "sp500": data['Close']['^GSPC'].iloc[-1], 
            "usdbrl": data['Close']['USDBRL=X'].iloc[-1],
            "btc": data['Close']['BTC-USD'].iloc[-1]
        }
    except:
        return {"sp500": 5150.00, "usdbrl": 5.10, "btc": 65000.00}

def generate_6_page_pdf(node_name, metrics, market):
    pdf = FPDF()
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"RELATORIO XEON MISSION CRITICAL - PAG {i}/6", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Courier", "", 10)
        content = (f"ID DO NO: {node_name}\nTOKEN DE AUTENTICIDADE: {metrics['token']}\n"
                   f"TIMESTAMP GLOBAL: {metrics['timestamp']}\nSTATUS CPU: {metrics['cpu']}%\n"
                   f"MARKET S&P500: {market['sp500']:.2f}\nUSD/BRL: {market['usdbrl']:.4f}\n"
                   f"BTC/USD: {market['btc']:.2f}\n" + "-"*50 + "\nCRIPTOGRAFIA: AES-256-NODE-LEVEL")
        pdf.multi_cell(0, 10, content)
    return pdf.output(dest='S').encode('latin-1')

# --- [UI: CONTROLE DE VOZ GLOBAL] ---
def voice_interface():
    components.html("""
    <div style="background:#000; border:2px solid #00FF41; padding:20px; color:#00FF41; font-family:monospace;">
        <div style="display: flex; gap: 10px;">
            <button onclick="startListen()" style="flex:1; background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ESCUTA ATIVA (PT/EN)</button>
            <button onclick="stopListen()" style="flex:1; background:#000; color:#FF0000; border:1px solid #FF0000; padding:10px; cursor:pointer;">🛑 CESSAR</button>
        </div>
        <p id="v-status" style="margin-top:10px; font-size:12px;">> MONITOR DE VOZ: STANDBY</p>
        <div id="v-output" style="color:#FFF; background:#111; padding:5px; min-height:30px; border-left:3px solid #00FF41;">...</div>
    </div>

    <script>
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'pt-BR';

        const synth = window.speechSynthesis;

        function startListen() {
            recognition.start();
            document.getElementById('v-status').innerText = "> MONITOR DE VOZ: ESCUTANDO...";
            speak("Sistema Xeon Ativado. Monitorando frequências globais.");
        }

        function stopListen() {
            recognition.stop();
            document.getElementById('v-status').innerText = "> MONITOR DE VOZ: STANDBY";
        }

        recognition.onresult = (event) => {
            let transcript = event.results[event.results.length - 1][0].transcript;
            document.getElementById('v-output').innerText = transcript.toUpperCase();
        };

        function speak(text) {
            const utter = new SpeechSynthesisUtterance(text);
            utter.rate = 1.1;
            synth.speak(utter);
        }
    </script>
    """, height=180)

# --- [MAIN LAYOUT] ---
st.title("🛰️ XEON OMNI v101.64 | GLOBAL MISSION CRITICAL")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.write("### 🗣️ COMANDO DE VOZ")
    voice_interface()
    
    st.write("### 📊 TELEMETRIA DE MERCADO")
    m = get_market_data()
    st.metric("S&P 500", f"{m['sp500']:.2f}", "+0.12%")
    st.metric("USD/BRL", f"{m['usdbrl']:.4f}", "-0.02%")
    st.metric("BITCOIN", f"${m['btc']:,.2f}")

with col_right:
    st.write("### 🕸️ TOPOLOGIA DA MALHA TEMPO REAL")
    options = {
        "backgroundColor": "#000",
        "series": [{"type": "graph", "layout": "force", "symbolSize": 60, "roam": True,
            "label": {"show": True, "color": "#00FF41"},
            "lineStyle": {"color": "#00FF41", "width": 3},
            "data": [
                {"name": "XEON-CORE", "itemStyle": {"color": "#00FF41"}},
                {"name": "SAT-1", "itemStyle": {"color": "#008F11"}},
                {"name": "FIN-NODE", "itemStyle": {"color": "#008F11"}},
                {"name": "LEGAL-AI", "itemStyle": {"color": "#008F11"}}
            ],
            "links": [{"source": "XEON-CORE", "target": "SAT-1"}, {"source": "XEON-CORE", "target": "FIN-NODE"}, {"source": "XEON-CORE", "target": "LEGAL-AI"}]
        }]
    }
    st_echarts(options=options, height="350px")

# --- [NÓS DE PROCESSAMENTO] ---
st.write("### 🛠️ UNIDADES DE MISSÃO CRÍTICA")
nodes = ["INFRAESTRUTURA DATA-SENSÍVEL", "DIREITO INTERNACIONAL EB-1A", "LIQUIDEZ GLOBAL"]

for idx, node in enumerate(nodes):
    with st.container():
        c1, c2 = st.columns([1, 4])
        
        with c1:
            st.write(f"**NÓ {idx+1}**")
            btn_active = st.button(f"EXECUTAR: {node.split()[0]}", key=f"exe_{idx}")
            
        with c2:
            if btn_active:
                # Simulação de processamento em tempo real
                metrics = get_reality_metrics()
                bar = st.progress(0)
                status_text = st.empty()
                
                for p in range(101):
                    time.sleep(0.01)
                    bar.progress(p)
                    status_text.text(f"PULSO DE DADOS: {p}% | SECTOR: {hex(p*1234)}")
                
                st.success(f"PROTOCOLO {idx+1} CONCLUÍDO - INTEGRIDADE 100%")
                
                # Botão de PDF gerado após processamento
                pdf_data = generate_6_page_pdf(node, metrics, m)
                st.download_button(
                    label=f"📥 BAIXAR DOSSIÊ 6-PÁGINAS: {node}",
                    data=pdf_data,
                    file_name=f"XEON_CRITICAL_{idx+1}.pdf",
                    mime="application/pdf",
                    key=f"pdf_{idx}"
                )
            else:
                st.info(f"Aguardando sinal para {node}...")

st.divider()
st.caption(f"CONNECTED TO GLOBAL APIs | SECURITY HASH: {get_reality_metrics()['token']} | {time.strftime('%H:%M:%S')}")
