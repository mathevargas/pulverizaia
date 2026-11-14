from dataclasses import replace
import pytest
import pandas as pd
from src.services.demo import DemoWeatherSource, DemoClassificationProvider
from src.services.runtime import build_application, load_application
from src.integrations.pending import RealWeatherSource, ExternalModelProvider
from src.integrations.interfaces import IntegrationUnavailable
from src.models.contracts import WeatherBatch


def test_demo_is_reproducible_and_complete():
    a, b = build_application(), build_application()
    pd.testing.assert_frame_equal(a.frame, b.frame)
    assert a.is_demo is True
    assert len(a.frame) == 166
    assert set(a.frame.data_kind) == {"historical"}
    assert set(a.frame.classification) == {"Favorável", "Desfavorável", "Dados insuficientes"}
    assert a.frame.confidence.isna().all()
    assert a.frame.temperature_c.isna().sum() == 2


def test_demo_labels_do_not_depend_on_weather():
    batch = DemoWeatherSource().load()
    changed = replace(batch,records=tuple(replace(r,temperature_c=90,humidity_pct=None) for r in batch.records))
    provider = DemoClassificationProvider()
    assert provider.classify(batch) == provider.classify(changed)


def test_demo_provider_refuses_real_data(batch):
    with pytest.raises(IntegrationUnavailable):
        DemoClassificationProvider().classify(replace(batch,is_demo=False))


def test_pending_adapters_are_explicit(batch):
    with pytest.raises(IntegrationUnavailable): RealWeatherSource().load()
    with pytest.raises(IntegrationUnavailable): ExternalModelProvider().classify(batch)
    with pytest.raises(IntegrationUnavailable): build_application("real")


def test_data_without_model_still_displays(record):
    class TestSource:
        def load(self): return WeatherBatch((record,), False)
    data = load_application(TestSource(), ExternalModelProvider())
    assert not data.is_demo
    assert data.notices and data.frame.classification.iloc[0] == "Não fornecida"


def test_empty_source_can_be_presented():
    class EmptySource:
        def load(self): return WeatherBatch((), False)
    data = load_application(EmptySource(), ExternalModelProvider())
    assert data.frame.empty
