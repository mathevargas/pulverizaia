"""Leitura de fixtures explícitas, sem inferência ou regras agronômicas."""
import json
from datetime import datetime

from src.config import DEMO_DIR
from src.integrations.interfaces import IntegrationUnavailable
from src.models.contracts import WeatherRecord, WeatherBatch, ClassificationResult


class DemoWeatherSource:
    def load(self):
        try:
            rows = json.loads((DEMO_DIR / "weather.json").read_text(encoding="utf-8"))
            records = tuple(WeatherRecord(**{**row, "timestamp": datetime.fromisoformat(row["timestamp"])}) for row in rows)
        except (OSError, ValueError, TypeError, KeyError) as exc:
            raise IntegrationUnavailable("Não foi possível carregar a base demonstrativa local. Verifique os arquivos em data/demo.") from exc
        return WeatherBatch(records=records, is_demo=True)


class DemoClassificationProvider:
    def classify(self, batch):
        if not batch.is_demo:
            raise IntegrationUnavailable("Classificações fictícias não podem ser associadas a dados reais.")
        try:
            rows = json.loads((DEMO_DIR / "classifications.json").read_text(encoding="utf-8"))
            requested = {r.timestamp for r in batch.records}
            return tuple(
                ClassificationResult(
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    predicted_class=row["predicted_class"], origin=row["origin"],
                    is_demo=True, justifications=tuple(row.get("justifications", [])),
                    limiting_factors=tuple(row.get("limiting_factors", [])),
                )
                for row in rows if datetime.fromisoformat(row["timestamp"]) in requested
            )
        except (OSError, ValueError, TypeError, KeyError) as exc:
            raise IntegrationUnavailable("Não foi possível carregar os rótulos fictícios de demonstração.") from exc
