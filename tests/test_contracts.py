from dataclasses import replace
from datetime import datetime, timedelta
import pytest
from src.models.contracts import WeatherBatch, ClassificationResult, ContractError
from src.services.presentation import with_results


@pytest.mark.parametrize("field,value", [
    ("timestamp", datetime(2026,11,1)), ("source", ""), ("data_kind", "real"),
    ("temperature_c", "24"), ("temperature_c", float("inf")),
    ("humidity_pct", 101), ("humidity_pct", -1), ("wind_speed_kmh", -1),
    ("precipitation_mm", -1), ("pressure_hpa", -1), ("temperature_c", True),
])
def test_weather_rejects_incompatible_contract(record, field, value):
    with pytest.raises(ContractError):
        replace(record, **{field:value})


def test_nullable_values_are_preserved(record):
    missing = replace(record, temperature_c=None, humidity_pct=None)
    assert missing.temperature_c is None and missing.humidity_pct is None


def test_duplicate_timestamps_rejected(record):
    with pytest.raises(ContractError): WeatherBatch((record,record), True)


def test_explicit_provenance(record):
    with pytest.raises(ContractError): WeatherBatch((record,), "true")


@pytest.mark.parametrize("changes", [
    {"predicted_class":"Segura"}, {"origin":""}, {"confidence":1.1},
    {"confidence":float("nan")}, {"justifications":["texto"]},
    {"is_demo":True,"confidence":.8}, {"is_demo":1},
])
def test_classification_contract(record, changes):
    values = dict(timestamp=record.timestamp,predicted_class="Favorável",origin="Teste de contrato",is_demo=False)
    values.update(changes)
    with pytest.raises(ContractError): ClassificationResult(**values)


def test_external_confidence_is_optional_and_preserved(record):
    batch = WeatherBatch((record,), False)
    result = ClassificationResult(record.timestamp, "Favorável", "Provedor sintético de teste", False, confidence=.7)
    frame = with_results(batch, (result,))
    assert frame.confidence.iloc[0] == .7
    assert frame.classification.iloc[0] == "Favorável"


def test_no_result_is_not_inferred(batch):
    frame = with_results(batch, ())
    assert frame.classification.iloc[0] == "Não fornecida"
    assert frame.confidence.isna().all()


def test_results_must_match_timestamps_and_provenance(batch, record):
    result = ClassificationResult(record.timestamp, "Dados insuficientes", "Fixture", True)
    with pytest.raises(ContractError): with_results(batch,(result,result))
    with pytest.raises(ContractError): with_results(batch,(replace(result, timestamp=record.timestamp+timedelta(hours=1)),))
    with pytest.raises(ContractError): with_results(batch,(replace(result,is_demo=False),))
