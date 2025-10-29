@echo off
REM Script para ejecutar ADK Web UI para MovilityAI
REM Asegúrate de que la variable GOOGLE_API_KEY esté configurada en tu .env

echo ========================================
echo   Iniciando ADK Web UI - MovilityAI
echo ========================================
echo.

cd /d "%~dp0"

REM Cargar la API key desde .env si existe
if exist "movility_ai\.env" (
    for /f "tokens=1,2 delims==" %%a in (movility_ai\.env) do (
        if "%%a"=="GOOGLE_API_KEY" set GOOGLE_API_KEY=%%b
    )
)

REM Verificar que la API key esté configurada
if "%GOOGLE_API_KEY%"=="" (
    echo ERROR: GOOGLE_API_KEY no está configurada
    echo Por favor, configúrala en movility_ai/.env
    pause
    exit /b 1
)

echo API Key configurada correctamente
echo Iniciando servidor ADK Web...
echo.
echo La interfaz estará disponible en: http://127.0.0.1:8000
echo Presiona Ctrl+C para detener el servidor
echo.

adk web agent

pause
