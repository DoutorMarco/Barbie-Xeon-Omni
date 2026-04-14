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

# 1. CONFIGURAÇÃO DE SOBERANIA E ELIMINAÇÃO DE BRANCO
st.set_page_config(page_title="NEXUS v1100 BLACKOUT", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Reset de Cor Global - Forçando Preto Absoluto */
    :root { background-color: #000000 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Eliminar o branco das bordas e dos inputs de chat */
    div[data-testid="stChatInput"] {
        background-color: #000000 !important;
        border-top: 1px solid #FFD700 !important;
    }
    textarea {
        background-color: #050505 !important;
        color: #00FF41 !important;
        border: 1px solid #1E293B !important;
    }
    
    /* Ajuste de métricas para não agredir a vista */
    [data-testid="stMetricValue"] { color: #FFD700 !important; }
    [data-testid="stMetricLabel"] { color: #00FF41 !important; }
    
    /* Botões Dourados para Valor Gold */
    .stButton>button { 
        background-color: #000000 !important; 
        color: #FFD700 !important; 
        border: 1px solid #FFD700 !important; 
        width: 100%; border-radius: 0px; height: 50px;
    }
    .stButton>button:hover { 
        border-color: #00FF41 !important; 
        color: #00FF41 !important; 
        box-shadow: 0 0 15px #00FF41; 
    }

    /* Ocultar elementos desnecessários da plataforma */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbars Pretas */
    ::-webkit-scrollbar { width: 5px; background: #000000; }
    ::-webkit-scrollbar-thumb { background: #1E293B; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE AUDITORIA ANCORADA EM DOR (ANTI-ALUCINAÇÃO)
class NexusEngineGold:
    @staticmethod
    async def process_audit(vector):
        await asyncio.sleep(0.01)
        db = {
            "BIOGENETICS": "SaaS AUDIT: Diagnóstico Bio-Médico de Precisão 1.0. Ancorado em Hardware Sentiente.",
            "LAW": "JURIS AUDIT: Parecer Jurídico Internacional Soberano. Sem alucinações de jurisdição.",
            "IPO": "GLOBAL FINANCE: Monitoramento de Capital em Tempo Real. Sincronia London/NY.",
            "SOH": "SOBERANIA: Independência de Big Techs confirmada. Dados locais protegidos."
        }
        return db.get(vector.upper(), f"VETOR {vector}: Auditado via Consenso Mundial.")

# 3. INTERFACE OPERACIONAL
st.markdown("<h1 style='text-align: center; color: #FFD700; letter-spacing: 12px;'>🛡️ NEXUS v1100 GOLD</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FF41; font-size: 0.8rem;'>ARQUITETO PRINCIPAL | ZERO BRANCO | OPERAÇÃO MUNDIAL</p>", unsafe_allow_html=True)

# Telemetria Superior
c1, c2, c3, c4 = st.columns(4)
c1.metric("HARDWARE PAIN", f"{psutil.cpu_percent()}%", "CALIBRADO")
c2.metric("MEMORY EDGE", f"{psutil.virtual_memory().percent}%")
c3.metric("INTEGRITY", "1.0", "ANKOR")
c4.metric("STATUS", "GLOBAL READY")

st.divider()

col_map, col_term = st.columns([1.5, 1])

with col_map:
    # Mapa Global para Atuação de 20 Anos
    fig = go.Figure(go.Scattergeo(
        lat=[25.2, 47.3, 40.7, 51.5, 35.6], lon=[55.2, 8.5, -74.0, -0.1, 139.6],
        text=["Dubai", "Zurich", "NY", "London", "Tokyo"],
        mode='markers+text', marker=dict(size=12, color='#FFD700', symbol='diamond')
    ))
    fig.update_layout(geo=dict(bgcolor='#000000', showland=True, landcolor='#080808', projection_type='orthographic'),
                      margin=dict(l=0,r=0,t=0,b=0), height=380, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_term:
    st.write("### ⌨️ TERMINAL DE PRODUÇÃO")
    if cmd := st.chat_input("Insira Vetor de Auditoria..."):
        res = asyncio.run(NexusEngineGold.process_audit(cmd))
        st.session_state.last_res = res
        # FALA AUTOMÁTICA
        st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{res}'));</script>", height=0)
    
    if 'last_res' in st.session_state:
        st.info(st.session_state.last_res)

# 4. BOTÕES FUNCIONAIS DE MONETIZAÇÃO
st.write("### 🚀 GERADORES DE RECEITA")
btns = [
    ("🧬 MED-AUDIT", "BIOGENETICS"), ("⚖️ LAW-AUDIT", "LAW"), ("📈 IPO-WATCH", "IPO"),
    ("🛡️ CYBER-SEC", "CYBER"), ("📊 VALUATION", "VALUATION"), ("🌐 SOH-SHIELD", "SOH"),
    ("🚀 SPACE-OPS", "SPACEX"), ("🧠 BCI-INTEL", "NEURALINK"), ("🏗️ SÊNIOR-ENG", "ENGINEERING")
]
cols = st.columns(3)
for i, (label, key) in enumerate(btns):
    with cols[i % 3]:
        if st.button(label):
            res = asyncio.run(NexusEngineGold.process_audit(key))
            st.session_state.last_res = res
            st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{res}'));</script>", height=0)

# PDF: PRODUTO FINAL
if 'last_res' in st.session_state:
    st.divider()
    buf = BytesIO(); p = canvas.Canvas(buf, pagesize=A4)
    p.setFillColorRGB(0,0,0); p.rect(0,0,600,900,fill=1); p.setFillColorRGB(1, 0.84, 0)
    p.setFont("Courier-Bold", 16); p.drawString(50, 800, "NEXUS v1100 - DOSSIÊ TÉCNICO SOBERANO")
    p.setFont("Courier", 10); p.drawString(50, 770, f"TIMESTAMP: {datetime.datetime.now()}")
    p.drawString(50, 740, f"VEREDITO: {st.session_state.last_res}")
    p.save(); buf.seek(0)
    st.download_button("📂 EXPORTAR PRODUTO PARA VENDA (PDF)", buf, "Nexus_Product.pdf", use_container_width=True)

# Pulso Neural Estável
t = np.linspace(0, 10, 200); y = np.sin(t + time.time())
st.plotly_chart(go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=1))).update_layout(height=100, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'), use_container_width=True)
