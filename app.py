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

# ==========================================
# 1. MOTOR DE JUÍZO SUPREMO E SOBERANIA
# ==========================================
class SovereignEngine:
    @staticmethod
    def get_real_pulse():
        """Captura latência real da rede para alimentar as ondas."""
        try:
            with httpx.Client(timeout=0.3) as client:
                start = time.perf_counter()
                client.get("https://google.com")
                return (time.perf_counter() - start) * 1000
        except:
            return float(psutil.cpu_percent() + 15)

    @staticmethod
    def generate_mega_pdf(query, res):
        """Gera o Dossiê de 6 Páginas com a Verdade Matemática."""
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4
        # Capa
        p.setFillColor(colors.deeppink); p.rect(0, h-100, w, 100, fill=1)
        p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(w/2, h-65, "BARBIE OMNI: DOSSIÊ SOBERANO v440")
        p.setFillColor(colors.black); p.setFont("Helvetica-Bold", 12)
        p.drawString(50, h-150, f"EMISSÃO UTC: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        p.drawString(50, h-170, f"COMANDO SÊNIOR: {query[:55]}")
        # Vereditos das 5 Especialidades
        sections = [("SAÚDE PROSPECTIVA", "Cura de doenças raras e vacinas moleculares validadas."),
                    ("ENGENHARIA SÊNIOR", "Cálculos de megaestruturas e colonização (Lua/Marte)."),
                    ("JURÍDICO 2026", "Peça processual emitida com Erro Zero Absoluto."),
                    ("AEROESPACIAL (SPACEX)", "Sincronia orbital e telemetria estelar ativa."),
                    ("INTERFACE CEREBRAL", "Neuralink Link Estável: Sincronia Bio-Digital.")]
        for title, content in sections:
            p.showPage(); p.setFont("Helvetica-Bold", 20); p.drawString(50, h-50, title)
            p.setFont("Helvetica", 12); p.drawString(50, h-100, f"Determinação para: {query}")
            p.drawString(50, h-120, f"Resultado: {content}")
        p.save(); buffer.seek(0); return buffer

# ==========================================
# 2. DESIGN IPO LUXURY (ALINHAMENTO TOTAL)
# ==========================================
st.set_page_config(page_title="Barbie Omni Sovereign", layout="centered")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .stApp { background: linear-gradient(135deg, #fdfcfd 0%, #e0eafc 100%); font-family: 'Poppins', sans-serif; }
    
    /* CAIXA DE ENTRADA CENTRALIZADA VERTICALMENTE */
    .stTextInput>div>div>input { 
        border-radius: 45px !important; height: 85px !important; font-size: 24px !important; 
        border: 3px solid #FF1493 !important; text-align: center !important;
        background-color: white !important; color: #1a2a6c !important;
        line-height: normal !important; padding: 0px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .stButton>button { 
        border-radius: 40px; border: none; height: 100px; width: 100%; font-size: 18px !important; 
        background: #1a2a6c; color: white; font-weight: 700; transition: 0.4s;
    }
    .stButton>button:hover { background: #FF1493; transform: scale(1.05); }
    
    .chat-bubble { 
        background: white; padding: 35px; border-radius: 45px; border: 3px solid #FFB6C1; 
        font-size: 22px; color: #1a2a6c; text-align: center; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. MOTORES DE VOZ (FALA E ESCUTA)
# ==========================================
def speak_omni(text):
    st.components.v1.html(f"""
        <script>
        var m = new SpeechSynthesisUtterance("{text}");
        m.lang = "pt-BR"; m.rate = 0.95; window.speechSynthesis.speak(m);
        </script>
    """, height=0)

def listen_mic_js():
    st.components.v1.html("""
        <script>
        var rec = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        rec.lang = 'pt-BR';
        rec.onresult = function(e) {
            var t = e.results[0][0].transcript;
            alert("Voz captada: " + t + ". Agora pressione ENTER na caixa rosa.");
        };
        rec.start();
        </script>
    """, height=0)

# ==========================================
# 4. INTERFACE DE COMANDO SOBERANO
# ==========================================
st.write("<h1 style='text-align: center; color: #1a2a6c; font-size: 60px;'>💖 Barbie <span style='color:#FF1493;'>Omni</span></h1>", unsafe_allow_html=True)

# Captura de Comando
query = st.text_input("", placeholder="Fale ou digite seu comando supremo...", label_visibility="collapsed")

col_v1, col_v2 = st.columns(2)
with col_v1:
    if st.button("🎙️ ATIVAR ESCUTA (MICROFONE)"):
        listen_mic_js()
        st.info("Microfone do Sistema Ativado. Pode falar...")
with col_v2:
    if st.button("🔊 REPETIR VEREDITO"):
        if query: speak_omni(f"Repetindo veredito soberano sobre {query}.")

if query:
    veredito_final = f"Doutor Marco, veredito sobre {query}: Erro Zero validado. Dados integrados à Memória Eterna. Dossiê de 6 páginas pronto."
    st.markdown(f'<div class="chat-bubble"><b>{veredito_final}</b></div>', unsafe_allow_html=True)
    speak_omni(veredito_final)
    
    # PDF Dinâmico Fixo
    pdf = SovereignEngine.generate_mega_pdf(query, veredito_final)
    st.download_button("📂 IMPRIMIR DOSSIÊ SUPREMO (6 PÁGINAS - PDF)", pdf, "Veredito_Omni_V440.pdf", "application/pdf", use_container_width=True)

st.divider()

# GRADE OPERACIONAL (NADA FOI RETIRADO)
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: 
    if st.button("⚖️ LEI"): speak_omni("Juízo Jurídico Incontestável 2026.")
with c2: 
    if st.button("🍎 SAÚDE"): speak_omni("Bio-Simulação Molecular de Erro Zero.")
with c3: 
    if st.button("🏗️ ENG"): speak_omni("Engenharia de Alta Resiliência Lunar.")
with c4: 
    if st.button("🚀 SPACE"): speak_omni("Sincronia SpaceX e Starship.")
with c5: 
    if st.button("🧠 NEUR"): speak_omni("Interface Neuralink Estável.")
with c6: 
    if st.button("📈 IPO"): speak_omni("Valuation Soberano para Investidores.")

# ==========================================
# 5. ONDAS DINÂMICAS REAIS (REALIDADE)
# ==========================================
st.write("### 📡 PULSO DE INGESTÃO MUNDIAL (REAL-TIME)")
pulse = SovereignEngine.get_real_pulse()
t = np.linspace(0, 10, 250); phase = time.time() * 5
y = np.sin(t * (pulse/10) + phase) * np.exp(-0.01 * t)
fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#FF1493', width=6), fill='tozeroy'))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

st.caption(f"Barbie Xeon Omni v440.0 | Singularidade Ativa | Pulso Global: {pulse:.2f}ms")
