#!/usr/bin/env python3
"""
Bot de Telegram para MovilityAI usando API REST directa
Compatible con Python 3.12 y 3.13
"""

import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

# Configurar path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Cargar variables de entorno
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validar configuración
if not TELEGRAM_TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN no encontrado en .env")
    sys.exit(1)
if not GOOGLE_API_KEY:
    print("❌ Error: GOOGLE_API_KEY no encontrado en .env")
    sys.exit(1)

print("🚀 MovilityAI Bot (API REST)")
print("=" * 60)
print(f"✅ Token encontrado: {TELEGRAM_TOKEN[:20]}...")
print(f"✅ Google API Key: {GOOGLE_API_KEY[:25]}...")
print()

# URL base de la API de Telegram
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Cargar el agente de MovilityAI
print("🔄 Cargando agente MovilityAI...")
try:
    # Intentar cargar desde el directorio raíz primero
    sys.path.insert(0, parent_dir)
    from movility_ai.agent import root_agent
    print("✅ Agente MovilityAI cargado correctamente")
    print(f"   Agentes disponibles: {len(root_agent.sub_agents)}")
except Exception as e:
    print(f"❌ Error cargando agente: {e}")
    print(f"   Ruta buscada: {parent_dir}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def get_me():
    """Obtiene información del bot"""
    try:
        response = requests.get(f"{BASE_URL}/getMe", timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("ok"):
            bot_info = result.get("result", {})
            return bot_info
        return None
    except Exception as e:
        print(f"❌ Error obteniendo info del bot: {e}")
        return None

def send_message(chat_id, text, parse_mode="Markdown"):
    """Envía un mensaje al chat"""
    try:
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        response = requests.post(f"{BASE_URL}/sendMessage", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error enviando mensaje: {e}")
        return None

def get_updates(offset=None):
    """Obtiene actualizaciones (mensajes nuevos)"""
    try:
        params = {"timeout": 30, "offset": offset}
        response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=35)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error obteniendo updates: {e}")
        return None

def process_message(chat_id, text, username):
    """Procesa un mensaje del usuario"""
    print(f"📩 Mensaje de @{username}: {text}")
    
    # Comandos especiales
    if text == "/start":
        response = """🚀 **¡Bienvenido a MovilityAI!**

Soy tu asistente inteligente para movilidad en Medellín.

Puedo ayudarte con:
🚇 Rutas de transporte óptimas
🚦 Pronósticos de tráfico en tiempo real
📊 Análisis de movilidad urbana
🚨 Alertas de contingencias

Pregúntame lo que necesites. Por ejemplo:
• "¿Cómo llego al Poblado?"
• "¿Cómo está el tráfico en la 80?"
• "Rutas alternativas a la Universidad"

¡Comencemos! 🚀"""
        
    elif text == "/help":
        response = """📚 **Ayuda - MovilityAI**

**Comandos:**
/start - Mensaje de bienvenida
/help - Esta ayuda
/test - Probar conexión

**Consultas:**
Escribe en lenguaje natural tus preguntas sobre:
• Rutas y transporte
• Estado del tráfico
• Análisis de movilidad
• Contingencias y alertas

**Ejemplos:**
• "Ruta más rápida al aeropuerto"
• "Tráfico en La 10"
• "Alternativas para llegar a Envigado"

¿En qué te puedo ayudar? 😊"""
    
    elif text == "/test":
        response = "✅ ¡Bot funcionando correctamente! Pregúntame sobre movilidad en Medellín."
    
    else:
        # Consulta al agente de IA
        print("🤖 Consultando al agente...")
        try:
            agent_response = root_agent.run(text)
            
            # Extraer el texto de la respuesta
            if hasattr(agent_response, 'text'):
                response = agent_response.text
            elif hasattr(agent_response, 'content'):
                response = agent_response.content
            elif isinstance(agent_response, str):
                response = agent_response
            else:
                response = str(agent_response)
            
            # Limitar longitud
            if len(response) > 4000:
                response = response[:4000] + "\n\n... (respuesta truncada)"
                
            print("✅ Respuesta del agente generada")
        except Exception as e:
            print(f"❌ Error consultando agente: {e}")
            response = f"❌ Lo siento, tuve un problema procesando tu consulta.\n\nError: {str(e)}"
    
    # Enviar respuesta
    send_message(chat_id, response)
    print("✅ Respuesta enviada")

def main():
    """Loop principal del bot"""
    # Verificar bot
    print("\n🔍 Verificando bot...")
    bot_info = get_me()
    
    if not bot_info:
        print("❌ No se pudo conectar con Telegram. Verifica el token.")
        return
    
    bot_username = bot_info.get("username", "Unknown")
    bot_id = bot_info.get("id", "Unknown")
    
    print(f"✅ Bot conectado: @{bot_username} (ID: {bot_id})")
    print(f"🔗 Link: https://t.me/{bot_username}")
    print()
    print("=" * 60)
    print("🟢 Bot en ejecución. Esperando mensajes...")
    print("⏹️  Presiona Ctrl+C para detener")
    print("=" * 60)
    print()
    
    offset = None
    error_count = 0
    max_errors = 5
    
    try:
        while True:
            # Obtener actualizaciones
            result = get_updates(offset)
            
            if not result:
                error_count += 1
                if error_count >= max_errors:
                    print(f"❌ Demasiados errores ({error_count}). Deteniendo bot.")
                    break
                time.sleep(5)
                continue
            
            error_count = 0  # Reset error count on success
            
            if not result.get("ok"):
                print(f"⚠️  Error en respuesta: {result}")
                time.sleep(5)
                continue
            
            updates = result.get("result", [])
            
            for update in updates:
                # Actualizar offset
                offset = update.get("update_id", 0) + 1
                
                # Procesar mensaje
                message = update.get("message")
                if message:
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")
                    username = message.get("from", {}).get("username", "Usuario")
                    
                    if chat_id and text:
                        try:
                            process_message(chat_id, text, username)
                        except Exception as e:
                            print(f"❌ Error procesando mensaje: {e}")
                            send_message(chat_id, "❌ Lo siento, ocurrió un error procesando tu mensaje.")
            
            # Pequeña pausa entre requests
            if not updates:
                time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Bot detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
