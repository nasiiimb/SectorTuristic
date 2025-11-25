# Script para crear ZIP del proyecto SectorTuristic
# Incluye exportacion de la base de datos PMS54870695D
# Fecha: Noviembre 2025

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Preparando entrega de SectorTuristic" -ForegroundColor Cyan
Write-Host "  Base de datos: PMS54870695D (PMS + NIF alumno)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Configuración
$proyectoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$nombreProyecto = "SectorTuristic_54870695D"
$fechaActual = Get-Date -Format "yyyy-MM-dd_HH-mm"
$nombreZip = "${nombreProyecto}_${fechaActual}.zip"
$rutaZip = Join-Path (Split-Path -Parent $proyectoPath) $nombreZip
$dbName = "PMS54870695D"
$dbUser = "root"
$exportPath = Join-Path $proyectoPath "BD\export_database.sql"

Write-Host "[1/5] Exportando base de datos..." -ForegroundColor Yellow

# Exportar la base de datos
Write-Host "   Exportando $dbName a BD\export_database.sql..." -ForegroundColor Cyan
Write-Host "   (Se solicitara la contrasena de MySQL root)" -ForegroundColor DarkYellow
try {
    $mysqldumpPath = "mysqldump"
    & $mysqldumpPath -u $dbUser -p --default-character-set=utf8mb4 --single-transaction --routines --triggers $dbName | Out-File -FilePath $exportPath -Encoding utf8
    
    if (Test-Path $exportPath) {
        $tamanoExport = (Get-Item $exportPath).Length / 1KB
        Write-Host "   Base de datos exportada exitosamente ($([math]::Round($tamanoExport, 2)) KB)" -ForegroundColor Green
    } else {
        Write-Host "   ADVERTENCIA: No se pudo exportar la base de datos" -ForegroundColor Yellow
        Write-Host "   Continuando sin export_database.sql..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ADVERTENCIA: Error al exportar base de datos: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "   Continuando sin export_database.sql..." -ForegroundColor Yellow
}
Write-Host ""

Write-Host "[2/5] Verificando carpetas..." -ForegroundColor Yellow

# Verificar que estamos en la carpeta correcta
if (!(Test-Path (Join-Path $proyectoPath "PMS"))) {
    Write-Host "ERROR: No se encontró la carpeta PMS. Asegúrate de ejecutar el script desde la carpeta SectorTuristic." -ForegroundColor Red
    exit 1
}

if (!(Test-Path (Join-Path $proyectoPath "WebService"))) {
    Write-Host "ERROR: No se encontró la carpeta WebService." -ForegroundColor Red
    exit 1
}

Write-Host "   Carpeta PMS encontrada" -ForegroundColor Green
Write-Host "   Carpeta WebService encontrada" -ForegroundColor Green
Write-Host "   Carpeta BD encontrada" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Buscando carpetas node_modules..." -ForegroundColor Yellow

# Buscar todas las carpetas node_modules
$nodeModulesPaths = Get-ChildItem -Path $proyectoPath -Recurse -Directory -Filter "node_modules" -ErrorAction SilentlyContinue

if ($nodeModulesPaths) {
    Write-Host "   Encontradas $($nodeModulesPaths.Count) carpeta(s) node_modules:" -ForegroundColor Yellow
    foreach ($path in $nodeModulesPaths) {
        $relativePath = $path.FullName.Replace($proyectoPath, ".")
        Write-Host "   - $relativePath" -ForegroundColor DarkYellow
    }
} else {
    Write-Host "   No se encontraron carpetas node_modules" -ForegroundColor Green
}
Write-Host ""

Write-Host "[4/5] Creando archivo ZIP..." -ForegroundColor Yellow
Write-Host "   Ruta destino: $rutaZip" -ForegroundColor Cyan

# Eliminar ZIP anterior si existe
if (Test-Path $rutaZip) {
    Write-Host "   Eliminando ZIP anterior..." -ForegroundColor DarkYellow
    Remove-Item $rutaZip -Force
}

# Función para obtener todos los archivos excluyendo node_modules
function Get-FilesToZip {
    param($basePath)
    
    $allFiles = Get-ChildItem -Path $basePath -Recurse -File -ErrorAction SilentlyContinue
    $filteredFiles = $allFiles | Where-Object { 
        $_.FullName -notmatch '\\node_modules\\' -and 
        $_.FullName -notmatch '\\\.git\\' -and
        $_.FullName -notmatch '\\\.__pycache__\\' -and
        $_.FullName -notmatch '\\\.pytest_cache\\' -and
        $_.FullName -notmatch '\\dist\\' -and
        $_.FullName -notmatch '\\build\\' -and
        $_.Name -ne '.DS_Store' -and
        $_.Name -ne 'README.md' -and
        $_.Name -ne 'crear_zip.sh'
    }
    
    return $filteredFiles
}

# Obtener archivos a comprimir
$archivos = Get-FilesToZip -basePath $proyectoPath
$totalArchivos = $archivos.Count
$archivosProcesados = 0

Write-Host "   Total de archivos a comprimir: $totalArchivos" -ForegroundColor Cyan
Write-Host ""

# Crear el ZIP
Add-Type -AssemblyName System.IO.Compression.FileSystem

$zip = [System.IO.Compression.ZipFile]::Open($rutaZip, 'Create')

try {
    foreach ($archivo in $archivos) {
        $archivosProcesados++
        
        # Mostrar progreso cada 50 archivos
        if ($archivosProcesados % 50 -eq 0 -or $archivosProcesados -eq $totalArchivos) {
            $porcentaje = [math]::Round(($archivosProcesados / $totalArchivos) * 100)
            Write-Host "   Progreso: $archivosProcesados/$totalArchivos archivos ($porcentaje%)" -ForegroundColor Cyan
        }
        
        # Ruta relativa dentro del ZIP
        $rutaRelativa = $archivo.FullName.Substring($proyectoPath.Length + 1)
        $entryPath = Join-Path $nombreProyecto $rutaRelativa
        
        # Agregar archivo al ZIP
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $archivo.FullName, $entryPath) | Out-Null
    }
    
    Write-Host ""
    Write-Host "[5/5] Finalizando..." -ForegroundColor Yellow
} 
finally {
    $zip.Dispose()
}

# Obtener tamaño del archivo
$tamanoBytes = (Get-Item $rutaZip).Length
$tamanoMB = [math]::Round($tamanoBytes / 1MB, 2)

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  ZIP creado exitosamente!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Detalles:" -ForegroundColor Cyan
Write-Host "  Archivo: $nombreZip" -ForegroundColor White
Write-Host "  Ubicación: $rutaZip" -ForegroundColor White
Write-Host "  Tamaño: $tamanoMB MB" -ForegroundColor White
Write-Host "  Archivos incluidos: $totalArchivos" -ForegroundColor White
Write-Host ""
Write-Host "Archivos incluidos:" -ForegroundColor Cyan
Write-Host "  - Codigo fuente PMS y WebService" -ForegroundColor White
Write-Host "  - Scripts de base de datos (dump.sql, insert.sql)" -ForegroundColor White
Write-Host "  - Exportacion de BD: export_database.sql" -ForegroundColor Green
Write-Host "  - Documentacion (README del PMS)" -ForegroundColor White
Write-Host ""
Write-Host "Carpetas excluidas:" -ForegroundColor Cyan
Write-Host "  - node_modules (dependencias de Node.js)" -ForegroundColor DarkYellow
Write-Host "  - .git (control de versiones)" -ForegroundColor DarkYellow
Write-Host "  - __pycache__ (cache de Python)" -ForegroundColor DarkYellow
Write-Host "  - Scripts de utilidad (crear_zip.sh, README.md raiz)" -ForegroundColor DarkYellow
Write-Host ""
Write-Host "IMPORTANTE: La base de datos se llama PMS54870695D" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
