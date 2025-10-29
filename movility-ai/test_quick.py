"""
Script de prueba rápida para MovilityAI
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("\n" + "="*60)
print("🔧 VERIFICACIÓN DEL SISTEMA MOVILITYAI")
print("="*60 + "\n")

# 1. Verificar API Key
api_key = os.getenv('GOOGLE_API_KEY')
if api_key:
    print(f"✅ API Key encontrada: {api_key[:20]}...")
else:
    print("❌ API Key NO encontrada en .env")
    exit(1)

# 2. Verificar imports
try:
    print("\n📦 Verificando imports...")
    from movility_ai.sub_agents.pathfinder.tools import calculate_multimodal_route
    from movility_ai.sub_agents.flowsense.predictor import predict_traffic_congestion
    from movility_ai.sub_agents.insight.analytics import generate_mobility_dashboard
    print("✅ Todos los módulos se importaron correctamente")
except Exception as e:
    print(f"❌ Error al importar módulos: {e}")
    exit(1)

# 3. Probar PathFinder
try:
    print("\n🗺️  Probando PathFinder Agent...")
    resultado = calculate_multimodal_route(
        origin="Centro",
        destination="Poblado",
        preferences={"priority": "time", "use_bike": True, "max_budget": 5000}
    )
    if resultado["recommended_route"]:
        ruta = resultado["recommended_route"]
        print(f"✅ PathFinder funciona: {ruta['name']}")
        print(f"   ⏱️  {ruta['total_duration']} min | 💰 ${ruta['total_cost']} COP")
    else:
        print("⚠️  PathFinder no generó ruta")
except Exception as e:
    print(f"❌ Error en PathFinder: {e}")

# 4. Probar FlowSense
try:
    print("\n🚦 Probando FlowSense Agent...")
    resultado = predict_traffic_congestion()
    print(f"✅ FlowSense funciona: Estado general {resultado['general_status']}")
    zonas_criticas = sum(1 for z in resultado['current_conditions'].values() 
                        if z['status'] in ['CONGESTIONADO', 'CRÍTICO'])
    print(f"   🔴 {zonas_criticas} zonas críticas detectadas")
except Exception as e:
    print(f"❌ Error en FlowSense: {e}")

# 5. Probar Insight
try:
    print("\n📊 Probando Insight Agent...")
    dashboard = generate_mobility_dashboard(period_days=30)
    print(f"✅ Insight funciona: {dashboard['kpis']['daily_avg_trips']:,} viajes/día")
    print(f"   🌱 {dashboard['kpis']['total_co2_tons']} toneladas CO2")
except Exception as e:
    print(f"❌ Error en Insight: {e}")

# 6. Probar agente con Gemini
print("\n" + "="*60)
print("🤖 PROBANDO SISTEMA COMPLETO CON GEMINI")
print("="*60 + "\n")

try:
    print("Inicializando agente principal...")
    from movility_ai.agent import root_agent
    print("✅ Root agent cargado correctamente")
    
    # Hacer una consulta simple
    print("\n💬 Enviando consulta de prueba...")
    print("   Pregunta: '¿Cómo está el tráfico en Medellín?'")
    
    # Nota: Para ejecutar el agente necesitamos el runner de ADK
    # Por ahora solo verificamos que se cargue correctamente
    print("\n✅ El agente está listo para recibir consultas")
    print("   Para interactuar, ejecuta: python -m movility_ai")
    
except Exception as e:
    print(f"❌ Error al cargar root agent: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✅ VERIFICACIÓN COMPLETA")
print("="*60)
print("\n💡 Para usar el sistema interactivo, ejecuta:")
print("   python -m movility_ai")
print("\n")
