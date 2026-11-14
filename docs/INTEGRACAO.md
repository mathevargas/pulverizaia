# Integração dos colegas — dados e modelo

## 1. Fronteira de responsabilidade

Esta entrega implementa a atividade 5: aplicação e testes. A leitura específica do JSON da empresa, limpeza, transformação, engenharia de atributos, treinamento, avaliação e integração real ficam com os colegas. Os nomes abaixo são um **contrato interno**, não uma suposição sobre o arquivo original.

Fluxo:

```text
Fonte/JSON autorizado → adaptador dos colegas → WeatherBatch
                                               ↓
                          provedor de classificação dos colegas
                                               ↓
                                 tuple[ClassificationResult, ...]
                                               ↓
                         load_application → DataFrame de apresentação
                                               ↓
                            filtros → dashboard/páginas/gráficos
```

## 2. Dados meteorológicos esperados

Contratos implementados em `src/models/contracts.py`:

| Campo de WeatherRecord | Tipo interno | Unidade / significado |
|---|---|---|
| `timestamp` | `datetime` com fuso | Instante do registro; a UI converte para America/Sao_Paulo |
| `temperature_c` | número finito ou `None` | °C |
| `humidity_pct` | número finito ou `None` | %, domínio 0–100 |
| `wind_speed_kmh` | número finito ou `None` | km/h, não negativo |
| `precipitation_mm` | número finito ou `None` | mm, não negativo; documentar intervalo/acumulado no adaptador |
| `pressure_hpa` | número finito ou `None` | hPa, não negativo |
| `source` | texto não vazio | Origem identificável do registro |
| `data_kind` | `historical` ou `forecast` | Histórico observado ou previsão fornecida pela fonte |

Todos os campos devem ser entregues; as cinco medidas podem ser `None` para representar ausência. Não envie `NaN`, infinito, textos numéricos ou booleanos como medidas: o contrato rejeita entradas incompatíveis. O software não corrige o dado nem escolhe valores para substituir ausências. Domínios numéricos não são critérios de segurança agronômica.

`WeatherBatch(records=tuple(...), is_demo=bool)` agrupa a série. `records` deve ser uma tupla de `WeatherRecord`, inclusive quando vazia. `is_demo` é obrigatório e explícito. Um lote representa uma série com timestamps únicos: caso existam várias estações ou históricos/previsões sobrepostos, o adaptador deve selecionar a série correta antes de entregá-la. A aplicação não resolve conflitos científicos nem agrega dados automaticamente.

Datas devem estar com fuso antes da entrega; interpretar datas sem offset e horários ambíguos é tarefa do adaptador. A UI não decide que um registro é previsão apenas porque sua data está no futuro. `data_kind` representa a natureza declarada pela fonte, e não um cálculo do relógio local.

## 3. Fonte real: o que implementar

A interface `WeatherSource`, em `src/integrations/interfaces.py`, exige:

```python
def load(self) -> WeatherBatch:
    ...
```

Implemente uma classe própria em `src/integrations/` ou substitua o corpo de `RealWeatherSource.load()` em `pending.py`. Somente o adaptador deve conhecer o JSON original, suas unidades e campos. Não altere as páginas para ler campos da empresa diretamente.

Exemplo **exclusivamente sintético**, demonstrando uma saída já normalizada, sem sugerir estrutura de entrada:

```python
from datetime import datetime, timezone
from src.models.contracts import WeatherRecord, WeatherBatch

class MinhaFonte:
    def load(self) -> WeatherBatch:
        # Substituir pela leitura/preparação realizada pelos colegas.
        registro = WeatherRecord(
            timestamp=datetime(2026, 11, 1, 12, tzinfo=timezone.utc),
            temperature_c=24.0,
            humidity_pct=70.0,
            wind_speed_kmh=6.0,
            precipitation_mm=0.0,
            pressure_hpa=None,  # Ausente: não inventar pressão.
            source="Exemplo sintético de documentação",
            data_kind="historical",
        )
        return WeatherBatch((registro,), is_demo=True)
```

Esse exemplo permanece demonstrativo intencionalmente. Somente a implementação com dados reais conferidos deve entregar `is_demo=False`.

## 4. Contrato de classificação

`ClassificationProvider.classify(batch)` recebe o lote completo e entrega `tuple[ClassificationResult, ...]`. Não é exigido um algoritmo específico. O modelo, seus atributos, artefatos e pré-processamento ficam encapsulados no provedor dos colegas.

| Campo | Obrigatoriedade | Significado |
|---|---|---|
| `timestamp` | Sim | Instante correspondente a um registro meteorológico do lote |
| `predicted_class` | Sim | `Favorável`, `Desfavorável` ou `Dados insuficientes` |
| `origin` | Sim | Nome/versão/origem do resultado, não vazio |
| `is_demo` | Sim | Deve coincidir com a origem demonstrativa/real do lote |
| `justifications` | Não, padrão `()` | Tupla de textos fornecidos pelo provedor |
| `limiting_factors` | Não, padrão `()` | Tupla de fatores fornecidos pelo provedor |
| `confidence` | Não, padrão `None` | Número finito entre 0 e 1, somente se fornecido pelo modelo |

Não invente justificativas, probabilidades ou calibração. Se o modelo não fornece confiança, mantenha `None`; a UI não exibe um percentual fictício. Resultados demonstrativos com confiança são rejeitados. Nenhuma confiança aparece nas fixtures entregues.

Exemplo sintético de formato:

```python
from src.models.contracts import ClassificationResult

def resultado_sintetico(registro):
    return ClassificationResult(
        timestamp=registro.timestamp,
        predicted_class="Dados insuficientes",
        origin="Exemplo de documentação — sem modelo",
        is_demo=True,
        justifications=("Texto ilustrativo, não inferido do clima.",),
        limiting_factors=(),
        confidence=None,
    )
```

Uma tupla vazia ou ausência de um resultado para determinado horário é permitida. A UI exibe **Não fornecida**, sem inferir “Dados insuficientes”. Esta última é uma classe que deve ser explicitamente retornada pelo fornecedor. Resultados com timestamps desconhecidos ou duplicados são rejeitados. Timestamps equivalentes em fusos diferentes correspondem ao mesmo instante.

## 5. Conectar os fornecedores

`src/services/runtime.py` é o ponto de composição. A função:

```python
load_application(source, classifier)
```

chama `source.load()`, recebe classificações e valida sua associação aos registros. Ela retorna `ApplicationData` para a UI. Para conectar sua implementação, altere somente a composição de `build_application("real")`:

```python
# Trecho ilustrativo para a futura composição, ainda não implementado:
return load_application(MinhaFonteReal(), MeuProvedorDeModelo())
```

Atualmente `RealWeatherSource` e `ExternalModelProvider` geram `IntegrationUnavailable` com mensagens claras. Se a fonte real existe mas o modelo ainda não, `load_application` preserva os dados e apresenta resultados não fornecidos, com aviso. Se a fonte não está conectada, a interface para a análise e mostra a pendência; não troca silenciosamente por demonstração.

Ao implementar um provedor real, erros esperados de indisponibilidade podem usar `IntegrationUnavailable`. Incompatibilidades do contrato usam `ContractError`. Erros inesperados são registrados no terminal; a UI mostra mensagem compreensível. Não esconda falhas retornando dados fictícios como se fossem reais.

## 6. Upload e integração futura

`src/services/uploads.py:inspect_json()` valida **apenas sintaxe** e cria uma prévia limitada. Não transforma conteúdo em `WeatherBatch` e não entrega o upload ao adaptador. A página não salva o arquivo.

Se os colegas optarem por integrar uploads em vez de outra fonte autorizada, deverão implementar o fluxo explícito entre o arquivo escolhido e seu adaptador, com confirmação de esquema, unidades, origem e fuso. Mantenham a inspeção de sintaxe separada da validação de contrato e não tratem “JSON válido” como “dados integrados”. Documentem o novo comportamento e criem seus testes antes de mudar essa mensagem.

## 7. Desativar corretamente a demonstração

1. Integre a fonte real e valide seus registros.
2. Entregue `WeatherBatch(..., is_demo=False)` somente para dados reais conferidos.
3. Conecte resultados reais com `ClassificationResult(..., is_demo=False)`, ou mantenha modelo indisponível/resultado ausente.
4. Selecione a fonte integrada na UI. A mensagem é derivada do lote, não de um CSS nem do nome do seletor.
5. Não reutilize `DemoClassificationProvider` com registros reais: a implementação bloqueia essa combinação.
6. Não esconda o aviso enquanto continuar usando fixtures. Se desejar tornar a fonte real o padrão após aprovação, ajuste a seleção inicial em `app.py` e sua documentação/testes.

`is_demo` é uma declaração do adaptador, não certificação independente da origem. Os responsáveis pela integração devem conferir essa declaração. Os contratos de software não validam qualidade científica, adequação agronômica, rotulagem ou desempenho do modelo.

## 8. Arquivos que não precisam mudar

Depois de implementar os fornecedores e conectá-los em `runtime.py`, não é necessário reconstruir:

- `src/pages/`: apresentação de dados e resultados.
- `src/components/`: indicadores, filtros e gráficos.
- `src/services/presentation.py`: preparação dos contratos para exibição.
- `data/demo/`: fixtures continuam disponíveis para demonstração e testes.

Preserve a base demonstrativa e as mensagens de proveniência. O nome `src/models/` designa os contratos de dados do software; não contém modelo treinado.

## 9. Testar a integração

```powershell
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m pip check
.venv\Scripts\python -m streamlit run app.py
```

Adicione testes do adaptador com amostras sintéticas ou autorizadas não confidenciais, verificando unidades, datas/fusos, ausências, campos obrigatórios, duplicidades, origem real/demonstrativa e resultados sem correspondência. Teste separadamente a integração com e sem classificador disponível. Confirme que os filtros e a tabela preservam histórico versus previsão e que nenhuma probabilidade aparece quando não é fornecida. A suíte já inclui esses casos para os contratos de software e fornecedores demonstrativos, mas não valida os futuros adaptadores.

Dados privados, uploads, `.env`, segredos e artefatos de modelo são ignorados pelo Git em localizações/padrões previstos no `.gitignore`. Guardem dados empresariais em `data/private/`, não em `data/demo/`. Não versionem credenciais ou arquivos reais em outros caminhos. Repositório: https://github.com/mathevargas/pulverizaia.
