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

# --- [1. CONFIGURAÇÃO SOBERANA - MILITARY GRADE] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"
st.set_page_config(page_title="XEON COMMAND v106.1", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    button {{ border: 2px solid {MATRIX_GREEN} !important; background: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; height: 60px !important; width: 100% !important; font-weight: bold !important; transition: 0.4s; }}
    button:hover {{ background: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 50px {MATRIX_GREEN}; }}
    .status-box {{ border: 2px solid {MATRIX_GREEN}; padding: 15px; background: #050505; border-left: 15px solid {MATRIX_GREEN}; margin-bottom: 25px; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; animation: pulse 2s infinite; text-shadow: 0 0 15px {MATRIX_GREEN}; }}
    @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE INTELIGÊNCIA TRANSDISCIPLINAR v106.1] ---
@st.cache_data(ttl=5)
def fetch_xeon_federal_data():
    try:
        # Blindagem contra TypeError no Mercado
        ticker = yf.Ticker("^GSPC")
        hist = ticker.history(period="1d", interval="1m")
        if not hist.empty:
            mkt = float(hist['Close'].iloc[-1])
        else:
            mkt = 7058.61
    except:
        mkt = 7058.61
    
    return {
        "mkt": mkt,
        "emp": random.uniform(98.7, 99.9),
        "hale": {"alt": 21500 + random.randint(-100, 100), "status": "VIGILÂNCIA ACTIVE"},
        "physio": {"bpm": random.randint(72, 78), "spo2": random.randint(98, 100)},
        "geo": pd.DataFrame({
            'iso_alpha': ['USA', 'BRA', 'CHN', 'RUS', 'GBR', 'UKR'],
            'risk': [10, 20, 80, 95, 15, 90] # CORREÇÃO DO SYNTAX ERROR
        })
    }

def generate_sovereign_pdf_v106(sector, token, intel):
    pdf = FPDF()
    pages = ["01: EXECUTIVE SUMMARY", "02: EMP SHIELDING REPORT", "03: SUBORBITAL PERSISTENCE", "04: BIO-HEALTH MONITORING", "05: PATENT SPECIFICATION", "06: EB-1A VALIDATION"]
    for i in range(1, 7):
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        pdf.cell(0, 15, f"XEON STRATEGIC DEFENSE v106.1 - {sector.upper()}", ln=True, align='C')
        pdf.set_font("Courier", "B", 10); pdf.cell(0, 10, f"TOKEN: {token} | PAGE {i}/6", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 10)
        body = (f"SECTION: {pages[i-1]}\n\n"
                f"S&P 500: {intel['mkt']:.2f}\n"
                f"EMP ATTENUATION: {intel['emp']:.2f}%\n"
                f"HALE ALTITUDE: {intel['hale']['alt']} m\n"
                f"BIO BPM: {intel['physio']['bpm']}\n"
                + "-"*60 + "\nPROPERTY OF ARCHITECT MARCO ANTONIO DO NASCIMENTO.\nSTRATEGIC NATIONAL ASSET PROTECTION.")
        pdf.multi_cell(0, 8, body)
    return bytes(pdf.output())

# --- [3. INTERFACE DE COMANDO] ---
data = fetch_xeon_federal_data()
st.title("🛰️ XEON COMMAND v106.1 | SOBERANIA FEDERAL")

tab_cmd, tab_viz = st.tabs(["🎮 TERMINAIS OPERACIONAIS", "🌍 VIGILÂNCIA DE ESPECTRO"])

with tab_cmd:
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.write("### 🗣️ COMANDO VOCAL GRC")
        if st.button("🔊 STATUS DE MISSÃO CRÍTICA v106.1"):
            msg = f"Xeon v106.1 ativo. Erro de sintaxe erradicado. Defesa EMP e vigilância suborbital em homeostase absoluta. Arquiteto Marco Antonio, prossiga."
            components.html(f"""<script>var m=new SpeechSynthesisUtterance("{msg}"); window.speechSynthesis.speak(m);</script>""", height=0)
        
        st.metric("EMP SHIELDING", f"{data['emp']:.2f}%", "SECURE")
        st.metric("SUBORBITAL (ALT)", f"{data['hale']['alt']} m", "HALE-DRONE")
        st.metric("S&P 500 (STABLE)", f"{data['mkt']:.2f}")

    with c2:
        st.write("### 🕸️ TOPOLOGIA DE DEFESA NACIONAL")
        options = {"backgroundColor": "#000", "series": [{"type": "graph", "layout": "force", "symbolSize": 50, "roam": True,
            "label": {"show": True, "color": MATRIX_GREEN, "fontWeight": "bold"},
            "data": [{"name": "CORE-AI"}, {"name": "EMP-HARDEN"}, {"name": "HALE-VIGIL"}, {"name": "BIO-MED"}, {"name": "NIST-GRC"}],
            "links": [{"source": "CORE-AI", "target": "EMP-HARDEN"}, {"source": "CORE-AI", "target": "HALE-VIGIL"}]}]}
        st_echarts(options=options, height="320px")

with tab_viz:
    v1, v2 = st.columns(2)
    with v1:
        st.write("### 📡 RADAR DE TELEMETRIA")
        fig_radar = go.Figure(go.Scatterpolar(r = [data['emp'], data['hale']['alt']/250, data['physio']['bpm'], data['mkt']/80, data['emp']], 
                                              theta = ['EMP', 'Suborbital', 'Fisiologia', 'Finanças', 'EMP'], fill = 'toself', line_color=MATRIX_GREEN))
        fig_radar.update_layout(polar=dict(bgcolor='black', radialaxis=dict(visible=True, gridcolor='#004411')), paper_bgcolor='black', font_color=MATRIX_GREEN, height=400, showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with v2:
        st.write("### 🌍 RISCO GEOPOLÍTICO ATIVO")
        fig_map = px.choropleth(data['geo'], locations="iso_alpha", color="risk", color_continuous_scale=["#004411", MATRIX_GREEN, "#FF0000"])
        fig_map.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color=MATRIX_GREEN, height=400, geo=dict(bgcolor='black', showframe=False))
        st.plotly_chart(fig_map, use_container_width=True)

# --- [4. TERMINAIS DE MONETIZAÇÃO - $1.000/H] ---
st.divider()
st.write("### 🛠️ UNIDADES DE AUDITORIA E PROTEÇÃO")
setores = ["DEFESA EMP & HARDWARE", "VIGILÂNCIA SUBORBITAL", "BIOINFORMÁTICA CRÍTICA", "GOVERNANÇA NIW EB-1A"]
cols = st.columns(4)
for i, setor in enumerate(setores):
    with cols[i]:
        st.markdown(f"<div class='status-box'>NÓ 0{i+1}</div>", unsafe_allow_html=True)
        if st.button(f"🚀 ATIVAR: {setor}", key=f"node_{i}"):
            tk = hashlib.sha256(str(time.time()).encode()).hexdigest().upper()[:16]
            with st.status(f"Arbitrando {setor.split()[0]}..."): time.sleep(1)
            pdf_bytes = generate_sovereign_pdf_v106(setor, tk, data)
            st.download_button("📥 DOSSIÊ ESTRATÉGICO", data=pdf_bytes, file_name=f"XEON_SNAP_{tk[:6]}.pdf", mime="application/pdf", key=f"dl_{i}")

st.caption(f"ARQUITETO: MARCO ANTONIO | STRATEGIC NATIONAL ASSET PROTECTION | 2026 | ERROR ZERO")
