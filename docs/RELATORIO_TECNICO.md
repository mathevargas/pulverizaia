# Relatório técnico de entrega — atividade 5

**PulverizaIA — reconstrução do protótipo**
Data de verificação: **14/11/2026**, fuso America/Sao_Paulo.

## 1. Localização e reconstrução

Raiz confirmada no terminal:

```text
C:\Users\<usuario>\pulverizacao-inteligente
```

A inspeção encontrou somente o protótipo anterior, arquivos demonstrativos, ambiente virtual e metadados Git sem commits/remotos. Não foram identificados dados reais da empresa, credenciais ou trabalho adicional de colaboradores nos arquivos inspecionados.

Código, testes, documentação, dados demonstrativos, configurações e dependências locais anteriores foram removidos. A aplicação foi escrita novamente a partir do novo escopo, sem reutilizar o código anterior. A pasta raiz foi preservada; nenhuma pasta duplicada de projeto foi criada. O ambiente `.venv` foi recriado.

O diretório antigo `.pytest_cache` teve acesso/exclusão bloqueados pelo Windows. Após a orientação do usuário, ele foi deixado intocado, sem mudança de permissões ou nova tentativa de exclusão. O Pytest usa `.test-cache`, ignorado pelo Git; o cache antigo não interfere nos testes executados. Os metadados Git vazios foram preservados, sem reescrita de histórico.

## 2. Estrutura entregue

```text
pulverizacao-inteligente/
├── .gitattributes
├── .gitignore
├── .streamlit/
│   └── config.toml
├── .vscode/
│   └── settings.json
├── app.py
├── iniciar_windows.bat
├── pytest.ini
├── README.md
├── requirements.txt
├── requirements-lock.txt
├── src/
│   ├── __init__.py
│   ├── config/
│   │   └── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   ├── filters.py
│   │   └── layout.py
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── interfaces.py
│   │   └── pending.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── contracts.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── about.py
│   │   ├── conditions.py
│   │   ├── dashboard.py
│   │   ├── hourly.py
│   │   ├── import_data.py
│   │   └── meteorology.py
│   └── services/
│       ├── __init__.py
│       ├── demo.py
│       ├── presentation.py
│       ├── runtime.py
│       └── uploads.py
├── data/
│   └── demo/
│       ├── classifications.json
│       └── weather.json
├── tests/
│   ├── conftest.py
│   ├── test_contracts.py
│   ├── test_demo_integration.py
│   ├── test_presentation.py
│   ├── test_ui.py
│   └── test_uploads.py
└── docs/
    ├── INTEGRACAO.md
    ├── RELATORIO_TECNICO.md
    └── screenshots/
        ├── analise-meteorologica.jpg
        ├── dashboard-mobile.jpg
        ├── dashboard-notebook.jpg
        ├── horarios-filtrados.jpg
        └── upload-json.jpg
```

Diretórios locais de execução, não entregáveis de código: `.git`, `.venv`, `.test-cache`, `__pycache__` e o cache antigo bloqueado.

## 3. Funcionalidades implementadas

| Área | Comportamento disponível |
|---|---|
| Dashboard | Cinco indicadores meteorológicos com unidades, último registro do recorte, fonte, datas, contagem, médias e rótulo demonstrativo explicado |
| Análise meteorológica | Cinco gráficos interativos Plotly, filtros compartilhados, unidades e tratamento de menos de dois valores disponíveis |
| Condições para pulverização | Contagem das três classes, seleção de registro, variáveis associadas, justificativas, fatores limitantes e origem; confiança somente quando um provedor real a fornecer |
| Análise por horários | Tabela, filtros de classes, ordenação por campo e sentido, identificação de natureza histórica/previsão e ausência de geração de horários futuros |
| Importação | Upload de JSON até 2 MB, validação de sintaxe UTF-8, nome, tamanho, estrutura raiz, prévia limitada e mensagens de erro |
| Sobre | Contexto acadêmico/extensionista, tecnologias, objetivos, limites e divisão de responsabilidades |
| Demonstração | 166 registros estáticos e fictícios de 01 a 07/11/2026, com lacunas/ausências e rótulos independentes do clima |
| Integração | Protocolos de fornecedores, dataclasses validadas e ponto de composição que permite trocar dados/modelo sem reconstruir páginas |

Não há regras agronômicas nem algoritmo científico de classificação nesta reconstrução. Os rótulos estão escritos em um arquivo demonstrativo separado; não são inferidos das variáveis. A demonstração não contém probabilidades. Registros ausentes não são preenchidos e não há totalização automática de precipitação.

O upload não modifica o dashboard e não implementa limpeza, mapeamento ou transformação de dados da empresa. JSON válido é tratado como sintaxe válida, não como integração concluída.

## 4. Ambiente e bibliotecas

| Componente | Versão verificada |
|---|---|
| Python | 3.14.3 |
| Streamlit | 1.67.0 |
| Pandas | 3.1.1 |
| Plotly | 6.9.0 |
| Pytest | 9.2.0 |
| Git | 2.53.0.windows.2 |

As quatro dependências diretas estão fixadas em `requirements.txt`; o ambiente completo está em `requirements-lock.txt`. NumPy foi instalado como dependência transitiva, não usado diretamente. Não foram instalados Scikit-learn, Joblib ou bibliotecas de treinamento. Não há serviços pagos, banco externo ou API meteorológica.

A criação inicial de `.venv`, o download de pacotes e a execução de testes/servidor precisaram de execução fora do ambiente restrito da ferramenta: houve bloqueio de temporários e rede/soquetes. As tentativas autorizadas subsequentes funcionaram. Isso não exigiu alterar permissões ou configurações de segurança do Windows. O uso da aplicação, depois da instalação, não depende de serviços externos.

## 5. Testes efetivamente executados

Comando final:

```powershell
.venv\Scripts\python -m pytest -q
```

Resultado observado após os ajustes finais:

```text
57 passed in 6.06s
```

Os testes cobrem:

- Carga e reprodutibilidade da demonstração, presença das três classes e ausência de probabilidades fictícias.
- Rejeição de contratos incompatíveis: tipos, fusos, domínios básicos, timestamps duplicados e falta de proveniência explícita.
- Validação de classe, justificativas, confiança opcional e correspondência entre resultados e registros.
- Bloqueio de rótulos demonstrativos em dados reais e de mistura de proveniências.
- Rótulos demonstrativos independentes dos valores meteorológicos.
- Filtros inclusivos por período e natureza, datas invertidas e recortes vazios.
- Preparação dos cinco gráficos, unidades e preservação de lacunas/valores ausentes.
- JSON válido inclusive com estrutura desconhecida/valor simples; JSON inválido, codificação inválida, constantes fora da sintaxe e limite de tamanho.
- Prévia limitada para textos extensos, muitos itens e estrutura profunda, sem executar HTML.
- Fonte/modelo indisponíveis, fonte vazia e dados existentes sem classificador conectado.
- Navegação das seis páginas, indicadores reagindo ao filtro, estado vazio e mensagens de integração pendente pelo Streamlit AppTest.
- Upload válido/inválido na página usando objetos de arquivo em memória; upload não altera o dashboard.

Uma execução intermediária teve um teste que esperava rejeição de JSON profundo, mesmo válido. O teste foi corrigido para verificar a limitação da prévia, que é o comportamento de software requerido. A suíte final passou integralmente. Nenhum teste executado é apresentado como validação científica/agronômica ou avaliação de ML.

Verificação adicional:

```text
python -m pip check → No broken requirements found.
```

## 6. Inicialização e conferência no navegador

Servidor efetivamente iniciado em `127.0.0.1:8501`. Para a conferência automatizada, foi utilizado:

```powershell
.venv\Scripts\python -m streamlit run app.py --server.headless true --server.fileWatcherType none
```

O observador de arquivos foi desativado apenas nessa execução de verificação; para desenvolvimento normal, o comando do README utiliza o comportamento padrão do Streamlit.

Respostas HTTP verificadas fora da restrição de soquetes da ferramenta:

```text
GET /                → HTTP 200
GET /_stcore/health   → HTTP 200, corpo: ok
```

Inspeção realizada no navegador integrado:

- Dashboard com os cinco valores e rótulo demonstrativo.
- Página dos gráficos e sua renderização.
- Página de condições e seus avisos/contagens/seletor de registro.
- Tabela por horários, filtro deixando somente **Desfavorável** (55 horários) e ordenação decrescente, confirmando os horários de 07/11/2026 no início.
- Upload real do arquivo sintético `data/demo/weather.json`: **45.829 bytes**, sintaxe válida, estrutura raiz lista e prévia limitada, sem alteração do dashboard.
- Navegação e informações da página Sobre.
- Layout de notebook em **1366 × 900** e layout estreito em **390 × 844**, incluindo abertura/fechamento da navegação móvel.

A inspeção revelou cartões cortados em janelas menores. Foram corrigidos a distribuição responsiva, o tamanho dos valores, a quebra de títulos e o espaço superior. O tamanho temporário de tela do navegador foi restaurado ao terminar. A aba do dashboard ficou disponível para avaliação.

Capturas de evidência estão em `docs/screenshots/`. A inspeção de JSON inválido foi coberta pelos testes automatizados; não é reivindicada como segundo upload manual no navegador. Não houve avaliação em dispositivos físicos ou por usuários da comunidade nesta etapa.

## 7. Executar no VS Code

Abra a raiz indicada no início e selecione `.venv/Scripts/python.exe` como interpretador. No terminal:

```powershell
.venv\Scripts\python -m streamlit run app.py
```

Ou dê dois cliques em `iniciar_windows.bat`. Acesse [http://127.0.0.1:8501](http://127.0.0.1:8501). Com `.venv` ativado, `python -m streamlit run app.py` também é o comando principal. Encerre o servidor pelo terminal com Ctrl+C. Se a sessão atual for encerrada, reinicie com esses mesmos comandos.

## 8. Git e publicação

O Git local foi preservado na mudança de pasta. O usuário criou o repositório [mathevargas/pulverizaia](https://github.com/mathevargas/pulverizaia) e autorizou a publicação da primeira versão na branch `main`.

A revisão anterior à publicação confirmou que o remoto estava vazio e que os arquivos selecionados não continham padrões conhecidos de credenciais. Foram verificados os padrões de exclusão de `.venv`, caches, `data/private/` e `.streamlit/secrets.toml`. O `.gitignore` também cobre uploads, `.env`, chaves e artefatos de modelo. Somente dados demonstrativos acompanham o código.

## 9. Entrega para integração dos colegas

Documento principal: [INTEGRACAO.md](INTEGRACAO.md).

| Arquivo/interface | Uso pelos colegas |
|---|---|
| `src/models/contracts.py` | Construir WeatherRecord, WeatherBatch e ClassificationResult com tipos/unidades/proveniência explícitos |
| `src/integrations/interfaces.py` | Implementar WeatherSource.load e ClassificationProvider.classify |
| `src/integrations/pending.py` | Substituir os fornecedores ainda indisponíveis, ou criar módulos próprios |
| `src/services/runtime.py` | Conectar os novos fornecedores no modo real |
| `tests/` | Executar a suíte existente e adicionar testes específicos dos adaptadores |

As páginas, componentes, filtros e gráficos não precisam ser reconstruídos. A documentação detalha como manter ausências, distinguir histórico/previsão e desativar a demonstração por metadados corretos, sem esconder avisos enquanto se usam fixtures.

## 10. Pendências e limites

- Integração específica do JSON real e qualquer preparação científica dos dados: colegas.
- Modelo treinado, engenharia de atributos, métricas, avaliação e resultados reais: colegas.
- Validação científica/agronômica e apresentação extensionista: fora desta entrega de software.
- O contrato atual representa uma série com timestamps únicos por lote; múltiplas estações/séries sobrepostas precisam de seleção no adaptador.
- Tabelas largas usam rolagem horizontal nativa; nem todas as colunas ficam simultaneamente visíveis em telas menores.
- Proveniência real é declarada pelo adaptador, não certificada independentemente pela aplicação.
- Não foram verificados navegadores/dispositivos físicos adicionais nem executada pesquisa de usabilidade.
- O diretório de cache antigo bloqueado foi ignorado conforme orientação; nenhum procedimento de mudança de permissões foi feito.

A atividade 5 está entregue para revisão do usuário. Não foram iniciadas as atividades científicas 3, 4 ou 6 nem as integrações científicas pendentes.
