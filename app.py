import streamlit as st
import time
import psutil
import unicodedata
import yfinance as yf
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
from openai import OpenAI
import textwrap

# --- [1. CONFIGURAÇÃO SOBERANA - BLACKOUT MATRIX] ---
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
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 10px; text-align: center; margin-bottom: 5px; background: rgba(0,255,65,0.05); }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF - PROTOCOLO DE RESILIÊNCIA ABSOLUTA] ---
def sanitize_text(text):
    if not text: return "N/A"
    # Remove qualquer caractere que não seja latin-1 para evitar crash de encode
    return unicodedata.normalize('NFKD', str(text)).encode('latin-1', 'ignore').decode('latin-1')

def get_pdf_bytes_blindado(node, cpu, ai_report):
    """Gera o PDF usando escrita linear para evitar o erro de horizontal space"""
    try:
        pdf = FPDF()
        pdf.set_margins(20, 20, 20)
        pdf.add_page()
        
        # Fundo Blackout
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(0, 0, 210, 297, 'F')
        
        # Cabeçalho
        pdf.set_text_color(0, 255, 65)
        pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, sanitize_text(f"XEON AUDIT: {node}"), ln=True, align='C')
        pdf.ln(10)
        
        # Corpo Técnico
        pdf.set_font("Courier", "", 10)
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Metadados fixos
        meta = [
            f"TIMESTAMP: {ts}",
            f"ARCHITECT: MARCO ANTONIO DO NASCIMENTO",
            f"FEE RATE: R$ 1.000,00 / HOUR",
            f"HOMEOSTASE: {100-(cpu*0.1):.2f}%",
            "-"*45,
            "GEN-AI PHYSIOLOGY ANALYSIS:"
        ]
        
        for m in meta:
            pdf.cell(0, 8, sanitize_text(m), ln=True)
        
        # Processamento do Parecer da IA (Blindagem contra Horizontal Space)
        # Forçamos uma largura de 60 caracteres para nunca estourar a margem
        report_safe = sanitize_text(ai_report)
        wrapped_lines = textwrap.wrap(report_safe, width=60)
        
        for line in wrapped_lines:
            pdf.cell(0, 7, line, ln=True)
            
        pdf.cell(0, 8, "-"*45, ln=True)
        
        return pdf.output()
    except Exception as e:
        # Se tudo falhar, retorna um PDF de emergência com o erro
        fail_pdf = FPDF()
        fail_pdf.add_page()
        fail_pdf.set_font("Courier", "B", 12)
        fail_pdf.cell(0, 10, "ERRO CRITICO DE RENDERIZACAO", ln=True)
        return fail_pdf.output()

# --- [3. DASHBOARD DE COMANDO] ---
@st.fragment(run_every=5)
def xeon_main():
    cpu_val = psutil.cpu_percent()
    c1, c2, c3 = st.columns([1, 1.2, 1])
    
    with c1:
        st.metric("STABILITY", "NOMINAL")
        st.metric("RATE", "R$ 1.000/h")
        try:
            usd = yf.Ticker("USDBRL=X").history(period="1d")['Close'].iloc[-1]
            st.metric("USD/BRL", f"{usd:.2f}")
        except: st.write("Relay Offline")

    with c2:
        st_echarts(options={"backgroundColor": "transparent", "series": [{"type": 'gauge', "data": [{"value": cpu_val}], "detail": {"color": MATRIX_GREEN}}]}, height="220px")

    with c3:
        st.metric("EB-1A READY", "YES")
        if st.button("🧠 SCAN IA"):
            with st.status("Processando...", expanded=False) as s:
                if client:
                    try:
                        res = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": f"Analise brevemente o valor de R$ 1000/h deste sistema de {cpu_val}% carga para o visto EB1A."}]
                        )
                        st.session_state.ai_report = res.choices.message.content
                        st.session_state.vox = "Analise concluída."
                        s.update(label="Concluído", state="complete")
                    except:
                        st.session_state.ai_report = "Erro na API OpenAI."
                        s.update(label="Erro", state="error")
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
                rep = st.session_state.get('ai_report', "Aguardando scan.")
                # Geração de PDF usando o motor blindado
                pdf_data = get_pdf_bytes_blindado(s, cpu_val, rep)
                st.download_button(
                    label="📥 BAIXAR EB-1A PDF", 
                    data=pdf_bytes if 'pdf_bytes' in locals() else pdf_data, 
                    file_name=f"XEON_{s}.pdf", 
                    mime="application/pdf", 
                    key=f"dl_{i}"
                )

    if st.session_state.get('vox'):
        components.html(f"""<script>
            window.speechSynthesis.cancel();
            var m = new SpeechSynthesisUtterance('{st.session_state.vox}');
            m.lang = 'pt-BR'; window.speechSynthesis.speak(m);
        </script>""", height=0)
        st.session_state.vox = ""

# --- [4. FINALIZAÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
if 'ai_report' not in st.session_state: st.session_state.ai_report = ""
if 'vox' not in st.session_state: st.session_state.vox = ""
xeon_main()
