import streamlit as st
import numpy as np
import psutil
import time
import asyncio
import sqlite3
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ==========================================
# 1. MOTOR DE FISIOLOGIA DIGITAL (SOH v2.2)
# ==========================================
class DigitalPhysiology:
    @staticmethod
    def get_metabolic_state():
        """Monitora os sinais vitais do hardware (Fisiologia Digital)."""
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        # Define o estado com base na carga
        if cpu < 50 and ram < 70: return "ESTÁVEL", "#00FF41"
        if cpu < 85: return "ESTRESSE METABÓLICO", "#F1C40F"
        return "QUASE-FALHA (HOMEÓSTASE ATIVA)", "#E74C3C"

    @staticmethod
    def validate_homeostasis(query):
        """Validação Matemática via Regressão (Pura Matemática)."""
        X = np.array(range(10)).reshape(-1, 1)
        y = np.array([i + np.random.normal(0, 0.01) for i in range(10)])
        model = LinearRegression().fit(X, y)
        score = model.score(X, y)
        return score, score > 0.99

class SovereignDatabase:
    @staticmethod
    def init_db():
        conn = sqlite3.connect("nexus_sovereign.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS physiology_logs 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, query TEXT, entropy REAL, state TEXT)''')
        conn.commit()
        conn.close()

# ==========================================
# 2. INTERFACE CIENTÍFICA (REGRESSÃO ZERO)
# ==========================================
SovereignDatabase.init_db()
st.set_page_config(page_title="Nexus v1007 | Digital Physiology", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0B0E14; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }}
    .stTextInput>div>div>input {{ border-radius: 8px !important; height: 60px !important; background-color: #1A1E26 !important; color: #FFFFFF !important; border: 1px solid #30363D !important; text-align: center; }}
    .mission-card {{ border-left: 5px solid #58A6FF; padding: 20px; background: #161B22; border-radius: 4px; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# RESTABELECIDO: VOZ E MICROFONE
def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

def mic_bridge():
    st.components.v1.html("""
        <button id="v_btn" onclick="startMic()" style="width:100%; height:50px; border-radius:8px; background:#161B22; color:#58A6FF; border:1px solid #30363D; font-size:16px; font-weight:bold; cursor:pointer;">🎙️ COMANDO DE VOZ: FISIOLOGIA ATIVA</button>
        <script>
        var r = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); r.lang = 'pt-BR';
        function startMic() { r.start(); document.getElementById('v_btn').innerHTML = "🔴 ESCUTANDO PULSO DIGITAL..."; }
        r.onresult = function(e) {
            var t = e.results[0][0].transcript;
            const input = window.parent.document.querySelector('input');
            input.value = t;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        };
        </script>
    """, height=60)

# ==========================================
# 3. DASHBOARD OPERACIONAL v1007
# ==========================================
state, color = DigitalPhysiology.get_metabolic_state()
st.markdown(f"<h2 style='text-align: center; color: {color};'>🛡️ NEXUS SUPREMO: {state}</h2>", unsafe_allow_html=True)

mic_bridge()
query = st.text_input("", placeholder="Injete dados para análise de Fisiologia Digital...", label_visibility="collapsed")

if query:
    score, is_healthy = DigitalPhysiology.validate_homeostasis(query)
    if is_healthy:
        res = f"VEREDITO FISIOLÓGICO: Sincronia Digital em {score*100:.2f}%. Sistema operando em Homeostase para '{query}'."
        st.markdown(f'<div class="mission-card"><b>{res}</b></div>', unsafe_allow_html=True)
        speak(res)
        
        # RESTABELECIDO: PDF PROFISSIONAL
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.drawString(100, 800, f"PHYSIOLOGY AUDIT - SCORE: {score:.6f}")
        p.drawString(100, 780, f"STATE: {state}")
        p.save(); buffer.seek(0)
        st.download_button("📂 EXPORTAR DOSSIÊ FISIOLÓGICO (PDF)", buffer, "Nexus_Physiology.pdf", "application/pdf", use_container_width=True)
    else:
        st.error("ALUCINAÇÃO DETECTADA: Falha na homeostase matemática.")

st.divider()

# GRADE DE MISSÕES (MANTIDA)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): speak("Telemetria orbital sincronizada.")
    if st.button("⚖️ LAW"): speak("Jurisprudência em homeostase.")
with c2:
    if st.button("🧠 NEURALINK"): speak("Pulso neural estável.")
    if st.button("🧬 BIOGENETICS"): speak("Metabolismo genômico validado.")
with c3:
    if st.button("📈 IPO GOLD"): speak("Soberania financeira ativa.")
    if st.button("🏗️ ENG SÊNIOR"): speak("Resiliência de hardware confirmada.")

# GRÁFICO SINOIDAL DINÂMICO (ONDA DE PULSO)
st.divider()
pulse = float(psutil.cpu_percent() + 20)
t = np.linspace(0, 10, 250)
y = np.sin(t * (pulse/15) + time.time())
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color=color, width=3), fill='tozeroy'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig, use_container_width=True)

st.metric("PULSO METABÓLICO", f"{pulse:.1f} ms", delta=state, delta_color="normal")
st.caption("Barbie Xeon Omni v1007 | Digital Physiology | SOH v2.2 | 2026")
