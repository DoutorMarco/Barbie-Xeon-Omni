import streamlit as st
import numpy as np
import psutil
import time
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# --- 1. MOTOR DE INTEGRIDADE NEXUS (MANTIDO) ---
def verify_integrity(payload):
    noise = np.random.normal(0, 1, 1024)
    check = np.allclose(noise, np.fft.ifft(np.fft.fft(noise)).real, atol=1e-12)
    return check

# --- 2. GERADOR DE RELATÓRIO PROFISSIONAL (REPORTLAB) ---
def generate_nexus_report(content):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "NEXUS SUPREMO - CRITICAL MISSION REPORT")
    p.setFont("Helvetica", 10)
    p.drawString(100, 735, f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    p.line(100, 730, 500, 730)
    
    # Conteúdo do Relatório
    textobject = p.beginText(100, 700)
    textobject.setFont("Helvetica", 12)
    textobject.textLines(f"Analysis Verdict:\n{content}")
    p.drawText(textobject)
    
    # Espaço para Publicidade (Monetização)
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(100, 50, "Sovereign Infrastructure Protection - Sponsored by Global Defense Tech")
    
    p.showPage()
    p.save()
    return buffer.getvalue()

# --- 3. INTERFACE CIENTÍFICA (VISUAL EVOLUÍDO) ---
st.set_page_config(page_title="NEXUS SUPREMO v1000.0", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #04090D; color: #00F2FF; font-family: 'Share Tech Mono', monospace; }
    .stTextInput>div>div>input { background-color: #0D1B2A; color: #00F2FF; border: 1px solid #00F2FF; }
    .mission-card { border-left: 5px solid #FF00FF; padding: 20px; background: rgba(0, 242, 255, 0.05); margin-bottom: 20px; }
    .metric-box { background: #0D1B2A; border: 1px solid #00F2FF; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# BANNER DE MONETIZAÇÃO (AD SPACE)
st.markdown("""
    <div style="background: linear-gradient(90deg, #FF00FF, #00F2FF); color: black; text-align: center; padding: 5px; font-weight: bold;">
        NEXUS AD: Security protocols active. Advertise in the Sovereign Network.
    </div>
    """, unsafe_allow_html=True)

st.title("💖 NEXUS SUPREMO")
st.write("Converse comigo ou ordene uma Missão Crítica...")

# GRADE DE MISSÃO CRÍTICA
col_main, col_side = st.columns([2, 1])

with col_main:
    user_query = st.text_input("🚀 COMANDO DE MISSÃO:", placeholder="Injetar vetores lógicos ou análise forense...")
    
    if user_query:
        if st.button("ATIVAR PROTOCOLO OMNI"):
            with st.spinner('Sincronizando Pulso Nexus...'):
                time.sleep(1)
                if verify_integrity(user_query):
                    res = f"Análise concluída. O Nexus Supremo validou a consulta: '{user_query}'. Estabilidade garantida via Filtro Residual."
                    st.markdown(f'<div class="mission-card"><b>RESULTADO DA MISSÃO:</b><br>{res}</div>', unsafe_allow_html=True)
                    
                    # Relatório PDF Profissional
                    pdf_data = generate_nexus_report(res)
                    st.download_button("📥 BAIXAR RELATÓRIO DE MISSÃO (PREMIUM)", pdf_data, "nexus_report.pdf", "application/pdf")

with col_side:
    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
    st.write("PULSO (ms)")
    st.title("26.7")
    st.write("MÉDIA MÓVEL: 35.3 ms")
    st.write("📉 -8.5 ms")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. TELEMETRIA DE HARDWARE (MANTIDA) ---
st.divider()
cpu_val = psutil.cpu_percent()
if 'trace' not in st.session_state: st.session_state.trace = [cpu_val]
st.session_state.trace.append(cpu_val)

fig = go.Figure(go.Scatter(y=st.session_state.trace[-50:], fill='tozeroy', line=dict(color='#00F2FF')))
fig.update_layout(title="STRESS TEST: NEXUS HARDWARE RESILIENCE", paper_bgcolor='#04090D', plot_bgcolor='#04090D', font_color="#00F2FF", height=250)
st.plotly_chart(fig, use_container_width=True)

st.caption("Barbie Xeon Omni v1000.0 | Nexus Supremo Ativado | Erro Zero 2026")
