import plotly.express as px
from src.config import WEATHER_FIELDS, KIND_LABELS
from src.services.presentation import chart_frame


def weather_chart(frame, field):
    label, unit = WEATHER_FIELDS[field]
    data = chart_frame(frame, field)
    data["Natureza"] = data.data_kind.map(KIND_LABELS)
    factory = px.bar if field == "precipitation_mm" else px.line
    options = {"barmode": "group"} if field == "precipitation_mm" else {"markers": True, "line_group": "source"}
    fig = factory(
        data, x="timestamp", y=field, color="Natureza",
        labels={"timestamp": "Data e horário · America/Sao_Paulo", field: f"{label} ({unit})", "source": "Fonte"},
        color_discrete_map={"Histórico observado": "#187552", "Previsão da fonte": "#b16a13"},
        hover_data=["source"], **options,
    )
    if factory == px.line:
        fig.update_traces(connectgaps=False)
    fig.update_layout(height=340, margin=dict(l=10, r=15, t=20, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      legend_title_text="", hovermode="closest", font_color="#20392d")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e0e8df")
    return fig
