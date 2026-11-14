"""Composição da aplicação: os colegas substituem somente os fornecedores."""
from dataclasses import dataclass
import pandas as pd

from src.integrations.interfaces import WeatherSource, ClassificationProvider, IntegrationUnavailable
from src.integrations.pending import RealWeatherSource, ExternalModelProvider
from src.services.demo import DemoWeatherSource, DemoClassificationProvider
from src.services.presentation import with_results


@dataclass
class ApplicationData:
    frame: pd.DataFrame
    is_demo: bool
    notices: tuple[str, ...] = ()


def load_application(source: WeatherSource, classifier: ClassificationProvider):
    batch = source.load()
    notices = ()
    try:
        results = classifier.classify(batch)
    except IntegrationUnavailable as exc:
        results = ()
        notices = (str(exc),)
    return ApplicationData(with_results(batch, results), batch.is_demo, notices)


def build_application(mode="demo"):
    if mode == "demo":
        return load_application(DemoWeatherSource(), DemoClassificationProvider())
    if mode == "real":
        return load_application(RealWeatherSource(), ExternalModelProvider())
    raise ValueError("Modo de dados desconhecido.")
