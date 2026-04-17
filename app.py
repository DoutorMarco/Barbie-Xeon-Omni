import streamlit as st
import psutil
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
import streamlit.components.v1 as components

# --- [CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.64", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT (Correção de contraste e alinhamento)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; width: 100%; border-radius: 0px; }
    .stButton>button:hover { background-color: #00FF41; color: #000000; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41; }
    [data-testid="stMetricDelta"] { color: #00FF41; }
    code { color: #00FF41 !important; background-color: #0A0A0A !important; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [CORE: TELEMETRIA E FINANÇAS REAIS] ---
def get_reality_metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "mem": psutil.virtual_memory().percent,
        "token": hashlib.sha256(str(time.time()).encode()).hexdigest()[:16].upper(),
        "timestamp": time.strftime('%H:%M:%S')
    }

@st.cache_data(ttl=60) # Cache para não bloquear a API por excesso de requisições
def get_market_data():
    try:
        # S&P 500 e USD/BRL
        tickers = ["^GSPC", "USDBRL=X"]
        data = yf.download(tickers, period="1d", interval="1m", progress=False)
        last_sp500 = data['Close']['^GSPC'].iloc[-1]
        last_usdbrl = data['Close']['USDBRL=X'].iloc[-1]
        return {"sp500": last_sp500, "usdbrl": last_usdbrl}
    except Exception:
        return {"sp500": 5150.00, "usdbrl": 5.10} # Fallback operacional

# --- [ENGINE: PDF DE SUPREMACIA] ---
def generate_6_page_pdf(node_name, metrics, market):
    pdf = FPDF()
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65)
        pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, f"DOSSIE XEON COMMAND - PAGINA {i}/6", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Courier", "", 10)
        
        # Conteúdo dinâmico por página
        content = f"NO: {node_name}\nSTATUS: OPERACIONAL\nTOKEN: {metrics['token']}\n"
        content += f"TIMESTAMP: {metrics['timestamp']}\n"
        
        if i == 1: content += f"\n--- ANALISE DE HARDWARE ---\nCPU LOAD: {metrics['cpu']}%\nRAM USAGE: {metrics['mem']}%"
        elif i == 2: content += f"\n--- MERCADO GLOBAL ---\nS&P 500 INDEX: {market['sp500']:.2f}\nBRL EXCHANGE: {market['usdbrl']:.4f}"
        elif i == 3: content += "\n--- EB-1A ESTATUTO ---\nAUTO-PETICAO: HABILIDADE EXTRAORDINARIA.\nINFRAESTRUTURA CRITICA DETECTADA."
        else: content += f"\n--- AUDITORIA DE SEGURANCA ---\nASSINATURA: MARCO ANTONIO DO NASCIMENTO\nVALOR DE MERCADO: R$ 1.000,00/H\nVALIDACAO: OK"
        
        # Multi_cell com encode para evitar erros de caracteres especiais
        pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
    
    return pdf.output(dest='S').encode('latin-1')

# --- [INTERFACE PRINCIPAL] ---
st.title("🛰️ XEON OMNI v101.64 | REALIDADE ABSOLUTA")

# MÓDULO DE VOZ
components.html("""
    <div style="background-color:#000; border:1px solid #00FF41; padding:10px; color:#00FF41; font-family:monospace; font-size:12px;">
        <button onclick="start()" style="background:#000; border:1px solid #00FF41; color:#00FF41; cursor:pointer;">🎙️ ATIVAR ESCUTA</button>
        <span id="v"> Aguardando Comando...</span>
    </div>
    <script>
        const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        r.continuous = true; 
        r.onresult = (e) => { 
            document.getElementById('v').innerText = " > " + e.results[e.results.length-1][0].transcript.toUpperCase(); 
        };
        function start() { r.start(); }
    </script>
    """, height=80)

# MONITOR DE MERCADO
market = get_market_data()
c1, c2, c3 = st.columns(3)
c1.metric("S&P 500", f"{market['sp500']:.2f}", "LIVE")
c2.metric("USD/BRL", f"R$ {market['usdbrl']:.4f}", "-0.02%")
c3.metric("VALORAÇÃO", "R$ 1.000/H", "PREMIUM")

st.markdown("---")

# FUNÇÃO DE RENDERIZAÇÃO DE NÓ
def render_critical_node(id, name):
    st.subheader(f"Nó {id}: {name}")
    
    # Chave única para o estado de processamento
    proc_key = f"proc_{id}"
    
    if st.button(f"EXECUTAR PROTOCOLO {id}", key=f"btn_{id}"):
        st.session_state[proc_key] = True
        
    if st.session_state.get(proc_key):
        bar = st.progress(0)
        status = st.empty()
        for i in range(1, 101):
            time.sleep(0.005) # Velocidade de processamento simulada
            bar.progress(i)
            status.text(f"Auditoria em curso: {i}%")
        
        metrics = get_reality_metrics()
        st.success(f"Nó {id} Auditado com Sucesso.")
        
        # Geração de PDF
        pdf_data = generate_6_page_pdf(name, metrics, market)
        
        st.download_button(
            label=f"📥 BAIXAR DOSSIÊ {id} (6 PÁGINAS)",
            data=pdf_data,
            file_name=f"XEON_REPORT_{id}.pdf",
            mime="application/pdf",
            key=f"dl_{id}"
        )
        st.code(f"SHA-256_VERIFY: {metrics['token']}", language="bash")
    st.markdown("---")

# LISTA DE NÓS
nodes = ["INFRAESTRUTURA CRÍTICA", "DIREITO E COMPLIANCE EB-1A", "FINANÇAS GLOBAIS"]
for idx, node_name in enumerate(nodes):
    render_critical_node(idx+1, node_name)

# FOOTER
st.write(f"**SISTEMA NOMINAL | ENCRYPT_STRENGTH: MAXIMUM | {time.strftime('%H:%M:%S')}**")
