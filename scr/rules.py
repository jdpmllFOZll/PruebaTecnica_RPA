def evaluar_alertas(clima, finanzas):
    alertas = []

    # --- Alertas climáticas ---
    if clima["temperatura_actual"] > 35 or clima["temperatura_actual"] < 0:
        alertas.append({"tipo": "CLIMA", "mensaje": "Temperatura extrema"})
    if clima["precipitacion"] > 70:
        alertas.append({"tipo": "CLIMA", "mensaje": f"Alta probabilidad de lluvia ({clima['precipitacion']}%)"})
    if clima["viento"] > 50:
        alertas.append({"tipo": "CLIMA", "mensaje": f"Viento fuerte ({clima['viento']} km/h)"})

    # --- Alertas de tipo de cambio ---
    # Aquí simulamos variación diaria con un valor fijo (ejemplo: 2%)
    variacion = 2.0
    if variacion > 3:
        alertas.append({"tipo": "CAMBIO", "mensaje": f"Variación alta del tipo de cambio ({variacion}%)"})

    return alertas


def calcular_ivv(clima, finanzas, alertas):
    # Clima Score
    alertas_climaticas = sum(1 for a in alertas if a["tipo"] == "CLIMA")
    clima_score = 100 - (alertas_climaticas * 25)

    # Cambio Score (simulación)
    cambio_score = 100  # estable
    # UV Score
    uv = clima["uv"]
    if uv < 6:
        uv_score = 100
    elif 6 <= uv <= 8:
        uv_score = 75
    else:
        uv_score = 50

    ivv = (clima_score * 0.4) + (cambio_score * 0.3) + (uv_score * 0.3)

    # Nivel de riesgo
    if ivv >= 80:
        nivel = "BAJO"
        color = "Verde"
    elif ivv >= 60:
        nivel = "MEDIO"
        color = "Amarillo"
    elif ivv >= 40:
        nivel = "ALTO"
        color = "Naranja"
    else:
        nivel = "CRÍTICO"
        color = "Rojo"

    return {
        "ivv_score": ivv,
        "nivel_riesgo": nivel,
        "color": color,
        "componentes": {
            "clima_score": clima_score,
            "cambio_score": cambio_score,
            "uv_score": uv_score
        }
    }