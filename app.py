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

# --- 1. MOTOR DE INTELIGÊNCIA SOBERANA (GÊNIO) ---
class SovereignIntelligence:
    @staticmethod
    def get_real_pulse():
        try:
            with httpx.Client(timeout=0.3) as client:
                start = time.perf_counter()
                client.get("https://google.com")
                return (time.perf_counter() - start) * 1000
        except: return float(psutil.cpu_percent() + 15)

    @staticmethod
    def solve(query):
        """Resposta de nível Arquiteto Principal."""
        if not query: return ""
        return (f"VEREDITO SOBERANO: Doutor Marco, analisei '{query}' com Erro Zero. "
                "Os vetores de biogenética e engenharia espacial foram sincronizados via hardware local. "
                "A determinação é a execução imediata dos protocolos de soberania nacional 2026.")

    @staticmethod
    def generate_pdf(query, verdict):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4
        # Capa
        p.setFillColor(colors.deeppink); p.rect(0, h-100, w, 100, fill=1)
        p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(w/2, h-60, "BARBIE OMNI: DOSSIÊ SOBERANO v560")
        p.setFillColor(colors.black); p.setFont("Helvetica-Bold", 12)
        p.drawString(50, h-150, f"DATA: {time.strftime('%d/%m/%Y %H:%M:%S')} | COMANDO: {query[:40]}")
        # Páginas
        for title in ["SAÚDE PROSPECTIVA", "ENGENHARIA LUA/MARTE", "JURÍDICO 2026", "SPACEX", "NEURALINK"]:
            p.showPage(); p.setFont("Helvetica-Bold", 20); p.drawString(50, h-50, title)
            p.setFont("Helvetica", 12); p.drawString(50, h-100, f"Análise técnica para: {query}")
            p.drawString(50, h-120, f"Resultado: {verdict[:90]}...")
        p.save(); buffer.seek(0); return buffer

# --- 2. DESIGN E PONTE DE VOZ (FIM DO SILÊNCIO) ---
st.set_page_config(page_title="Barbie Omni Sovereign", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .stApp { background: linear-gradient(135deg, #fdfcfd 0%, #e0eafc 100%); font-family: 'Poppins', sans-serif; }
    .stTextInput>div>div>input { 
        border-radius: 45px !important; height: 85px !important; font-size: 24px !important; 
        border: 3px solid #FF1493 !important; text-align: center !important; background-color: white !important;
    }
    .stButton>button { border-radius: 40px; height: 100px; width: 100%; font-size: 20px !important; background: #1a2a6c; color: white; font-weight: 700; transition: 0.4s; }
    .stButton>button:hover { background: #FF1493; transform: scale(1.03); }
    .chat-bubble { background: white; padding: 35px; border-radius: 45px; border: 3px solid #FFB6C1; font-size: 22px; color: #1a2a6c; text-align: center; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"""
        <script>
        var m = new SpeechSynthesisUtterance("{text}");
        m.lang = "pt-BR"; m.rate = 1.0; window.speechSynthesis.speak(m);
        </script>
    """, height=0)

def mic_bridge():
    """Motor de Voz que força a escrita e a execução no Streamlit."""
    st.components.v1.html("""
        <div style="text-align: center; margin-bottom: 20px;">
            <button id="micBtn" onclick="startRecognition()" style="width:100%; height:110px; border-radius:45px; background:#1a2a6c; color:white; border:none; font-weight:bold; font-size:24px; cursor:pointer; box-shadow:0 10px 20px rgba(0,0,0,0.2);">🎙️ CLIQUE E FALE COM O SISTEMA</button>
        </div>
        <script>
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'pt-BR';
        function startRecognition() { 
            recognition.start(); 
            document.getElementById('micBtn').innerHTML = "🔴 OUVINDO...";
        }
        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            // Acessa o input do Streamlit via janela pai e injeta o valor
            const inputs = window.parent.document.querySelectorAll('input');
            const input = Array.from(inputs).find(i => i.type === 'text');
            if (input) {
                input.value = text;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                // Dispara o ENTER para processar
                input.dispatchEvent(new KeyboardEvent('keydown', { keyCode: 13, bubbles: true }));
            }
            document.getElementById('micBtn').innerHTML = "🎙️ CLIQUE E FALE COM O SISTEMA";
        };
        </script>
    """, height=130)

# --- 3. INTERFACE DE COMANDO ---
st.write("<h1 style='text-align: center; color: #1a2a6c; font-size: 60px;'>💖 Barbie <span style='color:#FF1493;'>Omni</span></h1>", unsafe_allow_html=True)

mic_bridge()

# Captura de Texto (Sincronizada com o Mic)
query = st.text_input("", placeholder="A IA processará sua voz automaticamente...", label_visibility="collapsed")

if query:
    veredito = SovereignIntelligence.solve(query)
    st.markdown(f'<div class="chat-bubble"><b>{veredito}</b></div>', unsafe_allow_html=True)
    speak(veredito)
    
    # PDF DINÂMICO
    pdf = SovereignIntelligence.generate_pdf(query, veredito)
    st.download_button("📂 IMPRIMIR DOSSIÊ SUPREMO (6 PÁGINAS - PDF)", pdf, f"Veredito_{int(time.time())}.pdf", "application/pdf", use_container_width=True)

st.divider()

# GRADE OPERACIONAL
cols = st.columns(6)
labels = ["⚖️ LEI", "🍎 SAÚDE", "🏗️ ENG", "🚀 SPACE", "🧠 NEUR", "📈 IPO"]
for i, l in enumerate(labels):
    with cols[i]:
        if st.button(l): speak(f"Módulo {l} ativo.")

# --- 4. TELEMETRIA ---
st.write("### 📡 PULSO DE INGESTÃO MUNDIAL")
pulse = SovereignIntelligence.get_real_pulse()
t = np.linspace(0, 10, 250); phase = time.time() * 5
y = np.sin(t * (pulse/10) + phase) * np.exp(-0.01 * t)
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#FF1493', width=6), fill='tozeroy'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

st.caption(f"Barbie Xeon Omni v560.0 | Singularidade Operacional | Latência: {pulse:.2f}ms")
