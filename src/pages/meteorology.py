import streamlit as st
from src.config import WEATHER_FIELDS
from src.components.charts import weather_chart


def render(frame, is_demo):
    st.subheader("Evolução meteorológica")
    st.write("Explore os registros com o cursor, amplie um intervalo e consulte cada variável. Os filtros da barra lateral atualizam todos os gráficos.")
    items = list(WEATHER_FIELDS.items())
    for start in range(0, len(items), 2):
        for column, (field, (label, unit)) in zip(st.columns(2), items[start:start+2]):
            with column:
                st.markdown(f"#### {label} · {unit}")
                if frame[field].notna().sum() < 2:
                    st.info("Dados insuficientes: menos de dois valores disponíveis nesta variável.")
                else:
                    st.plotly_chart(weather_chart(frame, field), width="stretch")
    st.caption("Lacunas não são preenchidas. Linhas mostram a sequência de observações, sem estimar valores entre medições. Pressão é apenas descritiva.")
