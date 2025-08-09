@echo off
REM Script para ejecutar SeeYouInstagram con el entorno virtual correcto

echo 🚀 Iniciando SeeYouInstagram...
echo.

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Verificar que las dependencias estén instaladas
python -c "import colorama, instaloader" 2>nul
if errorlevel 1 (
    echo ❌ Error: Las dependencias no están instaladas correctamente
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
)

REM Ejecutar el programa principal
python main.py

REM Desactivar entorno virtual al salir
deactivate

echo.
echo 👋 ¡Hasta la próxima!
pause
