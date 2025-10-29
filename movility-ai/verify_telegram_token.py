#!/usr/bin/env python3
"""Verificar que el token de Telegram funciona correctamente"""

import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def verify_token():
    """Verifica el token de Telegram"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ No se encontró TELEGRAM_BOT_TOKEN en .env")
        return False
    
    print(f"🔍 Verificando token: {token[:15]}...{token[-10:]}\n")
    
    try:
        from telegram import Bot
        
        bot = Bot(token=token)
        
        # Obtener información del bot
        print("📡 Contactando a Telegram...")
        me = await bot.get_me()
        
        print("\n✅ ¡TOKEN VÁLIDO!\n")
        print("📋 Información del Bot:")
        print(f"   ID: {me.id}")
        print(f"   Nombre: {me.first_name}")
        print(f"   Username: @{me.username}")
        print(f"   Link: https://t.me/{me.username}")
        
        if me.can_join_groups:
            print(f"   ✅ Puede unirse a grupos")
        if me.can_read_all_group_messages:
            print(f"   ✅ Puede leer mensajes de grupo")
        
        print(f"\n🎯 Para probar:")
        print(f"   1. Abre: https://t.me/{me.username}")
        print(f"   2. Presiona START o envía /start")
        print(f"   3. El bot debería responder")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error verificando token: {e}\n")
        print("Posibles causas:")
        print("1. Token inválido o revocado")
        print("2. Sin conexión a internet")
        print("3. Bot eliminado por @BotFather")
        print("\n💡 Solución:")
        print("1. Ve a @BotFather en Telegram")
        print("2. Envía /mybots")
        print("3. Selecciona tu bot")
        print("4. Copia el API Token")
        print("5. Actualiza TELEGRAM_BOT_TOKEN en .env")
        return False

if __name__ == '__main__':
    result = asyncio.run(verify_token())
    sys.exit(0 if result else 1)
