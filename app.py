"""Entrada do Streamlit. Executar: python -m streamlit run app.py."""
import logging
import streamlit as st

from src.components import layout
from src.components.filters import period_filters
from src.integrations.interfaces import IntegrationUnavailable
from src.models.contracts import ContractError
from src.pages import dashboard, meteorology, conditions, hourly, import_data, about
from src.services.runtime import build_application

layout.setup()
layout.brand()
PAGES = {
    "Dashboard": ("Visão do campo", dashboard.render),
    "Análise meteorológica": ("Análise meteorológica", meteorology.render),
    "Condições para pulverização": ("Condições para pulverização", conditions.render),
    "Análise por horários": ("Análise por horários", hourly.render),
    "Importar dados meteorológicos": ("Inspecione seu arquivo", None),
    "Sobre o projeto": ("Sobre o projeto", None),
}
page = st.sidebar.radio("Navegação", list(PAGES))
mode = st.sidebar.selectbox("Fonte de dados", ["Demonstração", "Integração real (pendente)"])
st.sidebar.caption("Lajeado / RS · Monitoramento meteorológico")
heading, renderer = PAGES[page]
layout.title(heading, "Inteligência meteorológica para pulverização agrícola")

if page == "Importar dados meteorológicos":
    import_data.render()
elif page == "Sobre o projeto":
    about.render()
else:
    try:
        data = build_application("demo" if mode == "Demonstração" else "real")
        layout.provenance(data)
        frame = period_filters(data.frame)
        if frame.empty:
            st.info("Nenhum registro no recorte selecionado. Ajuste o período ou a natureza dos dados.")
        else:
            st.caption(f"{len(frame)} registros selecionados · {frame.timestamp.min():%d/%m/%Y %H:%M} a {frame.timestamp.max():%d/%m/%Y %H:%M}")
            renderer(frame, data.is_demo)
    except (IntegrationUnavailable, ContractError, ValueError) as exc:
        st.error(str(exc))
        st.info("Selecione Demonstração para explorar a aplicação. Instruções para integrar as fontes: docs/INTEGRACAO.md.")
    except Exception:
        logging.exception("Falha inesperada ao apresentar os dados")
        st.error("Não foi possível exibir os dados. Consulte o terminal e verifique o adaptador conectado.")
layout.footer()
