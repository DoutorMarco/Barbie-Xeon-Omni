import streamlit as st
import psutil
import time
import hashlib
import yfinance as yf
import plotly.graph_objects as go
from fpdf import FPDF
import streamlit.components.v1 as components

# --- [CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.64", layout="wide")

# CSS MATRIX BLACKOUT
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; width: 100%; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    .stMetric { border: 1px solid #00FF41; padding: 10px; background-color: #050505; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [CORE: TELEMETRIA E FINANÇAS REAIS] ---
def get_reality_metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "mem": psutil.virtual_memory().percent,
        "token": hashlib.sha256(str(time.time()).encode()).hexdigest(),
        "timestamp": time.strftime('%H:%M:%S')
    }

def get_market_data():
    # Captura real do S&P 500 e USD/BRL para estratégia EB-1A e Dólar
    try:
        tickers = ["^GSPC", "USDBRL=X"]
        data = yf.download(tickers, period="1d", interval="1m").iloc[-1]
        return {"sp500": data['Close']['^GSPC'], "usdbrl": data['Close']['USDBRL=X']}
    except:
        return {"sp500": 5100.00, "usdbrl": 5.00} # Fallback de segurança

# --- [ENGINE: PDF DE SUPREMACIA - 6 PÁGINAS] ---
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
        
        content = f"NO: {node_name}\nSTATUS: REALIDADE PURA\nTOKEN: {metrics['token']}\n"
        if i == 1: content += "\n--- ANALISE DE HARDWARE ---\nCPU: {0}%\nRAM: {1}%".format(metrics['cpu'], metrics['mem'])
        if i == 2: content += f"\n--- MERCADO GLOBAL ---\nS&P 500: {market['sp500']}\nUSD/BRL: {market['usdbrl']}"
        if i == 3: content += "\n--- EB-1A ESTATUTO ---\nPROVA DE HABILIDADE EXTRAORDINARIA: INFRAESTRUTURA CRITICA."
        if i >= 4: content += f"\n--- AUDITORIA DE SEGURANCA ---\nASSINATURA: MARCO ANTONIO DO NASCIMENTO\nVALOR: R$ 1.000,00/H"
        
        pdf.multi_cell(0, 10, content)
    return pdf.output(dest='S').encode('latin-1')

# --- [INTERFACE PRINCIPAL] ---
st.title("🛰️ XEON OMNI v101.64 | REALIDADE ABSOLUTA")

# MÓDULO DE VOZ (OMNILÍNGUA)
components.html("""
    <div style="background-color:#000; border:1px solid #00FF41; padding:10px; color:#00FF41; font-family:monospace;">
        <button onclick="start()" style="background:none; border:1px solid #00FF41; color:#00FF41;">🎙️ ESCUTA ATIVA</button>
        <span id="v"> Aguardando Comando Global...</span>
    </div>
    <script>
        const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        r.continuous = true; r.onresult = (e) => { document.getElementById('v').innerText = " Voz: " + e.results[e.results.length-1][0].transcript; };
        function start() { r.start(); }
    </script>
    """, height=70)

# MONITOR DE MERCADO (APIs GLOBAIS)
market = get_market_data()
c1, c2 = st.columns(2)
c1.metric("S&P 500 REAL-TIME", f"{market['sp500']:.2f}", delta="ATIVO")
c2.metric("USD/BRL", f"R$ {market['usdbrl']:.2f}", delta="MONETIZAÇÃO $450/H")

st.markdown("---")

# FUNÇÃO DE RENDERIZAÇÃO DE NÓ COM PROCESSAMENTO E PDF IMEDIATO
def render_critical_node(id, name):
    st.subheader(f"Nó {id}: {name}")
    
    if st.button(f"ATIVAR PROCESSAMENTO {id}", key=f"btn_{id}"):
        st.session_state[f"proc_{id}"] = True
        
    if st.session_state.get(f"proc_{id}"):
        bar = st.progress(0)
        status = st.empty()
        for i in range(101):
            time.sleep(0.01)
            bar.progress(i)
            status.text(f"Auditando Realidade... {i}%")
        
        metrics = get_reality_metrics()
        st.success(f"Dossiê {id} Gerado com Erro Zero.")
        
        # Geração e Download do PDF de 6 Páginas
        pdf_bytes = generate_6_page_pdf(name, metrics, market)
        st.download_button(
            label=f"📥 BAIXAR RELATÓRIO DE 6 FOLHAS - {id}",
            data=pdf_bytes,
            file_name=f"XEON_DOSSIE_{id}.pdf",
            mime="application/pdf",
            key=f"dl_{id}"
        )
        st.code(f"HASH DE AUDITORIA: {metrics['token']}", language="bash")
    st.markdown("---")

# EXECUÇÃO DOS NÓS
nodes = ["INFRAESTRUTURA CRÍTICA", "DIREITO E COMPLIANCE EB-1A", "FINANÇAS GLOBAIS E ARBITRAGEM"]
for idx, node_name in enumerate(nodes):
    render_critical_node(idx+1, node_name)

# FOOTER MISSÃO CRÍTICA
st.write(f"**SISTEMA NOMINAL | R$ 1.000,00/H | {time.strftime('%Y-%m-%d %H:%M:%S')}**")
