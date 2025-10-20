import streamlit as st
import pandas as pd
import json
import plotly.express as px

# --- Cargar datos ---
with open("../data/resultados.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convertir a DataFrame para tabla y gráficos
df = pd.json_normalize(data)

# --- Título ---
st.title("🌍 Dashboard de Viabilidad de Viaje")

# --- Mapa con nivel de riesgo ---
st.subheader("Mapa de Ciudades con Nivel de Riesgo")
coords = {
    "Nueva York": (40.7128, -74.0060),
    "Londres": (51.5074, -0.1278),
    "Tokio": (35.6762, 139.6503),
    "São Paulo": (-23.5505, -46.6333),
    "Sídney": (-33.8688, 151.2093)
}

map_data = []
for ciudad in data:
    lat, lon = coords[ciudad["ciudad"]]
    map_data.append({
        "ciudad": ciudad["ciudad"],
        "lat": lat,
        "lon": lon,
        "nivel_riesgo": ciudad["ivv"]["nivel_riesgo"],
        "color": ciudad["ivv"]["color"]
    })

map_df = pd.DataFrame(map_data)
fig_map = px.scatter_mapbox(
    map_df,
    lat="lat", lon="lon",
    color="nivel_riesgo",
    hover_name="ciudad",
    zoom=1,
    color_discrete_map={
        "BAJO": "green",
        "MEDIO": "yellow",
        "ALTO": "orange",
        "CRÍTICO": "red"
    }
)
fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map)

# --- Tabla resumen ---
st.subheader("Tabla Resumen de Ciudades")
st.dataframe(df[[
    "ciudad",
    "clima.temperatura_actual",
    "clima.precipitacion",
    "clima.viento",
    "clima.uv",
    "finanzas.tipo_cambio_actual",
    "ivv.ivv_score",
    "ivv.nivel_riesgo"
]])

# --- Gráfico de tendencias (ejemplo: temperatura máxima 7 días) ---
st.subheader("Pronóstico de Temperaturas (7 días)")
for ciudad in data:
    pronostico = pd.DataFrame(ciudad["clima"]["pronostico_7_dias"])
    fig = px.line(pronostico, x="fecha", y=["temp_max", "temp_min"],
                  title=f"📈 {ciudad['ciudad']}")
    st.plotly_chart(fig)

# --- Panel de alertas ---
st.subheader("🚨 Alertas Activas")
for ciudad in data:
    if ciudad["alertas"]:
        st.markdown(f"**{ciudad['ciudad']}**")
        for alerta in ciudad["alertas"]:
            st.warning(f"{alerta['tipo']}: {alerta['mensaje']}")
    else:
        st.success(f"{ciudad['ciudad']}: Sin alertas")