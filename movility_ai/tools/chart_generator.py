# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Generador de visualizaciones con código para demo.
Genera diagramas y gráficos usando matplotlib, seaborn, plotly.
"""

import io
import base64
from typing import Dict, List, Optional

try:
    import matplotlib
    matplotlib.use('Agg')  # Backend sin GUI
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


def generate_traffic_heatmap_medellin(zones_data: List[Dict]) -> str:
    """
    Genera un mapa de calor ASCII art de tráfico en Medellín.
    
    Args:
        zones_data: Lista de zonas con niveles de tráfico
        
    Returns:
        String con visualización ASCII del mapa de calor
    """
    # Crear representación ASCII del mapa de Medellín
    ascii_map = """
    ╔════════════════════════════════════════╗
    ║     MAPA DE CALOR - TRÁFICO MEDELLÍN   ║
    ╚════════════════════════════════════════╝
    
              NORTE (Bello)
                   ⬆
                   │
        ┌──────────┼──────────┐
        │          │          │
        │  Castilla│ Aranjuez │
        │    🟡    │    🟢    │
        ├──────────┼──────────┤
    OESTE│ Laureles │  Centro  │ESTE
    ◄────┤    🟡    │    🟠    ├────►
        ├──────────┼──────────┤
        │El Poblado│ Envigado │
        │    🔴    │    🟢    │
        └──────────┼──────────┘
                   │
                   ⬇
              SUR (Sabaneta)
    
    LEYENDA:
    🟢 FLUIDO     Velocidad: >40 km/h
    🟡 MODERADO   Velocidad: 25-40 km/h
    🟠 ALTO       Velocidad: 10-25 km/h
    🔴 CRÍTICO    Velocidad: <10 km/h
    """
    
    # Agregar tabla de datos
    table = "\n📊 DATOS POR ZONA:\n"
    table += "┌────────────────┬─────────┬──────────────┐\n"
    table += "│ Zona           │ Estado  │ Velocidad    │\n"
    table += "├────────────────┼─────────┼──────────────┤\n"
    
    for zone_data in zones_data:
        zone = zone_data['zone']
        level = zone_data['level']
        speed = zone_data['average_speed_kmh']
        
        # Icono según nivel
        icon_map = {
            'bajo': '🟢',
            'medio': '🟡',
            'alto': '🟠',
            'crítico': '🔴'
        }
        icon = icon_map.get(level.lower(), '⚪')
        
        # Formatear fila
        table += f"│ {zone:<14} │ {icon} {level:<5} │ {speed:>3} km/h     │\n"
    
    table += "└────────────────┴─────────┴──────────────┘\n"
    
    return ascii_map + table


def generate_eco_dashboard_chart(metrics: Dict) -> str:
    """
    Genera un dashboard ecológico con gráficos de matplotlib.
    
    Args:
        metrics: Diccionario con métricas ecológicas
        
    Returns:
        String con imagen base64 embebida en markdown
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from io import BytesIO
        import base64
        
        co2_saved = metrics.get('co2_saved_kg', 0)
        calories = metrics.get('calories_burned', 0)
        eco_score = metrics.get('eco_score', 0)
        trees = metrics.get('trees_equivalent', 0)
        
        # Crear figura con 4 subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('🌱 Dashboard Ecológico 🌱', fontsize=18, fontweight='bold', color='#2d5016')
        
        # 1. CO2 Ahorrado (Barra horizontal)
        ax1.barh(['CO2 Ahorrado'], [co2_saved], color='#4CAF50', height=0.5)
        ax1.set_xlim(0, max(50, co2_saved * 1.2))
        ax1.set_xlabel('Kilogramos (kg)', fontsize=10)
        ax1.set_title(f'🌍 CO2 Ahorrado: {co2_saved:.1f} kg', fontsize=12, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
        ax1.text(co2_saved/2, 0, f'{co2_saved:.1f} kg', ha='center', va='center', 
                fontweight='bold', fontsize=14, color='white')
        
        # 2. Calorías Quemadas (Barra horizontal)
        ax2.barh(['Calorías'], [calories], color='#FF9800', height=0.5)
        ax2.set_xlim(0, max(3000, calories * 1.2))
        ax2.set_xlabel('Kilocalorías (kcal)', fontsize=10)
        ax2.set_title(f'🔥 Calorías Quemadas: {int(calories)} kcal', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        ax2.text(calories/2, 0, f'{int(calories)} kcal', ha='center', va='center',
                fontweight='bold', fontsize=14, color='white')
        
        # 3. Eco Score (Gauge/medidor circular)
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 10)
        ax3.axis('off')
        
        # Crear círculo de fondo
        circle_bg = patches.Circle((5, 5), 3.5, color='#e0e0e0', zorder=1)
        ax3.add_patch(circle_bg)
        
        # Crear círculo de progreso
        theta = (eco_score / 100) * 360
        color_score = '#4CAF50' if eco_score >= 80 else '#FFC107' if eco_score >= 60 else '#FF9800'
        wedge = patches.Wedge((5, 5), 3.5, 90, 90 + theta, color=color_score, zorder=2)
        ax3.add_patch(wedge)
        
        # Círculo interior blanco
        circle_inner = patches.Circle((5, 5), 2.5, color='white', zorder=3)
        ax3.add_patch(circle_inner)
        
        # Texto central
        ax3.text(5, 5.5, f'{eco_score}', ha='center', va='center', 
                fontsize=40, fontweight='bold', color=color_score)
        ax3.text(5, 4, '/100', ha='center', va='center', fontsize=14, color='gray')
        ax3.text(5, 2, '⭐ Eco Score', ha='center', va='center', fontsize=12, fontweight='bold')
        
        # 4. Árboles Equivalentes (Visualización)
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 10)
        ax4.axis('off')
        
        # Dibujar árboles
        num_trees = int(trees)
        partial_tree = trees - num_trees
        
        tree_positions = [(2, 5), (5, 5), (8, 5), (2, 2), (5, 2)]
        for i, (x, y) in enumerate(tree_positions[:min(5, num_trees + 1)]):
            if i < num_trees:
                ax4.text(x, y, '🌳', ha='center', va='center', fontsize=40)
            elif i == num_trees and partial_tree > 0:
                # Árbol parcial con transparencia simulada
                ax4.text(x, y, '🌳', ha='center', va='center', fontsize=40, alpha=0.5)
        
        ax4.text(5, 8, f'🌳 {trees:.2f} árboles/año', ha='center', va='center',
                fontsize=14, fontweight='bold', color='#2d5016')
        ax4.text(5, 0.5, 'Equivalente en absorción de CO2', ha='center', va='center',
                fontsize=10, color='gray')
        
        # Ajustar espaciado
        plt.tight_layout()
        
        # Guardar imagen como base64 para incrustar en markdown
        from io import BytesIO
        import base64
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        
        # Convertir a base64
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        
        # Retornar HTML con imagen embebida (mejor compatibilidad que markdown)
        html_output = f"""
<div style="text-align: center; margin: 20px 0;">
    <img src="data:image/png;base64,{image_base64}" alt="Dashboard Ecológico" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <p style="color: #666; font-size: 12px; margin-top: 10px;">📊 Dashboard generado con Python + Matplotlib</p>
</div>
"""
        return html_output
        
    except ImportError:
        # Fallback a ASCII si no hay matplotlib
        co2_saved = metrics.get('co2_saved_kg', 0)
        calories = metrics.get('calories_burned', 0)
        eco_score = metrics.get('eco_score', 0)
        trees = metrics.get('trees_equivalent', 0)
        
        dashboard = """
╔══════════════════════════════════════════════════╗
║          🌱 DASHBOARD ECOLÓGICO 🌱               ║
╚══════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────┐
│  CO2 AHORRADO                                   │
│  ████████████████░░░░░░░░░░ {:.1f} kg           │
│  🌍 vs. Carro particular                        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  CALORÍAS QUEMADAS                              │
│  ██████████████░░░░░░░░░░░░ {} kcal         │
│  🔥 Actividad física                            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  ECO SCORE                                      │
│  ████████████████████████░░ {}/100              │
│  ⭐ {}                              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  EQUIVALENCIA EN ÁRBOLES                        │
│  🌳 {:.2f} árboles/año                          │
│  Absorción anual de CO2                         │
└─────────────────────────────────────────────────┘
""".format(
            co2_saved,
            int(calories),
            eco_score,
            "🟢 EXCELENTE" if eco_score >= 80 else "🟡 BUENO" if eco_score >= 60 else "🟠 REGULAR",
            trees
        )
        
        return dashboard


def generate_route_map_ascii(origin: str, destination: str, segments: List[Dict]) -> str:
    """
    Genera un mapa de ruta visual en ASCII.
    
    Args:
        origin: Punto de origen
        destination: Punto de destino
        segments: Lista de segmentos de la ruta
        
    Returns:
        String con mapa de ruta en ASCII
    """
    route_map = f"""
╔════════════════════════════════════════════════╗
║     🗺️  MAPA DE RUTA MULTIMODAL               ║
╚════════════════════════════════════════════════╝

    📍 {origin}
         │
         │ {segments[0]['mode']} {_get_mode_icon(segments[0]['mode'])}
         ▼
"""
    
    # Agregar segmentos intermedios
    for i, segment in enumerate(segments[:-1]):
        location = segment.get('to_location', f'Punto {i+1}')
        next_mode = segments[i+1]['mode'] if i+1 < len(segments) else ''
        next_icon = _get_mode_icon(next_mode) if next_mode else ''
        
        route_map += f"""    🔵 {location}
         │
         │ {next_mode} {next_icon}
         ▼
"""
    
    route_map += f"""    🎯 {destination}

────────────────────────────────────────────────
"""
    
    # Agregar leyenda de segmentos
    route_map += "\n📋 SEGMENTOS:\n\n"
    
    for i, segment in enumerate(segments, 1):
        mode = segment['mode']
        icon = _get_mode_icon(mode)
        duration = segment.get('duration_minutes', 'N/A')
        
        route_map += f"  {i}. {icon} {mode.upper()} - {duration} min\n"
    
    return route_map


def _get_mode_icon(mode: str) -> str:
    """Retorna el icono del modo de transporte."""
    icons = {
        "metro": "🚇",
        "metrocable": "🚠",
        "bus": "🚌",
        "bicicleta": "🚴",
        "caminando": "🚶",
        "carro": "🚗",
        "moto": "🏍️",
        "tranvia": "🚊"
    }
    return icons.get(mode.lower(), "🚶")


def generate_event_alert_visual(event_data: Dict) -> str:
    """
    Genera visualización de alerta de evento.
    
    Args:
        event_data: Datos del evento detectado
        
    Returns:
        String con alerta visual
    """
    event_type = event_data.get('type', 'Evento')
    location = event_data.get('location', 'Ubicación desconocida')
    impact = event_data.get('impact_level', 'MEDIO')
    time = event_data.get('time', 'Ahora')
    
    # Icono según tipo
    type_icons = {
        'manifestación': '🚨',
        'protesta': '🚨',
        'obra': '🚧',
        'accidente': '🚗💥',
        'evento': '🎉',
        'clima': '🌧️',
        'metro': '🚇'
    }
    icon = type_icons.get(event_type.lower(), '⚠️')
    
    # Color según impacto
    impact_colors = {
        'CRÍTICO': '🔴',
        'ALTO': '🟠',
        'MEDIO': '🟡',
        'BAJO': '🟢'
    }
    impact_icon = impact_colors.get(impact.upper(), '🟡')
    
    alert = f"""
╔═══════════════════════════════════════════════╗
║        {icon}  ALERTA DE EVENTO  {icon}          ║
╚═══════════════════════════════════════════════╝

    🏷️  TIPO: {event_type.upper()}
    📍 UBICACIÓN: {location}
    🕐 HORA: {time}
    📊 IMPACTO: {impact_icon} {impact}

════════════════════════════════════════════════

    ⚠️  RECOMENDACIÓN:
    Considerar rutas alternativas para evitar
    demoras en el tráfico.

════════════════════════════════════════════════
"""
    
    return alert


def generate_city_insights_chart(insights_data: Dict) -> str:
    """
    Genera visualización de insights de ciudad.
    
    Args:
        insights_data: Datos de análisis urbano
        
    Returns:
        String con gráfico de insights
    """
    chart = """
╔══════════════════════════════════════════════════╗
║       📊 ANÁLISIS URBANO - INSIGHTS              ║
╚══════════════════════════════════════════════════╝

🚦 DISTRIBUCIÓN DE MODOS DE TRANSPORTE:

Metro      ████████████████████████░░░░░░ 28%
Bus        ██████████████████░░░░░░░░░░░░ 22%
Carro      ███████████████░░░░░░░░░░░░░░░ 18%
Moto       ████████████░░░░░░░░░░░░░░░░░░ 15%
Caminando  ████████░░░░░░░░░░░░░░░░░░░░░░ 10%
Bicicleta  ████░░░░░░░░░░░░░░░░░░░░░░░░░░  4%
Taxi/Uber  ███░░░░░░░░░░░░░░░░░░░░░░░░░░░  3%

────────────────────────────────────────────────

📈 TENDENCIAS:

↗️ Uso de Metro:      +8% (último año)
↗️ Uso de Bicicleta:  +15% (último año)
↘️ Uso de Carro:      -3% (último año)
↗️ Congestión:        +3% (último mes)

────────────────────────────────────────────────

🎯 ESTADÍSTICAS CLAVE:

• Viajes diarios: 6.5M
• Pasajeros Metro: 1.8M/día
• Velocidad promedio pico: 18 km/h
• Tiempo promedio viaje: 45 min
"""
    
    return chart
