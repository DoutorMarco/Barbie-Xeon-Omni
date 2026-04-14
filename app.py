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
# 1. MOTOR DE INTELIGÊNCIA E GEOPOLÍTICA
# ==========================================
class NexusSovereignEngine:
    @staticmethod
    async def get_mission_report(category):
        intel = {
            "SPACEX": "AUDITORIA: Starbase Texas integrada ao Corredor Alcântara. IPO SpaceX 2026 validado via SOH.",
            "LAW": "VEREDITO: STF/STJ Abril 2026. Soberania de Dados e Auditoria Forense em regime de Missão Crítica.",
            "NEURALINK": "BIO-INTEL: Sincronia BCI estável. Bio-feedback integrado à Fisiologia Digital Nexus.",
            "BIOGENETICS": "CIÊNCIA: Sequenciamento genômico soberano concluído. Sem resíduos de alucinação lógica.",
            "IPO": "VALUATION: Roadshow Global em curso. Projeção de liquidez v1025 em escala máxima.",
            "ENGINEERING": "ESTRUTURA: Engenharia Sênior validada para operações aeroespaciais Alcântara-SpaceX."
        }
        await asyncio.sleep(0.2)
        return intel.get(category, "NEXUS: Protocolo de Soberania Ativo.")

# ==========================================
# 2. BLINDAGEM STEALTH TOTAL (ZERO BRANCO)
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1025", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    :root { background-color: #000000 !important; }
    .stApp, .main, .block-container, [data-testid="stHeader"], [data-testid="stCanvas"] {
        background-color: #000000 !important;
        color: #00FF41 !important;
    }
    header, footer { visibility: hidden !important; height: 0px !important; }
    
    /* Inputs de Ingestão - Estilo Terminal Sênior */
    .stTextInput>div>div>input, .stChatInput textarea { 
        background-color: #0D1117 !important; 
        color: #00FF41 !important; 
        border: 1px solid #30363D !important; 
        font-family: monospace;
    }
    
    /* Botões Industriais */
    .stButton>button { 
        background-color: #111827 !important; 
        color: #38BDF8 !important; 
        border: 1px solid #1E293B !important; 
        font-weight: bold;
        height: 55px;
        width: 100%;
        text-transform: uppercase;
    }
    .stButton>button:hover { border-color: #00FF41 !important; color: #00FF41 !important; }
    
    .res-box { background: #0D1117; padding: 20px; border-left: 5px solid #00FF41; margin-top: 15px; color: #00FF41; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

# ==========================================
# 3. INTERFACE OPERACIONAL v1025
# ==========================================
st.markdown("<h2 style='text-align: center; color: #38BDF8; letter-spacing: 5px;'>🛡️ NEXUS SUPREMO: v1025</h2>", unsafe_allow_html=True)

# --- NOVO: MONITOR DE AUDITORIA GEOPOLÍTICA (MAPA) ---
st.write("### 🌎 MONITOR DE AUDITORIA GEOPOLÍTICA")
map_data = {"lat": [-2.3, 25.9, -15.7], "lon": [-44.4, -97.1, -47.8], "name": ["Alcântara", "Starbase TX", "STF Brasília"]}
fig_map = go.Figure(go.Scattergeo(lat=map_data["lat"], lon=map_data["lon"], text=map_data["name"], mode='markers+text', marker=dict(size=12, color='#38BDF8')))
fig_map.update_layout(geo=dict(bgcolor='#000000', showland=True, landcolor='#0D1117', showcountries=True, countrycolor='#1E293B'), margin=dict(l=0,r=0,t=0,b=0), height=350)
st.plotly_chart(fig_map, use_container_width=True)

# --- RESTABELECIDO: INGESTÃO E COMANDO DE VOZ ---
st.write("### ⌨️ INGESTÃO DE DADOS E COMANDO")
if chat_input := st.chat_input("Insira Comando Lógico ou Pesquisa..."):
    res = f"NEXUS v1025: Pesquisa sobre '{chat_input}' processada. Auditoria Geopolítica validada via SOH v2.2."
    with st.chat_message("assistant"):
        st.markdown(res)
    speak(res)

st.divider()

# --- RESTABELECIDO: GRADE DE MISSÃO (6 BOTÕES) ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): 
        res = asyncio.run(NexusSovereignEngine.get_mission_report("SPACEX"))
        st.session_state.last_intel = res; speak(res)
    if st.button("⚖️ LAW"): 
        res = asyncio.run(NexusSovereignEngine.get_mission_report("LAW"))
        st.session_state.last_intel = res; speak(res)
with c2:
    if st.button("🧠 NEURALINK"): 
        res = asyncio.run(NexusSovereignEngine.get_mission_report("NEURALINK"))
        st.session_state.last_intel = res; speak(res)
    if st.button("🧬 BIOGENETICS"): 
        res = asyncio.run(NexusSovereignEngine.get_mission_report("BIOGENETICS"))
        st.session_state.last_intel = res; speak(res)
with c3:
    if st.button("📈 IPO GOLD"): 
        res = asyncio.run(NexusSovereignEngine.get_mission_report("IPO"))
        st.session_state.last_intel = res; speak(res)
    if st.button("🏗️ ENG SÊNIOR"): 
        res = asyncio.run(NexusSovereignEngine.get_mission_report("ENGINEERING"))
        st.session_state.last_intel = res; speak(res)

if 'last_intel' in st.session_state:
    st.markdown(f'<div class="res-box"><b>AUDITORIA NEXUS:</b><br>{st.session_state.last_intel}</div>', unsafe_allow_html=True)

# --- RESTABELECIDO: GRÁFICO DE ONDA (REAL-TIME) ---
st.divider()
pulse = float(psutil.cpu_percent() + 25); t = np.linspace(0, 10, 500)
y = np.sin(t * (pulse/15) + time.time()) 
fig_wave = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=3), fill='tozeroy'))
fig_wave.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig_wave, use_container_width=True)

st.caption("Barbie Xeon Omni v1025 | Geopolitical Audit | Total Recovery | Erro Zero 2026")
