from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMO_DIR = ROOT / "data" / "demo"
TIMEZONE = "America/Sao_Paulo"
MAX_UPLOAD_BYTES = 2 * 1024 * 1024
WEATHER_FIELDS = {
    "temperature_c": ("Temperatura", "°C"),
    "humidity_pct": ("Umidade relativa", "%"),
    "wind_speed_kmh": ("Velocidade do vento", "km/h"),
    "precipitation_mm": ("Precipitação", "mm"),
    "pressure_hpa": ("Pressão atmosférica", "hPa"),
}
CLASSES = (
    "Favorável",
    "Desfavorável",
    "Chuva prevista",
    "Sem chuva prevista",
    "Dados insuficientes",
)
KIND_LABELS = {"historical": "Histórico observado", "forecast": "Previsão da fonte"}
