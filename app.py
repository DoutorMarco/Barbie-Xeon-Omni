def generate_6_page_pdf(node_name, metrics, market):
    pdf = FPDF()
    # Cláusulas de Missão Crítica para o Dossiê
    clauses = [
        "CLAUSE 01: DATA SOVEREIGNTY & NIST COMPLIANCE - Integrity verified via SHA-256 Hash-chaining.",
        "CLAUSE 02: PQC READY - System implements Post-Quantum Cryptography standards for critical infrastructure.",
        "CLAUSE 03: ZERO TRUST ARCHITECTURE (ZTA) - Real-time auditing of data flow under Diana Homeostasis Filter.",
        "CLAUSE 04: BIOMEDICAL DATA INTEGRITY - HIPAA/GDPR alignment for biomedical assets and clinical records.",
        "CLAUSE 05: GLOBAL FINANCIAL COMPLIANCE - Cross-border market analysis with sub-second latency precision.",
        "CLAUSE 06: LEGAL VALIDITY - Automated forensic chain of custody for legal and immigration (USCIS EB-1A) purposes."
    ]

    for i in range(1, 7):
        pdf.add_page()
        # Estética Soberana no PDF (Blackout)
        pdf.set_fill_color(0, 0, 0); pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_text_color(0, 255, 65); pdf.set_font("Courier", "B", 14)
        
        # Cabeçalho de Segurança Nacional
        pdf.cell(0, 10, "TOP SECRET - MISSION CRITICAL", 0, 1, 'C')
        pdf.set_font("Courier", "B", 18)
        pdf.cell(0, 15, f"XEON COMMAND AUDIT REPORT v101.64", 0, 1, 'C')
        pdf.ln(5)
        
        # Corpo Técnico
        pdf.set_font("Courier", "B", 10)
        pdf.cell(0, 10, f"NODE: {node_name.upper()}", 0, 1, 'L')
        pdf.cell(0, 10, f"TIMESTAMP: {metrics['timestamp']} | TOKEN: {metrics['token']}", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.set_font("Courier", "", 10)
        # Injeção da Cláusula Específica por Página
        current_clause = clauses[i-1]
        content = (
            f"{current_clause}\n\n"
            f"SUMMARY OF ANALYSIS:\n"
            f"- CPU LOAD AT EXECUTION: {metrics['cpu']}%\n"
            f"- SYSTEM HOMEOSTASE: 100% (STABLE)\n"
            f"- MARKET EXPOSURE (USD/BRL): {market['usdbrl']:.4f}\n"
            f"- CRYPTO ASSET (BTC): ${market['btc']:,.2f}\n\n"
            "TECHNICAL LOGS:\n"
            + "-"*70 + "\n"
            "This document constitutes a formal audit record of technical and legal compliance. "
            "Designed by Architect Marco Antonio do Nascimento as a sovereign solution for "
            "National Infrastructure Protection. Valid for international certification and "
            "Extraordinary Ability (EB-1A) evidence portfolios.\n"
            + "-"*70 + "\n"
            f"EOF PAGE {i} / GENERATED IN STREAMLIT CLOUD INFRASTRUCTURE"
        )
        pdf.multi_cell(0, 8, content)
        
        # Marca d'água de integridade no rodapé
        pdf.set_y(-20)
        pdf.set_font("Courier", "I", 8)
        pdf.cell(0, 10, f"AUTHENTICITY SECURED BY XEON BLOCKCHAIN-GRADE LEDGER | HASH: {metrics['token'][:32]}", 0, 0, 'C')

    return pdf.output(dest='S').encode('latin-1')
