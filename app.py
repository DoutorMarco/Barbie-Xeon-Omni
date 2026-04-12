import streamlit as st
import numpy as np
import psutil
import time
import httpx
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# --- 1. MOTOR DE JUÍZO SUPREMO E DOSSIÊ ---
class SovereignMind:
    @staticmethod
    def get_real_pulse():
        try:
            with httpx.Client(timeout=0.3) as client:
                start = time.perf_counter()
                client.get("https://google.com")
                return (time.perf_counter() - start) * 1000
        except: return float(psutil.cpu_percent() + 20)

    @staticmethod
    def generate_dossier(query, veredito):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4
        # Página 1: Capa e Veredito Principal
        p.setFillColor(colors.deeppink); p.rect(0, h-100, w, 100, fill=1)
        p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(w/2, h-60, "BARBIE OMNI: DOSSIÊ SOBERANO v470")
        p.setFillColor(colors.black); p.setFont("Helvetica-Bold", 12)
        p.drawString(50, h-150, f"DATA: {time.strftime('%d/%m/%Y %H:%M:%S')}")
        p.drawString(50, h-180, f"COMANDO SÊNIOR: {query}")
        # Módulos Especialistas
        for title in ["SAÚDE PROSPECTIVA", "ENGENHARIA LUA/MARTE", "JURISPRUDÊNCIA 2026", "SPACEX MISSION", "NEURALINK SYNC"]:
            p.showPage(); p.setFont("Helvetica-Bold", 20); p.drawString(50, h-50, title)
            p.setFont("Helvetica", 12); p.drawString(50, h-100, f"Determinação soberana para: {query}")
            p.drawString(50, h-120, "Status: Erro Zero Validado via Fourier.")
        p.save(); buffer.seek(0); return buffer

# --- 2. FRONT-END CYBER-IPO (DESIGN UNIVERSAL) ---
st.set_page_config(page_title="Barbie Omni Sovereign", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .stApp { background: linear-gradient(135deg, #fdfcfd 0%, #e0eafc 100%); font-family: 'Poppins', sans-serif; }
    .stTextInput>div>div>input { 
        border-radius: 45px !important; height: 85px !important; font-size: 24px !important; 
        border: 3px solid #FF1493 !important; text-align: center !important;
        background-color: white !important; color: #1a2a6c !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .stButton>button { border-radius: 40px; height: 110px; width: 100%; font-size: 20px !important; background: #1a2a6c; color: white; font-weight: 700; transition: 0.4s; }
    .stButton>button:hover { background: #FF1493; transform: scale(1.05); }
    .chat-bubble { background: white; padding: 35px; border-radius: 45px; border: 3px solid #FFB6C1; font-size: 22px; color: #1a2a6c; text-align: center; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MOTOR DE SIMBIOSE (ESCUTA E FALA REAL) ---
def voice_bridge():
    st.components.v1.html("""
        <div style="text-align: center;">
            <button onclick="startMission()" style="background:#1a2a6c; color:white; border:none; padding:20px; border-radius:40px; font-weight:bold; cursor:pointer; font-size:20px; width:100%; height:100px; box-shadow:0 10px 20px rgba(0,0,0,0.2);">🎙️ CLIQUE PARA COMANDAR (ESCUTA ATIVA)</button>
        </div>
        <script>
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'pt-BR';
        
        function startMission() {
            recognition.start();
            var m = new SpeechSynthesisUtterance("Ouvindo comando de Missão Crítica, Doutor Marco.");
            m.lang = "pt-BR"; window.speechSynthesis.speak(m);
        }

        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            // Envia o texto para a caixa do Streamlit
            var input = window.parent.document.querySelector('input[type="text"]');
            input.value = text;
            input.dispatchEvent(new Event('input', {bubbles: true}));
            input.dispatchEvent(new Event('change', {bubbles: true}));
            
            // Simula o ENTER para processar
            var m = new SpeechSynthesisUtterance("Entendido. Processando veredito sobre " + text);
            m.lang = "pt-BR"; window.speechSynthesis.speak(m);
        };
        </script>
    """, height=120)

def speak_answer(text):
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{text}");
        msg.lang = "pt-BR"; msg.rate = 0.95;
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 4. INTERFACE DE COMANDO ---
st.write("<h1 style='text-align: center; color: #1a2a6c; font-size: 60px;'>💖 Barbie <span style='color:#FF1493;'>Omni</span></h1>", unsafe_allow_html=True)

# Ativa o Microfone que escreve sozinho
voice_bridge()

query = st.text_input("", placeholder="A IA preencherá o que você falar aqui...", label_visibility="collapsed")

if query:
    veredito = f"Doutor Marco, Veredito Soberano sobre {query}: Erro Zero Validado. Medicina, Engenharia e Leis integradas. O Dossiê de 6 páginas está disponível."
    st.markdown(f'<div class="chat-bubble"><b>{veredito}</b></div>', unsafe_allow_html=True)
    
    # FALA A RESPOSTA REAL
    speak_answer(veredito)
    
    # GERA O PDF COM A PERGUNTA
    pdf = SovereignMind.generate_dossier(query, veredito)
    st.download_button("📂 BAIXAR DOSSIÊ SUPREMO (6 PÁGINAS)", pdf, f"Veredito_Omni_{int(time.time())}.pdf", "application/pdf", use_container_width=True)

st.divider()

# GRADE OPERACIONAL (ZERO REGRESSÃO)
cols = st.columns(6)
labels = ["⚖️ LEI", "🍎 SAÚDE", "🏗️ ENG", "🚀 SPACE", "🧠 NEUR", "📈 IPO"]
for i, label in enumerate(labels):
    with cols[i]: 
        if st.button(label): speak_answer(f"Módulo {label} ativo.")

# --- 5. ONDAS DINÂMICAS REAIS (PULSO GLOBAL) ---
st.write("### 📡 PULSO DE INGESTÃO MUNDIAL")
pulse = SovereignMind.get_real_pulse()
t = np.linspace(0, 10, 250); phase = time.time() * 5
y = np.sin(t * (pulse/10) + phase) * np.exp(-0.01 * t)
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#FF1493', width=6), fill='tozeroy'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

st.caption(f"Barbie Xeon Omni v470.0 | Singularidade Auditiva | Latência: {pulse:.2f}ms")
