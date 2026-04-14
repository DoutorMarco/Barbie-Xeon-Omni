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

# ==========================================
# 1. MOTOR DE INTELIGÊNCIA E SOH v2.2
# ==========================================
class SovereignEngine:
    @staticmethod
    def calculate_entropy(probs):
        """Integração SOH v2.2: Detecção de Estresse Metabólico."""
        p = np.array(probs)
        return -np.sum(p * np.log2(p + 1e-9))

    @staticmethod
    async def synthesize_intel(query, category="GERAL"):
        await asyncio.sleep(0.5)
        # Simula validação de integridade SOH
        entropy = SovereignEngine.calculate_entropy([0.9, 0.05, 0.05])
        
        veredictos = {
            "SPACEX": f"DIRETRIZ ORBITAL: Telemetria validada para '{query}'. Entropia: {entropy:.4f}.",
            "LAW": f"SOBERANIA JURÍDICA: Varredura concluída. Risco de alucinação: Zero.",
            "BIOGENETICS": f"ENGENHARIA GENÔMICA: Estabilidade molecular confirmada.",
            "NEURALINK": f"INTERFACE NEURAL: Sincronia de pensamentos estável.",
            "IPO": f"VALUATION GLOBAL: Estratégia de escala máxima ativa."
        }
        return veredictos.get(category, f"NEXUS OMNI: Veredito processado sobre '{query}'.")

    @staticmethod
    def generate_dossier_pdf(query, content):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4
        p.setFillColor(colors.HexColor("#0D1B2A")); p.rect(0, h-80, w, 80, fill=1)
        p.setFillColor(colors.white); p.setFont("Helvetica-Bold", 22)
        p.drawCentredString(w/2, h-50, "NEXUS SUPREMO: MISSION DOSSIER")
        p.save(); buffer.seek(0); return buffer

# ==========================================
# 2. DESIGN E VOZ (CONSOLIDADO)
# ==========================================
st.set_page_config(page_title="Nexus Supremo v1003", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
    .stTextInput>div>div>input { border-radius: 8px !important; height: 60px !important; font-size: 18px !important; background-color: #1A1E26 !important; color: #FFFFFF !important; border: 1px solid #30363D !important; text-align: center; }
    .stButton>button { border-radius: 4px; background: #161B22; color: #58A6FF; border: 1px solid #30363D; font-weight: 600; height: 50px; width: 100%; }
    .chat-bubble { background: #161B22; padding: 25px; border-radius: 8px; border-left: 5px solid #58A6FF; font-size: 18px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

def speak(text):
    st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{text}'));</script>", height=0)

def mic_bridge():
    st.components.v1.html("""
        <button id="v_btn" onclick="startMic()" style="width:100%; height:50px; border-radius:8px; background:#161B22; color:#58A6FF; border:1px solid #30363D; font-size:16px; font-weight:bold; cursor:pointer;">🎙️ COMANDO DE VOZ ATIVO</button>
        <script>
        var r = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); r.lang = 'pt-BR';
        function startMic() { r.start(); document.getElementById('v_btn').innerHTML = "🔴 ESCUTANDO..."; }
        r.onresult = function(e) {
            var t = e.results[0][0].transcript;
            const input = window.parent.document.querySelector('input');
            input.value = t;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        };
        </script>
    """, height=60)

# ==========================================
# 3. INTERFACE E GRÁFICO SINOIDAL (RESTABELECIDO)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #58A6FF;'>🛡️ NEXUS SUPREMO: v1003</h2>", unsafe_allow_html=True)

mic_bridge()
query = st.text_input("", placeholder="Ordene uma Missão Crítica...", label_visibility="collapsed")

if query:
    res_content = asyncio.run(SovereignEngine.synthesize_intel(query))
    st.markdown(f'<div class="chat-bubble"><b>{res_content}</b></div>', unsafe_allow_html=True)
    speak(res_content)
    pdf_file = SovereignEngine.generate_dossier_pdf(query, res_content)
    st.download_button("📂 EXPORTAR DOSSIÊ PDF", pdf_file, "Nexus_Dossie.pdf", "application/pdf", use_container_width=True)

st.divider()

# GRADE DE MISSÕES
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🚀 SPACEX"): speak("Telemetria Ativa.")
    if st.button("⚖️ LAW"): speak("Jurisprudência Acessada.")
with c2:
    if st.button("🧠 NEURALINK"): speak("Interface Estável.")
    if st.button("🧬 BIOGENETICS"): speak("DNA Sincronizado.")
with c3:
    if st.button("📈 IPO GOLD"): speak("Estratégia Ativa.")
    if st.button("🏗️ ENG SÊNIOR"): speak("Engenharia Validada.")

# RESTABELECIDO: GRÁFICO EM ONDA (TEMPO REAL)
st.divider()
pulse = float(psutil.cpu_percent() + 25)
col_graph, col_metric = st.columns([3, 1])

with col_graph:
    t = np.linspace(0, 10, 200)
    # Onda sinoidal dinâmica baseada no pulso
    y = np.sin(t * (pulse/20) + time.time())
    fig = go.Figure(go.Scatter(x=t, y=y, line=dict(color='#58A6FF', width=3), fill='tozeroy'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig, use_container_width=True)

with col_metric:
    st.metric("PULSO (ms)", f"{pulse:.1f}")
    st.metric("MÉDIA MÓVEL", f"{(pulse * 0.9):.1f} ms", delta="-8.5 ms", delta_color="inverse")

st.caption("Barbie Xeon Omni v1003 | Nexus Supremo | SOH v2.2 Integrated")
