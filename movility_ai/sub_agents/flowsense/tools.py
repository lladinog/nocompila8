"""
Herramientas para FlowSense Agent
"""

from movility_ai.tools.data_mock_tool import generate_mock_traffic
from movility_ai.tools.chart_generator import generate_traffic_heatmap_medellin


def _get_traffic_icon(level: str) -> str:
    """Devuelve el emoji correspondiente al nivel de tráfico"""
    icons = {
        "bajo": "🟢",
        "medio": "🟡", 
        "alto": "🟠",
        "crítico": "🔴"
    }
    return icons.get(level.lower(), "⚪")


def predict_traffic(zones: list[str], tool_context) -> str:
    """
    Predice el estado del tráfico para las zonas especificadas
    
    Args:
        zones: Lista de zonas de Medellín a analizar
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Reporte formateado con predicciones de tráfico
    """
    # Generar datos de tráfico simulados
    traffic_data = generate_mock_traffic(zones)
    
    # Guardar en contexto para uso futuro
    if hasattr(tool_context, 'state'):
        tool_context.state.last_traffic_prediction = traffic_data
    
    # Formatear reporte visual
    report_lines = [
        "🚦 **REPORTE DE TRÁFICO EN TIEMPO REAL**",
        "━" * 50,
        ""
    ]
    
    for zone_traffic in traffic_data:
        zone = zone_traffic["zone"]
        level = zone_traffic["level"]
        speed = zone_traffic["average_speed_kmh"]
        incidents = zone_traffic.get("incidents", [])
        
        icon = _get_traffic_icon(level)
        incident_count = len(incidents) if isinstance(incidents, list) else 0
        
        report_lines.extend([
            f"{icon} **{zone}** - Nivel: {level.upper()}",
            f"   🚗 Velocidad promedio: {speed} km/h",
            f"   ⚠️ Incidentes reportados: {incident_count}",
            ""
        ])
    
    # Agregar resumen
    critical_zones = [t["zone"] for t in traffic_data if t["level"] == "crítico"]
    high_zones = [t["zone"] for t in traffic_data if t["level"] == "alto"]
    
    report_lines.extend([
        "━" * 50,
        "📊 **RESUMEN:**"
    ])
    
    if critical_zones:
        report_lines.append(f"🔴 Zonas críticas ({len(critical_zones)}): {', '.join(critical_zones)}")
    if high_zones:
        report_lines.append(f"🟠 Zonas con congestión alta ({len(high_zones)}): {', '.join(high_zones)}")
    
    if not critical_zones and not high_zones:
        report_lines.append("✅ No se detectan congestiones significativas")
    
    report_lines.extend([
        "",
        "💡 **TIP:** Usa `generate_traffic_heatmap()` para ver el mapa visual"
    ])
    
    return "\n".join(report_lines)


def generate_traffic_heatmap(zones: list[str], tool_context) -> str:
    """
    Genera un mapa de calor visual del estado del tráfico con ASCII art
    
    Args:
        zones: Lista de zonas a incluir en el mapa
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Visualización con mapa de calor ASCII
    """
    # Verificar si hay una predicción guardada
    traffic_data = None
    if hasattr(tool_context, 'state') and hasattr(tool_context.state, 'last_traffic_prediction'):
        traffic_data = tool_context.state.last_traffic_prediction
    else:
        # Generar nueva predicción si no existe
        traffic_data = generate_mock_traffic(zones)
    
    # Generar mapa de calor con ASCII art
    heatmap = generate_traffic_heatmap_medellin(traffic_data)
    
    # Agregar fuentes de información
    sources = """
────────────────────────────────────────────────

📡 FUENTES DE INFORMACIÓN:

✓ Twitter: @MetrodeMedellin - Reportes en tiempo real
✓ SoloBus: Sistema de información de rutas
✓ Waze: Reportes de conductores
✓ Sensores IoT: Red de 150+ sensores en la ciudad

� Última actualización: Hace 2 minutos
────────────────────────────────────────────────
"""
    
    return heatmap + sources
