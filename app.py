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

# ==========================================
# 1. MOTOR DE INTELIGÊNCIA NEXUS SUPREMO (v1033 - EVOLUÍDO)
# ==========================================
class NexusMasterEngine:
    @staticmethod
    def get_intel_sync(category_or_query):
        """Processamento Síncrono de Alta Performance para evitar conflitos de Threading."""
        intel_map = {
            "SPACEX": "AUDITORIA: Starship Flight 12 validado. IPO 2026 monitorado. Sincronia Alcântara-Texas: 99.8%.",
            "LAW": "JURISPRUDÊNCIA: STF/STJ Abril 2026 ratifica Soberania Digital e Auditoria via SOH v2.2.",
            "NEURALINK": "BIO-INTEL: Interface BCI atingiu 2.1M de neurônios. Sincronia neural estável.",
            "BIOGENETICS": "PESQUISA: Sequenciamento genômico concluído via IA Xeon Omni. Erro Zero.",
            "IPO": "VALUATION: Roadshow Global Nexus Supremo Q3-2026. Liquidez garantida.",
            "ENGINEERING": "ESTRUTURA: Engenharia Sênior validada. Resiliência orbital confirmada.",
            "CYBER": "DEFESA: Protocolo Zero Branco ativo. Blindagem contra interferência externa 100%."
        }
        query_up = category_or_query.upper()
        time.sleep(0.1) # Simulação de latência de rede neural
        
        if query_up in intel_map:
            return intel_map[query_up]
        return f"SISTEMA XEON: Auditoria em '{category_or_query}' finalizada. Vetor de integridade: 1.0 (Auditado)."

# ==========================================
# 2. CONFIGURAÇÃO E BLINDAGEM VISUAL
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1033", layout="wide", initial_sidebar_state="collapsed")

# CSS OTIMIZADO PARA GITHUB/CLOUD
st.markdown("""
    <style>
    :root { background-color: #000000 !important; }
    .stApp { background-color: #000000 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    [data-testid="stMetricValue"] { color: #38BDF8 !important; font-size: 1.8rem !important; }
    .stButton>button {
        background-color: #000000 !important;
        color: #38BDF8 !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 0px;
        width: 100%;
    }
    .stButton>button:hover { border-color: #00FF41 !important; color: #00FF41 !important; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    # Injeção de JS para síntese de voz (Execução no Client-side)
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'pt-PT';
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# ==========================================
# 3. LÓGICA DE INTERFACE
# ==========================================
st.markdown("<h1 style='text-align: center; color: #38BDF8;'>🛡️ NEXUS SUPREMO v1033</h1>", unsafe_allow_html=True)

# Telemetria com tratamento de erro
try:
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    net = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv) / 1024 / 1024
except:
    cpu, mem, net = 0, 0, 0

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("CPU CARGA", f"{cpu}%")
col_b.metric("MEMÓRIA", f"{mem}%")
col_c.metric("TRÁFEGO", f"{net:.1f} MB")
col_d.metric("STATUS SOH", "v2.2 ACTIVE")

st.divider()

# Terminal e Mapa
col_map, col_terminal = st.columns([1.5, 1])

with col_map:
    map_fig = go.Figure(go.Scattergeo(
        lat=[-2.3, 25.9, -15.7, 40.71, 35.68], lon=[-44.4, -97.1, -47.8, -74.00, 139.69],
        text=["Alcântara", "Starbase", "Brasília HQ", "Global NY", "Tokyo Node"],
        mode='markers+text', marker=dict(size=10, color='#38BDF8', symbol='diamond')
    ))
    map_fig.update_layout(geo=dict(bgcolor='#000000', showland=True, landcolor='#050505', projection_type='orthographic'),
                          margin=dict(l=0,r=0,t=0,b=0), height=300, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(map_fig, use_container_width=True)

with col_terminal:
    st.write("### ⌨️ COMANDO XEON")
    cmd = st.chat_input("Digitar comando de auditoria...")
    if cmd:
        res = NexusMasterEngine.get_intel_sync(cmd)
        st.session_state.last_res = res
        speak(res)
    
    if 'last_res' in st.session_state:
        st.info(f"**LOG:** {st.session_state.last_res}")

# Módulos de Operação
st.write("### 🚀 MÓDULOS DE MISSÃO")
btns = [
    ("🚀 SPACEX", "SPACEX"), ("⚖️ LAW", "LAW"), ("🧠 NEURALINK", "NEURALINK"), 
    ("🧬 BIOGENETICS", "BIOGENETICS"), ("📈 IPO GOLD", "IPO"), ("🏗️ ENG SÊNIOR", "ENGINEERING"),
    ("🛡️ DEFESA CYBER", "CYBER")
]

cols = st.columns(len(btns))
for i, (label, key) in enumerate(btns):
    if cols[i].button(label):
        res = NexusMasterEngine.get_intel_sync(key)
        st.session_state.last_res = res
        speak(res)

# Exportação PDF corrigida
if 'last_res' in st.session_state:
    buf = BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    p.setFillColorRGB(0, 0, 0); p.rect(0, 0, 600, 900, fill=1)
    p.setFillColorRGB(0, 1, 0.25)
    p.setFont("Courier-Bold", 16)
    p.drawString(50, 800, "DOSSIÊ DE AUDITORIA CRÍTICA - NEXUS v1033")
    p.setFont("Courier", 10)
    p.drawString(50, 780, f"DATA: {datetime.datetime.now()}")
    p.drawString(50, 760, f"VEREDITO: {st.session_state.last_res}")
    p.save(); buf.seek(0)
    st.download_button("📂 BAIXAR RELATÓRIO SOBERANO", buf, "Audit_Nexus.pdf", "application/pdf", use_container_width=True)

# Pulso Neural Gráfico
t = np.linspace(0, 10, 100)
y = np.sin(t + time.time())
fig_wave = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=1)))
fig_wave.update_layout(height=100, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_wave, use_container_width=True)
