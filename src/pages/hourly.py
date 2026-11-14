import streamlit as st
from src.config import WEATHER_FIELDS, KIND_LABELS


def render(frame, is_demo):
    st.subheader("Cada horário, com seu contexto")
    st.caption("Histórico observado é retrospectivo. Previsão significa dado futuro fornecido por uma fonte meteorológica, não previsão produzida pela aplicação.")
    choices = list(dict.fromkeys(frame.classification))
    classes = st.multiselect("Classificações exibidas", choices, default=choices)
    a, b = st.columns([2, 1])
    sort = a.selectbox("Ordenar por", ["timestamp", *WEATHER_FIELDS, "classification"],
                       format_func=lambda x: "Data e horário" if x == "timestamp" else "Classificação" if x == "classification" else WEATHER_FIELDS[x][0])
    ascending = b.selectbox("Ordem", ["Crescente", "Decrescente"]) == "Crescente"
    selected = frame[frame.classification.isin(classes)].sort_values(sort, ascending=ascending, na_position="last")
    if selected.empty:
        st.info("Nenhum horário atende aos filtros de classificação selecionados.")
        return
    table = selected.copy()
    table.insert(0, "Data", table.timestamp.dt.strftime("%d/%m/%Y"))
    table.insert(1, "Horário", table.timestamp.dt.strftime("%H:%M"))
    table["data_kind"] = table.data_kind.map(KIND_LABELS)
    table = table.drop(columns=["timestamp"]).rename(columns={
        **{key: f"{label} ({unit})" for key,(label,unit) in WEATHER_FIELDS.items()},
        "source": "Fonte", "data_kind": "Natureza", "classification": "Classificação",
        "justification": "Justificativa", "limiting_factors": "Fatores limitantes",
        "classification_origin": "Origem do resultado", "confidence": "Confiança fornecida",
    })
    if table["Confiança fornecida"].isna().all():
        table = table.drop(columns="Confiança fornecida")
    st.caption(f"{len(table)} horários · Clique também nos cabeçalhos para ordenar. Valores ausentes aparecem vazios.")
    st.dataframe(table, hide_index=True, width="stretch")
    st.caption("Um registro não comprova condições contínuas até o horário seguinte. Não há geração de horários futuros.")
