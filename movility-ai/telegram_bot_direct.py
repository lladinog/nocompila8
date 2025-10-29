#!/usr/bin/env python3
"""
Bot de Telegram para MovilityAI - Versión directa con Gemini API
Compatible con Python 3.12 y 3.13
"""

import os
import json
import time
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validar configuración
if not TELEGRAM_TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN no encontrado en .env")
    exit(1)
if not GOOGLE_API_KEY:
    print("❌ Error: GOOGLE_API_KEY no encontrado en .env")
    exit(1)

print("🚀 MovilityAI Bot (Gemini Direct API)")
print("=" * 60)
print(f"✅ Token encontrado: {TELEGRAM_TOKEN[:20]}...")
print(f"✅ Google API Key: {GOOGLE_API_KEY[:25]}...")
print()

# URLs
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GOOGLE_API_KEY}"

# Contexto del sistema
SYSTEM_CONTEXT = """Eres MovilityAI, un asistente inteligente de movilidad urbana para Medellín, Colombia.

CAPACIDADES:
🚇 PathFinder Agent: Planifica rutas óptimas usando TransMilenio, Metro, buses y bicicletas
🚦 FlowSense Agent: Predice tráfico y sugiere rutas alternativas  
📊 Insight Agent: Analiza patrones de movilidad urbana
⚡ Pulse Agent: Monitorea tráfico en tiempo real
🌱 EcoTrack Agent: Calcula huella de carbono del transporte

DATOS DE MEDELLÍN:
- Metro: Tarifa $3,150 COP, horario 4:30 AM - 11:00 PM
- Zonas: Poblado, Centro, Laureles, Envigado, Bello, Itagüí, Robledo
- Principales vías: La 10, La 33, La 80, Las Palmas, Regional, Guayabal

Responde de forma concisa, útil y amigable. Usa emojis para mejor UX."""

def get_me():
    """Obtiene información del bot"""
    try:
        r = requests.get(f"{TELEGRAM_URL}/getMe", timeout=10)
        r.raise_for_status()
        result = r.json()
        return result.get("result") if result.get("ok") else None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def send_message(chat_id, text):
    """Envía un mensaje"""
    try:
        data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        r = requests.post(f"{TELEGRAM_URL}/sendMessage", json=data, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"❌ Error enviando: {e}")
        return None

def get_updates(offset=None):
    """Obtiene actualizaciones"""
    try:
        params = {"timeout": 30, "offset": offset}
        r = requests.get(f"{TELEGRAM_URL}/getUpdates", params=params, timeout=35)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"❌ Error updates: {e}")
        return None

def ask_gemini(question):
    """Consulta a Gemini AI"""
    try:
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{SYSTEM_CONTEXT}\n\nUsuario pregunta: {question}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000,
            }
        }
        
        r = requests.post(GEMINI_URL, json=payload, timeout=30)
        r.raise_for_status()
        result = r.json()
        
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0].get("content", {})
            parts = content.get("parts", [])
            if parts:
                return parts[0].get("text", "No pude generar una respuesta.")
        
        return "No pude generar una respuesta válida."
    
    except Exception as e:
        print(f"❌ Error Gemini: {e}")
        return f"❌ Error consultando IA: {str(e)}"

def process_message(chat_id, text, username):
    """Procesa un mensaje"""
    print(f"📩 @{username}: {text}")
    
    if text == "/start":
        response = """🚀 **¡Bienvenido a MovilityAI!**

Soy tu asistente inteligente de movilidad para Medellín.

**Puedo ayudarte con:**
🚇 Rutas óptimas (Metro, TransMilenio, buses)
🚦 Predicción de tráfico
📊 Análisis de movilidad
⚡ Monitoreo en tiempo real
🌱 Huella de carbono

**Ejemplos de preguntas:**
• "¿Cómo llego al Poblado?"
• "¿Cómo está el tráfico en la 80?"
• "Ruta más rápida al aeropuerto"
• "Opciones ecológicas para ir a Envigado"

¡Pregúntame lo que necesites! 🎯"""
    
    elif text == "/help":
        response = """📚 **Ayuda - MovilityAI**

**Comandos:**
/start - Bienvenida
/help - Esta ayuda
/test - Probar conexión

**Consultas:**
Escribe en lenguaje natural:
• Planificación de rutas
• Estado del tráfico
• Análisis de movilidad
• Opciones de transporte

**Datos útiles:**
• Metro: $3,150 COP (4:30 AM - 11:00 PM)
• Zonas: Poblado, Centro, Laureles, Envigado...
• Vías: La 10, La 33, La 80, Regional...

¿En qué puedo ayudarte? 😊"""
    
    elif text == "/test":
        response = "✅ Bot funcionando correctamente con Gemini 2.0 Flash Exp!"
    
    else:
        # Consultar a Gemini
        print("🤖 Consultando Gemini AI...")
        response = ask_gemini(text)
        print("✅ Respuesta generada")
    
    send_message(chat_id, response)
    print("✅ Enviada")

def main():
    """Loop principal"""
    print("🔍 Verificando bot...")
    bot_info = get_me()
    
    if not bot_info:
        print("❌ No se pudo conectar. Verifica el token.")
        return
    
    username = bot_info.get("username", "Unknown")
    bot_id = bot_info.get("id", "Unknown")
    
    print(f"✅ Bot conectado: @{username} (ID: {bot_id})")
    print(f"🔗 Link: https://t.me/{username}")
    print()
    print("=" * 60)
    print("🟢 Bot en ejecución. Esperando mensajes...")
    print("⏹️  Presiona Ctrl+C para detener")
    print("=" * 60)
    print()
    
    offset = None
    error_count = 0
    
    try:
        while True:
            result = get_updates(offset)
            
            if not result:
                error_count += 1
                if error_count >= 5:
                    print("❌ Demasiados errores. Deteniendo.")
                    break
                time.sleep(5)
                continue
            
            error_count = 0
            
            if not result.get("ok"):
                print(f"⚠️  Error: {result}")
                time.sleep(5)
                continue
            
            updates = result.get("result", [])
            
            for update in updates:
                offset = update.get("update_id", 0) + 1
                
                message = update.get("message")
                if message:
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")
                    username = message.get("from", {}).get("username", "Usuario")
                    
                    if chat_id and text:
                        try:
                            process_message(chat_id, text, username)
                        except Exception as e:
                            print(f"❌ Error: {e}")
                            send_message(chat_id, "❌ Ocurrió un error procesando tu mensaje.")
            
            if not updates:
                time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Bot detenido")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")

if __name__ == "__main__":
    main()
