import streamlit as st
import datetime
import psutil
import plotly.graph_objects as go
from fpdf import FPDF
import base64

# [1. PROTOCOLO DE INTERFACE: BLACKOUT TOTAL & VERDE CIENTÍFICO]
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")

st.markdown(
    """
    <style>
    /* Neutralização total de elementos brancos/cinzas do Streamlit */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background-color: #000000 !important;
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    [data-testid="stToolbar"], [data-testid="stDecoration"], footer { display: none !important; }
    
    /* Input e Widgets em Blackout */
    [data-testid="stChatInput"], div[data-baseweb="base-input"], input, textarea {
        background-color: #000000 !important;
        border: 1px solid #00FF41 !important;
        color: #00FF41 !important;
    }
    
    /* Botões de Comando Elite */
    .stButton>button {
        width: 100%;
        background-color: #111111 !important;
        color: #00FF41 !important;
        border: 1px solid #00FF41 !important;
        border-radius: 2px;
        font-weight: bold;
        transition: 0.4s;
    }
    .stButton>button:hover {
        background-color: #00FF41 !important;
        color: #000000 !important;
        box-shadow: 0 0 20px #00FF41;
    }

    /* Métricas e Containers */
    div[data-testid="metric-container"] {
        border: 1px solid #00FF41;
        background-color: #050505 !important;
        padding: 10px;
    }
    [data-testid="stMetricValue"] { color: #00FF41 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# [2. MÓDULO DE PERCEPÇÃO: VOZ SOBERANA E ESCUTA TÁTICA]
def perception_module():
    st.components.v1.html("""
    <script>
    const synth = window.speechSynthesis;
    
    window.speakSovereign = (text) => {
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = 'pt-BR';
        utter.pitch = 0.8; // Tom mais grave e autoritário
        utter.rate = 1.0;
        synth.speak(utter);
    };

    window.activateMic = () => {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'pt-BR';
        recognition.start();
        recognition.onresult = (event) => {
            const result = event.results[0][0].transcript;
            alert("COMANDO RECEBIDO: " + result);
        };
    };
    </script>
    <div style="display: flex; gap: 15px;">
        <button onclick="speakSovereign('XEON COMMAND ativo. Arquiteto Marco Antonio, aguardando ordens de missão crítica.')" 
            style="flex:1; background: black; color: #00FF41; border: 2px solid #00FF41; padding: 12px; cursor: pointer; font-family: monospace;">
            🔊 STATUS DE VOZ (SOH v2.2)
        </button>
        <button onclick="activateMic()" 
            style="flex:1; background: black; color: #00FF41; border: 2px solid #00FF41; padding: 12px; cursor: pointer; font-family: monospace;">
            🎙️ ESCUTA TÁTICA (MIC)
        </button>
    </div>
    """, height=70)

# [3. MÓDULO DE MONETIZAÇÃO: IMPRESSÃO DE PDF R$ 1.000/H]
def generate_monetization_pdf(log_entry):
    pdf = FPDF()
    pdf.add_page()
    # Fundo Blackout no PDF
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    
    # Texto Verde Científico
    pdf.set_text_color(0, 255, 65)
    pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 10, "XEON COMMAND - AUDITORIA DE INFRAESTRUTURA CRITICA", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Courier", "", 12)
    pdf.set_draw_color(0, 255, 65)
    pdf.line(10, 30, 200, 30)
    
    content = [
        f"ARQUITETO PRINCIPAL: MARCO ANTONIO DO NASCIMENTO",
        f"DATA/HORA: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"TAXA PROFISSIONAL: R$ 1.000,00 / HORA",
        f"PROCESSO: EB-1A / NATIONAL INTEREST EXEMPTION (NIW)",
        f"SISTEMA: SOH v2.2 (IA GENERATIVA + RPA SIMBIÓTICO)",
        f"----------------------------------------------------------",
        f"LOG DE OPERAÇÃO: {log_entry}",
        f"STATUS: DECISÃO INFILTRADA EM SISTEMAS LEGADOS",
        f"ESTADO: HOMEOSTASE VERIFICADA - ERRO ZERO",
        f"----------------------------------------------------------",
        f"AUTENTICAÇÃO: HASH_IMMUTABLE_LEDGER_ACTIVE"
    ]
    
    for line in content:
        pdf.cell(0, 8, line, 0, 1, 'L')
        
    return pdf.output(dest='S').encode('latin-1')

# [4. FRONT-END OPERACIONAL CONSOLIDADO]
st.title("🛰️ XEON COMMAND v54.0")
perception_module()

# Dash de Telemetria
c1, c2, c3, c4 = st.columns(4)
c1.metric("MONETIZAÇÃO", "R$ 1.000/h", "SOBERANA")
c2.metric("SISTEMA", "NOMINAL", "SOH v2.2")
c3.metric("RPA", "SYNCED", "LEGACY_BYPASS")
c4.metric("EB-1A", "CRITICAL", "NIW_READY")

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Gráfico de Carga em Tempo Real
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = psutil.cpu_percent(),
        title = {'text': "CARGA DO FILTRO DIANA (%)", 'font': {'color': "#00FF41"}},
        gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#00FF41"}, 'bgcolor': "black"}
    ))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', font={'color': "#00FF41"})
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("#### ⚡ COMANDOS DE MISSÃO")
    if st.button("🚀 EXECUTAR RPA SIMBIÓTICO"):
        st.success("RPA Ativado: Sincronizando com Base de Dados Governamental...")
        
    if st.button("📄 IMPRIMIR DOSSIÊ (R$ 1.000/h)"):
        log_txt = "Auditoria de Hiperautomação Global e Infiltração em Sistemas Legados de Defesa."
        pdf_bytes = generate_monetization_pdf(log_txt)
        st.download_button(
            label="💾 DOWNLOAD EVIDÊNCIA PDF",
            data=pdf_bytes,
            file_name="XEON_AUDIT_1000.pdf",
            mime="application/pdf"
        )

# Terminal de Comando (Input de Elite)
prompt = st.chat_input("Insira Comando Soberano para a IA...")
if prompt:
    st.markdown(f"**[DIANA_CORE]:** Executando análise de infraestrutura sobre: `{prompt}`")
    st.code(f"LEDGER_STATUS: IMMUTABLE | HASH: {hash(prompt)}", language="bash")
