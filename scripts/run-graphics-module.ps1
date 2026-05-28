# Запуск оригинального Flask-сервера Graphics_Module (порт 5000)
$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $root "integrations\graphics-module\color-converter-backend"
$venvPython = Join-Path $root "backend\venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "Не найден Python venv: $venvPython. Создайте venv в backend."
}

Write-Host "Установка зависимостей модуля (Flask, Pillow)..."
& $venvPython -m pip install -q flask flask-cors pillow werkzeug

Set-Location $backendDir
Write-Host ""
Write-Host "Графический модуль: http://127.0.0.1:5000"
Write-Host "Проверка: http://127.0.0.1:5000/health"
Write-Host "Остановка: Ctrl+C"
Write-Host ""

& $venvPython app.py
