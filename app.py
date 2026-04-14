import streamlit as st
import numpy as np
import psutil
import time
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE (ANTI-FADIGA)
st.set_page_config(page_title="NEXUS v1037 FULL", layout="wide", initial_sidebar_state="collapsed")

# BLINDAGEM CONTRA O BRANCO (CSS INJECTION TOTAL)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    [data-testid="stMetricValue"] { color: #38BDF8 !important; }
    .stButton>button { 
        background-color: #000000 !important; color: #38BDF8 !important; 
        border: 1px solid #38BDF8 !important; width: 100%; border-radius: 0px; height: 50px;
    }
    .stButton>button:hover { border-color: #00FF41 !important; color: #00FF41 !important; box-shadow: 0 0 12px #00FF41; }
    div[data-testid="stChatInput"] { background-color: #050505 !important; border-top: 1px solid #1E293B !important; }
    hr { border-color: #1E293B !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE ÁUDIO E INTELIGÊNCIA
def nexus_speak(text):
    if text:
        js_code = f"<script>var m = new SpeechSynthesisUtterance('{text}'); m.lang='pt-BR'; window.speechSynthesis.speak(m);</script>"
        st.components.v1.html(js_code, height=0)

class NexusEngine:
    @staticmethod
    def audit(key):
        db = {
            "SPACEX": "AUDITORIA: Starship Flight 12 validado. IPO 2026 monitorado.",
            "LAW": "JURISPRUDÊNCIA: Soberania Digital v2.2 ratificada via SOH.",
            "NEURALINK": "BIO-INTEL: Interface BCI atingiu 2.1M de neurônios.",
            "BIOGENETICS": "PESQUISA: Sequenciamento IA Xeon Omni concluído. Erro Zero.",
            "IPO": "VALUATION: Roadshow Global Nexus Supremo Q3-2026.",
            "ENGINEERING": "ESTRUTURA: Engenharia Sênior validada. Resiliência orbital.",
            "CYBER": "DEFESA: Protocolo Zero Branco ativo. Blindagem 100%.",
            "VALUATION": "FINANCEIRO: Liquidez garantida para expansão global.",
            "SOBERANIA": "POLÍTICA: Vetor de soberania digital nacional ativado."
        }
        return db.get(key.upper(), f"SISTEMA: {key} auditado com integridade 1.0.")

# 3. INTERFACE DE COMANDO PRINCIPAL
st.markdown("<h1 style='text-align: center; color: #38BDF8; letter-spacing: 10px;'>🛡️ NEXUS SUPREMO v1037</h1>", unsafe_allow_html=True)

# Telemetria Superior
try:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CPU", f"{psutil.cpu_percent()}%")
    c2.metric("RAM", f"{psutil.virtual_memory().percent}%")
    c3.metric("TRÁFEGO", f"{(psutil.net_io_counters().bytes_sent / 1024 / 1024):.1f} MB")
    c4.metric("STATUS", "SOH ACTIVE")
except: pass

st.divider()

# Mapa e Terminal
col_map, col_term = st.columns([1.5, 1])

with col_map:
    map_fig = go.Figure(go.Scattergeo(
        lat=[-2.3, 25.9, -15.7, 40.71, 35.68], lon=[-44.4, -97.1, -47.8, -74.00, 139.69],
        text=["Alcântara", "Starbase", "Brasília", "NY Node", "Tokyo"],
        mode='markers+text', marker=dict(size=12, color='#38BDF8', symbol='diamond')
    ))
    map_fig.update_layout(geo=dict(bgcolor='#000000', showland=True, landcolor='#050505', projection_type='orthographic'),
                          margin=dict(l=0,r=0,t=0,b=0), height=350, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(map_fig, use_container_width=True)

with col_term:
    st.write("### ⌨️ TERMINAL XEON")
    if cmd := st.chat_input("Comando de Auditoria..."):
        res = NexusEngine.audit(cmd)
        st.session_state.last_res = res
        nexus_speak(res)
    if 'last_res' in st.session_state:
        st.info(f"**LOG:** {st.session_state.last_res}")

# 4. GRADE DE BOTÕES (TODOS OS 9 FUNCIONAIS)
st.write("### 🚀 MÓDULOS DE MISSÃO CRÍTICA")
btns = [
    ("🚀 SPACEX", "SPACEX"), ("⚖️ LAW", "LAW"), ("🧠 NEURALINK", "NEURALINK"), 
    ("🧬 BIOGENETICS", "BIOGENETICS"), ("📈 IPO GOLD", "IPO"), ("🏗️ ENG SÊNIOR", "ENGINEERING"),
    ("🛡️ DEFESA CYBER", "CYBER"), ("📊 VALUATION", "VALUATION"), ("🌐 SOBERANIA", "SOBERANIA")
]

# Distribuição em 3 colunas para simetria
cols = st.columns(3)
for i, (label, key) in enumerate(btns):
    with cols[i % 3]:
        if st.button(label, key=f"btn_{key}"):
            res = NexusEngine.audit(key)
            st.session_state.last_res = res
            nexus_speak(res)

# EXPORTAÇÃO PDF
if 'last_res' in st.session_state:
    st.divider()
    buf = BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    p.setFillColorRGB(0, 0, 0); p.rect(0, 0, 600, 900, fill=1)
    p.setFillColorRGB(0, 1, 0.25); p.setFont("Courier-Bold", 18)
    p.drawString(50, 800, "DOSSIÊ DE AUDITORIA CRÍTICA - v1037")
    p.setFont("Courier", 12); p.drawString(50, 770, f"DATA: {datetime.datetime.now()}")
    p.drawString(50, 740, f"VEREDITO: {st.session_state.last_res}")
    p.save(); buf.seek(0)
    st.download_button("📂 BAIXAR RELATÓRIO SOBERANO", buf, "Nexus_Audit.pdf", use_container_width=True)

# Pulso de Estabilidade
t = np.linspace(0, 10, 200)
y = np.sin(t + time.time())
fig_pulse = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=1), fill='tozeroy'))
fig_pulse.update_layout(height=100, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), 
                        yaxis=dict(visible=False), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_pulse, use_container_width=True)
