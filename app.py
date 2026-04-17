import streamlit as st
import time
import hashlib
import psutil
import unicodedata
import yfinance as yf
from fpdf import FPDF
import base64
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. CONFIGURAÇÃO SOBERANA] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; text-align: center; margin-bottom: 5px; background: rgba(0,255,65,0.05); }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF - PROTOCOLO DE BYTES PUROS] ---
def sanitize_text(text):
    if not text: return "N/A"
    return unicodedata.normalize('NFKD', str(text)).encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf_final(node, cpu, ai_report):
    """Gera PDF e garante o retorno em formato de bytes pronto para o Streamlit"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65)
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, sanitize_text(f"XEON AUDIT: {node}"), ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Courier", "", 10)
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        content = [
            f"TIMESTAMP: {ts}",
            f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
            f"VALOR: R$ 1.000,00 / HORA",
            f"ESTABILIDADE: {100-(cpu*0.1):.2f}%",
            "-"*40,
            "PARECER TECNICO IA:",
            sanitize_text(ai_report),
            "-"*40
        ]
        for line in content:
            pdf.multi_cell(0, 8, line)
        
        # O segredo da estabilidade: output em bytes (bytearray)
        return pdf.output()
    except Exception as e:
        return f"ERRO INTERNO: {str(e)}".encode('latin-1')

# --- [3. DASHBOARD DE COMANDO] ---
@st.fragment(run_every=5)
def xeon_main():
    cpu_val = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1.2, 1])
    
    with c1:
        st.metric("STABILITY", "NOMINAL")
        st.metric("FEE RATE", "R$ 1.000/h")
        try:
            usd = yf.Ticker("USDBRL=X").history(period="1d")['Close'].iloc[-1]
            st.metric("GLOBAL USD", f"{usd:.2f}")
        except: st.write("Offline")

    with c2:
        st_echarts(options={"backgroundColor": "transparent", "series": [{"type": 'gauge', "data": [{"value": cpu_val}], "detail": {"color": MATRIX_GREEN}}]}, height="220px")

    with c3:
        st.metric("EB-1A READY", "YES")
        if st.button("🧠 SCAN IA"):
            with st.status("Processando...", expanded=False) as s:
                if client:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Analise a homeostase de {cpu_val}% para visto EB1A."}]
                    )
                    st.session_state.ai_report = res.choices.message.content
                    st.session_state.vox = "Análise concluída."
                    s.update(label="Concluído", state="complete")
                else:
                    st.session_state.ai_report = "IA Offline."

    st.divider()

    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {s}", key=f"act_{i}"):
                st.session_state.active_node = s
                st.session_state.vox = f"Nó {s} operacional."
            
            if st.session_state.get('active_node') == s:
                rep = st.session_state.get('ai_report', "Aguardando Scan de IA.")
                # Geração de PDF e download direto
                pdf_data = generate_pdf_final(s, cpu_val, rep)
                st.download_button(
                    label="📥 BAIXAR DOSSIÊ", 
                    data=pdf_data, 
                    file_name=f"XEON_{s}.pdf", 
                    mime="application/pdf",
                    key=f"dl_{i}"
                )

    if st.session_state.get('vox'):
        components.html(f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{st.session_state.vox}'); m.lang='pt-BR'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.voice = ""

# --- [4. FINALIZAÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_report' not in st.session_state: st.session_state.ai_report = ""
if 'vox' not in st.session_state: st.session_state.vox = ""
xeon_main()
