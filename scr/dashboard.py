import streamlit as st
import pandas as pd
import json
import plotly.express as px
from pathlib import Path

# ==============================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================
st.set_page_config(
    page_title="🌍 Dashboard de Viabilidad de Viaje",
    page_icon="✈️",
    layout="wide"
)

# ==============================
# CARGA DE DATOS
# ==============================
resultados_path = Path("./data/resultados.json")
logs_path = Path("./data/logs.json")

try:
    with open(resultados_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.json_normalize(data)
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo resultados.json en la carpeta data/")
    st.stop()

# ==============================
# TÍTULO
# ==============================
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🌍 Dashboard de Viabilidad de Viaje</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Monitoreo de clima, finanzas y riesgos para viajes internacionales</p>", unsafe_allow_html=True)

st.markdown("---")

# ==============================
# MAPA DE RIESGO
# ==============================
st.subheader("🗺️ Mapa de Ciudades con Nivel de Riesgo")

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
    size_max=15,
    color_discrete_map={
        "BAJO": "green",
        "MEDIO": "yellow",
        "ALTO": "orange",
        "CRÍTICO": "red"
    }
)

fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0, "t":0, "l":0, "b":0},
    mapbox_center={"lat": 0, "lon": 0},
    mapbox_zoom=1
)

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# ==============================
# TABLA RESUMEN + MÉTRICAS
# ==============================
st.subheader("📊 Resumen de Ciudades")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌡️ Temp. Promedio", f"{df['clima.temperatura_actual'].mean():.1f} °C")
with col2:
    st.metric("☀️ UV Máx.", f"{df['clima.uv'].max()}")
with col3:
    st.metric("💱 Tipo Cambio Prom.", f"{df['finanzas.tipo_cambio_actual'].mean():.2f}")

st.dataframe(df[[
    "ciudad",
    "clima.temperatura_actual",
    "clima.precipitacion",
    "clima.viento",
    "clima.uv",
    "finanzas.tipo_cambio_actual",
    "ivv.ivv_score",
    "ivv.nivel_riesgo"
]], use_container_width=True)

st.markdown("---")

# ==============================
# GRÁFICOS DE TENDENCIAS
# ==============================
st.subheader("📈 Pronóstico de Temperaturas (7 días)")

for ciudad in data:
    pronostico = pd.DataFrame(ciudad["clima"]["pronostico_7_dias"])
    fig = px.line(
        pronostico, x="fecha", y=["temp_max", "temp_min"],
        title=f"📍 {ciudad['ciudad']}",
        markers=True
    )
    fig.update_layout(template="plotly_white", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==============================
# PANEL DE ALERTAS
# ==============================
st.subheader("🚨 Alertas Activas")

for ciudad in data:
    if ciudad["alertas"]:
        st.markdown(f"**{ciudad['ciudad']}**")
        for alerta in ciudad["alertas"]:
            st.warning(f"{alerta['tipo']}: {alerta['mensaje']}")
    else:
        st.success(f"{ciudad['ciudad']}: ✅ Sin alertas")

st.markdown("---")
