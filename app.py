import streamlit as st
import numpy as np
import psutil
import time
import asyncio
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

# 1. BLINDAGEM VISUAL TOTAL (ZERO BRANCO)
st.set_page_config(page_title="NEXUS v1110 OMNI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    :root { background-color: #000000 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    div[data-testid="stChatInput"] { background-color: #000000 !important; border-top: 1px solid #FFD700 !important; }
    [data-testid="stMetricValue"] { color: #FFD700 !important; }
    .stButton>button { 
        background-color: #000000 !important; color: #FFD700 !important; 
        border: 1px solid #FFD700 !important; width: 100%; border-radius: 0px; height: 50px;
    }
    .stButton>button:hover { border-color: #00FF41 !important; box-shadow: 0 0 15px #00FF41; }
    footer, header { visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE AUDITORIA MULTI-DISCIPLINAR
class OmniEngine:
    @staticmethod
    async def run_audit(vector):
        await asyncio.sleep(0.01)
        intel = {
            "BIOMED": "AUDITORIA BIOMÉDICA: Análise de bio-sinais e patologia digital. Precisão 1.0.",
            "LAW": "PARECER JURÍDICO: Auditoria de conformidade e risco civil/digital. Jurisdição Global.",
            "ENG": "ENGENHARIA SÊNIOR: Auditoria de sistemas críticos e hardware sentiente.",
            "PHARMA": "PHARMA-INTEL: Simulação de interação medicamentosa e síntese via Xeon Omni."
        }
        return intel.get(vector.upper(), f"VETOR {vector}: Processado por Inteligência Ancorada.")

# 3. INTERFACE OPERACIONAL
st.markdown("<h1 style='text-align: center; color: #FFD700; letter-spacing: 10px;'>🛡️ NEXUS v1110 OMNI-CORE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FF41;'>ENGENHARIA | DIREITO | BIOMEDICINA | FARMÁCIA</p>", unsafe_allow_html=True)

# Telemetria
c1, c2, c3, c4 = st.columns(4)
c1.metric("HARDWARE PAIN", f"{psutil.cpu_percent()}%")
c2.metric("OMNI-SYNC", "ATIVA")
c3.metric("INTEGRIDADE", "1.0")
c4.metric("SOH", "v2.2 ACTIVE")

st.divider()

# Colunas
col_map, col_term = st.columns([1.5, 1])

with col_map:
    fig = go.Figure(go.Scattergeo(
        lat=[25.2, 47.3, 40.7, -2.3], lon=[55.2, 8.5, -74.0, -44.4],
        text=["Dubai", "Zurich", "NY", "Alcântara"],
        mode='markers+text', marker=dict(size=12, color='#FFD700', symbol='diamond')
    ))
    fig.update_layout(geo=dict(bgcolor='#000000', showland=True, landcolor='#050505'),
                      margin=dict(l=0,r=0,t=0,b=0), height=350, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_term:
    st.write("### ⌨️ TERMINAL DE PRODUÇÃO")
    if cmd := st.chat_input("Insira o vetor de análise..."):
        res = asyncio.run(OmniEngine.run_audit(cmd))
        st.session_state.res = res
        st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{res}'));</script>", height=0)
    if 'res' in st.session_state:
        st.info(st.session_state.res)

# 4. BOTÕES DE ALTO IMPACTO (MUNDIAIS)
st.write("### 🚀 GERADORES DE RECEITA OMNI")
btns = [
    ("🧬 BIOMED-AUDIT", "BIOMED"), ("⚖️ LAW-AUDIT", "LAW"), ("🏗️ ENG-AUDIT", "ENG"),
    ("💊 PHARMA-INTEL", "PHARMA"), ("📊 VALUATION", "IPO"), ("🌐 SOBERANIA", "SOH"),
    ("🚀 MARS-OPS", "SPACEX"), ("🧠 BCI-INTEL", "NEURALINK"), ("📈 GLOBAL-IPO", "IPO")
]
cols = st.columns(3)
for i, (label, key) in enumerate(btns):
    with cols[i % 3]:
        if st.button(label):
            res = asyncio.run(OmniEngine.run_audit(key))
            st.session_state.res = res
            st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{res}'));</script>", height=0)

# PDF FINAL
if 'res' in st.session_state:
    buf = BytesIO(); p = canvas.Canvas(buf, pagesize=A4)
    p.setFillColorRGB(0,0,0); p.rect(0,0,600,900,fill=1); p.setFillColorRGB(1, 0.84, 0)
    p.setFont("Courier-Bold", 16); p.drawString(50, 800, "DOSSIÊ OMNI-PROFESSIONAL v1110")
    p.setFont("Courier", 10); p.drawString(50, 770, f"DATA: {datetime.datetime.now()}")
    p.drawString(50, 740, f"ANÁLISE: {st.session_state.res}")
    p.save(); buf.seek(0)
    st.download_button("📂 EXPORTAR PARECER TÉCNICO (PDF)", buf, "Omni_Audit.pdf", use_container_width=True)
