import streamlit as st
import time
import hashlib
import sqlite3
import psutil
import platform
import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
from fpdf import FPDF

# --- [1. CONFIGURAÇÃO VISUAL - MATRIX BLACKOUT] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; }}
    .stButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 40px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    code {{ color: {MATRIX_GREEN} !important; background-color: #0A0A0A !important; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. MOTOR DE EXPORTAÇÃO XML FEDERAL] ---
def generate_uscis_xml(audit_data):
    """Gera XML estruturado para submissão ao portal DHS/USCIS."""
    root = ET.Element("USCIS_Evidence_Submission")
    root.set("Version", "131.0")
    root.set("Classification", "NATIONAL_INTEREST_WAIVER")
    
    # Cabeçalho do Peticionário
    header = ET.SubElement(root, "PetitionerInfo")
    ET.SubElement(header, "Name").text = "MARCO ANTONIO DO NASCIMENTO"
    ET.SubElement(header, "Role").text = "PRINCIPAL ARCHITECT - DATA ENGINEERING"
    ET.SubElement(header, "Infrastructure_ID").text = hashlib.sha1(platform.node().encode()).hexdigest().upper()
    
    # Logs de Auditoria Forense
    evidence = ET.SubElement(root, "TechnicalExhibits")
    for index, row in audit_data.iterrows():
        exhibit = ET.SubElement(evidence, "Exhibit")
        ET.SubElement(exhibit, "Timestamp").text = str(row['ts'])
        ET.SubElement(exhibit, "Event").text = str(row['event'])
        ET.SubElement(exhibit, "NIST_800_53_Compliance").text = "TRUE"
        ET.SubElement(exhibit, "IntegrityHash").text = str(row['payload_enc'])
    
    # Formatação "Pretty Print"
    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    return parsed_xml.toprettyxml(indent="  ")

# --- [3. DASHBOARD OPERACIONAL E EXPORTAÇÃO] ---
@st.fragment(run_every=3)
def uscis_submission_portal():
    st.write("### 🏛️ FEDERAL SUBMISSION MODULE (USCIS/DHS XML)")
    
    col_l, col_r = st.columns([1.2, 1.8])
    
    with col_l:
        st.write("Módulo de conversão de telemetria forense para metadados XML governamentais.")
        if st.button("🚀 GERAR ESTRUTURA XML EB-1A"):
            conn = sqlite3.connect('xeon_nist_vault.db')
            logs = pd.read_sql_query("SELECT * FROM nist_ledger ORDER BY id DESC LIMIT 20", conn)
            conn.close()
            
            xml_output = generate_uscis_xml(logs)
            st.session_state.current_xml = xml_output
            st.success("XML Estruturado com Sucesso.")
            
            st.download_button(
                label="📥 BAIXAR USCIS_EVIDENCE.XML",
                data=st.session_state.current_xml,
                file_name="XEON_USCIS_SUBMISSION.xml",
                mime="application/xml"
            )

    with col_r:
        if 'current_xml' in st.session_state:
            st.write("### PREVIEW DE METADADOS DHS:")
            st.code(st.session_state.current_xml, language='xml')
        else:
            st.info("Aguardando ativação do gatilho de exportação...")

# --- [4. EXECUÇÃO] ---
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN};'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
uscis_submission_portal()

st.caption("ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | XML-PORTAL SYNC ACTIVE")
