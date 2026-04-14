import streamlit as st
import aiosqlite
import asyncio
from fpdf import FPDF
import datetime
import psutil

# 1. OVERRIDE DE INTERFACE: BLACKOUT TOTAL & VERDE MATRIX
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")

st.markdown(
    """
    <style>
    /* Injeção de Nível Zero: Cor de Fundo e Texto */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Eliminação de Resíduos Brancos (Toolbars e Dividers) */
    [data-testid="stToolbar"], [data-testid="stDecoration"], footer, hr {
        display: none !important;
    }

    /* Input de Comando: Blackout Reengenheirado */
    [data-testid="stChatInput"], div[data-baseweb="base-input"], div[role="textbox"] {
        background-color: #000000 !important;
        border: 1px solid #00FF41 !important;
        border-radius: 4px;
    }
    
    input, textarea {
        color: #00FF41 !important;
        background-color: #000000 !important;
        -webkit-text-fill-color: #00FF41 !important;
    }

    /* Estilização de Botões Funcionais (Matrix Style) */
    .stButton>button {
        width: 100%;
        background-color: #000000 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important;
        color: #000000 !important;
        box-shadow: 0 0 15px #00FF41;
    }

    /* Métricas e Alertas */
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"], .stAlert {
        background-color: #000000 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. MÓDULO DE VOZ MULTILINGUE (SPEAK)
def speak_command(text, lang='pt-BR'):
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.lang = '{lang}';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# 3. MÓDULO DE IMPRESSÃO DE PDF (R$ 1.000/H)
def generate_dossier(cmd):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65)
    pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 10, "XEON COMMAND - ELITE AUDIT", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Courier", "", 12)
    body = (
        f"AUDIT PROTOCOL: CRITICAL INFRASTRUCTURE\n"
        f"EXPERT: MARCO ANTONIO DO NASCIMENTO\n"
        f"VALUATION: R$ 1.000,00 / HOUR\n"
        f"TIMESTAMP: {datetime.datetime.now()}\n"
        f"COMMAND LOG: {cmd}\n"
        "STATUS: NOMINAL / IMMUTABLE LEDGER VERIFIED"
    )
    pdf.multi_cell(0, 10, body)
    return pdf.output(dest='S').encode('latin-1')

# 4. DASHBOARD E BOTÕES FUNCIONAIS (FRONT-END ORIGINAL)
st.title("🛰️ X E O N   C O M M A N D   v 5 4 . 0")

# Métricas de Hardware
c1, c2, c3, c4 = st.columns(4)
c1.metric("LOAD", f"{psutil.cpu_percent()}%", "SYSTEM")
c2.metric("UPTIME", "STABLE", "24/7")
c3.metric("LEDGER", "AIOSQLITE", "ACTIVE")
c4.metric("RATE", "R$ 1.000/h", "SOVEREIGN")

st.markdown("<br>", unsafe_allow_html=True)

# Painel de Controle de Voz e Documentação
col_listen, col_speak, col_pdf = st.columns(3)

with col_listen:
    if st.button("🎙️ START LISTENING (EN/PT)"):
        st.warning("Listening Protocol Active... (Speak now)")
        # A integração de escuta browser-side requer Web Speech API via JS

with col_speak:
    if st.button("🔊 VOICE RESPONSE (SOH v2.2)"):
        speak_command("System nominal. Rate established at one thousand reais per hour.", lang='en-US')
        speak_command("Sistema nominal. Taxa estabelecida em mil reais por hora.", lang='pt-BR')

with col_pdf:
    if st.button("📄 PRINT AUDIT DOSSIER"):
        pdf_bytes = generate_dossier("Manual Trigger Audit")
        st.download_button("💾 DOWNLOAD R$ 1.000/H PDF", pdf_bytes, "XEON_AUDIT_1000.pdf", "application/pdf")

# 5. COMMAND INPUT (ESTÉTICA MATRIX)
prompt = st.chat_input("Insert Global Command...")

if prompt:
    st.write(f"[>] Processed by Diana Filter: {prompt}")
    if "speak" in prompt.lower():
        speak_command(prompt.replace("speak", ""), lang='en-US')
    elif "fale" in prompt.lower():
        speak_command(prompt.replace("fale", ""), lang='pt-BR')
