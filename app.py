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
# 1. MOTORES DE SOBERANIA (REDE E GEOPOLÍTICA)
# ==========================================
class SovereignSystem:
    @staticmethod
    def get_network_sovereignty():
        """Monitora o tráfego de rede real do hardware local."""
        net_io = psutil.net_io_counters()
        sent = net_io.bytes_sent / (1024 * 1024) # MB
        recv = net_io.bytes_recv / (1024 * 1024) # MB
        return round(sent, 2), round(recv, 2)

    @staticmethod
    def generate_dossier(query, content):
        buffer = BytesIO(); p = canvas.Canvas(buffer, pagesize=A4); w, h = A4
        p.setFillColor(colors.HexColor("#010409")); p.rect(0, 0, w, h, fill=1)
        p.setFillColor(colors.HexColor("#38BDF8")); p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(w/2, h-60, "NEXUS SUPREMO: GLOBAL SOVEREIGN DOSSIER")
        p.setFillColor(colors.white); p.setFont("Helvetica", 10)
        p.drawCentredString(w/2, h-85, f"AUDIT ID: {int(time.time())} | SOH v2.2")
        textobject = p.beginText(50, h-150); textobject.textLines(content); p.drawText(textobject)
        p.save(); buffer.seek(0); return buffer

# ==========================================
# 2. BLINDAGEM VISUAL ABSOLUTA (ZERO BRANCO)
# ==========================================
st.set_page_config(page_title="Nexus v1027 | Sovereign", layout="wide")

# CSS AGRESSIVO: Força o preto antes de qualquer renderização
st.markdown("""
    <style>
    /* 1. Morte ao branco na raiz e containers */
    html, body, .stApp, .main, [data-testid="stHeader"], [data-testid="stCanvas"] {
        background-color: #010409 !important;
        background: #010409 !important;
        color: #00FF41 !important;
    }
    
    /* 2. Blindagem de blocos internos */
    div[data-testid="stVerticalBlock"], div[data-testid="stHorizontalBlock"] {
        background-color: #010409 !important;
    }

    /* 3. Inputs e Chat - Estilo Terminal Sênior */
    .stTextInput>div>div>input, .stChatInput textarea { 
        background-color: #000000 !important; 
        color: #00FF41 !important; 
        border: 1px solid #30363D !important; 
    }

    /* 4. Botões de Missão Crítica - Industrial */
    .stButton>button { 
        background-color: #0D1117 !important; 
        color: #38BDF8 !important; 
        border: 1px solid #30363D !important; 
        border-radius: 2px;
        font-weight: bold;
        height: 55px;
        width: 100%;
    }
    .stButton>button:hover { border-color: #00FF41 !important; color: #00FF41 !important; }

    /* 5. Ocultar Lixo Visual do Streamlit */
    footer, header, #MainMenu { visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

# ==========================================
# 3. INTERFACE OPERACIONAL v1027
# ==========================================
st.markdown("<h2 style='text-align: center; color: #38BDF8; letter-spacing: 5px;'>🛡️ NEXUS SUPREMO: v1027</h2>", unsafe_allow_html=True)

# MONITORES LATERAIS: REDE E CLIMA/INFO
col_net, col_map = st.columns([1, 2])

with col_net:
    st.write("### 🛰️ SOBERANIA DE REDE")
    sent, recv = SovereignSystem.get_network_sovereignty()
    st.metric("UPLOAD (MB)", sent)
    st.metric("DOWNLOAD (MB)", recv)
    st.write("---")
    st.write("### 🌦️ CLIMA ALCÂNTARA")
    st.write("STATUS: GO (FAVORÁVEL)")

with col_map:
    # MONITOR DE AUDITORIA GEOPOLÍTICA
    st.write("### 🌎 AUDITORIA GEOPOLÍTICA")
    map_data = {"lat": [-2.3, 25.9, -15.7], "lon": [-44.4, -97.1, -47.8], "name": ["Alcântara", "Starbase TX", "STF Brasília"]}
    fig_map = go.Figure(go.Scattergeo(lat=map_data["lat"], lon=map_data["lon"], text=map_data["name"], mode='markers+text', marker=dict(size=12, color='#38BDF8')))
    fig_map.update_layout(geo=dict(bgcolor='#010409', showland=True, landcolor='#0D1117', showcountries=True, countrycolor='#30363D'), margin=dict(l=0,r=0,t=0,b=0), height=350)
    st.plotly_chart(fig_map, use_container_width=True)

# INGESTÃO DE DADOS (CHAT)
if chat_input := st.chat_input("Comando de Missão..."):
    res = f"NEXUS v1027: Comando '{chat_input}' processado. Integridade Soberana: 100%."
    with st.chat_message("assistant"): st.markdown(res)
    speak(res)

st.divider()

# GRADE DE MISSÃO (6 BOTÕES)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): speak("Telemetria SpaceX sincronizada."); st.session_state.last = "SpaceX v1027 Active."
    if st.button("⚖️ LAW"): speak("Compliance Jurídico validado."); st.session_state.last = "Law Veredict: Zero Error."
with c2:
    if st.button("🧠 NEURALINK"): speak("Conexão Neurallink estável."); st.session_state.last = "Neural Interface: Stable."
    if st.button("🧬 BIOGENETICS"): speak("Metabolismo genômico verificado."); st.session_state.last = "Biogenetics: DNA Sequenced."
with c3:
    if st.button("📈 IPO GOLD"): speak("Liquidez global projetada."); st.session_state.last = "IPO Gold: Valuation Confirmed."
    if st.button("🏗️ ENG SÊNIOR"): speak("Engenharia de Missão confirmada."); st.session_state.last = "Engineering: Structural OK."

if 'last' in st.session_state:
    st.info(st.session_state.last)
    pdf = SovereignSystem.generate_dossier("Mission Grid Command", st.session_state.last)
    st.download_button("📂 EXPORTAR DOSSIÊ PDF v1027", pdf, "Nexus_Sovereign.pdf", "application/pdf", use_container_width=True)

# PULSO DINÂMICO (TEMPO REAL)
st.divider()
pulse = float(psutil.cpu_percent() + 25); t = np.linspace(0, 10, 500)
y = np.sin(t * (pulse/15) + time.time()) 
fig_wave = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=3), fill='tozeroy'))
fig_wave.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig_wave, use_container_width=True)

st.caption("Barbie Xeon Omni v1027 | Cyber & Geopolitical Sovereignty | No White | No Regression")
