from typing import Protocol
from src.models.contracts import WeatherBatch, ClassificationResult


class IntegrationUnavailable(RuntimeError):
    """Uma integração prevista ainda não foi implementada."""


class WeatherSource(Protocol):
    def load(self) -> WeatherBatch: ...


class ClassificationProvider(Protocol):
    def classify(self, batch: WeatherBatch) -> tuple[ClassificationResult, ...]: ...
