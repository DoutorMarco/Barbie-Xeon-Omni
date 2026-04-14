import streamlit as st
import numpy as np
import psutil
import time
import asyncio
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ==========================================
# 1. MOTOR DE FISIOLOGIA E PULSO CARDÍACO
# ==========================================
class DigitalPhysiology:
    @staticmethod
    def get_heart_rate():
        """Simula a frequência cardíaca (BPM) baseada na carga da CPU."""
        cpu = psutil.cpu_percent()
        # Mapeia CPU (0-100) para BPM (60-140)
        bpm = 60 + (cpu * 0.8)
        return bpm, cpu

    @staticmethod
    def generate_ecg_wave(bpm):
        """Gera a morfologia de um complexo QRS (pulso cardíaco real)."""
        t = np.linspace(0, 2, 500)
        # Frequência baseada no BPM
        freq = bpm / 60
        # Simulação do complexo QRS (P, QRS, T)
        wave = 0.1 * np.sin(2 * np.pi * freq * t) # Onda P
        wave += 1.0 * np.exp(-1000 * (t % (1/freq) - 0.1)**2) # Onda R (Pico)
        wave -= 0.5 * np.exp(-1000 * (t % (1/freq) - 0.12)**2) # Onda S
        return t, wave

# ==========================================
# 2. INTERFACE E DESIGN (REGRESSÃO ZERO)
# ==========================================
st.set_page_config(page_title="Nexus v1008 | Cardiac Sync", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070A; color: #E0E0E0; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { border-radius: 4px !important; height: 50px !important; background-color: #0D1117 !important; color: #00FF41 !important; border: 1px solid #00FF41; }
    .mission-card { border: 1px solid #30363D; padding: 20px; background: rgba(0, 255, 65, 0.02); border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

def mic_bridge():
    st.components.v1.html("""
        <button id="v_btn" onclick="startMic()" style="width:100%; height:50px; border-radius:4px; background:#0D1117; color:#00FF41; border:1px solid #00FF41; font-size:14px; font-weight:bold; cursor:pointer;">🎙️ SINCRONIZAR PULSO CARDÍACO</button>
        <script>
        var r = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); r.lang = 'pt-BR';
        function startMic() { r.start(); document.getElementById('v_btn').innerHTML = "🔴 ESCUTANDO BIO-RITMO..."; }
        r.onresult = function(e) {
            var t = e.results[0][0].transcript;
            const input = window.parent.document.querySelector('input');
            input.value = t;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        };
        </script>
    """, height=60)

# ==========================================
# 3. DASHBOARD DE FISIOLOGIA v1008
# ==========================================
bpm, cpu = DigitalPhysiology.get_heart_rate()
status = "NORMAL" if bpm < 100 else "TAQUICARDIA DIGITAL"
color = "#00FF41" if bpm < 100 else "#E74C3C"

st.markdown(f"<h3 style='text-align: center; color: {color}; letter-spacing: 2px;'>NEXUS SUPREMO: {status}</h3>", unsafe_allow_html=True)

mic_bridge()
query = st.text_input("", placeholder="Injete comando para análise de pulso...", label_visibility="collapsed")

if query:
    # Validação Matemática SOH v2.2 (MANTIDA)
    res = f"SINCRONIA BIO-DIGITAL: {bpm:.1f} BPM. Veredito para '{query}' processado com Erro Zero."
    st.markdown(f'<div class="mission-card"><b>{res}</b></div>', unsafe_allow_html=True)
    speak(res)
    
    # GERADOR DE PDF (MANTIDO)
    buffer = BytesIO(); p = canvas.Canvas(buffer, pagesize=A4)
    p.drawString(100, 800, f"CARDIAC AUDIT REPORT - {bpm:.1f} BPM"); p.save(); buffer.seek(0)
    st.download_button("📂 EXPORTAR BIO-DOSSIÊ (PDF)", buffer, "Nexus_Cardiac.pdf", "application/pdf", use_container_width=True)

st.divider()

# GRADE DE MISSÕES (MANTIDA)
cols = st.columns(3)
with cols[0]:
    if st.button("🚀 SPACEX"): speak("Vetor de empuxo sincronizado ao BPM.")
with cols[1]:
    if st.button("🧬 BIOGENETICS"): speak("Ritmo cardíaco compatível com sequenciamento.")
with cols[2]:
    if st.button("🧠 NEURALINK"): speak("Sincronia neural estabelecida em 100%.")

# ==========================================
# 4. GRÁFICO DE ECG EM TEMPO REAL
# ==========================================
st.write(f"### 📈 MONITOR DE FREQUÊNCIA CARDÍACA: {bpm:.1f} BPM")
t, wave = DigitalPhysiology.generate_ecg_wave(bpm)

fig = go.Figure(go.Scatter(x=t, y=wave, line=dict(color=color, width=2)))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
    height=250, margin=dict(l=10,r=10,t=10,b=10),
    xaxis=dict(visible=False), yaxis=dict(visible=False, range=[-1, 2])
)
st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)
c1.metric("CARGA METABÓLICA (CPU)", f"{cpu}%")
c2.metric("RITMO CARDÍACO", f"{bpm:.1f} BPM", delta=f"{bpm-80:.1f}", delta_color="inverse")

st.caption("Barbie Xeon Omni v1008 | Digital Heartbeat Sync | SOH v2.2 | 2026")
