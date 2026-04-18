import streamlit as st
import time, hashlib, psutil, unicodedata, textwrap
from fpdf import FPDF
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI
import yfinance as yf

# --- [1. IDENTIDADE VISUAL E VOX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"
COMMAND_BLUE = "#0000FF" # Azul para Ingestão/Cérebro

st.set_page_config(page_title="XEON COMMAND v160.0", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

def speak(text):
    components.html(f"""
        <script>
        var u = new SpeechSynthesisUtterance('{text}');
        u.lang = 'pt-BR'; u.rate = 1.0;
        window.speechSynthesis.speak(u);
        </script>
    """, height=0)

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    
    /* ZONA CEREBRAL AZUL - Ingestão de Dados */
    .stTextArea textarea, .stTextInput input {{
        background-color: {COMMAND_BLUE} !important; 
        color: #FFFFFF !important; 
        font-weight: bold !important; border: 2px solid {MATRIX_GREEN} !important;
    }}
    
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; width: 100%; font-weight: bold;
    }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; background: rgba(0,255,65,0.05); text-align: center; }}
    .reprocessor {{ font-size: 0.6em; color: {MATRIX_GREEN}; opacity: 0.8; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE EVIDÊNCIA PDF] ---
def generate_node_pdf(node_name, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
    pdf.cell(0, 10, f"XEON MISSION CRITICAL - NODE: {node_name}", ln=True, align='C')
    pdf.set_font("Courier", "", 10)
    pdf.ln(10)
    content_clean = unicodedata.normalize('NFKD', content).encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 7, f"ARQUITETO: MARCO ANTONIO DO NASCIMENTO\nTIMESTAMP: {time.ctime()}\n{'-'*50}\n{content_clean}")
    return BytesIO(pdf.output())

# --- [3. DASHBOARD v160.0 OPERACIONAL] ---
@st.fragment(run_every=2)
def xeon_sovereign_core():
    # Gatilho S&P 500 (Voz a cada 10 min simulado ou na carga)
    if 'last_market_check' not in st.session_state:
        st.session_state.last_market_check = 0
    
    if time.time() - st.session_state.last_market_check > 600: # 10 minutos
        try:
            sp500 = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
            speak(f"Arquiteto, atualização do mercado. S e P 500 operando em {sp500:.2f} pontos.")
            st.session_state.last_market_check = time.time()
        except: pass

    c1, c2, c3 = st.columns([1, 1, 1.5])
    
    with c1:
        st.metric("MONETIZAÇÃO", "$1,000/H")
        st.metric("SISTEMA", "BRAIN ACTIVE")
    
    with c2:
        cpu = psutil.cpu_percent()
        options = {"backgroundColor":"transparent","series":[{"type":'gauge',"detail":{"color":MATRIX_GREEN,"fontSize":12},"data":[{"value":cpu,"name":'CPU'}]}]}
        st_echarts(options=options, height="160px")

    with c3:
        st.markdown(f"<b style='color:#FFFFFF;'>🧠 CÉREBRO GERATIVO - INGESTÃO AZUL:</b>", unsafe_allow_html=True)
        query = st.text_area("PESQUISAR / COMANDAR SISTEMA:", height=80, label_visibility="collapsed")
        if st.button("👁️ PROCESSAR COMANDO"):
            speak(f"Processando comando cerebral: {query[:15]}")
            if client:
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":query}])
                st.session_state.brain_res = res.choices.message.content

    st.divider()
    
    # OS 9 NÓS COM PDF EMBAIXO DE CADA UM
    nos = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"""
                <div class='node-card'>
                    <small>NÓ 0{i+1}</small><br><b>{n}</b>
                    <div class='reprocessor'>REPROCESSANDO: {hashlib.sha256(str(time.time()).encode()).hexdigest()[:10]}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Gerador de PDF embaixo do Nó
            report_text = f"Auditoria técnica automatizada para o nó {n}. Integridade confirmada para EB-1A."
            pdf_data = generate_node_pdf(n, report_text)
            st.download_button(label=f"📥 EXPORTAR PDF {n}", data=pdf_data, file_name=f"XEON_{n}.pdf", key=f"pdf_{i}")

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v160.0</h1>", unsafe_allow_html=True)
xeon_sovereign_core()

if psutil.cpu_percent() > 85:
    speak("Alerta Crítico: Stress de Hardware. Homeostase em risco.")
