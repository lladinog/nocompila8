# Solución: Telegram Bloqueado (WinError 10051)

## Problema
El error `WinError 10051` indica que `api.telegram.org` está bloqueado por:
- Firewall corporativo/educativo
- ISP bloqueando Telegram
- Restricciones regionales
- Antivirus/Security software

## Soluciones Disponibles

### ✅ Opción 1: Usar VPN o Proxy
1. **Instalar VPN** (recomendado):
   - Windscribe (gratis)
   - ProtonVPN (gratis)
   - Cualquier VPN de confianza

2. **Activar VPN** y ejecutar:
   ```bash
   .\.venv_telegram\Scripts\python.exe movility-ai\telegram_bot_direct.py
   ```

### ✅ Opción 2: Usar Hotspot del celular
1. Activa el hotspot/tethering en tu celular
2. Conecta tu PC al hotspot
3. Ejecuta el bot

### ✅ Opción 3: Webhook con ngrok (sin necesidad de acceso directo)
1. **Instalar ngrok**: https://ngrok.com/download
2. **Crear túnel**:
   ```bash
   ngrok http 8084
   ```
3. **Configurar webhook** (el bot se conecta a Telegram una sola vez):
   ```python
   # Bot con webhook en lugar de polling
   ```

### ✅ Opción 4: Servidor web local (sin Telegram)
Ya tienes el servidor ADK funcionando. Podemos crear una interfaz web simple.

## Recomendación
**Usa una VPN** (Opción 1) - Es la solución más rápida y confiable.

## Verificar si funciona
```bash
# Probar conexión
curl https://api.telegram.org

# O con Python
python -c "import requests; print(requests.get('https://api.telegram.org').status_code)"
```

Si el código es 200, Telegram está accesible.
