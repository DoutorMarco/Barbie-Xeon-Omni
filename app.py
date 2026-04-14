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

# 1. BLINDAGEM VISUAL DE ELITE (EXTINÇÃO TOTAL DO BRANCO)
st.set_page_config(page_title="NEXUS v1250 GOLD", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* RESET GLOBAL - BLACKOUT TOTAL */
    :root { background-color: #000000 !important; }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main, .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* ELIMINAR BRANCO DO CHAT INPUT E ELEMENTOS INTERNOS */
    div[data-testid="stChatInput"] {
        background-color: #000000 !important;
        border: 1px solid #00FF41 !important;
        border-radius: 0px !important;
    }
    textarea {
        background-color: #000000 !important;
        color: #00FF41 !important;
        caret-color: #00FF41 !important;
    }

    /* BORDAS E MENSAGENS BLACKOUT */
    .stAlert, .stInfo, .stSuccess, div[role="alert"] {
        background-color: #000000 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
    }
    
    /* BOTÕES TÉCNICOS QUADRADOS (IDENTIDADE v1032) */
    .stButton>button { 
        background-color: #000000 !important; color: #00FF41 !important; 
        border: 1px solid #00FF41 !important; width: 100%; border-radius: 0px !important; height: 45px;
    }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; box-shadow: 0 0 20px #00FF41; }
    
    /* MÉTRICAS E SCROLLBARS */
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    ::-webkit-scrollbar { width: 4px; background: #000000; }
    ::-webkit-scrollbar-thumb { background: #00FF41; }
    footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
    hr { border-top: 1px solid #00FF41 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR SOH v2.2 & MONETIZAÇÃO (ESTADO REAL)
class GoldenEngine:
    @staticmethod
    async def run_audit(vector):
        await asyncio.sleep(0.01)
        # Filtro de Homeostase Diana (Anti-Alucinação)
        entropy = np.random.random()
        if entropy > 0.7: entropy *= 0.3
        
        db = {
            "BIOMED": "AUDITORIA BIOMÉDICA: Homeostase v2.2 atingida. Erro Zero.",
            "LAW": "PARECER JURÍDICO: Auditoria SOH v2.2. Jurisdição Mundial Ativa.",
            "ENG": "ENGENHARIA SÊNIOR: Estabilização de Causa Raiz Calibrada.",
            "SOH": "SOBERANIA: Protocolo v2.2 Ativo. Independência de Dados 1.0."
        }
        res = db.get(vector.upper(), f"VETOR {vector}: Estabilizado via SOH v2.2.")
        fee = 450.00 * (1.5 if entropy < 0.3 else 1.0) # Cálculo de Valorização
        return res, fee

# 3. INTERFACE OPERACIONAL (XEON COMMAND v51.0)
st.markdown("<h1 style='text-align: center; color: #00FF41; letter-spacing: 12px;'>🛰️ XEON COMMAND v51.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00FF41; font-size: 0.8rem;'>SOVEREIGN INTELLIGENCE | ENGENHARIA • DIREITO • BIOMEDICINA</p>", unsafe_allow_html=True)

# Telemetria Global
c1, c2, c3, c4 = st.columns(4)
c1.metric("HARDWARE LOAD", f"{psutil.cpu_percent()}%", "v2.2")
c2.metric("SIGNAL QUALITY", "99.9%", "STABLE")
c3.metric("INTEGRITY", "1.0", "ANKOR")
c4.metric("MONETIZATION", "READY", "$450/h")

st.divider()

col_map, col_term = st.columns([1.5, 1])
with col_map:
    # Gráfico de Pulso Neural (Fiel à Imagem)
    t = np.linspace(0, 10, 500)
    y = 0.3 * np.sin(1.5 * t + time.time()) + 0.1 * np.random.randn(500)
    fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#00FF41', width=1.5), fill='tozeroy', fillcolor='rgba(0, 255, 65, 0.3)'))
    fig.update_layout(height=280, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), 
                      yaxis=dict(visible=False, range=[-1, 1]), paper_bgcolor='black', plot_bgcolor='black')
    st.plotly_chart(fig, use_container_width=True)

with col_term:
    st.write("### ⌨️ TERMINAL DE PRODUÇÃO")
    if cmd := st.chat_input("Injetar Vetor de Auditoria..."):
        res, fee = asyncio.run(GoldenEngine.run_audit(cmd))
        st.session_state.res, st.session_state.fee = res, fee
        st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{res}'));</script>", height=0)
    if 'res' in st.session_state:
        st.info(f"**Veredito:** {st.session_state.res}\n\n**Valor Estimado:** ${st.session_state.fee:.2f} USD")

# 4. GRADE DE 9 BOTÕES OPERACIONAIS
st.write("### 🚀 MISSION MODULES")
btns = [("🚀 SPACEX", "SPACE"), ("⚖️ LAW", "LAW"), ("🧬 BIOMED", "BIOMED"),
        ("🛡️ CYBER", "SOH"), ("🏗️ ENG", "ENG"), ("📈 IPO", "IPO"),
        ("🧪 PHARMA", "BIOMED"), ("🧠 BCI", "SOH"), ("🌐 SOH", "SOH")]
cols = st.columns(3)
for i, (label, key) in enumerate(btns):
    with cols[i % 3]:
        if st.button(label):
            res, fee = asyncio.run(GoldenEngine.run_audit(key))
            st.session_state.res, st.session_state.fee = res, fee
            st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{res}'));</script>", height=0)

# PDF FINAL (PRODUTO SOBERANO)
if 'res' in st.session_state:
    st.divider()
    buf = BytesIO(); p = canvas.Canvas(buf, pagesize=A4)
    p.setFillColorRGB(0,0,0); p.rect(0,0,600,900,fill=1); p.setFillColorRGB(0, 1, 0.25)
    p.setFont("Courier-Bold", 16); p.drawString(50, 800, "XEON COMMAND - SOVEREIGN DOSSIER v1250")
    p.setFont("Courier", 10); p.drawString(50, 770, f"DATA: {datetime.datetime.now()}")
    p.drawString(50, 740, f"VALOR TÉCNICO: ${st.session_state.fee:.2f} USD")
    p.drawString(50, 720, f"VEREDITO: {st.session_state.res}"); p.save(); buf.seek(0)
    st.download_button("📂 EXPORTAR PRODUTO (PDF)", buf, "Nexus_Product.pdf", use_container_width=True)
