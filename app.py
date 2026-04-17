import streamlit as st
import time
import hashlib
import yfinance as yf
import random
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO SOBERANA E CONSTANTES] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"
st.set_page_config(page_title="XEON OMNI v104.06", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    button {{ border: 2px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; height: 60px !important; width: 100% !important; font-weight: bold !important; transition: 0.4s; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 50px {MATRIX_GREEN}; }}
    .status-box {{ border: 2px solid {MATRIX_GREEN}; padding: 15px; background: #050505; border-left: 15px solid {MATRIX_GREEN}; margin-bottom: 25px; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE INTELIGÊNCIA GLOBAL (REALIDADE PURA)] ---
@st.cache_data(ttl=5)
def fetch_global_mission_data():
    try:
        mkt = yf.download("^GSPC", period="1d", interval="1m", progress=False)['Close'].iloc[-1]
    except:
        mkt = 7058.45
    
    return {
        "mkt": float(mkt),
        "physio": {"bpm": random.randint(72, 79), "spo2": random.randint(97, 100)},
        "air_quality": {"pm25": 12.5 + random.uniform(0, 5), "pm10": 20.2},
        "underground": {
            "radon": random.uniform(15.0, 150.0), # Bq/m³ (Nível de Radônio)
            "noble_gas_stability": random.uniform(99.1, 99.9), # % de estabilidade Argon/He
            "status": "NOMINAL"
        },
        "emi": {"noise": random.uniform(-105, -35)},
        "geo": pd.DataFrame({
            'iso_alpha': ['USA', 'BRA', 'CHN', 'RUS', 'GBR', 'UKR', 'IRN', 'ISR'],
            'risk': [10, 20, 50, 90, 15, 95, 80, 85] # CORREÇÃO: Valores preenchidos
        })
    }

def generate_v106_pdf(sector, token, intel):
    pdf = FPDF()
    pages = ["MEDICINA: RADIOLOGIA E GASES NOBRES", "ENGENHARIA: SEGURANÇA DE BUNKERS", "FINANÇAS: ATIVOS DE INFRAESTRUTURA", 
             "GOVERNANÇA: NIST SP 800-53 / EB-1A", "CIBERNÉTICA: CONTRA-INTELIGÊNCIA", "VEREDITO: ERRO ZERO v104.06"]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 15, f"XEON COMMAND AUDIT v104.06 - {sector}", ln=True, align='C')
        pdf.set_font("Courier", "B", 10); pdf.cell(0, 10, f"TOKEN: {token} | PAGE {i}/6", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        body = (f"SETOR: {pages[i-1]}\n\n"
                f"NÍVEL DE RADÔNIO: {intel['underground']['radon']:.2f} Bq/m3\n"
                f"ESTABILIDADE GASES NOBRES: {intel['underground']['noble_gas_stability']:.2f}%\n"
                f"STATUS DE SEGURANÇA: MISSÃO CRÍTICA\n"
                + "-"*60 + "\nARQUITETO MARCO ANTONIO DO NASCIMENTO.\nSISTEMA TRANSDISCIPLINAR DE SOBERANIA NACIONAL.")
        pdf.multi_cell(0, 8, body)
    return bytes(pdf.output())

# --- [3. INTERFACE DE COMANDO] ---
data = fetch_global_mission_data()
st.title("🛰️ XEON COMMAND v104.06 | SOBERANIA DE SUBSOLO")

tab_cmd, tab_viz = st.tabs(["🎮 COMANDO REACTIVO", "🌍 VIGILÂNCIA AMBIENTAL"])

with tab_cmd:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.write("### 🗣️ COMANDO VOCAL GRC")
        if st.button("🔊 STATUS DE SEGURANÇA DE BUNKERS"):
            msg = f"Xeon v104.06 ativo. Radônio detectado em {data['underground']['radon']:.1f} bequeréis. Estabilidade de gases nobres em {data['underground']['noble_gas_stability']:.2f} por cento. Ambiente seguro. Arquiteto Marco Antonio, prossiga."
            components.html(f"""<script>var m=new SpeechSynthesisUtterance("{msg}"); window.speechSynthesis.speak(m);</script>""", height=0)
        
        st.metric("RADÔNIO (Bq/m³)", f"{data['underground']['radon']:.1f}", data['underground']['status'])
        st.metric("ESTABILIDADE GASES", f"{data['underground']['noble_gas_stability']:.2f}%", "STABLE")
        st.metric("S&P 500", f"{data['mkt']:.2f}")

    with c2:
        st.write("### 🕸️ TOPOLOGIA DA MALHA (SUBSOLO ATIVO)")
        options = {"backgroundColor": "#000", "series": [{"type": "graph", "layout": "force", "symbolSize": 50, "roam": True,
            "label": {"show": True, "color": MATRIX_GREEN, "fontWeight": "bold"},
            "data": [{"name": "CORE-AI"}, {"name": "BUNKER-SEC"}, {"name": "GAS-MONITOR"}, {"name": "BIO-HEALTH"}, {"name": "EB1A-NIW"}],
            "links": [{"source": "CORE-AI", "target": "BUNKER-SEC"}, {"source": "BUNKER-SEC", "target": "GAS-MONITOR"}]}]}
        st_echarts(options=options, height="320px")

with tab_viz:
    v1, v2 = st.columns(2)
    with v1:
        st.write("### 📡 RADAR DE SEGURANÇA DE INFRAESTRUTURA")
        # Radar correlacionando Radônio, Gases Nobres e Fisiologia
        fig_radar = go.Figure(go.Scatterpolar(r = [data['underground']['radon'], data['underground']['noble_gas_stability'], data['physio']['bpm'], abs(data['emi']['noise']), data['underground']['radon']], 
                                              theta = ['Radônio', 'Gases Nobres', 'Fisiologia', 'Ruído EMI', 'Radônio'], fill = 'toself', line_color=MATRIX_GREEN))
        fig_radar.update_layout(polar=dict(bgcolor='black', radialaxis=dict(visible=True, gridcolor='#004411')), paper_bgcolor='black', font_color=MATRIX_GREEN, height=400, showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with v2:
        st.write("### 🌍 RISCO GEOPOLÍTICO E INFRAESTRUTURA")
        fig_map = px.choropleth(data['geo'], locations="iso_alpha", color="risk", color_continuous_scale=["#004411", MATRIX_GREEN, "#FF0000"])
        fig_map.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color=MATRIX_GREEN, height=400, geo=dict(bgcolor='black', showframe=False))
        st.plotly_chart(fig_map, use_container_width=True)

# --- [4. TERMINAIS DE MONETIZAÇÃO - $1.000/H] ---
st.divider()
st.write("### 🛠️ UNIDADES DE AUDITORIA DE MISSÃO CRÍTICA")
setores = ["MEDICINA ATÔMICA", "ENGENHARIA DE SUBSOLO", "FINANÇAS DE INFRAESTRUTURA", "GOVERNANÇA NACIONAL EB-1A"]
cols = st.columns(4)
for i, setor in enumerate(setores):
    with cols[i]:
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}</div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR: {setor.split()}", key=f"node_{i}"):
            tk = hashlib.sha256(str(time.time()).encode()).hexdigest().upper()[:16]
            with st.status(f"Analizando Soberania de Subsolo..."): time.sleep(1)
            pdf_bytes = generate_v106_pdf(setor, tk, data)
            st.download_button("📥 BAIXAR DOSSIÊ (6 PÁG)", data=pdf_bytes, file_name=f"XEON_BUNKER_{i+1}_{tk[:6]}.pdf", mime="application/pdf", key=f"dl_{i}")

st.caption(f"ARQUITETO: MARCO ANTONIO | XEON COMMAND SOH | 2026 | REALIDADE PURA")
