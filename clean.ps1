# Script de limpieza del proyecto (estilo "mvn clean")
# Elimina dependencias y archivos temporales para reducir el tamaño

$projectPath = "C:\UIB\Solucions Turistiques\practica\SectorTuristic"

Write-Host "=== LIMPIEZA DEL PROYECTO ===" -ForegroundColor Cyan
Write-Host ""

$sizeBefore = [math]::Round((Get-ChildItem -Path $projectPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
Write-Host "Tamano actual: $sizeBefore MB" -ForegroundColor Yellow
Write-Host ""

# Eliminar node_modules
if (Test-Path "$projectPath\WebService\node_modules") {
    Write-Host "[1/6] Eliminando node_modules..." -ForegroundColor Yellow
    Remove-Item -Path "$projectPath\WebService\node_modules" -Recurse -Force
    Write-Host "  OK - node_modules eliminado" -ForegroundColor Green
} else {
    Write-Host "[1/6] node_modules no existe" -ForegroundColor Gray
}

# Eliminar dist
if (Test-Path "$projectPath\WebService\dist") {
    Write-Host "[2/6] Eliminando dist..." -ForegroundColor Yellow
    Remove-Item -Path "$projectPath\WebService\dist" -Recurse -Force
    Write-Host "  OK - dist eliminado" -ForegroundColor Green
} else {
    Write-Host "[2/6] dist no existe" -ForegroundColor Gray
}

# Eliminar __pycache__
Write-Host "[3/6] Eliminando __pycache__..." -ForegroundColor Yellow
Get-ChildItem -Path "$projectPath\PMS" -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Write-Host "  OK - __pycache__ eliminados" -ForegroundColor Green

# Eliminar archivos .pyc
Write-Host "[4/6] Eliminando archivos .pyc..." -ForegroundColor Yellow
Get-ChildItem -Path "$projectPath\PMS" -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force
Write-Host "  OK - archivos .pyc eliminados" -ForegroundColor Green

# Eliminar venv si existe
if (Test-Path "$projectPath\PMS\venv") {
    Write-Host "[5/6] Eliminando venv..." -ForegroundColor Yellow
    Remove-Item -Path "$projectPath\PMS\venv" -Recurse -Force
    Write-Host "  OK - venv eliminado" -ForegroundColor Green
} else {
    Write-Host "[5/6] venv no existe" -ForegroundColor Gray
}

# Eliminar archivos de log
Write-Host "[6/6] Eliminando archivos de log..." -ForegroundColor Yellow
Get-ChildItem -Path $projectPath -Recurse -Filter "*.log" -ErrorAction SilentlyContinue | Remove-Item -Force
Write-Host "  OK - archivos .log eliminados" -ForegroundColor Green

Write-Host ""
$sizeAfter = [math]::Round((Get-ChildItem -Path $projectPath -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
$saved = [math]::Round($sizeBefore - $sizeAfter, 2)

Write-Host "=== LIMPIEZA COMPLETADA ===" -ForegroundColor Green
Write-Host ""
Write-Host "  Tamano antes:  $sizeBefore MB" -ForegroundColor White
Write-Host "  Tamano ahora:  $sizeAfter MB" -ForegroundColor White
Write-Host "  Espacio liberado: $saved MB" -ForegroundColor Cyan
Write-Host ""
Write-Host "El proyecto esta listo para comprimir." -ForegroundColor Green
Write-Host ""
Write-Host "Para restaurar las dependencias:" -ForegroundColor Yellow
Write-Host "  WebService: cd WebService; npm install" -ForegroundColor Gray
Write-Host "  PMS: cd PMS; pip install -r requirements.txt" -ForegroundColor Gray
Write-Host ""
