# Script completo: Limpia el proyecto y crea el ZIP para entregar
# Equivalente a "mvn clean package"

$projectPath = "C:\UIB\Solucions Turistiques\practica\SectorTuristic"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$zipPath = "C:\UIB\Solucions Turistiques\practica\SectorTuristic_$timestamp.zip"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  PREPARACION DE ENTREGA - PROYECTO PMS" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# FASE 1: PREPARACION
Write-Host "FASE 1: Preparando archivos para comprimir..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

# Eliminar ZIPs anteriores en la carpeta del proyecto
Write-Host "  Limpiando ZIPs anteriores..." -ForegroundColor Gray
Get-ChildItem -Path $projectPath -Filter "*.zip" -File -ErrorAction SilentlyContinue | Remove-Item -Force

Write-Host ""
Write-Host "OK - Preparacion completada" -ForegroundColor Green
Write-Host ""

# FASE 2: COMPRESION (excluyendo carpetas pesadas)
Write-Host "FASE 2: Creando archivo ZIP..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Gray

# Obtener todos los archivos excluyendo patrones
$excludePatterns = @(
    '*\node_modules\*',
    '*\dist\*',
    '*\__pycache__\*',
    '*\venv\*',
    '*\env\*',
    '*.pyc',
    '*.log',
    '*\crear_zip.ps1',
    '*\crear_7z.ps1',
    '*\comprimir_y_restaurar.ps1',
    '*\crear_entrega.ps1',
    '*\.git\*'
)

Write-Host "  Recopilando archivos (excluyendo dependencias)..." -ForegroundColor Gray

$filesToZip = Get-ChildItem -Path $projectPath -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $filePath = $_.FullName
    $shouldInclude = $true
    
    foreach ($pattern in $excludePatterns) {
        if ($filePath -like $pattern) {
            $shouldInclude = $false
            break
        }
    }
    
    $shouldInclude
}

Write-Host "  Comprimiendo $($filesToZip.Count) archivos..." -ForegroundColor Gray

# Comprimir usando relative paths
$filesToZip | ForEach-Object {
    $relativePath = $_.FullName.Substring($projectPath.Length + 1)
    Compress-Archive -Path $_.FullName -DestinationPath $zipPath -Update
}

Write-Host ""
Write-Host "OK - Archivo comprimido" -ForegroundColor Green
Write-Host ""

# FASE 3: RESULTADO
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  ENTREGA LISTA" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

$zipSize = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)

Write-Host "Archivo:  $(Split-Path $zipPath -Leaf)" -ForegroundColor White
Write-Host "Ubicacion: $(Split-Path $zipPath -Parent)" -ForegroundColor White
Write-Host "Tamano:   $zipSize MB" -ForegroundColor White
Write-Host ""

if ($zipSize -lt 100) {
    Write-Host "Estado: OK - Listo para entregar" -ForegroundColor Green
} else {
    Write-Host "Estado: ADVERTENCIA - Supera 100 MB" -ForegroundColor Red
}

Write-Host ""
Write-Host "Contenido del ZIP:" -ForegroundColor Cyan
Write-Host "  - BD/          (Base de datos)" -ForegroundColor Gray
Write-Host "  - WebService/  (API REST)" -ForegroundColor Gray
Write-Host "  - PMS/         (Sistema de gestion)" -ForegroundColor Gray
Write-Host "  - Documentacion" -ForegroundColor Gray
Write-Host ""
Write-Host "NOTA: No incluye node_modules ni venv" -ForegroundColor Yellow
Write-Host "      Instrucciones de instalacion en LEEME_INSTALACION.md" -ForegroundColor Yellow
Write-Host ""
