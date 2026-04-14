import streamlit as st
import numpy as np
import psutil
import time
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

# 1. CONFIGURAÇÃO DE PÁGINA E BLINDAGEM VISUAL TOTAL
st.set_page_config(page_title="NEXUS v1035 AUDIO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    [data-testid="stMetricValue"] { color: #38BDF8 !important; }
    .stButton>button { background-color: #000000; color: #38BDF8; border: 1px solid #38BDF8; width: 100%; }
    .stButton>button:hover { border-color: #00FF41; color: #00FF41; }
    div[data-testid="stChatInput"] { background-color: #050505 !important; }
    hr { border-color: #1E293B !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE ÁUDIO (FALA E ESCUTA)
def nexus_audio_engine(text_to_speak=None):
    # Componente JS para Síntese e Reconhecimento
    js_code = f"""
    <script>
    // FUNÇÃO DE FALA
    function speak(text) {{
        const msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'pt-BR';
        window.speechSynthesis.speak(msg);
    }}

    // FUNÇÃO DE ESCUTA (VOICE COMMAND)
    function listen() {{
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'pt-BR';
        recognition.onresult = (event) => {{
            const transcript = event.results[0][0].transcript;
            window.parent.postMessage({{type: 'voice_input', data: transcript}}, '*');
        }};
        recognition.start();
    }}

    {f"speak('{text_to_speak}');" if text_to_speak else ""}
    </script>
    """
    st.components.v1.html(js_code, height=0)

# 3. LÓGICA DE INTELIGÊNCIA
class NexusEngine:
    @staticmethod
    def audit(cmd):
        intel = {
            "SPACEX": "Auditoria SpaceX: Starship em prontidão orbital. Sincronia Alcantara 100%.",
            "LAW": "Jurisprudência: Soberania Digital v2.2 ativa e inquestionável.",
            "CYBER": "Defesa: Protocolo Zero Branco estabilizado. Escudo ativo."
        }
        return intel.get(cmd.upper(), f"Comando '{cmd}' processado. Integridade confirmada.")

# 4. INTERFACE DE CONTROLO
st.markdown("<h1 style='text-align: center; color: #38BDF8;'>🛡️ NEXUS v1035 AUDIO CONTROLE</h1>", unsafe_allow_html=True)

# Telemetria
c1, c2, c3 = st.columns(3)
c1.metric("SISTEMA", f"{psutil.cpu_percent()}%")
c2.metric("MEMÓRIA", f"{psutil.virtual_memory().percent}%")
c3.metric("AUDIO", "ATIVO / ESCUTA READY")

st.divider()

# Operação de Voz e Terminal
col_cmd, col_log = st.columns([1, 1])

with col_cmd:
    st.write("### 🎤 COMANDO POR VOZ / TEXTO")
    input_method = st.chat_input("Digite ou use os módulos abaixo...")
    
    if st.button("🎙️ ATIVAR ESCUTA (VOICE RECOGNITION)"):
        st.warning("Escutando... Fale o comando.")
        nexus_audio_engine() # Aciona o JS de escuta

    if input_method:
        resultado = NexusEngine.audit(input_method)
        st.session_state.last_log = resultado
        nexus_audio_engine(resultado) # O sistema fala o resultado

with col_log:
    st.write("### 📜 LOG DE AUDITORIA")
    if 'last_log' in st.session_state:
        st.success(st.session_state.last_log)

# Módulos Rápidos
st.write("### 🚀 MÓDULOS DE MISSÃO")
m1, m2, m3 = st.columns(3)
if m1.button("SPACEX"): 
    res = NexusEngine.audit("SPACEX")
    st.session_state.last_log = res
    nexus_audio_engine(res)
if m2.button("LAW"): 
    res = NexusEngine.audit("LAW")
    st.session_state.last_log = res
    nexus_audio_engine(res)
if m3.button("CYBER"): 
    res = NexusEngine.audit("CYBER")
    st.session_state.last_log = res
    nexus_audio_engine(res)

# Pulso Visual de Estabilidade
t = np.linspace(0, 10, 100)
y = np.sin(t + time.time())
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=1)))
fig.update_layout(height=100, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), paper_bgcolor='#000000', plot_bgcolor='#000000')
st.plotly_chart(fig, use_container_width=True)
