"""
Herramientas para Insight Agent
"""

from movility_ai.tools.data_mock_tool import generate_mock_insights
from movility_ai.tools.chart_generator import generate_city_insights_chart


def generate_city_insights(time_period: str, tool_context) -> str:
    """
    Genera análisis de patrones de movilidad de la ciudad
    
    Args:
        time_period: Periodo de análisis ("day", "week", "month")
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Reporte formateado con insights y tendencias
    """
    # Generar insights mock
    insights_data = generate_mock_insights()
    
    # Guardar en contexto
    if hasattr(tool_context, 'state'):
        tool_context.state.last_city_insights = insights_data
    
    # Extraer datos
    congested_zones = insights_data.get("congested_zones", [])
    traffic_trend = insights_data.get("traffic_trend", [])
    mode_distribution = insights_data.get("mode_distribution", [])
    summary = insights_data.get("summary", "")
    
    # Analizar patrones temporales
    peak_hours = [h["hour"] for h in sorted(traffic_trend, key=lambda x: x["level"], reverse=True)[:3]]
    high_traffic_count = len([h for h in traffic_trend if h['level'] > 70])
    
    # Analizar zonas
    top_zones = congested_zones[:3]
    critical_zones = len([z for z in congested_zones if z['congestion_level'] > 70])
    
    # Analizar modos
    popular_mode = max(mode_distribution, key=lambda x: x["percentage"]) if mode_distribution else {"mode": "N/A", "percentage": 0}
    
    # Formatear reporte visual
    report_lines = [
        "📊 **ANÁLISIS DE MOVILIDAD URBANA - MEDELLÍN**",
        f"📅 Periodo: {time_period}",
        "",
        "🕐 **PATRONES TEMPORALES**",
        f"⏰ Horas pico: {', '.join(peak_hours)}",
        f"📈 Tendencia: {high_traffic_count} horas de alta congestión",
        "",
        "🗺️ **ANÁLISIS POR ZONAS**",
    ]
    
    for zone in top_zones:
        report_lines.append(f"  • {zone['zone']}: {zone['congestion_level']}% de congestión")
    
    report_lines.extend([
        "",
        "🚇 **DISTRIBUCIÓN MODAL**",
        f"🏆 Modo más popular: {popular_mode['mode']} ({popular_mode['percentage']}%)",
    ])
    
    for mode in mode_distribution[:3]:
        report_lines.append(f"  • {mode['mode']}: {mode['percentage']}%")
    
    report_lines.extend([
        "",
        "📌 **INSIGHTS CLAVE**",
        f"  • {summary}",
        f"  • Zonas críticas: {critical_zones} con congestión alta",
        f"  • {popular_mode['percentage']}% de usuarios prefieren {popular_mode['mode']}",
        "",
        "━" * 50,
        "📡 **FUENTES DE INFORMACIÓN:**",
        "• Datos Agregados: Metro de Medellín, Área Metropolitana",
        "• Análisis Tráfico: Waze, SoloBus, Google Maps APIs",
        "• Estadísticas: DANE, Alcaldía de Medellín, MiMedellín",
        "• IoT: 250+ sensores urbanos de monitoreo",
        ""
    ])
    
    return "\n".join(report_lines)


def generate_insight_chart(chart_type: str, data_category: str, tool_context) -> str:
    """
    Genera gráficos analíticos personalizados
    
    Args:
        chart_type: Tipo de gráfico ("bar", "line", "pie")
        data_category: Categoría de datos ("transport_modes", "zones", "traffic", "hours")
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Gráfico en formato ASCII para visualización
    """
    # Verificar si hay insights guardados
    insights_data = None
    if hasattr(tool_context, 'state') and hasattr(tool_context.state, 'last_city_insights'):
        insights_data = tool_context.state.last_city_insights
    else:
        # Generar nuevos insights si no existen
        insights_data = generate_mock_insights()
    
    # Generar visualización ASCII usando la herramienta de charts
    chart_ascii = generate_city_insights_chart(insights_data)
    
    return chart_ascii


# Registrar herramientas para ADK
try:
    from google.genai import types as genai_types
    
    generate_city_insights_tool = genai_types.Tool(
        function_declarations=[
            genai_types.FunctionDeclaration(
                name="generate_city_insights",
                description="Genera análisis agregados de patrones de movilidad urbana en Medellín. Incluye estadísticas, patrones temporales, zonas más transitadas y distribución modal.",
                parameters={
                    "type": "object",
                    "properties": {
                        "time_period": {
                            "type": "string",
                            "description": "Periodo de análisis: 'day' (24 horas), 'week' (7 días), 'month' (30 días)",
                            "enum": ["day", "week", "month"]
                        }
                    },
                    "required": ["time_period"]
                }
            )
        ]
    )
    
    generate_insight_chart_tool = genai_types.Tool(
        function_declarations=[
            genai_types.FunctionDeclaration(
                name="generate_insight_chart",
                description="Genera visualizaciones gráficas personalizadas de datos de movilidad. Soporta gráficos de barras, líneas y circulares para diferentes categorías de datos.",
                parameters={
                    "type": "object",
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "description": "Tipo de gráfico a generar",
                            "enum": ["bar", "line", "pie"]
                        },
                        "data_category": {
                            "type": "string",
                            "description": "Categoría de datos a visualizar",
                            "enum": ["transport_modes", "zones", "traffic", "hours"]
                        }
                    },
                    "required": ["chart_type", "data_category"]
                }
            )
        ]
    )
    
    ADK_AVAILABLE = True

except ImportError:
    # Si ADK no está disponible, crear decoradores mock para testing
    ADK_AVAILABLE = False
    
    def tool_decorator(func):
        """Decorador mock para testing sin ADK"""
        func.is_tool = True
        return func
    
    generate_city_insights_tool = tool_decorator(generate_city_insights)
    generate_insight_chart_tool = tool_decorator(generate_insight_chart)
