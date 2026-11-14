import streamlit as st
from src.config import KIND_LABELS
from src.services.presentation import filter_period


def period_filters(frame):
    if frame.empty:
        st.info("A fonte conectada não forneceu registros meteorológicos.")
        return frame.copy()
    with st.sidebar:
        st.divider()
        st.markdown("**Recorte dos dados**")
        dates = st.date_input(
            "Período de análise", value=(frame.timestamp.min().date(), frame.timestamp.max().date()),
            min_value=frame.timestamp.min().date(), max_value=frame.timestamp.max().date(),
            format="DD/MM/YYYY",
        )
        kinds = st.multiselect("Natureza dos dados", list(KIND_LABELS),
                               default=list(KIND_LABELS), format_func=KIND_LABELS.get)
        st.caption("Histórico e previsão são identificados pela fonte. O sistema não produz previsão meteorológica.")
    if len(dates) != 2:
        st.info("Selecione o início e o fim do período para visualizar os dados.")
        return frame.iloc[0:0].copy()
    return filter_period(frame, dates[0], dates[1], kinds)
