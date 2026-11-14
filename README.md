# 🌱 PulverizaIA

**Inteligência meteorológica para pulverização agrícola**

Aplicação web local para visualizar informações meteorológicas e resultados de classificação, preparada para receber posteriormente o trabalho de integração dos colegas. Esta entrega cobre exclusivamente a **atividade 5 — desenvolvimento e testes da aplicação (protótipo)**.

Título acadêmico: **Previsão de Condições Ideais para Pulverização Agrícola**. Universidade do Vale do Taquari — Univates · Ciência de Dados · Professor Evandro Franzen · Lajeado/RS · Metodologia CRISP-DM · Entrega final 03/12/2026.

O projeto tem finalidade extensionista: demonstrar à comunidade agrícola ou empresa participante possibilidades de aplicação da Ciência de Dados. Temperatura, umidade, vento e chuva são informações relevantes nesse contexto. A versão atual não avalia cientificamente as condições de pulverização, não produz previsão meteorológica e não substitui orientação agronômica.

## O que está implementado

- Dashboard com cinco indicadores, último registro selecionado, fonte, datas, contagem e médias do recorte.
- Cinco gráficos Plotly com unidades, informações ao passar o cursor, zoom e filtros de datas/natureza.
- Página de condições com três classes fictícias, variáveis, justificativas, fatores limitantes e origem do resultado.
- Tabela por horários com filtros por classificação, ordenação por variável e distinção entre histórico e previsão da fonte.
- Upload JSON com nome, tamanho, validação de sintaxe e prévia limitada, sem integração automática.
- Modo demonstração identificado e reproduzível, com ausências e lacunas intencionais.
- Contratos internos validados, pontos de extensão para dados e classificadores externos e mensagens explícitas quando a integração está indisponível.
- Tratamento de erros, testes automatizados e documentação de integração.

## Instalar no Windows e VS Code

Abra a pasta `pulverizacao-inteligente` como workspace. A versão utilizada na verificação está registrada em [docs/RELATORIO_TECNICO.md](docs/RELATORIO_TECNICO.md). Utilize Python 3.14 para reproduzir o ambiente testado; outras versões não foram verificadas nesta entrega.

No terminal PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

`requirements.txt` fixa as bibliotecas diretas. Para reproduzir também as dependências transitivas do ambiente verificado, instale com `-r requirements-lock.txt`. A instalação inicial exige acesso ao índice de pacotes; depois dela a aplicação utiliza arquivos e recursos locais, sem APIs externas. Não é necessário ativar o ambiente para usar os comandos com o caminho completo do interpretador.

O VS Code está configurado para selecionar `.venv/Scripts/python.exe` e descobrir testes Pytest. Se necessário, escolha esse interpretador em **Python: Select Interpreter**.

## Executar

Dê dois cliques em `iniciar_windows.bat` ou execute:

```powershell
.venv\Scripts\python -m streamlit run app.py
```

Com o ambiente virtual já ativado, o comando principal também é:

```powershell
python -m streamlit run app.py
```

Acesse [http://127.0.0.1:8501](http://127.0.0.1:8501). O servidor é restrito ao computador local. Encerre pelo terminal com **Ctrl+C**. O inicializador usa caminhos relativos à sua própria pasta e suporta espaços no caminho.

Se a porta estiver ocupada, use `--server.port 8502` e acesse o endereço correspondente. Se faltar uma biblioteca, repita a instalação no interpretador `.venv`; não instale pacotes globalmente para resolver erros deste projeto.

## Usar a aplicação

1. Em **Dashboard**, observe o aviso **MODO DEMONSTRAÇÃO — DADOS SIMULADOS** e os cartões do último registro do recorte.
2. Escolha o período e a natureza dos dados na barra lateral. Indicadores, gráficos e tabelas reagem ao mesmo recorte.
3. Em **Análise meteorológica**, passe o cursor sobre os registros e use as ferramentas de zoom do gráfico. Ausências não são interpoladas. Menos de dois valores gera mensagem explicativa.
4. Em **Condições para pulverização**, selecione um horário e consulte o rótulo, justificativa e fatores fornecidos. Os rótulos da demonstração foram previamente escritos; não há algoritmo que os derive do clima.
5. Em **Análise por horários**, filtre classes e selecione variável/ordem. Também é possível ordenar clicando nos cabeçalhos da tabela.
6. Em **Importar dados meteorológicos**, selecione ou arraste um JSON UTF-8 de até 2 MB. A página informa sintaxe, nome, tamanho e estrutura raiz. A prévia limita profundidade, quantidade e tamanho de textos e é exibida como código, sem executar conteúdo.
7. Consulte **Sobre o projeto** para contexto e responsabilidades.

O seletor **Integração real (pendente)** demonstra a mensagem de adaptador indisponível. Ele não carrega dados reais nem muda silenciosamente para dados fictícios. Retorne a **Demonstração** para explorar os dados locais. As páginas de upload e informações continuam acessíveis.

### Como interpretar a demonstração

`data/demo/weather.json` contém 166 registros fictícios entre 01 e 07/11/2026. A estrutura corresponde a uma série horária com dois horários omitidos e alguns valores ausentes. Os arquivos são estáticos e reproduzíveis. Não há atualização em tempo real.

`data/demo/classifications.json` contém rótulos independentes dos valores meteorológicos, com exemplos de **Favorável**, **Desfavorável** e **Dados insuficientes**. Até o estado “Dados insuficientes” é uma fixture de interface, não uma avaliação calculada. Não existem limites agronômicos, probabilidades ou métricas fictícias. Nenhum modelo foi treinado ou conectado. Pressão é apenas exibida.

Médias ignoram valores ausentes. Precipitação é apresentada por registro, sem totalização automática: a semântica dos intervalos será responsabilidade do adaptador real. Uma linha entre observações não comprova condições contínuas. A aplicação não inventa horários futuros e não converte histórico em previsão. `data_kind` é fornecido explicitamente pela fonte.

O upload **não integra o JSON ao dashboard** e não limpa nem mapeia seus campos. A inspeção é sintática; um arquivo válido pode ser incompatível com o contrato. Nenhum upload é persistido no disco pelo software, mas o conteúdo permanece temporariamente na memória da sessão do Streamlit. Não use esta inspeção como processamento definitivo da empresa.

## Arquitetura

```text
pulverizacao-inteligente/
├── app.py
├── requirements.txt
├── requirements-lock.txt
├── iniciar_windows.bat
├── pytest.ini
├── .gitignore
├── .gitattributes
├── .streamlit/config.toml
├── .vscode/settings.json
├── src/
│   ├── __init__.py
│   ├── config/__init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── layout.py
│   │   ├── filters.py
│   │   └── charts.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── meteorology.py
│   │   ├── conditions.py
│   │   ├── hourly.py
│   │   ├── import_data.py
│   │   └── about.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── contracts.py
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── interfaces.py
│   │   └── pending.py
│   └── services/
│       ├── __init__.py
│       ├── demo.py
│       ├── presentation.py
│       ├── runtime.py
│       └── uploads.py
├── data/demo/
│   ├── weather.json
│   └── classifications.json
├── tests/
│   ├── conftest.py
│   ├── test_contracts.py
│   ├── test_demo_integration.py
│   ├── test_presentation.py
│   ├── test_uploads.py
│   └── test_ui.py
└── docs/
    ├── INTEGRACAO.md
    ├── RELATORIO_TECNICO.md
    └── screenshots/            Evidências da conferência no navegador
```

`.venv` e caches são locais e ignorados pelo Git. Um cache antigo bloqueado pelo Windows foi deixado intocado, conforme orientação do usuário; o Pytest usa outro diretório e não depende dele.

## Contratos e colaboração

Veja [docs/INTEGRACAO.md](docs/INTEGRACAO.md) para a descrição completa, exemplos sintéticos e pontos de extensão.

- `WeatherSource.load()` entrega `WeatherBatch` com registros `WeatherRecord` nas unidades internas.
- `ClassificationProvider.classify(batch)` entrega uma tupla de `ClassificationResult` com horários correspondentes.
- `services/runtime.py` conecta fornecedores à interface. O dashboard não lê o JSON original e não conhece o algoritmo.
- `integrations/pending.py` contém os dois pontos explicitamente indisponíveis nesta versão.

As dataclasses validam o contrato de software e rejeitam incompatibilidades. Não fazem limpeza científica, conversões de unidades reais, imputação ou engenharia de atributos.

## Testes

```powershell
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m pip check
```

Cobertura funcional: base reproduzível; esquema meteorológico; contrato de classificações; origem real/demonstrativa; filtros inclusivos e recortes vazios; gráficos/unidades/lacunas; uploads válidos, inválidos e excessivos; ausência de adaptadores; navegação das páginas e atualização de indicadores via Streamlit AppTest. Os testes de upload da interface usam objetos de arquivo em memória, identificados como tal. A inspeção no navegador complementa os testes automatizados. Resultados observados estão no relatório técnico.

## Limites da entrega e próximos passos

Esta aplicação está preparada para integração, mas **não integra o JSON real nem um modelo treinado**. Não foram executadas limpeza científica, transformação dos dados da empresa, seleção de algoritmos, treinamento, avaliação, métricas ou apresentação extensionista. Essas atividades pertencem aos outros integrantes e dependem de seus dados e validações.

Os colegas devem implementar os adaptadores, confirmar origem/unidades/fusos/semântica, integrar os resultados validados e executar os testes de contrato e interface. A desativação do modo demonstrativo depende de `WeatherBatch.is_demo=False` e resultados externos com a mesma proveniência — não apenas de esconder o aviso.

Tecnologias: Python, Streamlit, Pandas, Plotly, Pytest e Git local. NumPy aparece somente como dependência transitiva; Scikit-learn e Joblib não são usados nem instalados. Não há login, banco de dados, APIs ou serviços comerciais. Repositório do projeto: [mathevargas/pulverizaia](https://github.com/mathevargas/pulverizaia).

## Obter o projeto

```powershell
git clone https://github.com/mathevargas/pulverizaia.git
cd pulverizaia
```

Em repositórios privados, o acesso depende de autorização do proprietário. Depois de clonar, siga as instruções de instalação e execução acima.
