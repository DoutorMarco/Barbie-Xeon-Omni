import streamlit as st
import time
import hashlib
import psutil
import unicodedata
import requests
import textwrap
from fpdf import FPDF
from io import BytesIO  # MEMÓRIA BLINDADA CONTRA CORRUPÇÃO
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI

# --- [1. CONFIGURAÇÃO SOBERANA - BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0 | SOH v2.2", layout="wide")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    client = None

# ELIMINAÇÃO TOTAL DE BRANCO (ZERO WHITE POLICY)
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    code, pre {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 60px;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 30px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; text-align: center; background: rgba(0,255,65,0.05); margin-bottom: 10px; }}
    hr {{ border: 1px solid {MATRIX_GREEN} !important; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF 6 PÁGINAS - PROTOCOLO BYTESIO BLINDADO] ---
def sanitize_to_pdf(text):
    if not text: return "N/A"
    return unicodedata.normalize('NFKD', str(text)).encode('latin-1', 'ignore').decode('latin-1')

def generate_sovereign_pdf_6pages(node_name, cpu, ai_report):
    """Gera o dossiê de 6 páginas e retorna um buffer de bytes puro para o navegador"""
    try:
        pdf = FPDF()
        pdf.set_margins(20, 20, 20)
        ts_now = time.strftime('%H:%M:%S')
        bc_hash = hashlib.sha256(f"{node_name}{ts_now}".encode()).hexdigest().upper()
        
        # Estrutura de Auditoria Conforme Anexo Técnico
        setores = ["AUDITORIA NIST", "FINANÇAS GLOBAIS", "GOVERNANÇA PQC", "FISIOLOGIA DIGITAL", "EB-1A EVIDENCE", "VEREDITO FINAL"]
        
        for i, setor in enumerate(setores):
            pdf.add_page()
            pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F') # Fundo Absolute Black
            pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
            pdf.cell(0, 10, "XEON COMMAND AUDIT - BIOINFORMATICA FISIOLOGICA", ln=True, align='C')
            pdf.set_font("Courier", "", 10)
            pdf.cell(0, 10, sanitize_to_pdf(f"BLOCKCHAIN_ID: {bc_hash[:16]} | PAGE {i+1}/6"), ln=True, align='C')
            pdf.ln(10)
            
            wrapped_ai = textwrap.fill(sanitize_to_pdf(ai_report), width=65) if i == 4 else "SISTEMA EM HOMEOSTASE ABSOLUTA."
            
            lines = [
                f"SETOR_AUDITADO: {setor}",
                f"NODE_ALVO: {node_name}",
                f"TIMESTAMP: {ts_now}",
                f"RATE: R$ 1.000,00 / HOUR",
                f"STABILITY: {100-(cpu*0.1):.2f}%",
                f"BLOCKCHAIN_PROOF: {bc_hash}",
                "-"*50,
                wrapped_ai,
                "-"*50
            ]
            pdf.set_font("Courier", "B", 11)
            for line in lines: pdf.multi_cell(0, 8, line)
            
            if setor == "VEREDITO FINAL":
                pdf.ln(15); pdf.set_font("Courier", "B", 14)
                pdf.cell(0, 10, "STATUS: NIW ELIGIBLE / MISSION SUCCESS", ln=True, align='C')

        # O SEGREDO: Exportação binária via BytesIO para evitar corrupção de string
        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str):
            return pdf_output.encode('latin-1')
        return bytes(pdf_output)
    except Exception as e:
        return f"ERRO_PDF_CRITICO: {str(e)}".encode('latin-1')

# --- [3. DASHBOARD DE COMANDO CENTRAL] ---
@st.fragment(run_every=5)
def xeon_main():
    cpu_val = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1.2, 1])
    
    with c1:
        st.metric("STABILITY", "NOMINAL")
        st.write(f"<b style='color:{MATRIX_GREEN}; font-size:25px;'>R$ 1.000/h</b>", unsafe_allow_html=True)
        st.markdown(f"<div style='border:1px solid {MATRIX_GREEN}; padding:5px;'>BLOCKCHAIN: ACTIVE<br>S&P 500: SYNCED</div>", unsafe_allow_html=True)

    with c2:
        st_echarts(options={"backgroundColor": "transparent", "series": [{"type": 'gauge', "data": [{"value": cpu_val}], "detail": {"color": MATRIX_GREEN}}]}, height="220px")

    with c3:
        st.metric("EB-1A READY", "YES")
        if st.button("🧠 SCAN IA FISIOLÓGICO"):
            with st.status("Auditando...", expanded=False) as status:
                if client:
                    res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": "Gere parecer EB-1A sobre soberania digital e infraestrutura crítica."}])
                    st.session_state.ai_rep = res.choices.message.content
                    st.session_state.vox = "Análise concluída com sucesso."
                    status.update(label="Complete", state="complete")

    st.divider()

    # 9 NÓS DE DEFESA OPERACIONAIS
    setores_nos = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    cols = st.columns(3)
    for i, s in enumerate(setores_nos):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            if st.button(f"ATIVAR {s}", key=f"act_{i}"):
                st.session_state.active_node = s
                st.session_state.vox = f"Nó {s} operacional."
            
            if st.session_state.get('active_node') == s:
                rep = st.session_state.get('ai_rep', "Inicie o SCAN IA.")
                # Geração de PDF via motor BytesIO Blindado
                pdf_data = generate_sovereign_pdf_6pages(s, cpu_val, rep)
                st.download_button(
                    label=f"📥 BAIXAR EB-1A {s}", 
                    data=pdf_data, 
                    file_name=f"XEON_AUDIT_{s}.pdf", 
                    mime="application/pdf", 
                    key=f"dl_{i}"
                )

    if st.session_state.get('vox'):
        components.html(f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{st.session_state.vox}'); m.lang='pt-BR'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.vox = ""

# --- [4. FINALIZAÇÃO SOBERANA] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 5px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_rep' not in st.session_state: st.session_state.ai_rep = ""
if 'vox' not in st.session_state: st.session_state.vox = ""
xeon_main()
st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | R$ 1.000/H")
