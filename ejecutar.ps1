# Script PowerShell para ejecutar SeeYouInstagram

Write-Host "🚀 Iniciando SeeYouInstagram..." -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
& ".\.venv\Scripts\Activate.ps1"

# Verificar que las dependencias estén instaladas
try {
    & python -c "import colorama, instaloader"
    Write-Host "✅ Dependencias verificadas correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Las dependencias no están instaladas correctamente" -ForegroundColor Red
    Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
    & pip install -r requirements.txt
}

Write-Host ""
Write-Host "🎯 Ejecutando SeeYouInstagram..." -ForegroundColor Green
Write-Host ""

# Ejecutar el programa principal
& python main.py

Write-Host ""
Write-Host "👋 ¡Hasta la próxima!" -ForegroundColor Cyan
