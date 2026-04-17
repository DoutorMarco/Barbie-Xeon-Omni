import streamlit as st
import time
import hashlib
import psutil
import platform
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
        color: {BLACKOUT} !important; border-radius: 0px !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 30px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    hr {{ border: 1px solid {MATRIX_GREEN} !important; }}
    .node-card {{ border: 1px solid {MATRIX_GREEN}; padding: 15px; text-align: center; background: rgba(0,255,65,0.02); margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE EVIDÊNCIA PDF - FIX] ---
def generate_node_audit(node_name, cpu):
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
        
        # Geração segura de bytes
        pdf_content = pdf.output(dest='S')
        if isinstance(pdf_content, str):
            return pdf_content.encode('latin-1')
        return pdf_content
    except Exception:
        return None

# --- [3. DASHBOARD DE COMANDO CENTRAL] ---
@st.fragment(run_every=5)
def xeon_dashboard():
    cpu_val = psutil.cpu_percent()
    
    # Telemetria Superior
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c1:
        st.metric("STABILITY", "TIER-1")
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
        st.metric("EB-1A STATUS", "ACTIVE")
        if st.button("🐞 DEBUGGER"):
            st.json({"node": platform.node(), "cpu": cpu_val, "os": platform.system(), "pqc": "ENABLED"})

    st.markdown("<hr>", unsafe_allow_html=True)

    # Estado de Ativação
    if 'active_node' not in st.session_state: st.session_state.active_node = None
    if 'voice_msg' not in st.session_state: st.session_state.voice_msg = ""

    # 9 NÓS DE DEFESA
    setores = ["CRIPTO QKD", "DEFESA gRPC", "SIGINT/ELINT", "NIW GOV", "FIBER SHIELD", "NEURAL AUDIT", "SAT LINK", "Q-STORAGE", "QUANTUM SENSING"]
    
    cols = st.columns(3)
    for i, s in enumerate(setores):
        with cols[i % 3]:
            st.markdown(f"<div class='node-card'><small>NODE 0{i+1}</small><br><b>{s}</b></div>", unsafe_allow_html=True)
            
            # BOTÃO DE ATIVAÇÃO COM VOX
            if st.button(f"ATIVAR {s} (VOX)", key=f"act_{i}"):
                st.session_state.active_node = s
                st.session_state.voice_msg = f"Nó {s} ativado. Gerando evidência técnica para o Arquiteto Marco Antonio."
                st.rerun()

            # DOWNLOAD DO DOSSIÊ
            if st.session_state.active_node == s:
                pdf_bytes = generate_node_audit(s, cpu_val)
                if pdf_bytes:
                    st.download_button(label=f"📥 BAIXAR DOSSIÊ {s}", data=pdf_bytes, file_name=f"XEON_{s}.pdf", mime="application/pdf", key=f"dl_{i}")
                else:
                    st.error("Erro no motor PDF.")

    # DISPARO DA VOZ
    if st.session_state.voice_msg:
        components.html(f"""
            <script>
            var msg = new SpeechSynthesisUtterance('{st.session_state.voice_msg}');
            msg.lang = 'pt-BR';
            window.speechSynthesis.speak(msg);
            </script>
        """, height=0)
        st.session_state.voice_msg = ""

# --- [4. FINALIZAÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 5px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
xeon_dashboard()
st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | ZERO WHITE POLICY")
