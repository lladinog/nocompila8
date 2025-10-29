# 🧪 Tests - MovilityAI

## 🎯 Estrategia TDD

Este proyecto sigue **Test-Driven Development (TDD)** con el ciclo:

1. **🔴 RED** - Escribir tests que fallan
2. **🟢 GREEN** - Implementar código mínimo para pasar tests
3. **🔵 REFACTOR** - Mejorar el código manteniendo tests verdes

## 📁 Estructura de Tests

```
tests/
├── __init__.py
└── unit/
    ├── __init__.py
    ├── test_tools.py      # Tests de herramientas (visualización, mock, memoria)
    └── test_agents.py     # Tests de agentes (root + sub-agentes)
```

## 🚀 Ejecutar Tests

### Todos los tests
```bash
cd movility_ai
pytest
```

### Solo tests unitarios
```bash
pytest tests/unit/
```

### Tests específicos
```bash
pytest tests/unit/test_tools.py
pytest tests/unit/test_agents.py
```

### Con verbose
```bash
pytest -v
```

### Con cobertura
```bash
pytest --cov=movility_ai --cov-report=html
```

## 📊 Estado Actual de Tests

### ✅ Fase RED (Completada)
- [x] Tests de `data_mock_tool` (9 tests)
- [x] Tests de `visualizer_tool` (5 tests)
- [x] Tests de `memory_display_tool` (4 tests)
- [x] Tests de `root_agent` (3 tests)
- [x] Tests de sub-agentes (12 tests marcados como skip)

**Total: 33 tests definidos** 

### 🟡 Fase GREEN (Pendiente)
Estos tests fallarán hasta que:
1. Las herramientas se conviertan en ADK tools con decoradores
2. Los sub-agentes se implementen completamente

## 🎨 Tests para la Demo

Los tests están diseñados para verificar:

✅ **Generación de datos simulados coherentes**
- Rutas entre zonas reales de Medellín
- Niveles de tráfico realistas
- Eventos urbanos típicos

✅ **Visualizaciones en formato JSON**
- Mapas de rutas con marcadores
- Heatmaps de tráfico con colores
- Dashboards ecológicos con métricas

✅ **Sistema de memoria funcional**
- Estado compartido entre agentes
- Historial de interacciones
- Transferencias visibles

✅ **Flujo multiagente**
- Colaboración entre agentes
- Delegación de tareas
- Contexto compartido

## 📝 Convenciones

- **test_[feature]_basic**: Test básico de funcionalidad
- **test_[feature]_with_[condition]**: Test con condiciones específicas
- **test_[feature]_visual**: Test de generación visual
- **@pytest.mark.skip**: Tests que requieren implementación futura

## 🐛 Debugging

Si un test falla:

1. Ejecutar solo ese test: `pytest tests/unit/test_tools.py::TestDataMockTool::test_generate_mock_route_basic -v`
2. Ver output completo: `pytest -v -s`
3. Usar breakpoint: `pytest --pdb`

## 🎯 Objetivo para la Hackathon

Estos tests garantizan que:
- ✨ Todo genera salidas visuales consistentes
- 🗺️ Los datos simulados son coherentes
- 🧠 El sistema de memoria funciona
- 🔄 Los agentes pueden colaborar

**Los tests nos permiten desarrollar rápido con confianza.**

---

**Fase actual:** 🔴 RED - Tests escritos, esperando implementación
**Siguiente:** 🟢 GREEN - Hacer que todos los tests pasen
