# 🧭 MovilityAI - Sistema Multiagente de Movilidad Urbana

> **Demo para Hackathon** - Sistema inteligente de movilidad urbana para Medellín basado en Google ADK

## 🎯 Objetivo

Demostrar un sistema multiagente vivo, coordinado y altamente visual que simula comportamientos urbanos inteligentes para la movilidad en Medellín.

**Prioridad:** Experiencia visual y narrativa del flujo > Funcionalidad real

## 🏗️ Arquitectura

```
movility_ai/
├── agent.py              # NaviMind Root Agent (orquestador)
├── prompt.py             # Prompts del sistema
├── shared_libraries/
│   ├── constants.py      # Constantes de Medellín
│   └── types.py          # Tipos de datos (Route, TrafficInfo, etc.)
├── tools/
│   ├── visualizer_tool.py      # 🎨 Genera mapas/gráficos
│   ├── memory_display_tool.py  # 🧠 Muestra estado/memoria
│   └── data_mock_tool.py       # 🎲 Datos simulados
└── sub_agents/
    ├── pathfinder/       # 🥇 Planificación de rutas multimodales
    ├── flowsense/        # 🥇 Predicción de tráfico y congestión
    ├── pulse/            # 🥈 Contexto urbano (eventos, clima)
    ├── ecotrack/         # 🥉 Métricas ecológicas
    └── insight/          # 🥉 Analítica urbana
```

## 🤖 Agentes

| Agente | Rol | Estado |
|--------|-----|--------|
| **NaviMind** | Orquestador conversacional | 🟢 Estructura lista |
| **PathFinder** | Planificación de rutas | ⏳ Pendiente |
| **FlowSense** | Predicción de tráfico | ⏳ Pendiente |
| **Pulse** | Contexto urbano | ⏳ Pendiente |
| **EcoTrack** | Métricas sostenibilidad | ⏳ Pendiente |
| **Insight** | Analítica urbana | ⏳ Pendiente |

## ✅ Progreso TDD

- ✅ **🔴 RED Phase**: Tests definidos (33 tests)
- ✅ **🟢 GREEN Phase**: Core implementado (17/17 tests passing)
- ⏳ **🔵 REFACTOR Phase**: Pendiente
- ⏳ **Sub-agentes**: 0/5 implementados

## 🔄 Flujo de Interacción

```
Usuario → NaviMind (Root) → [Sub-Agentes] → Visualización
                    ↓
              Session State (Memoria compartida)
```

## 🎨 Herramientas Visuales

✅ **Visualizer Tool** - Genera mapas, rutas, gráficos
✅ **Data Mock Tool** - Provee datos simulados coherentes
✅ **Memory Display Tool** - Muestra estado del sistema

## 🚀 Uso

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el agente en modo web
adk web movility_ai

# O ejecutar como API
adk api_server movility_ai
```

## 📊 Para la Demo

El sistema está diseñado para:
- ✨ Mostrar agentes colaborando en tiempo real
- 🗺️ Generar visualizaciones atractivas (mapas, rutas, alertas)
- 🧠 Demostrar memoria y contexto compartido
- 🎯 Crear un flujo narrativo coherente en 5 minutos

**Todo es simulado pero visualmente impresionante.**

## 📝 Notas de Desarrollo

- Basado en `travel-concierge` de Google ADK
- Los datos son mock pero coherentes
- La interfaz ADK muestra las transferencias entre agentes
- Sin integraciones reales (APIs, ML, scraping)

---

**Status:** 🟡 Estructura base creada - Sub-agentes pendientes
