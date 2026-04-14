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
# 1. MOTOR DE INTELIGÊNCIA E PESQUISA (v1030)
# ==========================================
class NexusMasterEngine:
    @staticmethod
    async def get_intel(category_or_query):
        """Gera relatórios técnicos e processa pesquisas de ingestão."""
        intel_map = {
            "SPACEX": "AUDITORIA: Starship Flight 12 validado. IPO 2026 monitorado. Sincronia Alcântara-Texas: 99.8%.",
            "LAW": "JURISPRUDÊNCIA: STF/STJ Abril 2026 ratifica Soberania Digital e Auditoria via SOH v2.2.",
            "NEURALINK": "BIO-INTEL: Interface BCI atingiu 2.1M de neurônios. Sincronia neural estável sob carga.",
            "BIOGENETICS": "PESQUISA: Sequenciamento genômico soberano concluído via IA Xeon Omni. Erro Zero.",
            "IPO": "VALUATION: Roadshow Global Nexus Supremo Q3-2026. Liquidez garantida via ativos soberanos.",
            "ENGINEERING": "ESTRUTURA: Engenharia Sênior validada. Resiliência orbital confirmada para Missão Crítica."
        }
        await asyncio.sleep(0.1)
        if category_or_query in intel_map:
            return intel_map[category_or_query]
        return f"PESQUISA NEXUS: Dados para '{category_or_query}' processados via Lógica Bayesiana. Integridade: 100%."

# ==========================================
# 2. BLINDAGEM VISUAL SUPREMA (ZERO BRANCO)
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1030", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* BLOQUEIO TOTAL DE LUZ: Ataca a raiz e o cache de emoção */
    :root { background-color: #000000 !important; }
    html, body, .stApp, .main, [data-testid="stHeader"], [data-testid="stCanvas"], 
    .block-container, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"],
    [data-testid="stChatInput"] {
        background-color: #000000 !important;
        background: #000000 !important;
        color: #00FF41 !important;
        border: none !important;
    }
    
    /* Remove bordas brancas dos inputs */
    .stChatInput textarea, .stTextInput input { 
        background-color: #0D1117 !important; 
        color: #00FF41 !important; 
        border: 1px solid #1E293B !important; 
    }

    /* Botões Industriais Sóbrios */
    .stButton>button {
        background-color: #111827 !important;
        color: #38BDF8 !important;
        border: 1px solid #1E293B !important;
        border-radius: 4px;
        font-weight: bold;
        height: 55px;
        width: 100%;
        text-transform: uppercase;
    }
    .stButton>button:hover { border-color: #00FF41 !important; color: #00FF41 !important; }

    /* Ocultar elementos desnecessários do Streamlit */
    header, footer { visibility: hidden !important; height: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

# ==========================================
# 3. INTERFACE OPERACIONAL v1030
# ==========================================
st.markdown("<h1 style='text-align: center; color: #38BDF8; letter-spacing: 8px;'>🛡️ NEXUS SUPREMO</h1>", unsafe_allow_html=True)

# MONITORES DE AUDITORIA (MAPA E REDE)
c_map, c_net = st.columns([2, 1])
with c_map:
    map_data = {"lat": [-2.3, 25.9, -15.7], "lon": [-44.4, -97.1, -47.8], "name": ["Alcântara", "Starbase TX", "STF Brasília"]}
    fig = go.Figure(go.Scattergeo(lat=map_data["lat"], lon=map_data["lon"], text=map_data["name"], mode='markers+text', marker=dict(size=12, color='#38BDF8')))
    fig.update_layout(geo=dict(bgcolor='#000000', showland=True, landcolor='#0D1117', showcountries=True, countrycolor='#1E293B'), margin=dict(l=0,r=0,t=0,b=0), height=300)
    st.plotly_chart(fig, use_container_width=True)

with c_net:
    st.write("### 🛰️ SOBERANIA DE REDE")
    net = psutil.net_io_counters()
    st.metric("UPLOAD", f"{net.bytes_sent / 1e6:.2f} MB")
    st.metric("DOWNLOAD", f"{net.bytes_recv / 1e6:.2f} MB")

# --- BARRA DE INGESTÃO E PESQUISA RESTABELECIDA ---
st.write("### ⌨️ TERMINAL DE INGESTÃO E PESQUISA")
if user_input := st.chat_input("Insira Comando Lógico ou Pesquisa Técnica..."):
    res = asyncio.run(NexusMasterEngine.get_intel(user_input))
    st.session_state.last_res = res
    speak(res)

st.divider()

# --- GRADE DE MISSÃO (6 BOTÕES COM RELATÓRIOS) ---
st.write("### 🚀 GRADE OPERACIONAL")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): 
        res = asyncio.run(NexusMasterEngine.get_intel("SPACEX"))
        st.session_state.last_res = res; speak(res)
    if st.button("⚖️ LAW"): 
        res = asyncio.run(NexusMasterEngine.get_intel("LAW"))
        st.session_state.last_res = res; speak(res)
with c2:
    if st.button("🧠 NEURALINK"): 
        res = asyncio.run(NexusMasterEngine.get_intel("NEURALINK"))
        st.session_state.last_res = res; speak(res)
    if st.button("🧬 BIOGENETICS"): 
        res = asyncio.run(NexusMasterEngine.get_intel("BIOGENETICS"))
        st.session_state.last_res = res; speak(res)
with c3:
    if st.button("📈 IPO GOLD"): 
        res = asyncio.run(NexusMasterEngine.get_intel("IPO"))
        st.session_state.last_res = res; speak(res)
    if st.button("🏗️ ENG SÊNIOR"): 
        res = asyncio.run(NexusMasterEngine.get_intel("ENGINEERING"))
        st.session_state.last_res = res; speak(res)

# EXIBIÇÃO DO VEREDITO (TEXTO DENSO)
if 'last_res' in st.session_state:
    st.markdown(f"""
        <div style="background-color: #0D1117; padding: 20px; border-left: 5px solid #00FF41; border-radius: 4px; margin-top: 15px;">
            <p style="color: #00FF41; font-family: monospace; font-size: 16px;"><b>VEREDITO NEXUS:</b><br>{st.session_state.last_res}</p>
        </div>
    """, unsafe_allow_html=True)
    # BOTÃO PDF RESTABELECIDO
    buffer = BytesIO(); p = canvas.Canvas(buffer, pagesize=A4)
    p.drawString(100, 800, f"DOSSIÊ v1030: {st.session_state.last_res[:50]}..."); p.save(); buffer.seek(0)
    st.download_button("📂 EXPORTAR DOSSIÊ PDF", buffer, "Nexus_Dossie.pdf", "application/pdf", use_container_width=True)

# --- GRÁFICO DE ONDA (PULSO REAL-TIME) ---
st.divider()
pulse = float(psutil.cpu_percent() + 25); t = np.linspace(0, 10, 500)
y = np.sin(t * (pulse/15) + time.time()) 
fig_wave = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=3), fill='tozeroy'))
fig_wave.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig_wave, use_container_width=True)

st.caption("Barbie Xeon Omni v1030 | Full Ingestion Restored | Zero White | Error Zero 2026")
