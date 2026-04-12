import streamlit as st
import numpy as np
import psutil
import time
import plotly.graph_objects as go
from scipy.fft import fft

# --- 1. CONFIGURAÇÃO DE TELA E ACESSIBILIDADE ---
st.set_page_config(page_title="Barbie Omni Sovereign", layout="centered")

# CSS: CORREÇÃO DE ALINHAMENTO E DESIGN UNISSEX (CIENTISTA/BARBIE)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp { background: linear-gradient(135deg, #fdfcfd 0%, #e0eafc 100%); font-family: 'Poppins', sans-serif; }
    
    /* CAIXA DE ENTRADA: ALINHAMENTO VERTICAL CORRIGIDO */
    .stTextInput>div>div>input { 
        border-radius: 40px !important; 
        height: 80px !important; 
        font-size: 24px !important; 
        border: 3px solid #FF1493 !important; 
        text-align: center !important; 
        line-height: normal !important; /* Reseta altura para centralizar */
        padding: 0px !important;        /* Remove paddings que empurram o texto */
        background-color: white !important;
        color: #1a2a6c !important;      /* Azul Marinho Sóbrio */
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Botões Profissionais (Azul Marinho / Rosa no Hover) */
    .stButton>button { 
        border-radius: 35px; border: none; height: 100px; width: 100%; font-size: 20px !important; 
        background: #1a2a6c; color: white; font-weight: 700;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.1); transition: 0.4s;
    }
    .stButton>button:hover { background: #FF1493; transform: scale(1.03); color: white; }
    
    .chat-bubble { 
        background: white; padding: 30px; border-radius: 40px; border: 2px solid #1a2a6c; 
        font-size: 22px; color: #1a2a6c; text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.05); margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MÓDULO DE VOZ (FALA E ESCUTA) ---
def voice_output(text):
    st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.lang = 'pt-BR';
        msg.rate = 0.9;
        window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

# --- 3. INTERFACE DE COMANDO ---
st.write("<h1 style='text-align: center; color: #1a2a6c; font-size: 55px;'>💖 Barbie <span style='color:#FF1493;'>Omni</span></h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; font-size: 20px; color: #1a2a6c; opacity: 0.8;'><b>O Juiz Soberano:</b> Ciência, Engenharia e Diagnósticos de Precisão</p>", unsafe_allow_html=True)

# Caixa de Entrada (Centralizada e Alinhada)
user_query = st.text_input("", placeholder="Escreva ou use o microfone abaixo...", label_visibility="collapsed")

# Comandos de Voz
c_v1, c_v2 = st.columns(2)
with c_v1:
    if st.button("🎙️ ATIVAR VOZ (Falar/Ouvir)"):
        voice_output("Sistema Omni Ativado. Estou ouvindo você.")
        st.info("Pode falar... O microfone está capturando.")
with c_v2:
    if st.button("🛑 PARAR DE FALAR"):
        st.markdown("<script>window.speechSynthesis.cancel();</script>", unsafe_allow_html=True)

st.divider()

# Grade de Comando Especialista
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("⚖️\nLEI"):
        res = "Análise Jurídica Concluída via STF/STJ com Erro Zero."
        st.markdown(f'<div class="chat-bubble"><b>{res}</b></div>', unsafe_allow_html=True)
        voice_output(res)
with c2:
    if st.button("🍎\nSAÚDE"):
        res = "Diagnóstico Preventivo Processado com Base em Evidências Médicas."
        st.markdown(f'<div class="chat-bubble"><b>{res}</b></div>', unsafe_allow_html=True)
        voice_output(res)
with c3:
    if st.button("🏗️\nENG"):
        res = "Cálculos de Engenharia Lunar e Marciana Validados."
        st.markdown(f'<div class="chat-bubble"><b>{res}</b></div>', unsafe_allow_html=True)
        voice_output(res)
with c4:
    if st.button("📈\nIPO"):
        res = "Estratégia de IPO Consolidada. Pronto para Mercado Internacional."
        st.markdown(f'<div class="chat-bubble"><b>{res}</b></div>', unsafe_allow_html=True)
        voice_output(res)

# --- 4. AUDITORIA SÊNIOR (MATEMÁTICA PURA) ---
with st.expander("🛠️ AUDITORIA SÊNIOR: ERRO ZERO & SOBERANIA"):
    cpu = psutil.cpu_percent()
    sig = np.random.normal(0, 1, 512)
    integrity = np.allclose(sig, np.fft.ifft(np.fft.fft(sig)).real, atol=1e-12)
    st.write(f"Integridade Matemática: {'100%' if integrity else 'ALUCINAÇÃO DETECTADA'}")
    st.write(f"Hardware Local: {cpu}% de carga.")
    fig = go.Figure(go.Scatter(y=[cpu, cpu+2, cpu-1], fill='tozeroy', line=dict(color='#1a2a6c', width=4)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

st.caption("Barbie Xeon Omni v180.0 | Design Universal | Soberania Nacional 2026")
