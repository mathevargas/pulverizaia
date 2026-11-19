"""Contratos internos estritos. Validar não significa limpar dados da empresa."""

from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from numbers import Real
from typing import Literal

from src.config import CLASSES, WEATHER_FIELDS


class ContractError(ValueError):
    """O adaptador entregou um contrato incompatível com a interface."""


def _text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field}: texto não vazio obrigatório.")


def _timestamp(value):
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise ContractError("timestamp: forneça datetime válido com fuso horário.")
    if str(value) == "NaT":
        raise ContractError("timestamp não pode ser NaT.")


def _number(value, field, minimum=None, maximum=None):
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(value):
        raise ContractError(f"{field}: número finito ou None obrigatório.")
    if (
        minimum is not None
        and value < minimum
        or maximum is not None
        and value > maximum
    ):
        raise ContractError(f"{field}: valor fora do domínio do contrato.")


@dataclass(frozen=True)
class WeatherRecord:
    timestamp: datetime
    temperature_c: float | None
    humidity_pct: float | None
    wind_speed_kmh: float | None
    precipitation_mm: float | None
    pressure_hpa: float | None
    source: str
    data_kind: Literal["historical", "forecast"]

    def __post_init__(self):
        _timestamp(self.timestamp)
        _text(self.source, "source")
        if self.data_kind not in ("historical", "forecast"):
            raise ContractError("data_kind deve ser historical ou forecast.")
        for field in WEATHER_FIELDS:
            _number(getattr(self, field), field)
        _number(self.humidity_pct, "humidity_pct", 0, 100)
        for field in ("wind_speed_kmh", "precipitation_mm", "pressure_hpa"):
            _number(getattr(self, field), field, 0)


@dataclass(frozen=True)
class WeatherBatch:
    records: tuple[WeatherRecord, ...]
    is_demo: bool

    def __post_init__(self):
        if type(self.is_demo) is not bool:
            raise ContractError("is_demo deve ser booleano explícito.")
        if not isinstance(self.records, tuple) or not all(
            isinstance(r, WeatherRecord) for r in self.records
        ):
            raise ContractError("records deve ser uma tupla de WeatherRecord.")
        stamps = [r.timestamp for r in self.records]
        if len(stamps) != len(set(stamps)):
            raise ContractError(
                "Horários duplicados: entregue uma série única por lote."
            )


@dataclass(frozen=True)
class ClassificationResult:
    timestamp: datetime
    predicted_class: Literal[
        "Favorável",
        "Desfavorável",
        "Chuva prevista",
        "Sem chuva prevista",
        "Dados insuficientes",
    ]
    origin: str
    is_demo: bool
    justifications: tuple[str, ...] = ()
    limiting_factors: tuple[str, ...] = ()
    confidence: float | None = None

    def __post_init__(self):
        _timestamp(self.timestamp)
        _text(self.origin, "origin")
        if self.predicted_class not in CLASSES:
            raise ContractError("Classe incompatível com o contrato de classificação.")
        if type(self.is_demo) is not bool:
            raise ContractError("is_demo deve ser booleano explícito.")
        for field in ("justifications", "limiting_factors"):
            values = getattr(self, field)
            if not isinstance(values, tuple):
                raise ContractError(f"{field}: forneça uma tupla de textos.")
            for value in values:
                _text(value, field)
        _number(self.confidence, "confidence", 0, 1)
        if self.is_demo and self.confidence is not None:
            raise ContractError(
                "Resultados demonstrativos não podem conter confiança fictícia."
            )
