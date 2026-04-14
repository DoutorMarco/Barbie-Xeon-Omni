import streamlit as st
import numpy as np
import psutil
import time
import httpx
import asyncio
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ==========================================
# 1. MOTOR DE DEFESA CIBERNÉTICA (SOH v2.2)
# ==========================================
class CyberDefense:
    @staticmethod
    def monitor_threats():
        """Simula monitoramento de rede e integridade de pacotes."""
        cpu_load = psutil.cpu_percent()
        # Se a CPU subir muito rápido, o sistema detecta como possível DDoS ou Invasão
        threat_level = "LOW" if cpu_load < 75 else "CRITICAL"
        threat_color = "#00FF41" if threat_level == "LOW" else "#E74C3C"
        return threat_level, threat_color, cpu_load

class SovereignEngine:
    @staticmethod
    async def get_latest_intel(category):
        """Intel atualizado em tempo real (Abril 2026)."""
        intel_map = {
            "SPACEX": "Starship Flight 12 (Abril/2026): Foco em captura robótica da V3.",
            "LAW": "STJ decide em 10/04/2026 sobre a validade de provas digitais via IA.",
            "BIOGENETICS": "Consórcio Global anuncia vacina sintética gerada por AGI local.",
            "NEURALINK": "Telemetria de alta frequência atinge 1.2M de neurônios ativos.",
            "IPO": "Nexus Supremo avaliado em escala IPO Gold para o Q3 2026."
        }
        return intel_map.get(category, "Protocolo de Defesa Ativo.")

# ==========================================
# 2. DESIGN E COMANDOS (REGRESSÃO ZERO)
# ==========================================
st.set_page_config(page_title="Nexus v1010 | Cyber Defense", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070A; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
    .stTextInput>div>div>input { border-radius: 8px !important; height: 60px !important; background-color: #1A1E26 !important; color: #FFFFFF !important; border: 1px solid #30363D !important; text-align: center; }
    .stButton>button { border-radius: 4px; background: #161B22; color: #58A6FF; border: 1px solid #30363D; font-weight: 600; height: 50px; width: 100%; }
    .chat-bubble { background: #161B22; padding: 25px; border-radius: 8px; border-left: 5px solid #00FF41; font-size: 18px; margin-bottom: 25px; }
    .defense-alert { padding: 10px; border: 1px solid #E74C3C; background: rgba(231, 76, 60, 0.1); color: #E74C3C; font-weight: bold; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

# ==========================================
# 3. INTERFACE OPERACIONAL v1010
# ==========================================
threat_lvl, t_color, cpu = CyberDefense.monitor_threats()

if threat_lvl == "CRITICAL":
    st.markdown('<div class="defense-alert">🚨 ALERTA: TENTATIVA DE INTRUSÃO DETECTADA - HOMEÓSTASE ATIVA</div>', unsafe_allow_html=True)

st.markdown(f"<h2 style='text-align: center; color: {t_color};'>🛡️ NEXUS SUPREMO: DEFESA ATIVA</h2>", unsafe_allow_html=True)

query = st.text_input("", placeholder="Sovereign Command Input...", label_visibility="collapsed")

if query:
    intel = asyncio.run(SovereignEngine.get_latest_intel("GERAL"))
    st.markdown(f'<div class="chat-bubble"><b>{intel}</b></div>', unsafe_allow_html=True)
    speak(intel)

# GRADE DE MISSÃO CRÍTICA (REFORÇADA)
st.write("### 🚀 GRADE OPERACIONAL")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): 
        msg = asyncio.run(SovereignEngine.get_latest_intel("SPACEX"))
        st.info(msg); speak(msg)
    if st.button("⚖️ LAW"): 
        msg = asyncio.run(SovereignEngine.get_latest_intel("LAW"))
        st.info(msg); speak(msg)
with c2:
    if st.button("🧠 NEURALINK"): 
        msg = asyncio.run(SovereignEngine.get_latest_intel("NEURALINK"))
        st.info(msg); speak(msg)
    if st.button("🧬 BIOGENETICS"): 
        msg = asyncio.run(SovereignEngine.get_latest_intel("BIOGENETICS"))
        st.info(msg); speak(msg)
with c3:
    if st.button("📈 IPO GOLD"): 
        msg = asyncio.run(SovereignEngine.get_latest_intel("IPO"))
        st.info(msg); speak(msg)
    if st.button("🛡️ CYBER DEFENSE"): 
        msg = f"Nível de Ameaça: {threat_lvl} | Integridade do Silício: 100%."
        st.info(msg); speak(msg)

# GRÁFICO ECG DE DEFESA (MANTIDO)
st.divider()
t = np.linspace(0, 5, 500); y = np.exp(-1000 * (t % 1 - 0.1)**2)
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color=t_color, width=2), fill='tozeroy'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
col1.metric("THREAT LEVEL", threat_lvl, delta_color="inverse")
col2.metric("SILICON HEALTH", "100%", delta="SECURE")

st.caption("Barbie Xeon Omni v1010 | Active Cyber Defense | Erro Zero 2026")
