#!/bin/bash
# MovilityAI - Setup and Test Script for Unix/Linux/Mac

echo "🚀 MovilityAI - Configuración e Instalación"
echo "=========================================="
echo ""

# Verificar que uv está instalado
echo "📦 Verificando uv..."
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv no está instalado"
    echo "Por favor instala uv desde: https://docs.astral.sh/uv/"
    exit 1
fi
echo "✅ uv está instalado"
echo ""

# Instalar dependencias
echo "📦 Instalando dependencias..."
uv sync
if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi
echo "✅ Dependencias instaladas correctamente"
echo ""

# Ejecutar tests
echo "🧪 Ejecutando tests..."
echo ""
uv run pytest tests/unit/ -v
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Todos los tests pasaron correctamente!"
else
    echo ""
    echo "⚠️  Algunos tests fallaron - revisar output arriba"
fi

echo ""
echo "========================================"
echo "🎉 Setup completado"
echo ""
echo "Próximos pasos:"
echo "1. Configura tus credenciales de Google Cloud en .env"
echo "2. Ejecuta: uv run python -m movility_ai"
echo "3. Para tests: uv run pytest tests/"
echo ""
