# MovilityAI - Setup and Test Script
# Este script instala dependencias y ejecuta tests

Write-Host "🚀 MovilityAI - Configuración e Instalación" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que uv está instalado
Write-Host "📦 Verificando uv..." -ForegroundColor Yellow
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvInstalled) {
    Write-Host "❌ Error: uv no está instalado" -ForegroundColor Red
    Write-Host "Por favor instala uv desde: https://docs.astral.sh/uv/" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ uv está instalado" -ForegroundColor Green
Write-Host ""

# Instalar dependencias
Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
uv sync
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
Write-Host ""

# Ejecutar tests
Write-Host "🧪 Ejecutando tests..." -ForegroundColor Yellow
Write-Host ""
uv run pytest tests/unit/ -v
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ ¡Todos los tests pasaron correctamente!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️  Algunos tests fallaron - revisar output arriba" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 Setup completado" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Configura tus credenciales de Google Cloud en .env" -ForegroundColor White
Write-Host "2. Ejecuta: uv run python -m movility_ai" -ForegroundColor White
Write-Host "3. Para tests: uv run pytest tests/" -ForegroundColor White
Write-Host ""
