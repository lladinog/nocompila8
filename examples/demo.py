# Copyright 2025 MovilityAI
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
Ejemplo de uso de MovilityAI

Este script demuestra cómo usar el sistema multiagente para:
1. Planificar una ruta multimodal
2. Consultar predicción de tráfico
3. Generar un dashboard de movilidad
"""

import os
import sys
from datetime import datetime

# Asegurarse de que el paquete esté en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def ejemplo_pathfinder():
    """Ejemplo de PathFinder Agent - Planificación de ruta"""
    print("\n" + "="*60)
    print("🗺️  EJEMPLO 1: PathFinder Agent - Planificación de Ruta")
    print("="*60 + "\n")
    
    from movility_ai.sub_agents.pathfinder.tools import calculate_multimodal_route
    
    # Consulta de ruta
    origen = "Universidad de Antioquia"
    destino = "Parque Lleras, El Poblado"
    
    preferencias = {
        "priority": "time",  # puede ser: time, cost, sustainability
        "use_bike": True,
        "max_budget": 5000,
    }
    
    print(f"📍 Origen: {origen}")
    print(f"📍 Destino: {destino}")
    print(f"⚙️  Preferencias: {preferencias}\n")
    
    resultado = calculate_multimodal_route(
        origin=origen,
        destination=destino,
        preferences=preferencias,
        current_time=datetime.now().isoformat()
    )
    
    if resultado["recommended_route"]:
        ruta = resultado["recommended_route"]
        print(f"✅ Ruta Recomendada: {ruta['name']}")
        print(f"⏱️  Tiempo: {ruta['total_duration']} minutos")
        print(f"💰 Costo: ${ruta['total_cost']} COP")
        print(f"🌱 CO2: {ruta['co2_kg']} kg")
        print(f"\n📋 Segmentos:")
        for i, seg in enumerate(ruta['segments'], 1):
            print(f"   {i}. {seg['instruction']} ({seg.get('duration', 'N/A')} min)")
    
    if resultado["alerts"]:
        print(f"\n⚠️  Alertas:")
        for alerta in resultado["alerts"]:
            print(f"   {alerta}")


def ejemplo_flowsense():
    """Ejemplo de FlowSense Agent - Predicción de tráfico"""
    print("\n" + "="*60)
    print("🚦 EJEMPLO 2: FlowSense Agent - Predicción de Tráfico")
    print("="*60 + "\n")
    
    from movility_ai.sub_agents.flowsense.predictor import predict_traffic_congestion
    
    # Predicción de tráfico
    resultado = predict_traffic_congestion(
        target_time=None,  # Ahora
        zone=None,  # Toda la ciudad
        weather_condition="clear"
    )
    
    print(f"🕐 Hora: {datetime.now().strftime('%H:%M')}")
    print(f"📊 Estado General: {resultado['general_status']}\n")
    
    print("🔴 Zonas Críticas:")
    for zone_id, data in resultado['current_conditions'].items():
        if data['status'] in ['CONGESTIONADO', 'CRÍTICO']:
            print(f"   {data['emoji']} {data['name']}: {data['status']} ({data['level']*100:.0f}%)")
            print(f"      Causas: {', '.join(data['causes'])}")
    
    print(f"\n📈 Predicción a 30 minutos:")
    for zone_id, prediccion in resultado['prediction_30min'].items():
        if 'Aumentará' in prediccion or 'Mejorará' in prediccion:
            zone_name = resultado['current_conditions'][zone_id]['name']
            print(f"   • {zone_name}: {prediccion}")


def ejemplo_insight():
    """Ejemplo de Insight Agent - Dashboard de movilidad"""
    print("\n" + "="*60)
    print("📊 EJEMPLO 3: Insight Agent - Dashboard de Movilidad")
    print("="*60 + "\n")
    
    from movility_ai.sub_agents.insight.analytics import (
        generate_mobility_dashboard,
        analyze_critical_zones
    )
    
    # Generar dashboard
    dashboard = generate_mobility_dashboard(period_days=30)
    
    print(f"📅 Período: {dashboard['period']['days']} días")
    print(f"   ({dashboard['period']['start_date']} a {dashboard['period']['end_date']})\n")
    
    print("🎯 KPIs Principales:")
    kpis = dashboard['kpis']
    print(f"   • Viajes diarios promedio: {kpis['daily_avg_trips']:,}")
    print(f"   • Tiempo promedio viaje: {kpis['avg_trip_duration_min']} min")
    print(f"   • Costo promedio viaje: ${kpis['avg_trip_cost_cop']:,} COP")
    print(f"   • CO2 total generado: {kpis['total_co2_tons']} toneladas")
    
    print(f"\n🚌 Distribución Modal:")
    modal = dashboard['modal_split']
    print(f"   • Transporte público: {modal['public_transport']['percentage']:.1f}%")
    print(f"   • Vehículo privado: {modal['private_vehicle']['percentage']:.1f}%")
    print(f"   • Movilidad activa: {modal['active_mobility']['percentage']:.1f}%")
    
    print(f"\n🔥 Top 3 Zonas Críticas:")
    for i, zona in enumerate(dashboard['top_critical_zones'][:3], 1):
        print(f"   {i}. {zona['name']}")
        print(f"      Congestión promedio: {zona['avg_congestion_pct']}%")
        print(f"      Viajes diarios: {zona['daily_trips']:,}")
    
    print(f"\n💡 Insights Clave:")
    for i, insight in enumerate(dashboard['key_insights'][:3], 1):
        print(f"   {i}. {insight}")
    
    print(f"\n🎯 Recomendaciones:")
    for i, rec in enumerate(dashboard['recommendations'][:3], 1):
        print(f"   {i}. {rec}")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "🚦"*30)
    print("   MOVILITYAI - Sistema Inteligente de Movilidad Urbana")
    print("   Medellín, Colombia")
    print("🚦"*30)
    
    try:
        # Ejemplo 1: Planificación de ruta
        ejemplo_pathfinder()
        
        # Ejemplo 2: Predicción de tráfico
        ejemplo_flowsense()
        
        # Ejemplo 3: Dashboard y analytics
        ejemplo_insight()
        
        print("\n" + "="*60)
        print("✅ Todos los ejemplos ejecutados correctamente")
        print("="*60 + "\n")
        
        print("💡 Para usar el sistema completo con Gemini, ejecuta:")
        print("   uv run python -m movility_ai")
        print("\n📝 No olvides configurar GOOGLE_API_KEY en .env")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
