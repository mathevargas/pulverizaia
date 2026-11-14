import streamlit as st


def render():
    st.subheader("Tecnologia para compreender as condições do campo")
    st.write("**PulverizaIA — Previsão de Condições Ideais para Pulverização Agrícola**")
    st.write("O objetivo é oferecer uma interface de apoio à análise meteorológica para a pulverização agrícola, reunindo dados e resultados em uma experiência acessível à comunidade.")
    a,b = st.columns(2)
    with a:
        st.markdown("#### Contexto acadêmico")
        st.write("**Instituição:** Universidade do Vale do Taquari — Univates")
        st.write("**Disciplina:** Ciência de Dados")
        st.write("**Professor:** Evandro Franzen")
        st.write("**Território:** Lajeado — Rio Grande do Sul")
        st.write("**Área de aplicação:** Pulverização agrícola")
    with b:
        st.markdown("#### Finalidade extensionista")
        st.write("Aproximar a Ciência de Dados da comunidade agrícola por meio de informações meteorológicas organizadas e acessíveis.")
        st.write("Vento, temperatura, umidade e chuva são relevantes no contexto de deriva, evaporação e eficiência de aplicação. O protótipo não avalia cientificamente esses riscos.")
    st.markdown("#### Metodologia")
    st.write("O projeto adota a metodologia CRISP-DM para organizar a compreensão do problema, a análise dos dados e a evolução da solução.")
    st.markdown("#### Tecnologias")
    st.write("Python · Streamlit · Pandas · Plotly. Aplicação local com acesso pelo navegador.")
    st.warning("Versão demonstrativa com dados e classificações simulados. A integração de dados reais e de modelos validados está em desenvolvimento. O upload permite inspecionar arquivos JSON, sem incorporá-los ao painel.")
