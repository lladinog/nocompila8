# Script PowerShell para ejecutar ADK Web UI para MovilityAI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Iniciando ADK Web UI - MovilityAI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
Set-Location $PSScriptRoot

# Cargar variables de entorno desde .env
$envFile = Join-Path $PSScriptRoot "movility_ai\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, 'Process')
        }
    }
}

# Verificar que la API key esté configurada
if (-not $env:GOOGLE_API_KEY) {
    Write-Host "ERROR: GOOGLE_API_KEY no esta configurada" -ForegroundColor Red
    Write-Host "Por favor, configurala en movility_ai/.env" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[OK] API Key configurada correctamente" -ForegroundColor Green
Write-Host "Iniciando servidor ADK Web..." -ForegroundColor Yellow
Write-Host ""
Write-Host "IMPORTANTE: En el navegador, selecciona 'movility_ai' del dropdown" -ForegroundColor Yellow
Write-Host ""
Write-Host "La interfaz estara disponible en: " -NoNewline
Write-Host "http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Ejecutar ADK Web desde el directorio raiz
# El ADK detectara automaticamente las carpetas con agentes
adk web
