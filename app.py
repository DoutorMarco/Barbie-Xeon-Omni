import streamlit as st
import time
import hashlib
import psutil
import unicodedata
import textwrap
from fpdf import FPDF # Requisito: fpdf2
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. CONFIGURAÇÃO SOBERANA - ZERO BRANCO] ---
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
    code, pre {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN}; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 60px;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 30px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; text-align: center; background: rgba(0,255,65,0.05); margin-bottom: 10px; }}
    /* REMOVE FUNDO BRANCO DE COMPONENTES EXTERNOS */
    iframe {{ background-color: transparent !important; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF - PROTOCOLO DE INTEGRIDADE] ---
def sanitize_pdf(text):
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')

def generate_xeon_pdf(node_name, cpu, ai_report):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    ts = time.strftime('%H:%M:%S')
    bc = hashlib.sha256(f"{node_name}{ts}".encode()).hexdigest().upper()
    
    for i in range(6): # 6 Páginas de Auditoria
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, "XEON COMMAND - AUDIT LOG", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Courier", "B", 11)
        pdf.multi_cell(0, 8, f"NODE: {node_name}\nTAXA: R$ 1.000/H\nCPU: {cpu}%\nHASH: {bc[:16]}\n{'-'*50}\n{sanitize_pdf(ai_report)}")
    
    output = pdf.output()
    if isinstance(output, str): output = output.encode('latin-1')
    return BytesIO(output)

# --- [3. DASHBOARD DE COMANDO - GRÁFICO MATRIX] ---
@st.fragment(run_every=5)
def xeon_core():
    cpu = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1.5, 1])
    
    with c1:
        st.metric("ESTABILIDADE", "NOMINAL")
        st.write(f"<b style='color:{MATRIX_GREEN}; font-size:20px;'>TAXA: R$ 1.000/H</b>", unsafe_allow_html=True)
        st.caption("Filtro Diana: ATIVO")

    with c2:
        # GRÁFICO COM FUNDO TRANSPARENTE E ESTÉTICA VERDE
        options = {
            "backgroundColor": "transparent",
            "series": [{
                "type": 'gauge',
                "axisLine": {"lineStyle": {"width": 10, "color": [[0.3, '#00ff41'], [0.7, '#00ff41'], [1, '#ff4100']]}},
                "pointer": {"itemStyle": {"color": MATRIX_GREEN}},
                "detail": {"valueAnimation": True, "formatter": '{value}%', "color": MATRIX_GREEN},
                "data": [{"value": cpu, "name": 'CPU'}]
            }]
        }
        st_echarts(options=options, height="250px")

    with c3:
        if st.button("🧠 SCAN IA"):
            if client:
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": "Auditoria de Homeostase."}])
                st.session_state.ai_rep = res.choices.message.content
                st.session_state.vox = "Scan completo."

    st.divider()
    
    nos = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'>NÓ 0{i+1}<br><b>{n}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {n}", key=f"btn_{i}"):
                st.session_state.active_node = n
                st.session_state.vox = f"Nó {n} sincronizado."
            
            if st.session_state.get('active_node') == n:
                pdf_data = generate_xeon_pdf(n, cpu, st.session_state.get('ai_rep', "Aguardando Scan..."))
                st.download_button(
                    label="📥 BAIXAR PDF", 
                    data=pdf_data, 
                    file_name=f"XEON_{n}.pdf", 
                    mime="application/pdf", 
                    key=f"dl_{i}"
                )

    if st.session_state.get('vox'):
        components.html(f"<script>var u=new SpeechSynthesisUtterance('{st.session_state.vox}');u.lang='pt-BR';window.speechSynthesis.speak(u);</script>", height=0)
        st.session_state.vox = ""

# --- [4. FINALIZAÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_rep' not in st.session_state: st.session_state.ai_rep = ""
if 'vox' not in st.session_state: st.session_state.vox = ""
xeon_core()
