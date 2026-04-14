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
# 1. MOTOR DE INTELIGÊNCIA E MAPA (ABRIL 2026)
# ==========================================
class SovereignEngine:
    @staticmethod
    async def get_mission_intel(category):
        intel_map = {
            "SPACEX": "ESTRATÉGIA: SpaceX protocola IPO histórico (Abril/2026). Starbase Texas e Alcântara em sincronia.",
            "LAW": "JURISPRUDÊNCIA: STJ (13/04/2026) define novos limites para provas via IA generativa. Erro Zero exigido.",
            "BIOGENETICS": "BIOTEC: Consórcio Global valida vacinas sintéticas via IA (Abril/2026).",
            "NEURALINK": "NEUROTECH: Elon Musk anuncia produção em massa (BCI) para 2026.",
            "IPO": "VALUATION: Mercado global aguarda roadshow da SpaceX em Junho.",
            "MAPA": "SOBERANIA: Corredor Alcântara-SpaceX-STF ativado via satélites Starlink."
        }
        await asyncio.sleep(0.1)
        return intel_map.get(category, "NEXUS: Ativo.")

    @staticmethod
    def generate_dossier_pdf(query, category, content):
        """CORREÇÃO: Agora aceita 3 argumentos conforme a chamada do sistema."""
        buffer = BytesIO(); p = canvas.Canvas(buffer, pagesize=A4); w, h = A4
        p.setFillColor(colors.HexColor("#0D1B2A")); p.rect(0, h-80, w, 80, fill=1)
        p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(w/2, h-45, "NEXUS SUPREMO: MISSION AUDIT")
        p.setFont("Helvetica", 8); p.drawCentredString(w/2, h-65, f"SOURCE: {category} | 2026")
        textobject = p.beginText(50, h-120); textobject.setFont("Helvetica", 10); textobject.textLines(content); p.drawText(textobject)
        p.save(); buffer.seek(0); return buffer

# ==========================================
# 2. INTERFACE E DESIGN (ZERO REGRESSION)
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1014", layout="wide")
st.markdown("""<style>.stApp { background-color: #05070A; color: #E0E0E0; }</style>""", unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

st.markdown("<h2 style='text-align: center; color: #00FF41;'>🛡️ NEXUS SUPREMO: v1014</h2>", unsafe_allow_html=True)

# MAPA DE SOBERANIA (DADO REAL)
st.write("### 🌎 MONITOR DE SOBERANIA GLOBAL")
map_data = {
    "lat": [-2.3, 25.9, -15.7], # Alcântara, Starbase Texas, Brasília
    "lon": [-44.4, -97.1, -47.8],
    "name": ["Alcântara Spaceport", "Starbase SpaceX", "STF Brasília"]
}
fig_map = go.Figure(go.Scattergeo(lat=map_data["lat"], lon=map_data["lon"], text=map_data["name"], mode='markers+text', marker=dict(size=10, color='#00FF41')))
fig_map.update_layout(geo=dict(bgcolor='#05070A', showland=True, landcolor='#161B22'), margin=dict(l=0,r=0,t=0,b=0), height=300)
st.plotly_chart(fig_map, use_container_width=True)

# GRADE DE MISSÃO
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
    st.success(st.session_state.last_res)
    pdf = SovereignEngine.generate_dossier_pdf("Comando Nexus", "ABRIL_2026", st.session_state.last_res)
    st.download_button("📂 EXPORTAR AUDITORIA (PDF)", pdf, "Nexus_Audit.pdf", "application/pdf", use_container_width=True)

# ONDA DE PULSO (TEMPO REAL)
st.divider()
pulse = float(psutil.cpu_percent() + 25); t = np.linspace(0, 10, 500)
y = np.sin(t * (pulse/15) + time.time()) 
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=3), fill='tozeroy'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
st.plotly_chart(fig, use_container_width=True)

st.caption("Barbie Xeon Omni v1014 | Erro Zero Corrigido | Sovereign Map Active")
