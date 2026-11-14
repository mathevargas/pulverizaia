import streamlit as st
from src.config import WEATHER_FIELDS, TIMEZONE


def setup():
    st.set_page_config(page_title="PulverizaIA · Painel meteorológico", page_icon="🌱", layout="wide")
    st.markdown("""<style>
      .block-container {max-width:1480px; padding-top:4.5rem; padding-bottom:2rem}
      h1 {letter-spacing:-1.3px; font-weight:750!important}
      h2 {letter-spacing:-.5px}
      div[data-testid="stMetric"] {background:#fff;border:1px solid #dce5da;
         border-radius:14px;padding:16px;min-height:120px}
      div[data-testid="stMetricLabel"] {color:#45604d}
      div[data-testid="stMetricValue"] {font-size:clamp(1.15rem,1.6vw,1.55rem)}
      div[data-testid="stMetricLabel"] p {white-space:normal;overflow:visible}
      [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]) {flex-wrap:wrap}
      [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"] [data-testid="stMetric"]) > [data-testid="stColumn"] {min-width:min(100%,145px);flex:1 1 145px!important}
      [data-testid="stSidebar"] {border-right:1px solid #dce5da}
      [data-testid="stSidebar"] h2 {color:#187552}
      .eyebrow {font-size:.78rem;letter-spacing:.16em;font-weight:700;color:#53705d;margin-bottom:.6rem}
      .intro {color:#526456;font-size:1.05rem;margin-top:-.6rem;margin-bottom:1.5rem}
      @media(max-width:1100px) {
        [data-testid="stHorizontalBlock"] {flex-wrap:wrap}
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {min-width:min(100%,260px);flex:1 1 260px!important}
      }
      @media(max-width:700px) {.block-container{padding-top:4rem}h1{font-size:2rem!important}}
    </style>""", unsafe_allow_html=True)


def brand():
    st.sidebar.markdown("## 🌱 PulverizaIA")
    st.sidebar.caption("DADOS DO CLIMA, VISÃO DO CAMPO")
    st.sidebar.divider()


def title(heading, description):
    st.markdown('<div class="eyebrow">PULVERIZAIA / PAINEL METEOROLÓGICO</div>', unsafe_allow_html=True)
    st.title(heading)
    # Textos fixos da aplicação; conteúdo dos adaptadores nunca é HTML.
    st.caption(description)


def provenance(data):
    if data.is_demo:
        st.warning("MODO DEMONSTRAÇÃO — DADOS SIMULADOS")
        st.caption("Dados e classificações simulados para demonstração. Os resultados não constituem recomendações de aplicação.")
    else:
        st.info("DADOS INTEGRADOS — origem fornecida pelo adaptador. Resultados externos dependem da validação dos responsáveis.")
    for notice in data.notices:
        st.warning(notice)
    sources = ", ".join(sorted(set(data.frame.source))) if not data.frame.empty else "Sem registros"
    st.caption(f"Fonte: {sources} · Fuso de exibição: {TIMEZONE} · {len(data.frame)} registros disponíveis")


def weather_metrics(row):
    import pandas as pd
    for column, (field, (label, unit)) in zip(st.columns(5), WEATHER_FIELDS.items()):
        value = row[field]
        column.metric(label, "Sem dado" if pd.isna(value) else f"{value:.1f} {unit}")


def status(label, text):
    if label == "Favorável":
        st.success("● Favorável" + text)
    elif label == "Desfavorável":
        st.error("● Desfavorável" + text)
    elif label == "Dados insuficientes":
        st.warning("● Dados insuficientes" + text)
    else:
        st.info("Classificação não fornecida" + text)


def footer():
    st.divider()
    st.caption("PulverizaIA · Inteligência meteorológica para o campo · Lajeado/RS")
