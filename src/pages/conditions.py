import pandas as pd
import streamlit as st
from src.config import CLASSES
from src.components.layout import weather_metrics, status


def render(frame, is_demo):
    st.subheader("Condições para pulverização")
    if is_demo:
        st.info("Classificações demonstrativas, sem modelo conectado. Os resultados são simulados e não representam uma avaliação agronômica.")
    cols = st.columns(3)
    for col, label in zip(cols, CLASSES):
        col.metric(label, int((frame.classification == label).sum()))
    st.divider()
    selected = st.selectbox("Consultar registro", list(frame.index),
                            format_func=lambda i: frame.loc[i, "timestamp"].strftime("%d/%m/%Y · %H:%M"))
    row = frame.loc[selected]
    status(row.classification, " · demonstração" if is_demo else " · modelo externo")
    st.caption(f"{row.timestamp:%d/%m/%Y às %H:%M} · Origem do resultado: {row.classification_origin}")
    weather_metrics(row)
    a, b = st.columns(2)
    with a:
        st.markdown("#### Justificativas fornecidas")
        st.write(row.justification)
    with b:
        st.markdown("#### Fatores limitantes fornecidos")
        st.write(row.limiting_factors)
    if pd.notna(row.confidence):
        st.write(f"Confiança informada pelo modelo: {row.confidence:.1%}")
    else:
        st.caption("Confiança/probabilidade não fornecida. Nenhum valor foi estimado pela interface.")
    st.warning("Resultados exibidos não substituem orientação agronômica, recomendações do fabricante ou avaliação das condições locais.")
