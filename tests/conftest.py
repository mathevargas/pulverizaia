from datetime import datetime, timezone
import pytest
from src.models.contracts import WeatherRecord, WeatherBatch


@pytest.fixture
def record():
    return WeatherRecord(
        timestamp=datetime(2026, 11, 1, 12, tzinfo=timezone.utc),
        temperature_c=24.0, humidity_pct=70.0, wind_speed_kmh=6.0,
        precipitation_mm=0.0, pressure_hpa=1012.0,
        source="Fonte sintética de teste", data_kind="historical",
    )


@pytest.fixture
def batch(record):
    return WeatherBatch((record,), is_demo=True)
