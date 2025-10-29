# 🚦 MovilityAI

**Sistema Inteligente de Movilidad Urbana para Medellín**

> Hackathon Project - Sistema multiagente con Google ADK & Gemini

---

## 📋 Descripción

MovilityAI es un sistema multiagente que ayuda a navegar y entender la movilidad de Medellín, Colombia. Combina **planificación de rutas inteligentes**, **predicción de tráfico** y **análisis de datos urbanos** usando Google ADK y Gemini.

### 🎯 Agentes Especializados:

1. **🗺️ PathFinder Agent** - Planificador de rutas multimodales
   - Combina metro, bus, bicicleta (EnCicla) y caminata
   - Considera tráfico, clima y preferencias del usuario
   - Optimiza por tiempo, costo o sostenibilidad

2. **🚦 FlowSense Agent** - Predictor de congestión vial
   - Predice tráfico en zonas clave de Medellín (30-60 min)
   - Identifica zonas críticas en tiempo real
   - Analiza impacto de clima y eventos

3. **📊 Insight Agent** - Analista de movilidad urbana
   - Genera dashboards y visualizaciones
   - Identifica patrones y tendencias
   - Métricas de sostenibilidad y eficiencia

---

## 🏗️ Arquitectura

```
root_agent (coordinador)
    ├── pathfinder_agent (rutas multimodales)
    ├── flowsense_agent (predicción de tráfico)
    └── insight_agent (analytics y visualización)
```

### Estructura del proyecto:

```
movility-ai/
├── movility_ai/
│   ├── agent.py              # Root agent coordinador
│   ├── prompt.py             # Instrucciones principales
│   ├── sub_agents/
│   │   ├── pathfinder/       # 🗺️ Planificador de rutas
│   │   │   ├── agent.py
│   │   │   ├── prompt.py
│   │   │   └── tools.py      # Google Maps, EnCicla, clima
│   │   ├── flowsense/        # 🚦 Predictor de tráfico
│   │   │   ├── agent.py
│   │   │   ├── prompt.py
│   │   │   └── predictor.py  # Lógica de predicción
│   │   └── insight/          # 📊 Analista urbano
│   │       ├── agent.py
│   │       ├── prompt.py
│   │       └── analytics.py  # Dashboards y visualizaciones
│   └── shared_libraries/     # Tipos y constantes
├── tests/                    # Tests unitarios
└── pyproject.toml
```

---

## 🚀 Instalación Rápida

### Prerrequisitos:
- Python 3.10 - 3.12
- [uv](https://docs.astral.sh/uv/) (recomendado) o pip

### Opción 1: Con uv (Recomendado)

```bash
# Instalar uv si no lo tienes
pip install uv

# Clonar e instalar
git clone <repository-url>
cd movility-ai
uv sync
```

### Opción 2: Con pip

```bash
pip install -e .
```

### Configurar API Keys:

1. Copia el archivo de ejemplo:
```bash
copy .env.example .env
```

2. Edita `.env` y agrega tu API key de Google:
```env
GOOGLE_API_KEY=tu_api_key_aqui
```

**📌 Obtener API Keys gratuitas:**

- **Gemini (Google AI)**: https://makersuite.google.com/app/apikey
  - ✅ GRATIS con límites generosos
  - ✅ REQUERIDO para que funcione el sistema

- **Google Maps** (Opcional): https://console.cloud.google.com/google/maps-apis
  - ✅ $200 USD gratis/mes
  - Si no la configuras, usa datos mock

- **OpenWeather** (Opcional): https://openweathermap.org/api
  - ✅ 1000 llamadas gratis/día
  - Si no la configuras, usa datos mock

---

## 💻 Uso

### Ejecutar el sistema:

```bash
uv run python -m movility_ai
```

### Ejemplos de consultas:

**Para PathFinder (rutas):**
```
"¿Cómo llego del Centro a El Poblado?"
"Ruta más rápida y barata de Laureles a Universidad"
"Quiero ir en bici y metro, ¿cómo combino?"
```

**Para FlowSense (tráfico):**
```
"¿Cómo está el tráfico en la Autopista Norte?"
"¿Habrá trancón a las 6pm en El Poblado?"
"¿Qué zonas están congestionadas ahora?"
```

**Para Insight (análisis):**
```
"Muéstrame un dashboard de movilidad de Medellín"
"¿Cuáles son las zonas más críticas?"
"Análisis de sostenibilidad del transporte"
```

---

## 🧪 Tests

```bash
# Ejecutar todos los tests
uv run pytest

# Tests con cobertura
uv run pytest --cov=movility_ai tests/
```

---

## 🌟 Características Principales

### PathFinder Agent
- ✅ Rutas multimodales (metro + bici + caminata)
- ✅ Optimización por tiempo, costo o CO2
- ✅ Integración con EnCicla (bicicletas públicas)
- ✅ Considera clima y tráfico
- ✅ Memoria contextual de preferencias

### FlowSense Agent
- ✅ Predicción 30-60 minutos
- ✅ Zonas clave de Medellín mapeadas
- ✅ Patrones por hora del día
- ✅ Impacto de clima y eventos
- ✅ Alertas de congestión

### Insight Agent
- ✅ Dashboards ejecutivos
- ✅ Top zonas críticas
- ✅ Análisis temporal (horas pico, días)
- ✅ Métricas de sostenibilidad
- ✅ Comparativas entre zonas
- ✅ Detección de anomalías

---

## 🎨 Tech Stack

- **LLM**: Google Gemini 2.0 Flash
- **Framework**: Google ADK (Agent Development Kit)
- **APIs**: Google Maps, OpenWeather (opcionales)
- **Lenguaje**: Python 3.10+
- **Gestión**: uv / pip

---

## � Datos Mock vs APIs Reales

El sistema funciona 100% con **datos hardcodeados** para hackathon, pero puede conectarse a APIs reales:

| Componente | Datos Mock | API Real |
|------------|------------|----------|
| Rutas | ✅ Incluidos | Google Maps Directions |
| Clima | ✅ Incluidos | OpenWeather |
| Tráfico | ✅ Incluidos | Google Maps Traffic |
| EnCicla | ✅ Incluidos | (API no pública) |
| Analytics | ✅ Incluidos | - |

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agrega nueva característica'`)
4. Push (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

## 📝 Notas para Hackathon

- ⚡ El sistema funciona **sin APIs externas** (usa datos mock)
- 🔑 Solo necesitas **GOOGLE_API_KEY** para Gemini (gratis)
- 🚀 Setup en **menos de 5 minutos**
- 📦 Todo incluido: rutas, tráfico, analytics
- 🇨🇴 Datos específicos de **Medellín, Colombia**

---

## 📄 Licencia

Apache License 2.0 - Ver [LICENSE](LICENSE)

---

## 🔗 Referencias

- [Google ADK](https://cloud.google.com/products/agent-builder)
- [Google AI Studio](https://makersuite.google.com)
- [Metro de Medellín](https://www.metrodemedellin.gov.co/)
- [EnCicla](https://www.encicla.gov.co/)

---

**Desarrollado con ❤️ para Medellín usando Google Gemini & ADK**
