import streamlit as st
import numpy as np
import psutil
import time
import httpx
import asyncio
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ==========================================
# 1. MOTOR DE INTELIGÊNCIA E CHAT (v1015)
# ==========================================
class SovereignEngine:
    @staticmethod
    async def get_mission_intel(category):
        intel_map = {
            "SPACEX": "ESTRATÉGIA: IPO SpaceX (Abril/2026). Starship V3 em teste de reentrada.",
            "LAW": "JURISPRUDÊNCIA: STJ 13/04/2026 exige Erro Zero em perícias de IA.",
            "BIOGENETICS": "BIOTEC: Vacinas sintéticas validadas via Nexus v1015.",
            "MAPA": "SOBERANIA: Corredor Alcântara-Texas monitorado via Starlink.",
            "IPO": "VALUATION: Q3 2026 confirmado para roadshow global."
        }
        await asyncio.sleep(0.1)
        return intel_map.get(category, "NEXUS: Protocolo operacional.")

    @staticmethod
    def generate_dossier_pdf(query, category, content):
        buffer = BytesIO(); p = canvas.Canvas(buffer, pagesize=A4); w, h = A4
        p.setFillColor(colors.HexColor("#05070A")); p.rect(0, h-80, w, 80, fill=1)
        p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(w/2, h-45, "NEXUS SUPREMO: MISSION AUDIT")
        p.save(); buffer.seek(0); return buffer

# ==========================================
# 2. DESIGN STEALTH & MISSION CRITICAL (DARK ONLY)
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1015", layout="wide")

st.markdown("""
    <style>
    /* Fundo e Texto Global */
    .stApp { background-color: #05070A; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
    
    /* Input de Texto - Stealth Dark */
    .stTextInput>div>div>input { background-color: #0D1117 !important; color: #00FF41 !important; border: 1px solid #30363D !important; border-radius: 4px; text-align: center; }
    
    /* Botões Missão Crítica - Fundo Preto/Cinza (Sem Branco) */
    .stButton>button { 
        background-color: #161B22 !important; 
        color: #58A6FF !important; 
        border: 1px solid #30363D !important; 
        border-radius: 4px; 
        font-weight: 600; 
        height: 50px; 
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { border-color: #00FF41 !important; color: #00FF41 !important; background-color: #0D1117 !important; }
    
    /* Chat Bubble Mission Control */
    .chat-bubble { background: #0D1117; padding: 20px; border-radius: 4px; border-left: 5px solid #00FF41; margin-top: 10px; border-top: 1px solid #30363D; border-right: 1px solid #30363D; border-bottom: 1px solid #30363D; }
    
    /* Esconder o header branco do Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

# ==========================================
# 3. INTERFACE OPERACIONAL v1015
# ==========================================
st.markdown("<h2 style='text-align: center; color: #00FF41; letter-spacing: 2px;'>🛡️ NEXUS SUPREMO: v1015</h2>", unsafe_allow_html=True)

# MAPA DE SOBERANIA
map_data = {"lat": [-2.3, 25.9, -15.7], "lon": [-44.4, -97.1, -47.8], "name": ["Alcântara", "Starbase", "Brasília"]}
fig_map = go.Figure(go.Scattergeo(lat=map_data["lat"], lon=map_data["lon"], text=map_data["name"], mode='markers+text', marker=dict(size=12, color='#00FF41')))
fig_map.update_layout(geo=dict(bgcolor='#05070A', showland=True, landcolor='#161B22', showcountries=True), margin=dict(l=0,r=0,t=0,b=0), height=350)
st.plotly_chart(fig_map, use_container_width=True)

# NOVO: CHAT EM TEMPO REAL (Stealth)
st.write("### 💬 NEXUS REAL-TIME CHAT")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if chat_input := st.chat_input("Comande o Nexus via Chat Real-Time..."):
    st.session_state.messages.append({"role": "user", "content": chat_input})
    with st.chat_message("user"):
        st.markdown(chat_input)
    
    res = f"NEXUS v1015: Veredito para '{chat_input}' processado com Erro Zero. Homeostase estável."
    st.session_state.messages.append({"role": "assistant", "content": res})
    with st.chat_message("assistant"):
        st.markdown(res)
    speak(res)

st.divider()

# GRADE DE MISSÃO (CORES SÓBRIAS - SEM BRANCO)
st.write("### 🚀 GRADE OPERACIONAL")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): 
        msg = asyncio.run(SovereignEngine.get_mission_intel("SPACEX"))
        st.session_state.last_res = msg; speak(msg)
    if st.button("⚖️ LAW"): 
        msg = asyncio.run(SovereignEngine.get_mission_intel("LAW"))
        st.session_state.last_res = msg; speak(msg)
with c2:
    if st.button("🧠 NEURALINK"): 
        msg = asyncio.run(SovereignEngine.get_mission_intel("NEURALINK"))
        st.session_state.last_res = msg; speak(msg)
    if st.button("🧬 BIOGENETICS"): 
        msg = asyncio.run(SovereignEngine.get_mission_intel("BIOGENETICS"))
        st.session_state.last_res = msg; speak(msg)
with c3:
    if st.button("📈 IPO GOLD"): 
        msg = asyncio.run(SovereignEngine.get_mission_intel("IPO"))
        st.session_state.last_res = msg; speak(msg)
    if st.button("🛰️ MAPA"): 
        msg = asyncio.run(SovereignEngine.get_mission_intel("MAPA"))
        st.session_state.last_res = msg; speak(msg)

if 'last_res' in st.session_state:
    st.markdown(f'<div class="chat-bubble">{st.session_state.last_res}</div>', unsafe_allow_html=True)
    pdf = SovereignEngine.generate_dossier_pdf("Nexus Command", "STEALTH_AUDIT", st.session_state.last_res)
    st.download_button("📂 EXPORTAR DOSSIÊ PDF", pdf, "Nexus_Stealth.pdf", "application/pdf", use_container_width=True)

# ONDA DE PULSO (ONDA REAL-TIME MANTIDA)
st.divider()
pulse = float(psutil.cpu_percent() + 25); t = np.linspace(0, 10, 500)
y = np.sin(t * (pulse/15) + time.time()) 
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=3), fill='tozeroy'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig, use_container_width=True)

st.caption("Barbie Xeon Omni v1015 | Stealth Mission Architecture | No Regression")
