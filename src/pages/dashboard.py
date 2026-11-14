import pandas as pd
import streamlit as st
from src.components.layout import weather_metrics, status
from src.components.charts import weather_chart


def render(frame, is_demo):
    latest = frame.iloc[-1]
    st.subheader("O clima no período selecionado")
    st.caption(f"Último registro do recorte: {latest.timestamp:%d/%m/%Y às %H:%M} · Não representa atualização automática")
    weather_metrics(latest)
    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.subheader("Evolução da temperatura")
        if frame.temperature_c.notna().sum() < 2:
            st.info("São necessários ao menos dois valores para analisar a evolução temporal.")
        else:
            st.plotly_chart(weather_chart(frame, "temperature_c"), width="stretch")
    with right:
        st.subheader("Condição exibida")
        status(latest.classification, " · resultado fictício" if is_demo else " · resultado externo")
        st.write(latest.justification)
        st.caption("Origem: " + latest.classification_origin)
        if pd.notna(latest.confidence):
            st.write(f"Confiança fornecida pelo modelo: {latest.confidence:.1%}")
        st.info("Resultado demonstrativo. A classificação apresentada não constitui uma recomendação agronômica.") if is_demo else None
    st.subheader("Resumo do recorte")
    a, b, c, d = st.columns(4)
    a.metric("Registros selecionados", len(frame))
    b.metric("Temperatura média", "Sem dado" if frame.temperature_c.isna().all() else f"{frame.temperature_c.mean():.1f} °C")
    c.metric("Umidade média", "Sem dado" if frame.humidity_pct.isna().all() else f"{frame.humidity_pct.mean():.1f}%")
    d.metric("Rótulos favoráveis" if is_demo else "Resultados favoráveis", int((frame.classification == "Favorável").sum()))
    st.caption("Médias calculadas somente com valores disponíveis. Precipitação não é somada: a semântica do intervalo depende da fonte.")
