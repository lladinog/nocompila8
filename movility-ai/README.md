# 🚦 MovilityAI

**Sistema Inteligente de Análisis y Optimización de Movilidad Urbana**

---

## 📋 Descripción

MovilityAI es un sistema modular basado en **Google Agent Development Kit (ADK)** que integra datos de múltiples fuentes (Google Maps, Moovit, datos abiertos) para analizar, predecir y optimizar patrones de movilidad urbana.

### Características principales:

- ✅ **Análisis de tráfico en tiempo real**
- ✅ **Predicción de congestión vehicular**
- ✅ **Optimización de rutas multimodales**
- ✅ **Arquitectura multiagente modular**
- ✅ **Registro automático de aprendizaje (memoria_ia.md)**
- ✅ **Desarrollo guiado por pruebas (TDD)**

---

## 🏗️ Arquitectura

El sistema sigue una **arquitectura multiagente jerárquica** inspirada en el patrón del Travel Concierge del Google ADK:

```
root_agent (orquestador)
    ├── ingest_agent (obtiene datos de APIs)
    ├── clean_agent (procesa y normaliza datos)
    ├── analyze_agent (análisis y predicción)
    └── report_agent (genera reportes y registros)
```

### Estructura del proyecto:

```
movility-ai/
├── movility_ai/          # Código principal
│   ├── agent.py          # Root agent (orquestador)
│   ├── prompt.py         # Instrucciones del agente
│   ├── sub_agents/       # Agentes especializados
│   ├── tools/            # Adaptadores y herramientas
│   └── shared_libraries/ # Tipos y constantes compartidas
├── tests/                # Tests unitarios
├── eval/                 # Tests de evaluación
├── deployment/           # Scripts de despliegue
└── docs/                 # Documentación y memoria
```

---

## 🚀 Instalación

### Prerrequisitos:

- Python 3.10, 3.11, o 3.12
- [uv](https://docs.astral.sh/uv/) (gestor de paquetes)
- Cuenta de Google Cloud con APIs habilitadas

### Pasos:

1. **Clonar el repositorio:**

```bash
git clone <repository-url>
cd movility-ai
```

2. **Instalar dependencias:**

```bash
uv sync
```

3. **Configurar variables de entorno:**

Crea un archivo `.env` con tus credenciales:

```env
GOOGLE_CLOUD_PROJECT=tu-proyecto
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=True
```

4. **Verificar instalación:**

```bash
uv run pytest tests/
```

---

## 💻 Uso

### Ejecutar el agente principal:

```bash
uv run python -m movility_ai
```

### Ejecutar tests:

```bash
# Tests unitarios
uv run pytest tests/unit/

# Tests de evaluación
uv run pytest eval/
```

### Ejecutar con datos de prueba:

```bash
uv run python -m movility_ai --test-mode
```

---

## 🧪 Desarrollo

Este proyecto sigue **Test-Driven Development (TDD)**:

1. Escribir el test primero
2. Implementar el código mínimo
3. Refactorizar
4. Documentar en `docs/memoria_ia.md`

### Agregar un nuevo agente:

1. Crear carpeta en `movility_ai/sub_agents/nombre_agente/`
2. Implementar `agent.py` y `prompt.py`
3. Escribir tests en `tests/unit/test_nombre_agente.py`
4. Registrar en `sub_agents/__init__.py`
5. Agregar al `root_agent`

---

## 📚 Documentación

- **Arquitectura completa:** `docs/ARCHITECTURE.md`
- **Descripción del proyecto:** `docs/PROJECT_DESCRIPTION.md`
- **Memoria de IA:** `docs/memoria_ia.md` (registro automático de aprendizaje)
- **Documentación ADK:** `docs_adk/`

---

## 🤝 Contribuciones

Este proyecto sigue principios de código limpio y arquitectura hexagonal. Por favor revisa:

1. La arquitectura definida en `docs/ARCHITECTURE.md`
2. Los patrones del Travel Concierge en `travel-concierge/`
3. La documentación del ADK en `docs_adk/`

---

## 📄 Licencia

Apache License 2.0 - Ver [LICENSE](LICENSE) para más detalles.

---

## 🔗 Referencias

- [Google Agent Development Kit](https://cloud.google.com/products/agent-builder)
- [Google Maps Platform](https://developers.google.com/maps)
- [Moovit Developer APIs](https://company.moovit.com/es/maas-solutions-es/transit-apis/)
- [Datos Abiertos Colombia](https://datos.gov.co)

---

**Desarrollado con ❤️ usando Google ADK**
