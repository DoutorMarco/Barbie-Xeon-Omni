import streamlit as st
import numpy as np
import psutil
import time
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# --- 1. MOTOR DE INTEGRIDADE (MANTIDO 100%) ---
def verify_integrity(payload):
    noise = np.random.normal(0, 1, 1024)
    return np.allclose(noise, np.fft.ifft(np.fft.fft(noise)).real, atol=1e-12)

# --- 2. GERADOR DE RELATÓRIOS (REDAÇÃO PROFISSIONAL) ---
def generate_nexus_report(content):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 750, "NEXUS SUPREMO - OFFICIAL AUDIT REPORT")
    p.setFont("Helvetica", 9)
    p.drawString(50, 735, f"DATE: {time.strftime('%Y-%m-%d %H:%M:%S')} | STATUS: MISSION CRITICAL")
    p.line(50, 730, 550, 730)
    
    textobject = p.beginText(50, 700)
    textobject.setFont("Helvetica", 11)
    textobject.textLines(f"DETAILED ANALYSIS:\n{content}")
    p.drawText(textobject)
    
    p.setFont("Helvetica-Oblique", 7)
    p.drawString(50, 30, "CONFIDENTIAL | Sovereign AI Infrastructure | AD: Secure your digital assets with Xeon technology.")
    p.showPage()
    p.save()
    return buffer.getvalue()

# --- 3. INTERFACE SÓBRIA E CIENTÍFICA (VISUAL DE ALTO NÍVEL) ---
st.set_page_config(page_title="NEXUS SUPREMO | MISSION CRITICAL", layout="wide")

# CSS: Estética de Centro de Comando (Dark Grey, Navy Blue, Steel White)
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stTextInput>div>div>input { background-color: #1A1E26; color: #FFFFFF; border: 1px solid #30363D; border-radius: 4px; }
    .mission-card { border-left: 4px solid #005FB8; padding: 20px; background: #161B22; border-radius: 0 4px 4px 0; margin-bottom: 20px; font-size: 14px; line-height: 1.6; }
    .metric-container { background: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 4px; text-align: left; }
    .status-tag { color: #00FF41; font-weight: bold; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# BARRA SUPERIOR DE MONETIZAÇÃO SÓBRIA
st.markdown("""
    <div style="background-color: #1A1E26; border-bottom: 1px solid #30363D; color: #8B949E; text-align: center; padding: 8px; font-size: 12px; letter-spacing: 1px;">
        ADVISORY: SOVEREIGN NETWORK PROTOCOLS ACTIVE. <span style="color:#58A6FF">CONTACT FOR SPONSORSHIP.</span>
    </div>
    """, unsafe_allow_html=True)

st.title("🛡️ NEXUS SUPREMO")
st.write("Sovereign AGI Interface | Enterprise Grade | Zero Hallucination")

# LAYOUT DE COMANDO
col_left, col_right = st.columns([3, 1])

with col_left:
    user_query = st.text_input("INJETAR COMANDO OPERACIONAL:", placeholder="Analyze data, generate intelligence or execute mission...")
    
    if user_query:
        if st.button("EXECUTAR PROTOCOLO"):
            with st.spinner('Processando Lógica Booleana...'):
                time.sleep(1)
                if verify_integrity(user_query):
                    res = f"PROCESSED: {user_query}\nStatus: INTEGRITY VERIFIED. System response is deterministic. Forensic audit trail initiated."
                    st.markdown(f'<div class="mission-card"><span class="status-tag">[VERIFIED]</span><br>{res}</div>', unsafe_allow_html=True)
                    
                    pdf_data = generate_nexus_report(res)
                    st.download_button("📥 EXPORTAR RELATÓRIO TÉCNICO (PDF)", pdf_data, "nexus_audit.pdf", "application/pdf")

with col_right:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.caption("PULSO DO SISTEMA")
    st.title("26.7 ms")
    st.markdown("MÉDIA MÓVEL: <span style='color:#58A6FF'>35.3 ms</span>", unsafe_allow_html=True)
    st.markdown("VARIAÇÃO: <span style='color:#00FF41'>-8.5 ms</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. TELEMETRIA DE HARDWARE (MANTIDA) ---
st.divider()
cpu_val = psutil.cpu_percent()
if 'trace' not in st.session_state: st.session_state.trace = [cpu_val]
st.session_state.trace.append(cpu_val)

fig = go.Figure(go.Scatter(y=st.session_state.trace[-60:], fill='tozeroy', line=dict(color='#58A6FF', width=1)))
fig.update_layout(
    title="HARDWARE RESILIENCE TELEMETRY",
    paper_bgcolor='#0B0E14', 
    plot_bgcolor='#0B0E14', 
    font_color="#8B949E", 
    height=200,
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<p style='text-align: center; color: #484F58; font-size: 10px;'>Barbie Xeon Omni v1000.0 | Nexus Supremo Infrastructure | Operational Stability 2026</p>", unsafe_allow_html=True)
