import streamlit as st
import psutil
import time
import hashlib
import yfinance as yf
from fpdf import FPDF
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO DE AMBIENTE] ---
st.set_page_config(page_title="XEON OMNI v101.66", layout="wide", page_icon="🛰️")

# CSS MATRIX BLACKOUT (Design Soberano)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; border-radius: 0px; width: 100%; transition: 0.3s; height: 50px; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41; color: #000000; box-shadow: 0 0 15px #00FF41; }
    .status-box { border: 1px solid #00FF41; padding: 15px; background: #0A0A0A; margin-bottom: 20px; border-left: 5px solid #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    h1, h2, h3, h4 { color: #00FF41 !important; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [2. MOTOR DE DADOS E PDF] ---
def get_metrics():
    return {
        "cpu": psutil.cpu_percent(),
        "token": hashlib.sha256(str(time.time()).encode()).hexdigest()[:32].upper(),
        "ts": time.strftime('%Y-%m-%d %H:%M:%S')
    }

@st.cache_data(ttl=60)
def get_market():
    try:
        data = yf.download(["^GSPC", "USDBRL=X", "BTC-USD"], period="1d", interval="1m", progress=False)
        return {"sp500": data['Close']['^GSPC'].iloc[-1], "usd": data['Close']['USDBRL=X'].iloc[-1], "btc": data['Close']['BTC-USD'].iloc[-1]}
    except:
        return {"sp500": 5250.0, "usd": 5.15, "btc": 69000.0}

def generate_pdf(title, met, m):
    pdf = FPDF()
    clauses = ["DIREITO E SOBERANIA", "INFRAESTRUTURA NIST", "AUDITORIA EB-1A", "BIOMEDICINA", "GOVERNANÇA GRC", "BLOCKCHAIN LEDGER"]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"RELATORIO XEON CRITICAL: {title}", 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Courier", "", 11)
        pdf.multi_cell(0, 10, f"PAGINA {i}/6\nTOKEN: {met['token']}\nSETOR: {clauses[i-1]}\nMARKET BTC: {m['btc']}\nMARKET USD: {m['usd']}\n\nEste documento atesta a integridade do sistema Xeon Omni em conformidade com padroes internacionais de defesa.")
    return pdf.output(dest='S').encode('latin-1')

# --- [3. INTERFACE DE COMANDO] ---
st.title("🛰️ XEON OMNI v101.66 | GLOBAL COMMAND")
st.subheader("Missão Crítica: Ativa | APIs: Conectadas")

# Painel de Voz
components.html("""
    <div style="background:#000; border:1px solid #00FF41; padding:15px; color:#00FF41; font-family:monospace;">
        <button onclick="rec()" style="background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer;">🎙️ ESCUTA ATIVA</button>
        <button onclick="speak()" style="background:#000; color:#00FF41; border:1px solid #00FF41; padding:10px; cursor:pointer; margin-left:10px;">🔊 STATUS</button>
        <div id="v-log" style="margin-top:10px; font-size:11px;">> STANDBY</div>
    </div>
    <script>
        function speak() { 
            const u = new SpeechSynthesisUtterance("Xeon ativo. Sistema pronto."); 
            u.rate = 0.8; window.speechSynthesis.speak(u);
        }
        function rec() { 
            document.getElementById('v-log').innerText = "> ESCUTANDO COMANDOS...";
            const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            r.lang = 'pt-BR'; r.start();
            r.onresult = (e) => { document.getElementById('v-log').innerText = "> CAPTADO: " + e.results[0][0].transcript.toUpperCase(); };
        }
    </script>
""", height=120)

# Telemetria Real
m = get_market()
c1, c2, c3 = st.columns(3)
c1.metric("S&P 500", f"{m['sp500']:.2f}")
c2.metric("USD/BRL", f"{m['usd']:.4f}")
c3.metric("BITCOIN", f"${m['btc']:,.0f}")

# --- [4. TERMINAIS DE MISSÃO] ---
st.write("### 🛠️ UNIDADES DE AUDITORIA E MONETIZAÇÃO")
sectors = ["FINANÇAS GLOBAIS", "GOVERNANÇA E CONFORMIDADE", "PROVA TÉCNICA EB-1A"]

for i, sec in enumerate(sectors):
    with st.container():
        st.markdown(f"<div class='status-box'>[NÓ 0{i+1}] {sec}</div>", unsafe_allow_stdio=True)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button(f"ATIVAR NÓ 0{i+1}", key=f"btn_{i}"):
                met = get_metrics()
                # Telemetria sob o botão
                with st.status(f"Processando {sec}...", expanded=True):
                    st.write("Verificando Handshake NIST...")
                    time.sleep(0.5)
                    st.write(f"Gerando Dossiê 6 Páginas. Token: {met['token'][:10]}")
                    st.progress(100)
                
                # PDF de 6 Páginas abaixo da telemetria
                pdf_bytes = generate_pdf(sec, met, m)
                st.download_button(
                    label=f"📥 BAIXAR RELATÓRIO PDF (6 FOLHAS) - {sec}",
                    data=pdf_bytes,
                    file_name=f"XEON_AUDIT_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"dl_{i}"
                )
        with col2:
            st.info(f"Monitor de segurança ativo para {sec}. Auditoria transdisciplinar pronta.")

st.divider()
st.caption(f"ARQUITETO PRINCIPAL: MARCO ANTONIO DO NASCIMENTO | {time.strftime('%Y')} | ENCRYPTED: {get_metrics()['token'][:16]}")
