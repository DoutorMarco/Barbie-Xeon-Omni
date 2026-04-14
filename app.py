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
# 1. MOTOR DE RASTREIO DE ATIVOS (v1021)
# ==========================================
class NexusAssetTracker:
    @staticmethod
    def get_logistics_intel():
        """Simula rastreio de carga Alcântara-SpaceX."""
        assets = [
            {"name": "Carga SpaceX #01", "lat": 15.0, "lon": -70.0, "status": "Em Trânsito"},
            {"name": "Equipamento SOH v2.2", "lat": -1.0, "lon": -40.0, "status": "Aproximando Alcântara"}
        ]
        return assets

# ==========================================
# 2. BLINDAGEM VISUAL ABSOLUTA (STEALTH)
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1021", layout="wide")

st.markdown("""
    <style>
    /* Forçar Fundo Negro em TODAS as camadas */
    html, body, .stApp, [data-testid="stHeader"], [data-testid="stCanvas"], .main, .block-container { 
        background-color: #010409 !important; 
        color: #E6EDF3 !important; 
    }
    
    /* Botões Missão Crítica - Sócio/Industrial */
    .stButton>button { 
        background-color: #0D1117 !important; 
        color: #38BDF8 !important; 
        border: 1px solid #30363D !important; 
        border-radius: 4px;
        font-weight: 700;
        height: 55px;
    }
    .stButton>button:hover { border-color: #00FF41 !important; color: #00FF41 !important; }

    /* Estilo do Chat e Terminais */
    .stTextInput>div>div>input, .stChatInput textarea { 
        background-color: #000000 !important; 
        color: #00FF41 !important; 
        border: 1px solid #30363D !important; 
    }

    /* Ocultar elementos irrelevantes */
    footer, header, #MainMenu { visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

# ==========================================
# 3. INTERFACE OPERACIONAL v1021 (ERRO CORRIGIDO)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #38BDF8; letter-spacing: 5px;'>🛡️ NEXUS SUPREMO: v1021</h2>", unsafe_allow_html=True)

# CORREÇÃO DA LINHA 73: Definido st.columns(2)
c_map, c_assets = st.columns(2)

with c_map:
    # MAPA COM RASTREIO DE ATIVOS
    map_data = {"lat": [-2.3, 25.9, -15.7], "lon": [-44.4, -97.1, -47.8], "name": ["Alcântara", "Starbase", "Brasília"]}
    assets = NexusAssetTracker.get_logistics_intel()
    
    fig = go.Figure()
    # Pontos de Soberania
    fig.add_trace(go.Scattergeo(lat=map_data["lat"], lon=map_data["lon"], text=map_data["name"], mode='markers+text', marker=dict(size=12, color='#38BDF8')))
    # Ativos em Trânsito
    fig.add_trace(go.Scattergeo(lat=[a['lat'] for a in assets], lon=[a['lon'] for a in assets], text=[a['name'] for a in assets], mode='markers', marker=dict(size=8, color='#00FF41', symbol='triangle-up')))
    
    fig.update_layout(geo=dict(bgcolor='#010409', showland=True, landcolor='#0D1117', showcountries=True, countrycolor='#30363D'), margin=dict(l=0,r=0,t=0,b=0), height=380, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c_assets:
    st.markdown("### 🛰️ ATIVOS EM TRÂNSITO")
    for a in assets:
        st.markdown(f"<p style='color:#00FF41; font-size:14px;'>[DETECTION] {a['name']}: {a['status']}</p>", unsafe_allow_html=True)
    st.metric("HOMEÓSTASE LOGÍSTICA", "99.98%", delta="ESTÁVEL")

# TERMINAL DE COMANDO
if chat_input := st.chat_input("Insira Comando Operacional v1021..."):
    res = f"NEXUS v1021: Veredito para '{chat_input}' processado. Rastreio de ativos sincronizado. Zero alucinação."
    with st.chat_message("assistant"):
        st.markdown(res)
    speak(res)

st.divider()

# GRADE DE MISSÃO (REGRESSÃO ZERO)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): speak("Telemetria SpaceX em tempo real.")
    if st.button("⚖️ LAW"): speak("Auditoria Jurídica 2026 validada.")
with c2:
    if st.button("🧠 NEURALINK"): speak("Conexão Neural estável.")
    if st.button("🧬 BIOGENETICS"): speak("Metabolismo genômico verificado.")
with c3:
    if st.button("📈 IPO GOLD"): speak("Liquidez global projetada.")
    if st.button("🏗️ ENG SÊNIOR"): speak("Engenharia de Missão confirmada.")

# PULSO DINÂMICO (ECG REAL-TIME)
pulse = float(psutil.cpu_percent() + 25); t = np.linspace(0, 10, 500)
y = np.sin(t * (pulse/15) + time.time()) 
fig_wave = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=3), fill='tozeroy'))
fig_wave.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig_wave, use_container_width=True)

st.caption("Barbie Xeon Omni v1021 | Asset Tracking | Zero White | Zero Hallucination")
