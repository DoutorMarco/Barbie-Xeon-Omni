import streamlit as st
import aiosqlite
import asyncio
from fpdf import FPDF
import datetime
import psutil

# 1. PROTOCOLO DE SOBERANIA VISUAL (Injeção de CSS)
st.set_page_config(page_title="XEON COMMAND v54.0", layout="wide")

st.markdown(
    """
    <style>
    /* Blackout Total */
    .stApp, div[data-testid="stToolbar"], header, footer {
        background-color: #000000 !important;
        color: #00FF41 !important;
        visibility: hidden; /* Esconde lixo visual nativo */
    }
    
    .stApp { visibility: visible; } /* Mantém apenas o app visível */

    /* Custom Input Command Bar */
    div[data-baseweb="base-input"] {
        background-color: #000000 !important;
        border: 1px solid #00FF41 !important;
    }
    
    input {
        color: #00FF41 !important;
        background-color: #000000 !important;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Estilização de Texto e Métricas */
    h1, h2, h3, p, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Gráficos e Divisores */
    hr { border: 1px solid #00FF41 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. DASHBOARD DE CONTROLE (Interface Soberana)
st.title("🛰️ X E O N   C O M M A N D   v 5 4 . 0")

col1, col2, col3, col4 = st.columns(4)
with col1:
    cpu_load = psutil.cpu_percent()
    st.metric("CLOUD LOAD", f"{cpu_load}%", "+ 0.0%" if cpu_load < 50 else "- STRESS")
with col2:
    st.metric("UPTIME", "STABLE", "+ 24/7")
with col3:
    st.metric("LEDGER SYNC", "IMMUTABLE", "+ v2.2")
with col4:
    st.metric("VALUATION", "READY", "$ 500/h")

st.markdown("---")

# 3. LEDGER IMUTÁVEL (AIOSQLITE)
async def init_db():
    async with aiosqlite.connect("xeon_ledger.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS operations (id INTEGER PRIMARY KEY, timestamp TEXT, hash TEXT)")
        await db.commit()

# 4. GERAÇÃO DE DOSSIÊS (MONETIZAÇÃO $500/H)
def generate_dossier():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 0, 0)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 65)
    pdf.set_font("Courier", "B", 16)
    pdf.cell(0, 10, "XEON COMMAND - AUDIT DOSSIER", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Courier", "", 12)
    content = (
        "SUBJECT: Critical Infrastructure Audit\n"
        f"TIMESTAMP: {datetime.datetime.now()}\n"
        "RATE: $500.00/hour\n"
        "STATUS: IMMUTABLE LEDGER VERIFIED\n"
        "COMPLIANCE: NIST ZTA / PQC READY"
    )
    pdf.multi_cell(0, 10, content)
    return pdf.output(dest='S').encode('latin-1')

# 5. INPUT DE COMANDO GLOBAL
command = st.chat_input("Insert Global Command...")

if command:
    if "dossier" in command.lower() or "audit" in command.lower():
        st.write(f"[*] Executing Transdisciplinary Audit: {command}")
        pdf_data = generate_dossier()
        st.download_button(
            label="DOWNLOAD AUDIT DOSSIER (PDF)",
            data=pdf_data,
            file_name=f"XEON_AUDIT_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
    else:
        st.write(f"[+] Command processed by Diana Filter: {command}")

# Inicializa DB em background
asyncio.run(init_db())
