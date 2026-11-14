"""Conversões de contratos para apresentação, sem preparar dados científicos."""
from dataclasses import asdict
from datetime import date
import pandas as pd

from src.config import TIMEZONE, WEATHER_FIELDS
from src.models.contracts import WeatherBatch, ClassificationResult, ContractError


def weather_frame(batch: WeatherBatch):
    columns = ["timestamp", *WEATHER_FIELDS, "source", "data_kind"]
    frame = pd.DataFrame([asdict(record) for record in batch.records], columns=columns)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True).dt.tz_convert(TIMEZONE)
    for field in WEATHER_FIELDS:
        frame[field] = frame[field].astype("float64")
    return frame.sort_values("timestamp").reset_index(drop=True)


def with_results(batch: WeatherBatch, results: tuple[ClassificationResult, ...]):
    if not isinstance(results, tuple) or not all(isinstance(r, ClassificationResult) for r in results):
        raise ContractError("O classificador deve entregar uma tupla de ClassificationResult.")
    frame = weather_frame(batch)
    lookup = {}
    timestamps = {r.timestamp for r in batch.records}
    for result in results:
        if result.is_demo != batch.is_demo:
            raise ContractError("Dados e classificações não podem misturar origem real e demonstrativa.")
        if result.timestamp not in timestamps:
            raise ContractError("Classificação sem registro meteorológico correspondente.")
        if result.timestamp in lookup:
            raise ContractError("Classificações duplicadas para o mesmo horário.")
        lookup[result.timestamp] = result
    entries = [lookup.get(stamp) for stamp in frame.timestamp]
    frame["classification"] = [r.predicted_class if r else "Não fornecida" for r in entries]
    frame["justification"] = ["; ".join(r.justifications) if r and r.justifications else "Justificativa não fornecida" for r in entries]
    frame["limiting_factors"] = ["; ".join(r.limiting_factors) if r and r.limiting_factors else "Não informados" for r in entries]
    frame["classification_origin"] = [r.origin if r else "Classificador não conectado / resultado ausente" for r in entries]
    frame["confidence"] = [r.confidence if r else None for r in entries]
    return frame


def filter_period(frame, start: date, end: date, kinds=None):
    if start > end:
        raise ValueError("A data inicial deve ser anterior ou igual à data final.")
    mask = (frame.timestamp.dt.date >= start) & (frame.timestamp.dt.date <= end)
    if kinds is not None:
        mask &= frame.data_kind.isin(kinds)
    return frame.loc[mask].copy()


def chart_frame(frame, field):
    if field not in WEATHER_FIELDS:
        raise ValueError("Variável meteorológica desconhecida.")
    # Mantém NaN para interromper linhas; não interpola nem remove lacunas.
    return frame[["timestamp", field, "source", "data_kind"]].sort_values("timestamp").copy()
