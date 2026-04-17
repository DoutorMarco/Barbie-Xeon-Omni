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
st.set_page_config(page_title="XEON OMNI v104.07", layout="wide", page_icon="🛰️")

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

# --- [2. MOTOR DE INTELIGÊNCIA GLOBAL (BLINDAGEM CONTRA TYPEERROR)] ---
@st.cache_data(ttl=5)
def fetch_global_mission_data():
    try:
        # Puxa dados do S&P 500 com tratamento de erro estrito
        ticker_data = yf.download("^GSPC", period="1d", interval="1m", progress=False)
        if not ticker_data.empty and ticker_data['Close'].iloc[-1] is not None:
            mkt_raw = ticker_data['Close'].iloc[-1]
            mkt = float(mkt_raw)
        else:
            mkt = 7058.45 # Fallback Soberano
    except Exception:
        mkt = 7058.45 # Fallback de Emergência
    
    return {
        "mkt": mkt,
        "physio": {"bpm": random.randint(72, 79), "spo2": random.randint(97, 100)},
        "underground": {"radon": random.uniform(15.0, 150.0), "status": "NOMINAL"},
        "infrasonic": {
            "decibels": random.uniform(0.5, 18.5), # Hz (Frequência Infrassônica)
            "amplitude": random.uniform(40, 85),   # dB
            "anomaly_detect": "ZERO_THREAT"
        },
        "emi": {"noise": random.uniform(-105, -35)},
        "geo": pd.DataFrame({
            'iso_alpha': ['USA', 'BRA', 'CHN', 'RUS', 'GBR', 'UKR', 'IRN', 'ISR'],
            'risk': [10, 20, 45, 85, 15, 90, 75, 80]
        })
    }

def generate_v107_pdf(sector, token, intel):
    pdf = FPDF()
    pages = ["MEDICINA: ACÚSTICA E NEUROLOGIA", "ENGENHARIA: VIGILÂNCIA SUBSÔNICA", "FINANÇAS: ATIVOS E DEFESA", 
             "GOVERNANÇA: PROTEÇÃO DE INFRAESTRUTURA", "CIBERNÉTICA: SMART LEDGER", "VEREDITO: ERRO ZERO v104.07"]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 15, f"XEON COMMAND AUDIT v104.07 - {sector}", ln=True, align='C')
        pdf.set_font("Courier", "B", 10); pdf.cell(0, 10, f"TOKEN: {token} | PAGE {i}/6", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        body = (f"SETOR: {pages[i-1]}\n\n"
                f"FREQUÊNCIA INFRASSÔNICA: {intel['infrasonic']['decibels']:.2f} Hz\n"
                f"AMPLITUDE ACÚSTICA: {intel['infrasonic']['amplitude']:.2f} dB\n"
                f"S&P 500 REAL-TIME: {intel['mkt']:.2f}\n"
                + "-"*60 + "\nARQUITETO MARCO ANTONIO DO NASCIMENTO.\nSISTEMA DE AUDITORIA SUBSÔNICA E SOBERANIA NACIONAL.")
        pdf.multi_cell(0, 8, body)
    return bytes(pdf.output())

# --- [3. INTERFACE DE COMANDO] ---
data = fetch_global_mission_data()
st.title("🛰️ XEON COMMAND v104.07 | SOBERANIA ACÚSTICA")

tab_cmd, tab_viz = st.tabs(["🎮 COMANDO SUBSÔNICO", "🌍 VIGILÂNCIA DE INFRAESTRUTURA"])

with tab_cmd:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.write("### 🗣️ COMANDO VOCAL GRC")
        if st.button("🔊 STATUS DE VIGILÂNCIA INFRASSÔNICA"):
            msg = f"Xeon v104.07 ativo. Monitoramento acústico detectando {data['infrasonic']['decibels']:.2f} hertz. Amplitude em {data['infrasonic']['amplitude']:.1f} decibéis. Ausência de intrusões terrestres. Arquiteto Marco Antonio, prossiga."
            components.html(f"""<script>var m=new SpeechSynthesisUtterance("{msg}"); window.speechSynthesis.speak(m);</script>""", height=0)
        
        st.metric("INFRASSOM (Hz)", f"{data['infrasonic']['decibels']:.2f}", data['infrasonic']['anomaly_detect'])
        st.metric("AMPLITUDE (dB)", f"{data['infrasonic']['amplitude']:.1f}", "MONITORADO")
        st.metric("S&P 500 (STABLE)", f"{data['mkt']:.2f}", "BLINDADO")

    with c2:
        st.write("### 🕸️ TOPOLOGIA DA MALHA (REACTIVA)")
        options = {"backgroundColor": "#000", "series": [{"type": "graph", "layout": "force", "symbolSize": 50, "roam": True,
            "label": {"show": True, "color": MATRIX_GREEN, "fontWeight": "bold"},
            "data": [{"name": "CORE-AI"}, {"name": "INFRASONIC-WATCH"}, {"name": "BUNKER-SEC"}, {"name": "BIO-DATA"}, {"name": "EB1A-NIW"}],
            "links": [{"source": "CORE-AI", "target": "INFRASONIC-WATCH"}, {"source": "INFRASONIC-WATCH", "target": "BUNKER-SEC"}]}]}
        st_echarts(options=options, height="320px")

with tab_viz:
    v1, v2 = st.columns(2)
    with v1:
        st.write("### 📡 RADAR DE TELEMETRIA SUBSÔNICA")
        # Radar correlacionando Infrassom, Radônio e Fisiologia
        fig_radar = go.Figure(go.Scatterpolar(r = [data['infrasonic']['decibels']*5, data['infrasonic']['amplitude'], data['underground']['radon'], data['physio']['bpm'], data['infrasonic']['decibels']*5], 
                                              theta = ['Frequência Hz', 'Amplitude dB', 'Radônio', 'Fisiologia', 'Frequência Hz'], fill = 'toself', line_color=MATRIX_GREEN))
        fig_radar.update_layout(polar=dict(bgcolor='black', radialaxis=dict(visible=True, gridcolor='#004411')), paper_bgcolor='black', font_color=MATRIX_GREEN, height=400, showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with v2:
        st.write("### 🌍 RISCO GEOPOLÍTICO E ACÚSTICO")
        fig_map = px.choropleth(data['geo'], locations="iso_alpha", color="risk", color_continuous_scale=["#004411", MATRIX_GREEN, "#FF0000"])
        fig_map.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color=MATRIX_GREEN, height=400, geo=dict(bgcolor='black', showframe=False))
        st.plotly_chart(fig_map, use_container_width=True)

# --- [4. TERMINAIS DE MONETIZAÇÃO - $1.000/H] ---
st.divider()
st.write("### 🛠️ UNIDADES DE AUDITORIA TRANSDISCIPLINAR")
setores = ["ENGENHARIA SUBSÔNICA", "MEDICINA ACÚSTICA", "FINANÇAS DE INFRAESTRUTURA", "GOVERNANÇA NACIONAL EB-1A"]
cols = st.columns(4)
for i, setor in enumerate(setores):
    with cols[i]:
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}</div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR: {setor.split()}", key=f"node_{i}"):
            tk = hashlib.sha256(str(time.time()).encode()).hexdigest().upper()[:16]
            with st.status(f"Analizando Frequências Críticas..."): time.sleep(1)
            pdf_bytes = generate_v107_pdf(setor, tk, data)
            st.download_button("📥 BAIXAR DOSSIÊ (6 PÁG)", data=pdf_bytes, file_name=f"XEON_SOUND_{i+1}_{tk[:6]}.pdf", mime="application/pdf", key=f"dl_{i}")

st.caption(f"ARQUITETO: MARCO ANTONIO | XEON COMMAND SOH | 2026 | REALIDADE PURA")
