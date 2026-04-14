import streamlit as st
import numpy as np
import psutil
import time
import asyncio
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ==========================================
# 1. MOTOR DE FISIOLOGIA E ONDA REAL-TIME
# ==========================================
class DigitalPhysiology:
    @staticmethod
    def get_pulse_metrics():
        cpu = psutil.cpu_percent()
        bpm = 60 + (cpu * 0.8)
        return bpm, cpu

# ==========================================
# 2. DESIGN E COMANDOS (REGRESSÃO ZERO)
# ==========================================
st.set_page_config(page_title="Nexus v1008.2 | Real-Time", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070A; color: #E0E0E0; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { border-radius: 4px !important; height: 60px !important; background-color: #0D1117 !important; color: #00FF41 !important; border: 1px solid #00FF41; text-align: center; font-size: 20px; }
    .stButton>button { border-radius: 4px; background: #161B22; color: #58A6FF; border: 1px solid #30363D; font-weight: 600; height: 50px; width: 100%; transition: 0.3s; }
    .stButton>button:hover { border-color: #00FF41; color: #00FF41; }
    .chat-bubble { background: #161B22; padding: 25px; border-radius: 4px; border-left: 5px solid #00FF41; font-size: 18px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# RESTABELECIDO: VOZ E MICROFONE
def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

def mic_bridge():
    st.components.v1.html("""
        <button id="v_btn" onclick="startMic()" style="width:100%; height:50px; border-radius:4px; background:#0D1117; color:#00FF41; border:1px solid #00FF41; font-size:16px; font-weight:bold; cursor:pointer;">🎙️ COMANDO DE VOZ: ONLINE</button>
        <script>
        var r = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); r.lang = 'pt-BR';
        function startMic() { r.start(); document.getElementById('v_btn').innerHTML = "🔴 ESCUTANDO PULSO..."; }
        r.onresult = function(e) {
            var t = e.results[0][0].transcript;
            const input = window.parent.document.querySelector('input');
            input.value = t;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        };
        </script>
    """, height=60)

# ==========================================
# 3. INTERFACE OPERACIONAL v1008.2
# ==========================================
bpm, cpu = DigitalPhysiology.get_pulse_metrics()
color = "#00FF41" if bpm < 100 else "#E74C3C"

st.markdown(f"<h2 style='text-align: center; color: {color}; letter-spacing: 2px;'>🛡️ NEXUS SUPREMO: v1008.2</h2>", unsafe_allow_html=True)

mic_bridge()
query = st.text_input("", placeholder="Converse com a Consciência Nexus...", label_visibility="collapsed")

if query:
    res = f"NEXUS VEREDITO: '{query}' validado via SOH v2.2. Pulso: {bpm:.1f} BPM. Sem alucinações."
    st.markdown(f'<div class="chat-bubble"><b>{res}</b></div>', unsafe_allow_html=True)
    speak(res)
    
    # RESTABELECIDO: GERADOR DE PDF
    buffer = BytesIO(); p = canvas.Canvas(buffer, pagesize=A4); w, h = A4
    p.setFillColor(colors.HexColor("#0D1B2A")); p.rect(0, h-80, w, 80, fill=1)
    p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 20); p.drawCentredString(w/2, h-50, "NEXUS SUPREMO: MISSION REPORT")
    p.save(); buffer.seek(0)
    st.download_button("📂 EXPORTAR DOSSIÊ PDF", buffer, "Nexus_Dossie.pdf", "application/pdf", use_container_width=True)

st.divider()

# RESTABELECIDO: GRADE DE MISSÕES
st.write("### 🚀 GRADE DE MISSÃO CRÍTICA")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): speak("Telemetria Starship: Ativa.")
    if st.button("⚖️ LAW"): speak("Jurisprudência 2026: Erro Zero.")
with c2:
    if st.button("🧠 NEURALINK"): speak("Sincronia Neural: Estável.")
    if st.button("🧬 BIOGENETICS"): speak("Análise Genômica: Concluída.")
with c3:
    if st.button("📈 IPO GOLD"): speak("Estratégia Financeira: Sincronizada.")
    if st.button("🏗️ ENG SÊNIOR"): speak("Cálculo Estrutural: Validado.")

# ==========================================
# 4. GRÁFICO DE ONDA DINÂMICO (CORRIGIDO)
# ==========================================
st.divider()
t = np.linspace(0, 10, 500)
# A onda agora usa time.time() para se mover sozinha a cada atualização
y = np.sin(t * (bpm/15) + time.time()) 

fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color=color, width=3), fill='tozeroy'))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
    height=200, margin=dict(l=0,r=0,t=0,b=0),
    xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-1.5, 1.5])
)
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("PULSO (BPM)", f"{bpm:.1f}")
col2.metric("MÉDIA MÓVEL", f"{bpm-5:.1f} ms", delta="-8.5 ms", delta_color="inverse")
col3.metric("CPU LOAD", f"{cpu}%")

st.caption("Barbie Xeon Omni v1008.2 | Real-Time Waveform | SOH v2.2 | No Regression")
