import json
from datetime import datetime
from apis import get_weather, get_exchange_rate, get_timezone
from rules import evaluar_alertas, calcular_ivv

# --- Lista de ciudades ---
ciudades = [
    {"nombre": "Nueva York", "lat": 40.7128, "lon": -74.0060, "moneda": "USD", "timezone": "America/New_York"},
    {"nombre": "Londres", "lat": 51.5074, "lon": -0.1278, "moneda": "GBP", "timezone": "Europe/London"},
    {"nombre": "Tokio", "lat": 35.6762, "lon": 139.6503, "moneda": "JPY", "timezone": "Asia/Tokyo"},
    {"nombre": "São Paulo", "lat": -23.5505, "lon": -46.6333, "moneda": "BRL", "timezone": "America/Sao_Paulo"},
    {"nombre": "Sídney", "lat": -33.8688, "lon": 151.2093, "moneda": "AUD", "timezone": "Australia/Sydney"}
]

# --- Función para registrar logs ---
def registrar_log(estado, mensaje):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "estado": estado,
        "mensaje": mensaje
    }
    try:
        with open("../data/logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)

    with open("../data/logs.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

# --- Función principal ---
def run_pipeline():
    resultados = []
    try:
        for c in ciudades:
            clima = get_weather(c["lat"], c["lon"])
            cambio = get_exchange_rate(c["moneda"])
            hora = get_timezone(c["timezone"])

            if not clima or not cambio or not hora:
                raise Exception(f"Datos incompletos para {c['nombre']}")

            resultado = {
                "timestamp": datetime.utcnow().isoformat(),
                "ciudad": c["nombre"],
                "clima": {
                    "temperatura_actual": clima["current"]["temperature_2m"],
                    "precipitacion": clima["daily"]["precipitation_probability_max"][0],
                    "viento": clima["current"]["wind_speed_10m"],
                    "uv": clima["current"]["uv_index"],
                    "pronostico_7_dias": [
                        {
                            "fecha": clima["daily"]["time"][i],
                            "temp_max": clima["daily"]["temperature_2m_max"][i],
                            "temp_min": clima["daily"]["temperature_2m_min"][i],
                            "precipitacion": clima["daily"]["precipitation_probability_max"][i]
                        }
                        for i in range(len(clima["daily"]["time"]))
                    ]
                },
                "finanzas": {
                    "tipo_cambio_actual": cambio["tipo_cambio_actual"],
                    "base": cambio["base"]
                },
                "hora_local": hora
            }

            # --- Reglas de negocio ---
            alertas = evaluar_alertas(resultado["clima"], resultado["finanzas"])
            ivv = calcular_ivv(resultado["clima"], resultado["finanzas"], alertas)

            resultado["alertas"] = alertas
            resultado["ivv"] = ivv

            resultados.append(resultado)

        # Guardar todos los resultados en un solo archivo
        with open("../data/resultados.json", "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=4, ensure_ascii=False)

        print("Datos guardados para todas las ciudades")
        registrar_log("OK", "Datos guardados para todas las ciudades")

    except Exception as e:
        print(f"Error en pipeline: {e}")
        registrar_log("ERROR", str(e))

if __name__ == "__main__":
    import schedule, time

    # --- Ejecución inmediata para pruebas ---
    print("Ejecutando recolección de datos inicial...")
    run_pipeline()

    # --- Para pruebas: cada 30 segundos ---
    schedule.every(30).seconds.do(run_pipeline)

    print("Robot iniciado. Ejecutando cada 30 segundos (modo prueba)...")
    while True:
        schedule.run_pending()
        time.sleep(1)