from src.integrations.interfaces import IntegrationUnavailable


class RealWeatherSource:
    def load(self):
        raise IntegrationUnavailable(
            "Adaptador de dados reais ainda não conectado. Selecione Demonstração para explorar o painel."
        )


class ExternalModelProvider:
    def classify(self, batch):
        raise IntegrationUnavailable(
            "Modelo externo ainda não conectado. Não há resultados de classificação disponíveis para estes dados."
        )
