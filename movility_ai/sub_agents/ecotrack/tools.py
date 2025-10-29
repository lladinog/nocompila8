"""
Herramientas para EcoTrack Agent
"""

from movility_ai.tools.data_mock_tool import generate_mock_eco_metrics
from movility_ai.tools.visualizer_tool import generate_eco_dashboard as viz_eco_dashboard


# Factores de emisión de CO2 por modo (g/km)
CO2_FACTORS = {
    "caminando": 0,
    "bicicleta": 0,
    "metro": 20,
    "metrocable": 20,
    "tranvia": 20,
    "bus": 60,
    "moto": 90,
    "carro": 150
}

# Calorías quemadas por modo (kcal/km)
CALORIES_FACTORS = {
    "caminando": 50,
    "bicicleta": 30,
    "metro": 0,
    "metrocable": 0,
    "tranvia": 0,
    "bus": 0,
    "moto": 0,
    "carro": 0
}


def _get_eco_icon(transport_mode: str) -> str:
    """Devuelve el emoji ecológico del modo de transporte"""
    icons = {
        "caminando": "🚶",
        "bicicleta": "🚴",
        "metro": "🚇",
        "metrocable": "🚡",
        "bus": "🚌",
        "tranvia": "🚊",
        "moto": "🏍️",
        "carro": "🚗"
    }
    return icons.get(transport_mode.lower(), "🚀")


def _calculate_eco_score(transport_mode: str) -> int:
    """Calcula un score ecológico de 0-100"""
    scores = {
        "caminando": 100,
        "bicicleta": 100,
        "metro": 90,
        "metrocable": 90,
        "tranvia": 90,
        "bus": 70,
        "moto": 40,
        "carro": 20
    }
    return scores.get(transport_mode.lower(), 50)


def calculate_eco_metrics(transport_mode: str, distance_km: float, tool_context) -> str:
    """
    Calcula métricas ecológicas de un viaje
    
    Args:
        transport_mode: Modo de transporte utilizado
        distance_km: Distancia recorrida en kilómetros
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Reporte formateado con métricas ecológicas
    """
    # Calcular emisiones del modo seleccionado
    co2_emitted = CO2_FACTORS.get(transport_mode.lower(), 100) * distance_km
    
    # Calcular CO2 que se habría emitido en carro
    co2_if_car = CO2_FACTORS["carro"] * distance_km
    co2_saved = co2_if_car - co2_emitted
    
    # Calcular calorías quemadas
    calories_burned = CALORIES_FACTORS.get(transport_mode.lower(), 0) * distance_km
    
    # Calcular árboles equivalentes (1 árbol absorbe ~21kg CO2/año)
    trees_equivalent = co2_saved / 1000 / 21  # Convertir g a kg, dividir por 21
    
    # Calcular eco score
    eco_score = _calculate_eco_score(transport_mode)
    
    # Guardar métricas en contexto
    metrics_data = {
        "transport_mode": transport_mode,
        "distance_km": distance_km,
        "co2_emitted_g": co2_emitted,
        "co2_saved_g": co2_saved,
        "calories_burned": calories_burned,
        "eco_score": eco_score,
        "trees_equivalent": trees_equivalent
    }
    
    if hasattr(tool_context, 'state'):
        tool_context.state.last_eco_metrics = metrics_data
    
    # Formatear reporte visual
    icon = _get_eco_icon(transport_mode)
    report_lines = [
        "🌱 **ECOTRACK - MÉTRICAS ECOLÓGICAS**",
        "━" * 50,
        "",
        f"{icon} **Modo:** {transport_mode.capitalize()}",
        f"📏 **Distancia:** {distance_km} km",
        "",
        "♻️ **IMPACTO AMBIENTAL:**",
        f"   💨 CO2 emitido: {co2_emitted:.1f}g",
        f"   💚 CO2 ahorrado vs. carro: {co2_saved:.1f}g",
        f"   🌳 Árboles equivalentes: {trees_equivalent:.3f}",
        ""
    ]
    
    # Agregar calorías si aplica
    if calories_burned > 0:
        report_lines.extend([
            "💪 **EJERCICIO:**",
            f"   🔥 Calorías quemadas: {calories_burned:.0f} kcal",
            ""
        ])
    
    # Agregar eco score con barra visual
    score_bar = "█" * (eco_score // 10) + "░" * (10 - (eco_score // 10))
    report_lines.extend([
        f"📊 **ECO SCORE:** {eco_score}/100",
        f"   [{score_bar}]",
        ""
    ])
    
    # Sugerir alternativas más ecológicas
    if eco_score < 90:
        report_lines.extend([
            "💡 **ALTERNATIVAS MÁS ECOLÓGICAS:**"
        ])
        
        if transport_mode.lower() not in ["caminando", "bicicleta"]:
            report_lines.append("   🚴 Considera usar bicicleta (100% eco)")
        if transport_mode.lower() not in ["metro", "metrocable", "tranvia"]:
            report_lines.append("   🚇 El metro es altamente eficiente (90% eco)")
        
        report_lines.append("")
    
    report_lines.extend([
        "━" * 50,
        "🌍 **¡Cada viaje ecológico cuenta!** 💚"
    ])
    
    return "\n".join(report_lines)


def generate_eco_dashboard(user_trips: int, tool_context) -> str:
    """
    Genera dashboard personalizado de sostenibilidad
    
    Args:
        user_trips: Número de viajes realizados por el usuario
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Dashboard visual con logros y progreso ecológico
    """
    # Generar métricas mock acumuladas
    dashboard_data = generate_mock_eco_metrics(user_trips=user_trips)
    
    # Generar visualización usando la herramienta de visualización
    dashboard_json = viz_eco_dashboard(dashboard_data)
    
    # Agregar contexto adicional y celebración
    co2_saved = dashboard_data.get("co2_saved_kg", 0)
    calories = dashboard_data.get("calories_burned", 0)
    trees = dashboard_data.get("trees_equivalent", 0)
    eco_score = dashboard_data.get("eco_score", 0)
    
    result_lines = [
        "🎉 **TU DASHBOARD ECOLÓGICO** 🎉",
        "━" * 50,
        "",
        f"📊 **VIAJES REGISTRADOS:** {user_trips}",
        "",
        dashboard_json,
        "",
        "━" * 50,
        "🏆 **LOGROS DESBLOQUEADOS:**"
    ]
    
    # Agregar logros según progreso
    if co2_saved > 1:
        result_lines.append("   ✅ **Guardián del Aire:** Ahorraste más de 1kg de CO2")
    if calories > 500:
        result_lines.append("   ✅ **Atleta Urbano:** Quemaste más de 500 calorías")
    if user_trips >= 10:
        result_lines.append("   ✅ **Viajero Consciente:** Completaste 10 viajes ecológicos")
    if eco_score >= 80:
        result_lines.append("   ✅ **Héroe Verde:** Eco score superior a 80")
    
    result_lines.extend([
        "",
        "💡 **META PRÓXIMA:** 100 viajes ecológicos = 10kg CO2 ahorrados",
        "",
        "🌍 ¡Sigue así! Cada viaje sostenible mejora nuestra ciudad 💚"
    ])
    
    return "\n".join(result_lines)
