# MovilityAI - Setup Simple
Write-Host "MovilityAI - Setup" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
python --version
Write-Host ""

# Paso 2: Crear entorno virtual
Write-Host "2. Creando entorno virtual..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "   Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "   Entorno virtual ya existe" -ForegroundColor Green
}
Write-Host ""

# Paso 3: Activar entorno
Write-Host "3. Activando entorno virtual..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "   Entorno activado" -ForegroundColor Green
Write-Host ""

# Paso 4: Actualizar pip
Write-Host "4. Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip -q
Write-Host "   pip actualizado" -ForegroundColor Green
Write-Host ""

# Paso 5: Instalar dependencias basicas
Write-Host "5. Instalando dependencias basicas..." -ForegroundColor Yellow
python -m pip install pydantic python-dotenv pytest pytest-asyncio -q
Write-Host "   Dependencias instaladas" -ForegroundColor Green
Write-Host ""

# Paso 6: Validar estructura
Write-Host "6. Validando estructura del proyecto..." -ForegroundColor Yellow
python -c "from movility_ai.shared_libraries.types import Location; print('   Estructura OK')"
Write-Host ""

Write-Host "==================" -ForegroundColor Cyan
Write-Host "Setup completado!" -ForegroundColor Green
Write-Host ""
Write-Host "Para usar el entorno virtual:" -ForegroundColor Yellow
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
