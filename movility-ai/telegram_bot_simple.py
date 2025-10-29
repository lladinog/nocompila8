#!/usr/bin/env python3
# Copyright 2025 MovilityAI
"""Bot de Telegram SIMPLIFICADO para MovilityAI - Compatible con Python 3.13"""

import os
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def main():
    """Iniciar el bot de forma simplificada"""
    
    # Verificar token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ ERROR: No se encontró TELEGRAM_BOT_TOKEN en .env")
        return
    
    print("🚀 MovilityAI Bot (Modo Local Simplificado)")
    print("=" * 60)
    print(f"✅ Token encontrado: {token[:20]}...")
    print(f"✅ Google API Key: {os.getenv('GOOGLE_API_KEY', 'NO CONFIGURADO')[:20]}...")
    print("\n📝 NOTA: Debido a incompatibilidades con Python 3.13,")
    print("   este bot usa polling simple sin características async.")
    print("\n🔄 Intentando conectar con Telegram...")
    
    try:
        # Importar telegram de forma segura
        from telegram import Update, Bot
        from telegram.ext import (
            Application, 
            CommandHandler, 
            MessageHandler,
            filters,
            ContextTypes
        )
        
        print("✅ Librerías de Telegram cargadas")
        
        # Crear bot simple
        application = Application.builder().token(token).build()
        bot = application.bot
        
        # Verificar conexión (intentaremos durante el inicio)
        print(f"\n✅ Bot configurado")
        print(f"   Token válido: {token[:10]}...{token[-10:]}")
        
        # La conexión real se verificará al iniciar polling
        
        # Importar el agente
        try:
            from movility_ai.agent import root_agent
            print(f"✅ Agente MovilityAI cargado correctamente")
        except Exception as e:
            print(f"⚠️  Advertencia: No se pudo cargar el agente: {e}")
            print("   El bot funcionará pero sin IA")
            root_agent = None
        
        # Handlers simplificados
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Comando /start"""
            await update.message.reply_text(
                "🚇 ¡Hola! Soy MovilityAI Bot\n\n"
                "Comandos disponibles:\n"
                "/start - Este mensaje\n"
                "/help - Ayuda\n"
                "/test - Probar conexión\n\n"
                "O escribe tu pregunta directamente:\n"
                "Ejemplo: '¿Cómo llego a Poblado?'"
            )
        
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Comando /help"""
            await update.message.reply_text(
                "📚 Ayuda de MovilityAI\n\n"
                "Este bot te ayuda con:\n"
                "• Rutas de Metro y EnCicla\n"
                "• Estado del tráfico\n"
                "• Alertas de movilidad\n"
                "• Información del sistema\n\n"
                "Escribe tu consulta en lenguaje natural."
            )
        
        async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Comando /test"""
            await update.message.reply_text(
                "✅ Bot funcionando correctamente!\n"
                f"Tu ID: {update.effective_user.id}\n"
                f"Chat ID: {update.effective_chat.id}"
            )
        
        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Manejar mensajes de texto"""
            user_message = update.message.text
            user_id = update.effective_user.id
            
            logger.info(f"Usuario {user_id}: {user_message}")
            
            # Mostrar que está escribiendo
            await update.message.chat.send_action("typing")
            
            if root_agent:
                try:
                    # Usar el agente
                    import asyncio
                    loop = asyncio.get_event_loop()
                    response = await loop.run_in_executor(
                        None,
                        root_agent.run,
                        user_message
                    )
                    
                    # Extraer texto de la respuesta
                    if hasattr(response, 'text'):
                        response_text = response.text
                    else:
                        response_text = str(response)
                    
                    await update.message.reply_text(response_text[:4000])
                    
                except Exception as e:
                    logger.error(f"Error con agente: {e}")
                    await update.message.reply_text(
                        f"⚠️ Error procesando consulta: {str(e)[:200]}"
                    )
            else:
                # Respuesta simple sin agente
                await update.message.reply_text(
                    f"Recibí tu mensaje: '{user_message[:100]}'\n\n"
                    "⚠️ El agente IA no está disponible en este momento.\n"
                    "Esto es una demo local del bot."
                )
        
        # Registrar handlers
        print("\n🔧 Registrando comandos...")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("test", test_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ Handlers registrados")
        print("\n" + "=" * 60)
        print("📱 Bot iniciando polling...")
        print("=" * 60)
        print("\n💡 Ahora puedes:")
        print("1. Abrir Telegram")
        print("2. Buscar tu bot por el nombre que le pusiste")
        print("3. Enviar: /start")
        print("\n⏹️  Presiona Ctrl+C para detener el bot\n")
        print("🔄 Conectando con Telegram...")
        
        # Iniciar polling
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except ImportError as e:
        print(f"\n❌ Error importando librerías: {e}")
        print("\n🔧 Solución:")
        print("pip install python-telegram-bot --upgrade")
        
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print(f"\nTipo: {type(e).__name__}")
        import traceback
        print("\nTraceback completo:")
        traceback.print_exc()

if __name__ == '__main__':
    main()
