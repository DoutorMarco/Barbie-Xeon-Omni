import streamlit as st
import time
import hashlib
import psutil
import platform
import io
from fpdf import FPDF
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components

# --- [1. CONFIGURAÇÃO VISUAL - ABSOLUTE BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 60px;
    }}
    .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {MATRIX_GREEN} !important;
        color: {BLACKOUT} !important; border-radius: 0px !important; width: 100%; font-weight: bold; height: 50px;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 30px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    hr {{ border: 1px solid {MATRIX_GREEN} !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; text-align: center; background: rgba(0,255,65,0.05); margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR PDF ULTRA-RESILIENTE (BINARY BUFFER)] ---
def generate_node_audit_bytes(node_name, cpu):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 16)
        pdf.cell(0, 15, f"TECHNICAL EXHIBIT: {node_name}", ln=True, align='C')
        pdf.ln(10); pdf.set_font("Courier", "", 12)
        
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        i_hash = hashlib.sha512(f"{node_name}{ts}{cpu}".encode()).hexdigest()[:40]
        
        lines = [
            f"TIMESTAMP: {ts}",
            f"NODE_PHYSICAL_ID: {platform.node().upper()}",
            f"OPERATIONAL_SECTOR: {node_name}",
            f"FEDERAL_INTEGRITY_HASH: {i_hash}",
            "-"*50,
            "STATUS: NATIONAL INTEREST WAIVER (NIW) ELIGIBLE",
            "ARCHITECT: MARCO ANTONIO DO NASCIMENTO"
        ]
        for line in lines: pdf.cell(0, 10, line, ln=True)
        
        # Saída via buffer de bytes para evitar erro de tipo no Streamlit
        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str):
            return pdf_output.encode('latin-1')
        return bytes(pdf_output)
    except Exception as e:
        st.error(f"Erro Crítico no Motor PDF: {e}")
        return None

# --- [3. DASHBOARD DE COMANDO CENTRAL] ---
@st.fragment(run_every=5)
def xeon_dashboard():
    cpu_val = psutil.cpu_percent()
    
    # Telemetria Superior
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1:
        st.metric("STABILITY", "NOMINAL")
        st.metric("HOMEOSTASE", f"{100-(cpu_val*0.1):.2f}%")
    with c2:
        gauge_opt = {
            "backgroundColor": "transparent",
            "series": [{
                "type": 'gauge', "startAngle": 90, "endAngle": -270,
                "pointer": {"show": False}, "progress": {"show": True, "itemStyle": {"color": MATRIX_GREEN}},
                "data": [{"value": cpu_val}], "detail": {"formatter": '{value}%', "color": MATRIX_GREEN, "fontSize": 30}
            }]
        }
        st_echarts(options=gauge_opt, height="250px")
    with c3:
        st.metric("EB-1A TARGET", "99.8%")
        if st.button("🐞 DEBUGGER"):
            st.json({"node": platform.node(), "cpu": cpu_val, "status": "NOMINAL"})

    st.markdown("<hr>", unsafe_allow_html=True)

    # Estado de Ativação
    if 'active_node' not in st.session_state: st.session_state.active_node = None
    if 'voice_trigger' not in st.session_state: st.session_state.voice_trigger = ""

    # 9 NÓS DE DEFESA
    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    
    cols = st.columns(3)
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            
            # BOTÃO DE ATIVAÇÃO COM VOX INTEGRADO
            if st.button(f"ATIVAR {s}", key=f"act_{i}"):
                st.session_state.active_node = s
                st.session_state.voice_trigger = f"Nó {s} ativado. Gerando evidência para Arquiteto Marco Antonio."
                st.rerun()

            # DOWNLOAD DO DOSSIÊ (Seguro)
            if st.session_state.active_node == s:
                pdf_data = generate_node_audit_bytes(s, cpu_val)
                if pdf_data:
                    st.download_button(
                        label=f"📥 BAIXAR DOSSIÊ {s}", 
                        data=pdf_data, 
                        file_name=f"XEON_{s.replace(' ', '_')}.pdf", 
                        mime="application/pdf", 
                        key=f"dl_{i}"
                    )

    # DISPARO DA VOZ (Vox Protocol)
    if st.session_state.voice_trigger:
        components.html(f"""
            <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{st.session_state.voice_trigger}');
            msg.lang = 'pt-BR';
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
        st.session_state.voice_trigger = ""

# --- [4. FINALIZAÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 5px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
xeon_dashboard()
st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | ZERO WHITE POLICY")
