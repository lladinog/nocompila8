"""
Servidor de desarrollo para MovilityAI usando Google ADK Dev Server

Este script inicia el servidor de desarrollo de Google ADK que proporciona
una interfaz web para interactuar con los agentes.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar API Key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ ERROR: No se encontró GOOGLE_API_KEY en .env")
    print("Por favor configura tu API key en el archivo .env")
    exit(1)

print("\n" + "🚦"*30)
print("   MOVILITYAI - Servidor de Desarrollo")
print("   Google ADK Dev Server")
print("🚦"*30 + "\n")

print(f"✅ API Key configurada: {api_key[:20]}...\n")

try:
    # Importar el agente principal
    from movility_ai.agent import root_agent
    
    print("📦 Agente cargado:")
    print(f"   • Nombre: {root_agent.name}")
    print(f"   • Modelo: {root_agent.model}")
    print(f"   • Sub-agentes: {len(root_agent.sub_agents)}")
    for agent in root_agent.sub_agents:
        print(f"     - {agent.name}")
    
    print("\n" + "="*60)
    print("🚀 Iniciando servidor de desarrollo...")
    print("="*60 + "\n")
    
    # Iniciar el servidor de desarrollo de ADK
    from google.adk import dev_server
    
    dev_server.start(
        agent=root_agent,
        port=8000,
        reload=True  # Auto-reload en cambios
    )
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n💡 Instalando servidor de desarrollo...")
    import subprocess
    subprocess.check_call([
        "pip", "install", "google-adk[dev]"
    ])
    print("\n✅ Instalación completada. Por favor ejecuta el script nuevamente.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Intentando método alternativo...")
    
    # Método alternativo: usar el servidor ADK directamente
    try:
        from google.adk.cli import main as adk_main
        import sys
        
        # Simular argumentos de línea de comandos
        sys.argv = ['adk', 'serve', '--agent', 'movility_ai.agent:root_agent', '--port', '8000']
        adk_main()
        
    except Exception as e2:
        print(f"❌ Error en método alternativo: {e2}")
        print("\n" + "="*60)
        print("📝 INSTRUCCIONES MANUALES")
        print("="*60)
        print("\nEjecuta uno de estos comandos en la terminal:\n")
        print("Opción 1 - Usando ADK CLI:")
        print("   adk serve --agent movility_ai.agent:root_agent --port 8000\n")
        print("Opción 2 - Usando Python module:")
        print("   python -m google.adk.cli serve --agent movility_ai.agent:root_agent\n")
        print("Opción 3 - Usando script directo:")
        print("   python -m google.adk serve movility_ai.agent:root_agent\n")
        print("="*60)
