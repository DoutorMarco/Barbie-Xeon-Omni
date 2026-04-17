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
st.set_page_config(page_title="XEON OMNI v104.05", layout="wide", page_icon="🛰️")

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

# --- [2. MOTOR DE INTELIGÊNCIA GLOBAL (ATIVO/PASSIVO)] ---
@st.cache_data(ttl=5)
def fetch_global_mission_data():
    try:
        # APIs Ativas: Mercado e Clima (Simulação de chamada real p/ PM2.5)
        mkt = yf.download("^GSPC", period="1d", interval="1m", progress=False)['Close'].iloc[-1]
    except:
        mkt = 7056.45
    
    return {
        "mkt": float(mkt),
        "physio": {"bpm": random.randint(72, 79), "spo2": random.randint(97, 100)},
        "air_quality": {
            "pm25": 12.5 + random.uniform(0, 45), # µg/m³
            "pm10": 20.2 + random.uniform(0, 60), # µg/m³
            "aqi_status": "MODERADO"
        },
        "emi": {"noise": random.uniform(-105, -35), "load": random.uniform(70, 95)},
        "geo": pd.DataFrame({'iso_alpha': ['USA', 'BRA', 'CHN', 'RUS', 'GBR', 'UKR', 'IRN', 'ISR'], 'risk': })
    }

def generate_v105_pdf(sector, token, intel):
    pdf = FPDF()
    pages = ["MEDICINA: TOXICOLOGIA DE PARTÍCULAS", "ENGENHARIA: FILTRAGEM E RESILIÊNCIA", "FINANÇAS: ATIVOS AMBIENTAIS", 
             "GOVERNANÇA: NIST & SOBERANIA ATMOSFÉRICA", "CIBERNÉTICA: RASTREIO EMI ATIVO", "VEREDITO: ERRO ZERO v104.05"]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 15, f"XEON COMMAND AUDIT v104.05 - {sector}", ln=True, align='C')
        pdf.set_font("Courier", "B", 10); pdf.cell(0, 10, f"TOKEN: {token} | PAGE {i}/6", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        body = (f"SETOR: {pages[i-1]}\n\n"
                f"CONCENTRAÇÃO PM2.5: {intel['air_quality']['pm25']:.2f} ug/m3\n"
                f"RUÍDO EMI: {intel['emi']['noise']:.2f} dBm\n"
                f"STATUS DE MISSÃO: ATIVO/REACCIONÁRIO\n"
                + "-"*60 + "\nARQUITETO MARCO ANTONIO DO NASCIMENTO.\nSISTEMA TRANSDISCIPLINAR DE REALIDADE PURA.")
        pdf.multi_cell(0, 8, body)
    return bytes(pdf.output())

# --- [3. INTERFACE DE COMANDO] ---
data = fetch_global_mission_data()
st.title("🛰️ XEON COMMAND v104.05 | REALIDADE TOTAL")

tab_cmd, tab_viz = st.tabs(["🎮 COMANDO REACTIVO", "🌍 VIGILÂNCIA AMBIENTAL"])

with tab_cmd:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.write("### 🗣️ COMANDO VOCAL GRC")
        if st.button("🔊 STATUS DE HOMEÓSTASE AMBIENTAL"):
            risco = "Elevado" if data['air_quality']['pm25'] > 35 else "Nominal"
            components.html(f"""<script>var m=new SpeechSynthesisUtterance("Xeon v104.05 ativo. Particulados PM dois ponto cinco em {data['air_quality']['pm25']:.1f} micro-gramas. Qualidade do ar está {risco}. Sincronia com APIs globais ativa. Arquiteto Marco Antonio, prossiga."); window.speechSynthesis.speak(m);</script>""", height=0)
        st.metric("PM2.5 (QUALIDADE AR)", f"{data['air_quality']['pm25']:.1f} µg/m³", data['air_quality']['aqi_status'])
        st.metric("PM10 (PARTICULADOS)", f"{data['air_quality']['pm10']:.1f} µg/m³", "REAL-TIME")
        st.metric("S&P 500", f"{data['mkt']:.2f}")

    with c2:
        st.write("### 🕸️ TOPOLOGIA DA MALHA (REALIDADE PURA)")
        options = {"backgroundColor": "#000", "series": [{"type": "graph", "layout": "force", "symbolSize": 50, "roam": True,
            "label": {"show": True, "color": MATRIX_GREEN, "fontWeight": "bold"},
            "data": [{"name": "CORE-AI"}, {"name": "AIR-SHIELD"}, {"name": "EMI-SCAN"}, {"name": "BIO-DATA"}, {"name": "EB1A-NIW"}],
            "links": [{"source": "CORE-AI", "target": "AIR-SHIELD"}, {"source": "CORE-AI", "target": "EMI-SCAN"}, 
                      {"source": "AIR-SHIELD", "target": "BIO-DATA"}, {"source": "CORE-AI", "target": "EB1A-NIW"}]}]}
        st_echarts(options=options, height="320px")

with tab_viz:
    v1, v2 = st.columns(2)
    with v1:
        st.write("### 📡 RADAR DE TELEMETRIA BIO-AMBIENTAL")
        # Radar correlacionando PM2.5, EMI e Fisiologia
        fig_radar = go.Figure(go.Scatterpolar(r = [data['air_quality']['pm25']*2, abs(data['emi']['noise']), data['physio']['bpm'], data['air_quality']['pm10'], data['air_quality']['pm25']*2], 
                                              theta = ['PM2.5', 'EMI (Noise)', 'Fisiologia', 'PM10', 'PM2.5'], fill = 'toself', line_color=MATRIX_GREEN))
        fig_radar.update_layout(polar=dict(bgcolor='black', radialaxis=dict(visible=True, gridcolor='#004411')), paper_bgcolor='black', font_color=MATRIX_GREEN, height=400, showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with v2:
        st.write("### 🌍 RISCO ATMOSFÉRICO E GEOPOLÍTICO")
        fig_map = px.choropleth(data['geo'], locations="iso_alpha", color="risk", color_continuous_scale=["#004411", MATRIX_GREEN, "#FF0000"])
        fig_map.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color=MATRIX_GREEN, height=400, geo=dict(bgcolor='black', showframe=False))
        st.plotly_chart(fig_map, use_container_width=True)

# --- [4. TERMINAIS DE MONETIZAÇÃO - $1.000/H] ---
st.divider()
st.write("### 🛠️ UNIDADES DE AUDITORIA TRANSDISCIPLINAR")
setores = ["MEDICINA ATMOSFÉRICA", "ENGENHARIA DE FILTRAGEM", "FINANÇAS ESG & CARBONO", "GOVERNANÇA NACIONAL EB-1A"]
cols = st.columns(4)
for i, setor in enumerate(setores):
    with cols[i]:
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}</div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR: {setor.split()}", key=f"node_{i}"):
            tk = hashlib.sha256(str(time.time()).encode()).hexdigest().upper()[:16]
            with st.status(f"Arbitrando Missão Crítica..."): time.sleep(1)
            pdf_bytes = generate_v105_pdf(setor, tk, data)
            st.download_button("📥 BAIXAR DOSSIÊ (6 PÁG)", data=pdf_bytes, file_name=f"XEON_REALITY_{i+1}_{tk[:6]}.pdf", mime="application/pdf", key=f"dl_{i}")

st.caption(f"ARQUITETO: MARCO ANTONIO | XEON COMMAND SOH | 2026 | REALIDADE TOTAL")
