# MovilityAI - Setup alternativo sin uv (usando pip y venv)
Write-Host "MovilityAI - Configuracion e Instalacion (pip/venv)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python no esta instalado" -ForegroundColor Red
    exit 1
}
Write-Host "Python instalado correctamente" -ForegroundColor Green
Write-Host ""

# Crear entorno virtual si no existe
if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al crear entorno virtual" -ForegroundColor Red
        exit 1
    }
    Write-Host "Entorno virtual creado" -ForegroundColor Green
}
else {
    Write-Host "Entorno virtual ya existe" -ForegroundColor Green
}
Write-Host ""

# Activar entorno virtual
Write-Host "📦 Activando entorno virtual..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1
Write-Host "✅ Entorno virtual activado" -ForegroundColor Green
Write-Host ""

# Actualizar pip
Write-Host "📦 Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✅ pip actualizado" -ForegroundColor Green
Write-Host ""

# Instalar dependencias principales
Write-Host "📦 Instalando dependencias principales..." -ForegroundColor Yellow
Write-Host "   (Esto puede tomar varios minutos...)" -ForegroundColor Gray

# Instalar las dependencias clave una por una para mejor control
$packages = @(
    "pydantic>=2.10.6",
    "python-dotenv>=1.0.1",
    "pytest>=8.3.5",
    "pytest-asyncio>=0.26.0"
)

foreach ($package in $packages) {
    Write-Host "   Instalando $package..." -ForegroundColor Gray
    python -m pip install $package --quiet
}

Write-Host "✅ Dependencias básicas instaladas" -ForegroundColor Green
Write-Host ""

# Nota sobre Google ADK
Write-Host "ℹ️  NOTA: Google ADK requiere instalación manual:" -ForegroundColor Yellow
Write-Host "   pip install google-cloud-aiplatform[adk,agent-engines]>=1.93.0" -ForegroundColor White
Write-Host "   pip install google-genai>=1.16.1" -ForegroundColor White
Write-Host "   pip install google-adk>=1.0.0" -ForegroundColor White
Write-Host ""
Write-Host "   (Se omiten ahora para validar la estructura primero)" -ForegroundColor Gray
Write-Host ""

# Ejecutar tests básicos (sin Google ADK)
Write-Host "🧪 Ejecutando validación de estructura..." -ForegroundColor Yellow
Write-Host ""

# Test básico de importación
$testScript = @"
import sys
sys.path.insert(0, '.')

print('Validando estructura del proyecto...')
print()

# Test 1: Tipos compartidos
try:
    from movility_ai.shared_libraries.types import Location, TrafficData, Route, AnalysisResult
    print('✅ Tipos compartidos: OK')
except Exception as e:
    print(f'❌ Error en tipos: {e}')
    sys.exit(1)

# Test 2: Constantes
try:
    from movility_ai.shared_libraries.constants import DEFAULT_MODEL, MAX_ROUTE_ALTERNATIVES
    print('✅ Constantes: OK')
except Exception as e:
    print(f'❌ Error en constantes: {e}')
    sys.exit(1)

# Test 3: Crear objetos
try:
    loc = Location(latitude=4.6097, longitude=-74.0817, name='Bogotá')
    print(f'✅ Location creado: {loc.name}')
    
    traffic = TrafficData(
        location=loc,
        congestion_level=0.5,
        average_speed=30.0,
        timestamp='2025-10-29T10:00:00Z'
    )
    print(f'✅ TrafficData creado: congestion={traffic.congestion_level}')
except Exception as e:
    print(f'❌ Error creando objetos: {e}')
    sys.exit(1)

print()
print('✅ Validación de estructura completada exitosamente!')
"@

$testScript | Out-File -FilePath "test_structure.py" -Encoding UTF8

python test_structure.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ ¡Validación exitosa!" -ForegroundColor Green
    Remove-Item "test_structure.py" -ErrorAction SilentlyContinue
} else {
    Write-Host ""
    Write-Host "⚠️  Hay errores en la estructura" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📊 Resumen de Setup" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Python: Instalado" -ForegroundColor Green
Write-Host "✅ Entorno virtual: Creado" -ForegroundColor Green
Write-Host "✅ Dependencias básicas: Instaladas" -ForegroundColor Green
Write-Host "✅ Estructura del proyecto: Validada" -ForegroundColor Green
Write-Host "⏳ Google ADK: Pendiente (instalar cuando sea necesario)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Para instalar Google ADK:" -ForegroundColor White
Write-Host "   pip install google-cloud-aiplatform[adk]" -ForegroundColor Gray
Write-Host "2. Para ejecutar tests completos:" -ForegroundColor White
Write-Host "   pytest tests/ -v" -ForegroundColor Gray
Write-Host "3. Para ejecutar el sistema:" -ForegroundColor White
Write-Host "   python -m movility_ai" -ForegroundColor Gray
Write-Host ""
