import streamlit as st
import numpy as np
import psutil
import time
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

# 1. CONFIGURAÇÃO DE PÁGINA (IMEDIATA)
st.set_page_config(page_title="NEXUS BLACKOUT", layout="wide", initial_sidebar_state="collapsed")

# 2. BLINDAGEM CONTRA O BRANCO (FORCE BLACK MODE)
st.markdown("""
    <style>
    /* Forçar fundo preto em todos os níveis */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
    [data-testid="stToolbar"], [data-testid="stSidebar"], .main {
        background-color: #000000 !important;
        color: #00FF41 !important;
    }
    
    /* Eliminar flashes brancos e bordas */
    div[block-container] { padding-top: 1rem; background-color: #000000 !important; }
    
    /* Customizar inputs para não brilharem */
    input, textarea, [data-testid="stChatInput"] {
        background-color: #050505 !important;
        color: #00FF41 !important;
        border: 1px solid #1E293B !important;
    }

    /* Ajuste de métricas para contraste de conforto */
    [data-testid="stMetricValue"] { color: #38BDF8 !important; }
    [data-testid="stMetricLabel"] { color: #00FF41 !important; }

    /* Scrollbars escuras */
    ::-webkit-scrollbar { width: 5px; background: #000000; }
    ::-webkit-scrollbar-thumb { background: #1E293B; }
    
    hr { border-color: #1E293B !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE INTELIGÊNCIA (SINCRONIZADO)
class NexusEngine:
    @staticmethod
    def get_data(key):
        data = {
            "SPACEX": "AUDITORIA: Starship Flight 12 OK. Sincronia Alcantara ativa.",
            "LAW": "JURIS: Soberania Digital v2.2 ratificada.",
            "CYBER": "DEFESA: Protocolo Zero Branco Ativado. Monitor de Fadiga OK."
        }
        return data.get(key.upper(), f"VETOR: {key} Auditado 100%.")

# 4. INTERFACE DE COMANDO
st.markdown("<h1 style='text-align: center; color: #38BDF8; letter-spacing: 10px;'>🛡️ NEXUS SUPREMO v1034</h1>", unsafe_allow_html=True)

# Telemetria Superior
try:
    c1, c2, c3 = st.columns(3)
    c1.metric("SISTEMA", f"{psutil.cpu_percent()}%", "CPU")
    c2.metric("MEMÓRIA", f"{psutil.virtual_memory().percent}%", "RAM")
    c3.metric("INTEGRIDADE", "100%", "ESTÁVEL")
except: pass

st.divider()

# Colunas Principais
col_map, col_cmd = st.columns([1.5, 1])

with col_map:
    # Mapa em tons de cinza/preto para não agredir a vista
    fig = go.Figure(go.Scattergeo(
        lat=[-2.3, 25.9, -15.7], lon=[-44.4, -97.1, -47.8],
        mode='markers+text', marker=dict(size=12, color='#38BDF8')
    ))
    fig.update_layout(
        geo=dict(bgcolor='#000000', showland=True, landcolor='#080808', 
                 showcountries=True, countrycolor='#1E293B'),
        margin=dict(l=0,r=0,t=0,b=0), height=350, paper_bgcolor='#000000'
    )
    st.plotly_chart(fig, use_container_width=True)

with col_cmd:
    st.write("### ⌨️ COMANDO")
    if prompt := st.chat_input("Insira Ordem..."):
        res = NexusEngine.get_data(prompt)
        st.session_state.log = res
    
    if 'log' in st.session_state:
        st.code(st.session_state.log, language='bash')

# 5. MÓDULOS BLACKOUT
st.write("### 🚀 ACESSO RÁPIDO")
m1, m2, m3, m4 = st.columns(4)
if m1.button("SPACEX"): st.session_state.log = NexusEngine.get_data("SPACEX")
if m2.button("LAW"): st.session_state.log = NexusEngine.get_data("LAW")
if m3.button("CYBER"): st.session_state.log = NexusEngine.get_data("CYBER")
if m4.button("REPORT"): 
    # Gerar PDF Rápido
    buf = BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    p.setFillColorRGB(0,0,0); p.rect(0,0,600,900,fill=1)
    p.setFillColorRGB(0,1,0); p.drawString(100, 800, "RELATÓRIO NEXUS v1034 - AUDITADO")
    p.save(); buf.seek(0)
    st.download_button("📂 BAIXAR PDF", buf, "report.pdf")

# Gráfico de Pulso Estável (Verde Dark)
t = np.linspace(0, 10, 100)
y = np.sin(t + time.time())
fig_pulse = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#006400', width=2)))
fig_pulse.update_layout(height=100, margin=dict(l=0,r=0,t=0,b=0), 
                        xaxis=dict(visible=False), yaxis=dict(visible=False),
                        paper_bgcolor='#000000', plot_bgcolor='#000000')
st.plotly_chart(fig_pulse, use_container_width=True)
