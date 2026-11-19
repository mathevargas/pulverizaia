"""Adaptador real conectando Etapa 3 (dados) e Etapa 4 (modelo) ao PulverizaIA."""
from __future__ import annotations

import math
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from src.integrations.interfaces import IntegrationUnavailable
from src.models.contracts import ClassificationResult, WeatherBatch, WeatherRecord

# Caminhos relativos a partir de pulverizaia/src/integrations/etapa4_adapter.py
RAIZ_PROJETO = Path(__file__).resolve().parents[3]
CAMINHO_HORARIOS = RAIZ_PROJETO / "etapa3_preparacao" / "dados_horarios.csv"
CAMINHO_5MIN = RAIZ_PROJETO / "etapa3_preparacao" / "dados_limpos_5min.csv"
CAMINHO_MODELO = RAIZ_PROJETO / "etapa4_mineracao" / "resultados" / "modelo_chuva_6h.joblib"

FUSO_LOCAL = ZoneInfo("America/Sao_Paulo")


def _garantir_import_etapa4():
    raiz_str = str(RAIZ_PROJETO)
    if raiz_str not in sys.path:
        sys.path.insert(0, raiz_str)


def _numero_ou_none(valor, multiplicador: float = 1.0) -> float | None:
    if valor is None or pd.isna(valor):
        return None
    num = float(valor) * multiplicador
    return num if math.isfinite(num) else None


def _parse_timestamp(valor) -> datetime:
    ts = pd.to_datetime(valor)
    dt = ts.to_pydatetime()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=FUSO_LOCAL)
    return dt


class Etapa4WeatherSource:
    """Lê a série horária real preparada na Etapa 3."""

    def __init__(self, ultimos: int = 168):
        self.ultimos = ultimos  # Exibe os últimos 7 dias (168h) no painel

    def load(self) -> WeatherBatch:
        if not CAMINHO_HORARIOS.exists():
            raise IntegrationUnavailable(
                f"Arquivo não encontrado: {CAMINHO_HORARIOS}"
            )

        df = pd.read_csv(CAMINHO_HORARIOS)
        col_tempo = next(
            (c for c in ("timestamp", "data_hora", "datetime", "hora_referencia", "time") if c in df.columns),
            df.columns[0],
        )

        df = df.sort_values(col_tempo).drop_duplicates(subset=[col_tempo]).tail(self.ultimos)

        registros = []
        for _, row in df.iterrows():
            registros.append(
                WeatherRecord(
                    timestamp=_parse_timestamp(row[col_tempo]),
                    temperature_c=_numero_ou_none(row.get("temperature")),
                    humidity_pct=_numero_ou_none(row.get("humidity")),
                    wind_speed_kmh=_numero_ou_none(row.get("wind_speed"), multiplicador=3.6),
                    precipitation_mm=_numero_ou_none(row.get("rain_mm")),
                    pressure_hpa=_numero_ou_none(row.get("pressure")),
                    source="Estação meteorológica (Etapa 3 - mm/h)",
                    data_kind="historical",
                )
            )

        return WeatherBatch(records=tuple(registros), is_demo=False)


class Etapa4ModelProvider:
    """Executa o modelo de risco de chuva em 6h treinado na Etapa 4."""

    def classify(self, batch: WeatherBatch) -> tuple[ClassificationResult, ...]:
        if not CAMINHO_MODELO.exists() or not CAMINHO_5MIN.exists():
            raise IntegrationUnavailable(
                "Modelo da Etapa 4 ou dados de 5 min não encontrados."
            )

        _garantir_import_etapa4()
        from etapa4_mineracao.dados import Configuracao, preparar_dados
        from etapa4_mineracao.prever import carregar_modelo, prever_horarios

        pacote = carregar_modelo(str(CAMINHO_MODELO))
        dados = preparar_dados(
            str(CAMINHO_HORARIOS),
            str(CAMINHO_5MIN),
            Configuracao(**pacote["configuracao"]),
        )

        # Passa o histórico completo para preparar_dados e recorta só o tamanho do lote
        saida = prever_horarios(pacote, dados, ultimos=len(batch.records))
        if isinstance(saida, dict):
            itens = next(
                (v for v in saida.values() if isinstance(v, list) and (not v or isinstance(v[0], dict))),
                [],
            )
        else:
            itens = saida

        stamps_validos = {r.timestamp for r in batch.records}
        resultados = []

        for item in itens:
            ts = _parse_timestamp(item["hora_referencia"])
            if ts not in stamps_validos:
                continue

            classe = item["classe_prevista"]
            janela = f"{item.get('inicio_janela_prevista', '')} até {item.get('fim_janela_prevista_exclusivo', '')}"
            justificativas = (f"Janela prevista (chuva >= 0,2 mm em 6h): {janela}",)

            indisponiveis = item.get("atributos_indisponiveis") or []
            fatores = tuple(str(a) for a in indisponiveis)

            resultados.append(
                ClassificationResult(
                    timestamp=ts,
                    predicted_class=classe,
                    origin="Etapa 4 - Modelo Chuva 6h (probabilidade não calibrada)",
                    is_demo=batch.is_demo,
                    justifications=justificativas,
                    limiting_factors=fatores,
                    confidence=None,  # Probabilidade não calibrada não deve ir como confiança
                )
            )

        return tuple(resultados)