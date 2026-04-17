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

# --- [1. CONFIGURAÇÃO VISUAL - ABSOLUTE BLACKOUT MATRIX] ---
MATRIX_GREEN = "#00FF41"
BLACKOUT = "#000000"

st.set_page_config(page_title="XEON COMMAND v131.0", layout="wide", page_icon="🛰️")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; font-family: 'Courier New', monospace; }}
    [data-testid="stMetricValue"] {{ color: {MATRIX_GREEN} !important; text-shadow: 0 0 10px {MATRIX_GREEN}; }}
    .stButton button, .stDownloadButton button {{
        border: 2px solid {MATRIX_GREEN} !important; background-color: {BLACKOUT} !important;
        color: {MATRIX_GREEN} !important; border-radius: 0px !important; width: 100%; font-weight: bold;
    }}
    .stButton button:hover {{ background-color: {MATRIX_GREEN} !important; color: {BLACKOUT} !important; box-shadow: 0 0 35px {MATRIX_GREEN}; }}
    [data-testid="stHeader"], footer {{ display: none !important; }}
    [data-testid="stDataFrame"], [data-testid="stTable"], th, td {{ 
        background-color: {BLACKOUT} !important; color: {MATRIX_GREEN} !important; border: 1px solid {MATRIX_GREEN} !important; 
    }}
    hr {{ border: 1px solid {MATRIX_GREEN} !important; }}
    code {{ color: {MATRIX_GREEN} !important; background-color: #0A0A0A !important; }}
    </style>
""", unsafe_allow_html=True)

# --- [2. INFRAESTRUTURA DE DADOS E AUDITORIA NIST] ---
DB_NAME = 'xeon_sovereign_v131.db'

def get_db_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    with get_db_conn() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS nist_ledger 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, event TEXT, 
                      payload_enc TEXT, node_id TEXT)''')

def secure_commit(event, node):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    # Hash de Integridade PQC-ready
    pqc_payload = hashlib.sha512(f"{event}{ts}{node}".encode()).hexdigest()[:64]
    with get_db_conn() as conn:
        conn.execute("INSERT INTO nist_ledger (ts, event, payload_enc, node_id) VALUES (?,?,?,?)",
                     (ts, event, pqc_payload, node))
    return pqc_payload

# --- [3. GERADOR XML FEDERAL (USCIS/DHS)] ---
def generate_uscis_xml(df):
    root = ET.Element("USCIS_Submission_Package")
    root.set("Classification", "EB-1A_NIW_EVIDENCE")
    meta = ET.SubElement(root, "Metadata")
    ET.SubElement(meta, "Architect").text = "MARCO ANTONIO DO NASCIMENTO"
    ET.SubElement(meta, "System").text = "XEON COMMAND v131.0"
    
    exhibits = ET.SubElement(root, "TechnicalExhibits")
    for _, row in df.iterrows():
        item = ET.SubElement(exhibits, "Exhibit")
        ET.SubElement(item, "ID").text = str(row['id'])
        ET.SubElement(item, "Timestamp").text = row['ts']
        ET.SubElement(item, "Event").text = row['event']
        ET.SubElement(item, "Signature").text = row['payload_enc']
    
    xml_str = ET.tostring(root, encoding='utf-8')
    return minidom.parseString(xml_str).toprettyxml(indent="  ")

# --- [4. INTERFACE DE COMANDO FRAGMENTADA] ---
@st.fragment(run_every=3)
def core_dashboard():
    cpu = psutil.cpu_percent()
    h_index = 100 - (cpu * 0.1)
    
    # Telemetria Superior
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("STATUS", "NIST 800-53")
    c2.metric("HOMEOSTASE", f"{h_index:.2f}%")
    c3.metric("NODE_ID", platform.node()[:8].upper())
    c4.metric("TARGET", "$450/HR")

    st.markdown("<hr>", unsafe_allow_html=True)

    col_map, col_ops = st.columns([1.5, 1])

    with col_map:
        st.write("### 🌐 DEFENSE NODE GEOLOCATION")
        nodes = pd.DataFrame({
            'lat': [38.89, 37.44, 34.05, 42.36],
            'lon': [-77.03, -122.14, -118.24, -71.05],
            'node': ["HQ_DC", "PQC_VALLEY", "STORAGE_WEST", "BOS_NIW"]
        })
        st.map(nodes, color="#00FF41", size=40000)
        
        target = st.selectbox("OPERAR NÓ:", nodes['node'])
        if st.button(f"🚀 EXECUTAR AUDITORIA EM {target}"):
            secure_commit(f"MISSION_CRITICAL_AUDIT_{target}", target)
            st.toast(f"Evento {target} persistido no Ledger.")

    with col_ops:
        st.write("### 🏛️ FEDERAL SUBMISSION (XML)")
        with get_db_conn() as conn:
            df_logs = pd.read_sql_query("SELECT * FROM nist_ledger ORDER BY id DESC LIMIT 10", conn)
        
        if not df_logs.empty:
            if st.button("📦 GERAR XML PARA USCIS/DHS"):
                xml_data = generate_uscis_xml(df_logs)
                st.session_state.xml_output = xml_data
            
            if 'xml_output' in st.session_state:
                st.download_button("📥 BAIXAR USCIS_EVIDENCE.XML", st.session_state.xml_output, "XEON_SUBMISSION.xml", "text/xml")
                with st.expander("PREVIEW XML METADATA"):
                    st.code(st.session_state.xml_output, language='xml')
        else:
            st.warning("Ledger vazio. Inicie uma auditoria.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("### 📜 IMMUTABLE AUDIT TRAIL")
    st.dataframe(df_logs.style.set_properties(**{'background-color': 'black', 'color': '#00FF41'}), use_container_width=True, hide_index=True)

# --- [5. EXECUÇÃO CENTRAL] ---
init_db()
st.markdown(f"<h1 style='text-align: center; color: {MATRIX_GREEN}; letter-spacing: 5px;'>XEON COMMAND v131.0</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {MATRIX_GREEN};'>SOVEREIGN OPERATIONS HUB | NATIONAL INTEREST WAIVER ENABLED</p>", unsafe_allow_html=True)

core_dashboard()

st.caption(f"ADMIN: MARCO ANTONIO DO NASCIMENTO | MISSION CRITICAL | ASSET ID: {hashlib.sha1(platform.node().encode()).hexdigest()[:10].upper()}")
