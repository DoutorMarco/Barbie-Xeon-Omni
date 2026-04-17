import streamlit as st
import time
import hashlib
import psutil
import unicodedata
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. CONFIGURAÇÃO SOBERANA] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0 | R$ 1.000/h", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; font-size: 2rem !important; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; text-align: center; margin-bottom: 5px; background: rgba(0,255,65,0.05); }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF BLINDADO (SAÍDA DE BYTES PUROS)] ---
def sanitize_to_pdf(text):
    if not text: return "N/A"
    return unicodedata.normalize('NFKD', str(text)).encode('latin-1', 'ignore').decode('latin-1')

def generate_dossier_final(node, cpu, ai_report):
    try:
        pdf = FPDF()
        pdf.set_margins(15, 15, 15)
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        
        # Header
        pdf.set_text_color(0, 255, 65)
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, sanitize_to_pdf(f"TECHNICAL AUDIT: {node}"), ln=True, align='C')
        pdf.ln(5)
        
        # Meta Dados
        pdf.set_font("Courier", "", 10)
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        content = [
            f"TIMESTAMP: {ts}",
            f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
            f"FEE_RATE: R$ 1.000,00 / HOUR",
            f"SYSTEM_HOMEOSTASE: {100-(cpu*0.1):.2f}%",
            f"NIW_EVIDENCE_HASH: {hashlib.sha256(ts.encode()).hexdigest().upper()[:32]}",
            "-"*50,
            "GEN-AI PHYSIOLOGY ANALYSIS:",
            sanitize_to_pdf(ai_report),
            "-"*50
        ]
        
        for line in content:
            pdf.multi_cell(0, 8, line)
        
        # Retorno direto de bytes para evitar erro de abertura
        return pdf.output()
    except Exception as e:
        return b"ERROR_GENERATING_VALID_PDF"

# --- [3. DASHBOARD DE COMANDO E MONETIZAÇÃO] ---
@st.fragment(run_every=5)
def xeon_main():
    cpu_val = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1.2, 1])
    
    with c1:
        st.metric("STABILITY", "NOMINAL")
        # Injeção de Monetização Direta
        st.metric("TAXA DE CONSULTORIA", "R$ 1.000/h", delta="MONETIZAÇÃO ATIVA")
        try:
            usd = yf.Ticker("USDBRL=X").history(period="1d")['Close'].iloc[-1]
            st.metric("GLOBAL USD/BRL", f"{usd:.2f}")
        except: st.write("Relay Offline")

    with c2:
        st_echarts(options={"backgroundColor": "transparent", "series": [{"type": 'gauge', "data": [{"value": cpu_val}], "detail": {"color": MATRIX_GREEN, "fontSize": 20}}]}, height="220px")

    with c3:
        st.metric("TARGET", "EB-1A / NIW")
        if st.button("🧠 SCAN IA FISIOLÓGICO"):
            with st.status("Processando...", expanded=False) as s:
                if client:
                    res = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Analise o valor técnico de R$ 1.000/h para um sistema com {cpu_val}% de carga para o visto EB1A."}]
                    )
                    st.session_state.ai_report = res.choices.message.content
                    st.session_state.vox = "Análise de alto valor concluída."
                    s.update(label="Análise Pronta", state="complete")
                else:
                    st.session_state.ai_report = "IA em modo redundância local."

    st.divider()

    # Operação de Nós
    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {s}", key=f"act_{i}"):
                st.session_state.node_active = s
                st.session_state.vox = f"Nó {s} integrado ao faturamento."
            
            if st.session_state.get('node_active') == s:
                rep = st.session_state.get('ai_report', "Dados de IA pendentes.")
                pdf_bytes = generate_dossier_final(s, cpu_val, rep)
                # O download_button recebe os bytes puros agora
                st.download_button(
                    label="📥 DOWNLOAD DOSSIÊ", 
                    data=pdf_bytes, 
                    file_name=f"XEON_{s}.pdf", 
                    mime="application/pdf", 
                    key=f"dl_{i}"
                )

    # Vox Protocol (Voz Ativa)
    if st.session_state.get('vox'):
        components.html(f"""<script>
            window.speechSynthesis.cancel();
            var m = new SpeechSynthesisUtterance('{st.session_state.vox}');
            m.lang = 'pt-BR'; window.speechSynthesis.speak(m);
        </script>""", height=0)
        st.session_state.vox = ""

# --- [4. FINALIZAÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 5px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_report' not in st.session_state: st.session_state.ai_report = ""
if 'vox' not in st.session_state: st.session_state.vox = ""
xeon_main()
st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | TAXA: R$ 1.000/H | REALIDADE PURA")
