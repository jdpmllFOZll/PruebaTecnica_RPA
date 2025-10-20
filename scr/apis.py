import requests
from datetime import datetime
import pytz

# -------------------------------
# API de Clima (Open-Meteo)
# -------------------------------
def get_weather(lat, lon, retries=3):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,wind_speed_10m,uv_index"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        f"&timezone=auto"
    )
    for intento in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if intento < retries - 1:
                print(f"⚠️ Error en API clima, reintentando... ({intento+1})")
                continue
            else:
                print(f"❌ Error definitivo en API clima: {e}")
                return None


# -------------------------------
# API de Tipos de Cambio (ExchangeRate-API)
# -------------------------------
def get_exchange_rate(moneda_destino, retries=3):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    for intento in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if moneda_destino in data["rates"]:
                return {
                    "tipo_cambio_actual": data["rates"][moneda_destino],
                    "base": "USD"
                }
            else:
                print(f"⚠️ Moneda {moneda_destino} no encontrada en API")
                return None
        except Exception as e:
            if intento < retries - 1:
                print(f"⚠️ Error en API de tipo de cambio, reintentando... ({intento+1})")
                continue
            else:
                print(f"❌ Error definitivo en API de tipo de cambio: {e}")
                return None


# -------------------------------
# API de Zonas Horarias (WorldTimeAPI + fallback con pytz)
# -------------------------------
def get_timezone(timezone, retries=3):
    url = f"http://worldtimeapi.org/api/timezone/{timezone}"
    for intento in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "hora_local": data["datetime"],
                "utc_offset": data["utc_offset"],
                "fuente": "API"
            }
        except Exception:
            if intento < retries - 1:
                print(f"⚠️ Error en API de zona horaria, reintentando... ({intento+1})")
                continue
            else:
                print("❌ API de zona horaria no disponible, usando fallback local...")
                # --- Fallback con pytz ---
                try:
                    tz = pytz.timezone(timezone)
                    now = datetime.now(tz)
                    bogota = datetime.now(pytz.timezone("America/Bogota"))
                    diff = (now.utcoffset().total_seconds() - bogota.utcoffset().total_seconds()) / 3600
                    return {
                        "hora_local": now.isoformat(),
                        "diferencia_bogota_horas": diff,
                        "fuente": "fallback_local"
                    }
                except Exception as e:
                    print(f"❌ Error en fallback de zona horaria: {e}")
                    return None