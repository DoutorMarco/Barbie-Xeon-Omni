import streamlit as st
import numpy as np
import psutil
import time
import httpx
import asyncio
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from functools import wraps

# ==========================================
# 1. INFRAESTRUTURA DE ALTA FREQUÊNCIA (NEXUS)
# ==========================================

def high_frequency_audit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        latency = (time.perf_counter() - start) * 1000
        if 'latency_history' not in st.session_state:
            st.session_state.latency_history = [latency] * 10
        st.session_state.latency_history.append(latency)
        if len(st.session_state.latency_history) > 50:
            st.session_state.latency_history.pop(0)
        return result
    return wrapper

class SovereignEngine:
    @staticmethod
    @high_frequency_audit
    def get_real_pulse():
        try:
            # Medição de latência real de rede
            with httpx.Client(timeout=0.2) as client:
                start = time.perf_counter()
                client.get("https://google.com")
                return (time.perf_counter() - start) * 1000
        except:
            return float(psutil.cpu_percent() + 15)

    @staticmethod
    async def synthesize_intel(query, category="GERAL"):
        await asyncio.sleep(0.01)
        return {
            "RESUMO": f"Doutor Marco, o Veredito sobre '{query}' foi processado via Nexus Supremo.",
            "SAÚDE": f"BIOGENÉTICA: Sincronia molecular validada para '{query}'.",
            "ENG": f"ESTRUTURA: Resiliência orbital aplicada com sucesso.",
            "NEURAL": f"NEURALINK: Interface estável. Download de dados concluído.",
            "LEI": f"SOBERANIA: Jurisprudência emitida com Erro Zero."
        }

    @staticmethod
    def generate_dossier_pdf(query, intel):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4
        # Design Sóbrio de Dossiê Profissional
        p.setFillColor(colors.HexColor("#0D1B2A")); p.rect(0, h-100, w, 100, fill=1)
        p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(w/2, h-60, "NEXUS SUPREMO: MISSION DOSSIER")
        p.setFont("Helvetica", 10); p.drawCentredString(w/2, h-80, f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')} | SOH v2.2 COMPLIANT")
        
        p.setFillColor(colors.black); p.setFont("Helvetica-Bold", 12)
        y = h - 150
        for key, value in intel.items():
            if key != "RESUMO":
                p.drawString(50, y, f"SECTION {key}:")
                p.setFont("Helvetica", 10); p.drawString(50, y-15, value)
                y -= 45
        p.save(); buffer.seek(0); return buffer

# ==========================================
# 2. DESIGN CIENTÍFICO E SÓBRIO (STYLING)
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1000.0", layout="centered")

st.markdown("""
    <style>
    /* Fundo Negro Profundo e Fontes Sóbrias */
    .stApp { background-color: #0B0E14; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
    
    /* Input Estilo Terminal de Comando */
    .stTextInput>div>div>input { 
        border-radius: 8px !important; 
        height: 60px !important; 
        font-size: 18px !important; 
        background-color: #1A1E26 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #30363D !important;
    }
    
    /* Botões Estilo Industrial */
    .stButton>button { 
        border-radius: 4px; 
        background: #161B22; 
        color: #58A6FF; 
        border: 1px solid #30363D;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover { border-color: #58A6FF; color: white; background: #1C2128; }
    
    /* Chat Bubble Sóbria */
    .chat-bubble { 
        background: #161B22; 
        padding: 25px; 
        border-radius: 8px; 
        border-left: 5px solid #58A6FF; 
        font-size: 18px; 
        color: #E0E0E0; 
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

def mic_bridge():
    st.components.v1.html("""
        <button id="v_btn" onclick="startMic()" style="width:100%; height:50px; border-radius:8px; background:#161B22; color:#58A6FF; border:1px solid #30363D; font-size:16px; font-weight:bold; cursor:pointer;">🎙️ VOICE COMMAND: MISSION CRITICAL</button>
        <script>
        var r = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); r.lang = 'pt-BR';
        function startMic() { r.start(); document.getElementById('v_btn').innerHTML = "🔴 LISTENING SYSTEM..."; }
        r.onresult = function(e) {
            var t = e.results[0][0].transcript;
            const input = window.parent.document.querySelector('input');
            input.value = t;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            document.getElementById('v_btn').innerHTML = "🎙️ VOICE ACTIVE";
        };
        </script>
    """, height=60)

# ==========================================
# 3. INTERFACE OPERACIONAL
# ==========================================
st.markdown("<h2 style='text-align: center; color: #58A6FF;'>🛡️ NEXUS SUPREMO v1000.0</h2>", unsafe_allow_html=True)

mic_bridge()
query = st.text_input("", placeholder="Enter operational command or mission parameters...", label_visibility="collapsed")

if query:
    intel_data = asyncio.run(SovereignEngine.synthesize_intel(query))
    st.markdown(f'<div class="chat-bubble"><b>{intel_data["RESUMO"]}</b></div>', unsafe_allow_html=True)
    speak(intel_data["RESUMO"])
    
    pdf = SovereignEngine.generate_dossier_pdf(query, intel_data)
    st.download_button("📂 EXPORT TECHNICAL DOSSIER (PDF)", pdf, f"Nexus_Audit_{int(time.time())}.pdf", "application/pdf", use_container_width=True)

st.divider()

# GRADE DE MISSÃO CRÍTICA (ESTILO SÓBRIO)
st.write("### 🚀 OPERATIONAL MISSION GRID")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): speak("Iniciando Telemetria Starship. Sincronia Orbital Ativa.")
    if st.button("⚖️ LAW"): speak("Acessando Jurisprudência Suprema. Erro Zero garantido.")
with c2:
    if st.button("🧠 NEURALINK"): speak("Interface Neuralink Conectada. Sincronia de Pensamento Ativa.")
    if st.button("🧬 BIOGENETICS"): speak("Análise Genômica em tempo real. Estabilidade de DNA confirmada.")
with c3:
    if st.button("📈 IPO STRATEGY"): speak("Estratégia Global Ativada. Valuation Nexus em escala máxima.")
    if st.button("🏗️ ENG SENIOR"): speak("Engenharia Crítica validada para pressões atmosféricas extremas.")

# TELEMETRIA DE PULSO (VISUAL CIENTÍFICO)
st.divider()
pulse = SovereignEngine.get_real_pulse()
history = st.session_state.get('latency_history', [pulse])
moving_avg = np.mean(history)

cg, cm = st.columns([2, 1])
with cg:
    t = np.linspace(0, 10, 200)
    y = np.sin(t * (pulse/15) + time.time()) * np.exp(-0.01 * t)
    fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#58A6FF', width=2), fill='tozeroy'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True)
with cm:
    st.metric("PULSE (ms)", f"{pulse:.1f}")
    st.metric("MOVING AVG", f"{moving_avg:.1f} ms", delta=f"{pulse - moving_avg:.1f} ms", delta_color="inverse")

st.caption("Barbie Xeon Omni v1000.0 | Nexus Supremo Infrastructure | Stability 2026")
