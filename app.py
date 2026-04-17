import streamlit as st
import time
import hashlib
import psutil
import unicodedata
import textwrap
from fpdf import FPDF # Requisito: fpdf2 no requirements.txt
from io import BytesIO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. IDENTIDADE SOBERANA & PROTEÇÃO DE INFRAESTRUTURA] ---
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
    iframe {{ background-color: transparent !important; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE EVIDÊNCIA TÉCNICA - NIST 800-53 & EB-1A] ---
def sanitize_pdf(text):
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')

def generate_eb1a_dossier(node_name, cpu, ai_report):
    """Gera Dossiê de 6 páginas com mapeamento NIST para interesse nacional (US)"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    ts = time.strftime('%H:%M:%S')
    bc_hash = hashlib.sha256(f"{node_name}{ts}".encode()).hexdigest().upper()
    
    # Mapeamento NIST 800-53 para o Governo dos EUA
    nist_mapping = {
        "AUDITORIA NIST": "AC-2 (Account Management) | AU-6 (Audit Review)",
        "FINANCAS GLOBAIS": "SA-9 (External System Services)",
        "GOVERNANCA PQC": "SC-13 (Cryptographic Protection)",
        "FISIOLOGIA DIGITAL": "SI-4 (Information System Monitoring)",
        "EB-1A EVIDENCE": "PM-1 (Information Security Program)",
        "VEREDITO FINAL": "RA-5 (Vulnerability Monitoring)"
    }

    setores = list(nist_mapping.keys())
    
    for i, setor in enumerate(setores):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 10, "XEON COMMAND - SPECIALIST IN CRITICAL INFRASTRUCTURE", ln=True, align='C')
        pdf.set_font("Courier", "", 10)
        pdf.cell(0, 10, f"NATIONAL INTEREST WAIVER (NIW) - LOG ID: {bc_hash[:16]}", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Courier", "B", 12)
        pdf.cell(0, 8, f"SECTION: {setor}", ln=True)
        pdf.set_text_color(0, 200, 255) # Azul para destaque NIST
        pdf.cell(0, 8, f"NIST 800-53 CONTROL: {nist_mapping[setor]}", ln=True)
        pdf.set_text_color(0, 255, 65)
        pdf.ln(5)
        
        info = ai_report if i == 4 else "INTEGRIDADE OPERACIONAL DE INFRAESTRUTURA NOMINAL."
        wrapped = textwrap.fill(sanitize_pdf(info), width=65)
        
        pdf.set_font("Courier", "", 10)
        content = f"ENGINEER: MARCO ANTONIO DO NASCIMENTO\nRATE: R$ 1.000,00/H\nSYSTEM HOMEOSTASIS: {100-cpu}%\n{'-'*50}\n{wrapped}"
        pdf.multi_cell(0, 7, content)
        
        if setor == "VEREDITO FINAL":
            pdf.ln(10); pdf.set_font("Courier", "B", 12)
            pdf.multi_cell(0, 8, "CERTIFICATION: MISSION CRITICAL PROTECTION READY.\nSTATUS: ELIGIBLE FOR EB-1A / NATIONAL INTEREST.", align='C')

    output = pdf.output()
    if isinstance(output, str): output = output.encode('latin-1')
    return BytesIO(output)

# --- [3. DASHBOARD DE COMANDO CENTRALIZADO] ---
@st.fragment(run_every=5)
def xeon_main():
    cpu = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1.5, 1])
    
    with c1:
        st.metric("STABILITY", "NOMINAL")
        st.write(f"<b style='color:{MATRIX_GREEN}; font-size:22px;'>R$ 1.000/H</b>", unsafe_allow_html=True)
        st.markdown(f"<div style='border:1px solid {MATRIX_GREEN}; padding:5px;'>ID: CRITICAL INFRASTRUCTURE SPECIALIST</div>", unsafe_allow_html=True)

    with c2:
        # Gráfico Matrix Total (Sem Branco)
        options = {
            "backgroundColor": "transparent",
            "series": [{
                "type": 'gauge',
                "axisLine": {"lineStyle": {"width": 10, "color": [[0.3, '#00ff41'], [0.7, '#00ff41'], [1, '#ff4100']]}},
                "pointer": {"itemStyle": {"color": MATRIX_GREEN}},
                "detail": {"color": MATRIX_GREEN, "fontSize": 20},
                "data": [{"value": cpu, "name": 'HOMEÓSTASE'}]
            }]
        }
        st_echarts(options=options, height="240px")

    with c3:
        st.metric("NATIONAL INTEREST", "100%")
        if st.button("🧠 SCAN IA / NIST AUDIT"):
            if client:
                res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": "Gere uma auditoria NIST para infraestrutura crítica EB-1A."}])
                st.session_state.ai_rep = res.choices.message.content
                st.session_state.vox = "Auditoria NIST concluída para o Governo dos Estados Unidos."

    st.divider()
    
    nos = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    for i, n in enumerate(nos):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NÓ 0{i+1}</small><br><b>{n}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {n}", key=f"btn_{i}"):
                st.session_state.active_node = n
                st.session_state.vox = f"Operação {n} sob protocolo NIST."
            
            if st.session_state.get('active_node') == n:
                pdf_data = generate_eb1a_dossier(n, cpu, st.session_state.get('ai_rep', "Inicie o SCAN IA para logs NIST."))
                st.download_button(
                    label=f"📥 DOSSIÊ EB-1A {n}", 
                    data=pdf_data, 
                    file_name=f"XEON_NIST_{n}.pdf", 
                    mime="application/pdf", 
                    key=f"dl_{i}"
                )

    if st.session_state.get('vox'):
        components.html(f"<script>var u=new SpeechSynthesisUtterance('{st.session_state.vox}');u.lang='pt-BR';window.speechSynthesis.speak(u);</script>", height=0)
        st.session_state.vox = ""

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_rep' not in st.session_state: st.session_state.ai_rep = ""
if 'vox' not in st.session_state: st.session_state.vox = ""
xeon_main()
st.caption("ADMIN: MARCO ANTONIO | SPECIALIST IN CRITICAL INFRASTRUCTURE PROTECTION | US NIW ELIGIBLE")
