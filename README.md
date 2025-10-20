README – Prueba Técnica RPA (TravelCorp)

//////////////////////////////////////////////////////
ARQUITECTURA DE LA SOLUCIÓN
/////////////////////////////////////////////////////

La solución está compuesta por tres capas principales:

- Extracción de datos (APIs)

    - Clima: Open-Meteo (temperatura, viento, precipitación, UV, pronóstico 7 días).
    - Divisas: ExchangeRate-API (USD → moneda local, simulación de histórico ±2%).
    - Zonas horarias: WorldTimeAPI con fallback en pytz (hora local y diferencia con Bogotá).

- Procesamiento y reglas de negocio

    - Sistema de alertas climáticas y financieras.
    - Cálculo del IVV (Índice de Viabilidad de Viaje) con ponderación de clima, divisas y UV.
    - Asignación de nivel de riesgo (verde, amarillo, naranja, rojo).

- Automatización y visualización

    - Ejecución automática cada 30 minutos con schedule.
    - Manejo de errores con reintentos (máx. 3 por API).
    - Logs estructurados en logs.json.
    - Dashboard interactivo en Streamlit + Plotly con mapa, tabla, gráficos y panel de alertas.

//////////////////////////////////////////////////////
ESTRUCTURA DE CARPETAS
//////////////////////////////////////////////////////

PruebaTecnica_RPA/
│
├── scr/
│   ├── main.py          # Script principal
│   ├── apis.py          # Conexión a APIs con reintentos y fallback
│   ├── rules.py         # Reglas de negocio (alertas, IVV)
│   ├── dashboard.py     # Dashboard en Streamlit
│   └── requirements.txt # Dependencias del proyecto
│
├── data/
│   ├── resultados.json  # Última ejecución consolidada
│   └── logs.json        # Historial de ejecuciones
│
└── README.md            # Documentación técnica


//////////////////////////////////////////////////////
INSTALACIÓN Y EJECUCIÓN
//////////////////////////////////////////////////////

- Instalar python 3.9.12 (Aplicación funcional comprobada con esta versión python)

- Crear una carpeta llamada PruebaTecnica_RPA en disco local C preferiblemente 

- Dentro de la carpeta "PruebaTecnica_RPA" Clonar repositorio o descomprimir ZIP usando los siguientes comandos por consola

git clone https://github.com/usuario/PruebaTecnica_RPA.git
cd PruebaTecnica_RPA/scr

- Crear entorno virtual e instalar dependencias usando los siguientes comandos por consola 

    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
    pip install -r requirements.txt

- Ejecutar el Algoritmo 

    - (En la consola moverse a la carpeta "scr" con el comando "cd") con el comando
    cd scr/
    - Luego con el comando
    python main.py

    debería obtener una ejecución así:

    * Primera ejecución inmediata.
    * Luego cada 30 minutos (configurable en main.py).
    * Resultados en ../data/resultados.json.
    * Logs en ../data/logs.json.

Despues de ejecutada la aplicación revisar los archivos JSON para verificar que la aplicación está funcionando de manera correcta.

- Ejecutar el Dashboard

    * con el siguiente comando "streamlit run dashboard.py" ejecuta el dashboard para visualizar la información en el frontend
    * abrir el dashboard. En un navegador web colocar "http://localhost:8501", con esto ya debería poder visualizar el dashboard
    con toda la informacion de la aplicación.
    

//////////////////////////////////////////////////////
DASHBOARD
//////////////////////////////////////////////////////

Incluye:
- Mapa con las 5 ciudades y su nivel de riesgo (verde/amarillo/naranja/rojo).
- Tabla resumen con métricas de clima, divisas e IVV.
- Gráficos de línea con evolución de temperatura 7 días.
- Gráfico de barras comparando tipos de cambio.
- Panel de alertas con alertas activas e histórico de las últimas 24h

//////////////////////////////////////////////////////
MANEJO DE ERRORES
//////////////////////////////////////////////////////

- Reintentos automáticos: hasta 3 por API.
- Fallback horario: si WorldTimeAPI falla, se usa pytz.
- Logs estructurados: cada ejecución se registra con estado (OK o ERROR) y mensaje.
- Notificaciones: alertas críticas se muestran en consola y en el dashboard


//////////////////////////////////////////////////////
DIAGRAMA DE FLUJO
//////////////////////////////////////////////////////

[Scheduler cada 30 min]
        ↓
   [main.py]
        ↓
 ┌───────────────┐
 │   apis.py     │ → Clima, Divisas, Hora
 └───────────────┘
        ↓
 ┌───────────────┐
 │   rules.py    │ → Alertas + IVV
 └───────────────┘
        ↓
 [resultados.json + logs.json]
        ↓
 [dashboard.py → Streamlit]


///////////////////////////////////////////////////////
ESCENARIOS DE PRUEBA
///////////////////////////////////////////////////////

- API caída → fallback o log de error.
- Datos incompletos → excepción controlada.
- Límite de rate → reintentos + log.
- Formato inesperado → validación de claves antes de procesar.

///////////////////////////////////////////////////////
LIBRERÍAS REQUERIDAS (requirements.txt)
//////////////////////////////////////////////////////

requests
pytz
schedule
streamlit
plotly
pandas






