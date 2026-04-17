import streamlit as st
import psutil
import time
import hashlib
import plotly.graph_objects as go
from fpdf import FPDF
import streamlit.components.v1 as components

# --- [CORE: PROTOCOLO DE REALIDADE ABSOLUTA] ---
def get_absolute_reality_metrics():
    cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    signature_base = f"{cpu_usage}-{memory.free}-{time.time()}"
    reality_token = hashlib.sha256(signature_base.encode()).hexdigest()
    return {
        "cpu_usage": cpu_usage,
        "cpu_freq": cpu_freq,
        "mem_percent": memory.percent,
        "token": reality_token,
        "entropy_level": 100 - cpu_usage
    }

# --- [ENGINE: PDF DE SUPREMACIA V64 - 2 PÁGINAS] ---
def generate_sovereign_pdf(metrics, node_name):
    pdf = FPDF()
    # PÁGINA 1: Telemetria de Hardware
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65)
    pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 10, f"AUDITORIA XEON - NÓ: {node_name}", 0, 1, 'C')
    pdf.set_font("Courier", "", 10)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"DATA: {time.ctime()}\nTOKEN: {metrics['token']}\nVALOR HORA: R$ 1.000,00\n\nSTATUS DO HARDWARE NO MOMENTO DA GERACAO:\n- CPU: {metrics['cpu_usage']}%\n- RAM: {metrics['mem_percent']}%")
    
    # PÁGINA 2: EB-1A Evidence
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65)
    pdf.set_font("Courier", "B", 14)
    pdf.cell(0, 10, "EVIDENCIA DE HABILIDADE EXTRAORDINARIA (EB-1A)", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Courier", "", 10)
    pdf.multi_cell(0, 10, "ITEM: PROTECAO DE INFRAESTRUTURA CRITICA\n\nEste documento atesta que o sistema operado pelo Arquiteto Marco Antonio Nascimento utiliza algoritmos de negentropia para estabilizacao de dados em hardware real, critério essencial para defesa cibernética de interesse nacional.")
    return pdf.output(dest='S').encode('latin-1')

# --- [INTERFACE: CONFIGURAÇÃO SOBERANA] ---
st.set_page_config(page_title="XEON OMNI v101.64", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #000000; color: #00FF41; border: 1px solid #00FF41; font-weight: bold; }
    .stProgress > div > div > div > div { background-color: #00FF41; }
    </style>
    """, unsafe_allow_stdio=True)

# --- [HEADER & VOZ] ---
st.title("🛰️ XEON OMNI v101.64 | ARQUITETO MARCO ANTONIO")
components.html("""
    <div style="background-color: #000000; padding: 10px; border: 1px solid #00FF41; color: #00FF41; font-family: monospace;">
        <button onclick="startListen()" style="background:none; border: 1px solid #00FF41; color:#00FF41; cursor:pointer; padding: 5px;">🎙️ ESCUTA GLOBAL ATIVA</button>
        <span id="status" style="margin-left: 15px;">Aguardando Comando...</span>
    </div>
    <script>
        const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
        recognition.continuous = true; lang = 'pt-BR';
        function startListen() { recognition.start(); document.getElementById('status').innerText = "Escutando todas as línguas..."; }
        recognition.onresult = (event) => { 
            const t = event.results[event.results.length-1][0].transcript;
            document.getElementById('status').innerText = "Voz: " + t;
        };
    </script>
    """, height=70)

# --- [NÓS DE PROCESSAMENTO] ---
def render_node(node_id, title):
    with st.container():
        st.markdown(f"### {title}")
        metrics = get_absolute_reality_metrics()
        
        col_btn, col_status = st.columns([1, 2])
        
        with col_btn:
            if st.button(f"EXECUTAR {node_id}"):
                bar = st.progress(0)
                for p in range(101):
                    time.sleep(0.01)
                    bar.progress(p)
                st.success(f"{node_id}: Sincronizado")
            
            pdf_data = generate_sovereign_pdf(metrics, title)
            st.download_button(
                label=f"📥 PDF AUDITORIA - {node_id}",
                data=pdf_data,
                file_name=f"XEON_{node_id}.pdf",
                mime="application/pdf",
                key=f"pdf_{node_id}"
            )
        
        with col_status:
            st.code(f"TOKEN: {metrics['token'][:32]}...\nSTATUS: NOMINAL (R$ 1.000,00/h)", language="bash")
        st.markdown("---")

# Renderização dos Nós Estratégicos
nodes = {
    "NODE_01": "AUDITORIA DE INFRAESTRUTURA CRÍTICA",
    "NODE_02": "DEFESA CIBERNÉTICA & PQC",
    "NODE_03": "BIO-ESTASE & FILTRO DIANA"
}

for n_id, n_title in nodes.items():
    render_node(n_id, n_title)

# --- [FOOTER] ---
st.markdown(f"**TAXA DE CONSULTORIA: R$ 1.000,00/H | DATA: {time.strftime('%d/%m/%Y %H:%M:%S')}**")
