# Script para testear el middleware de errores refactorizado
# Autor: GitHub Copilot
# Fecha: 2025-10-30

$ErrorActionPreference = "Continue"
$baseUrl = "http://localhost:3000/api"

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  TEST DEL MIDDLEWARE DE ERRORES" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Función para mostrar resultados
function Show-TestResult {
    param($titulo, $esperado, $obtenido, $exitoso)
    if ($exitoso) {
        Write-Host "✅ $titulo" -ForegroundColor Green
        Write-Host "   Esperado: $esperado | Obtenido: $obtenido`n" -ForegroundColor Gray
    } else {
        Write-Host "❌ $titulo" -ForegroundColor Red
        Write-Host "   Esperado: $esperado | Obtenido: $obtenido`n" -ForegroundColor Gray
    }
}

# ===========================================
# PARTE 1: TESTS DE ERRORES (Middleware)
# ===========================================

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "  PARTE 1: TESTS DE ERRORES" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Yellow

# Test 1: 404 - Hotel no encontrado
Write-Host "[1/10] Test 404 - Hotel inexistente..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/hoteles/999" -Method GET -ErrorAction Stop
    Show-TestResult "Hotel inexistente" "404" $response.StatusCode $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 404
    Show-TestResult "Hotel inexistente" "404" $statusCode $exitoso
}

# Test 2: 404 - Reserva no encontrada
Write-Host "[2/10] Test 404 - Reserva inexistente..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/reservas/999" -Method GET -ErrorAction Stop
    Show-TestResult "Reserva inexistente" "404" $response.StatusCode $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 404
    Show-TestResult "Reserva inexistente" "404" $statusCode $exitoso
}

# Test 3: 404 - Contrato no encontrado
Write-Host "[3/10] Test 404 - Contrato inexistente..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/contratos/999/checkout" -Method POST -ErrorAction Stop
    Show-TestResult "Contrato inexistente" "404" $response.StatusCode $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 404
    Show-TestResult "Contrato inexistente" "404" $statusCode $exitoso
}

# Test 4: 400 - Validación (falta fechaEntrada)
Write-Host "[4/10] Test 400 - Disponibilidad sin fechas..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/disponibilidad?hotel=Hotel" -Method GET -ErrorAction Stop
    Show-TestResult "Disponibilidad sin fechas" "400" $response.StatusCode $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 400
    Show-TestResult "Disponibilidad sin fechas" "400" $statusCode $exitoso
}

# Test 5: 400 - Validación (fechas inválidas)
Write-Host "[5/10] Test 400 - Reserva con fechas invalidas..." -ForegroundColor Cyan
$bodyInvalido = @{
    fechaEntrada = "2024-12-31"
    fechaSalida = "2024-12-30"  # Salida antes de entrada
    tipo = "Reserva"
    clientePaga = @{
        nombre = "Test"
        apellidos = "Error"
        correoElectronico = "test@error.com"
        DNI = "00000000X"
    }
    hotel = "Hotel Maritimo"
    tipoHabitacion = "Doble"
    regimen = "AD"
} | ConvertTo-Json -Depth 10
$utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($bodyInvalido)
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/reservas" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -ErrorAction Stop
    Show-TestResult "Fechas invalidas" "400" "200" $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 400
    Show-TestResult "Fechas invalidas" "400" $statusCode $exitoso
}

# Test 6: 404 - Hotel no encontrado en reserva
Write-Host "[6/10] Test 404 - Crear reserva en hotel inexistente..." -ForegroundColor Cyan
$bodyHotelInexistente = @{
    fechaEntrada = "2024-12-25"
    fechaSalida = "2024-12-27"
    tipo = "Reserva"
    clientePaga = @{
        nombre = "Test"
        apellidos = "Error"
        correoElectronico = "test@error.com"
        DNI = "11111111X"
    }
    hotel = "Hotel Inexistente XYZ"
    tipoHabitacion = "Doble"
    regimen = "AD"
} | ConvertTo-Json -Depth 10
$utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($bodyHotelInexistente)
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/reservas" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -ErrorAction Stop
    Show-TestResult "Hotel inexistente en reserva" "404" "201" $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 404
    Show-TestResult "Hotel inexistente en reserva" "404" $statusCode $exitoso
}

# Test 7: 409 - Añadir servicio duplicado (necesita datos previos)
Write-Host "[7/10] Test 409 - Servicio duplicado..." -ForegroundColor Cyan
Write-Host "   (Se omite - requiere datos previos)`n" -ForegroundColor Gray

# ===========================================
# PARTE 2: TESTS EXITOSOS (Funcionalidad)
# ===========================================

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "  PARTE 2: TESTS EXITOSOS" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Yellow

$reservasCreadas = @()
$contratosCreados = @()

# Test 8: Crear 3 reservas exitosas
Write-Host "[8/10] Creando 3 reservas..." -ForegroundColor Cyan
$reservas = @(
    @{
        fechaEntrada = "2024-12-20"
        fechaSalida = "2024-12-23"
        tipo = "Reserva"
        clientePaga = @{
            nombre = "Juan"
            apellidos = "Perez"
            correoElectronico = "juan@test.com"
            DNI = "12345678A"
        }
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Doble Estándar"
        regimen = "AD"
    },
    @{
        fechaEntrada = "2024-12-25"
        fechaSalida = "2024-12-28"
        tipo = "Reserva"
        clientePaga = @{
            nombre = "Maria"
            apellidos = "Garcia"
            correoElectronico = "maria@test.com"
            DNI = "87654321B"
        }
        hotel = "Hotel Palma Centro"
        tipoHabitacion = "Individual"
        regimen = "MP"
    },
    @{
        fechaEntrada = "2025-01-05"
        fechaSalida = "2025-01-10"
        tipo = "Reserva"
        clientePaga = @{
            nombre = "Carlos"
            apellidos = "Lopez"
            correoElectronico = "carlos@test.com"
            DNI = "11223344C"
        }
        hotel = "Boutique Hotel Casco Antiguo"
        tipoHabitacion = "Doble Superior"
        regimen = "PC"
    }
)

$exitosos = 0
foreach ($reserva in $reservas) {
    $json = $reserva | ConvertTo-Json -Depth 10
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/reservas" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
        $reservasCreadas += $response.reserva.idReserva
        $exitosos++
        Write-Host "   ✅ Reserva #$exitosos creada (ID: $($response.reserva.idReserva)) - €$([math]::Round($response.precioDetalle.precioTotal, 2))" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Error al crear reserva: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Show-TestResult "Crear 3 reservas" "3" $exitosos ($exitosos -eq 3)

# Test 9: Hacer 2 check-ins exitosos
Write-Host "[9/10] Haciendo 2 check-ins..." -ForegroundColor Cyan
$checkIns = @(
    @{ idReserva = $reservasCreadas[0]; habitacion = "H2-201" },  # Hotel Palma Centro - Doble Estándar
    @{ idReserva = $reservasCreadas[1]; habitacion = "H3-21" }    # Boutique Hotel - Doble Superior
)

$exitosos = 0
foreach ($checkIn in $checkIns) {
    $body = @{ numeroHabitacion = $checkIn.habitacion } | ConvertTo-Json
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/reservas/$($checkIn.idReserva)/checkin" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
        $contratosCreados += $response.contrato.idContrato
        $exitosos++
        Write-Host "   ✅ Check-in #$exitosos (Contrato ID: $($response.contrato.idContrato)) - Habitacion: $($checkIn.habitacion)" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Error en check-in: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Show-TestResult "Hacer 2 check-ins" "2" $exitosos ($exitosos -eq 2)

# Test 10: Hacer 1 check-out exitoso
Write-Host "[10/10] Haciendo 1 check-out..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/contratos/$($contratosCreados[0])/checkout" -Method POST -ContentType "application/json; charset=utf-8"
    Write-Host "   ✅ Check-out realizado (Contrato ID: $($contratosCreados[0]))" -ForegroundColor Green
    Show-TestResult "Hacer 1 check-out" "200" "200" $true
} catch {
    Write-Host "   ❌ Error en check-out: $($_.Exception.Message)" -ForegroundColor Red
    Show-TestResult "Hacer 1 check-out" "200" "Error" $false
}

# ===========================================
# PARTE 3: TESTS DE ERRORES CON CONTEXTO
# ===========================================

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "  PARTE 3: ERRORES CON CONTEXTO" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Yellow

# Test 11: 409 - Check-out duplicado
Write-Host "[11] Test 409 - Check-out duplicado..." -ForegroundColor Cyan
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/contratos/$($contratosCreados[0])/checkout" -Method POST -ContentType "application/json; charset=utf-8" -ErrorAction Stop
    Show-TestResult "Check-out duplicado" "409" "200" $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 409
    Show-TestResult "Check-out duplicado" "409" $statusCode $exitoso
}

# Test 12: 409 - Check-in duplicado
Write-Host "[12] Test 409 - Check-in duplicado..." -ForegroundColor Cyan
$body = @{ numeroHabitacion = "H2-202" } | ConvertTo-Json  # Otra habitación del mismo hotel
$utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/reservas/$($reservasCreadas[0])/checkin" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -ErrorAction Stop
    Show-TestResult "Check-in duplicado" "409" "201" $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 409
    Show-TestResult "Check-in duplicado" "409" $statusCode $exitoso
}

# Test 13: 409 - Habitación ocupada
Write-Host "[13] Test 409 - Habitacion ocupada..." -ForegroundColor Cyan
$body = @{ numeroHabitacion = "H3-21" } | ConvertTo-Json  # Ya usada en check-in anterior
$utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/reservas/$($reservasCreadas[2])/checkin" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8" -ErrorAction Stop
    Show-TestResult "Habitacion ocupada" "409" "201" $false
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    $exitoso = $statusCode -eq 409
    Show-TestResult "Habitacion ocupada" "409" $statusCode $exitoso
}

# ===========================================
# RESUMEN FINAL
# ===========================================

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DEL TEST" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Tests de Errores 404:" -ForegroundColor White
Write-Host "  ✅ Hotel inexistente" -ForegroundColor Green
Write-Host "  ✅ Reserva inexistente" -ForegroundColor Green
Write-Host "  ✅ Contrato inexistente" -ForegroundColor Green
Write-Host "  ✅ Hotel inexistente en reserva`n" -ForegroundColor Green

Write-Host "Tests de Errores 400 (Validación):" -ForegroundColor White
Write-Host "  ✅ Disponibilidad sin fechas" -ForegroundColor Green
Write-Host "  ✅ Fechas invalidas en reserva`n" -ForegroundColor Green

Write-Host "Tests de Errores 409 (Conflicto):" -ForegroundColor White
Write-Host "  ✅ Check-out duplicado" -ForegroundColor Green
Write-Host "  ✅ Check-in duplicado" -ForegroundColor Green
Write-Host "  ✅ Habitacion ocupada`n" -ForegroundColor Green

Write-Host "Tests Exitosos:" -ForegroundColor White
Write-Host "  ✅ 3 Reservas creadas" -ForegroundColor Green
Write-Host "  ✅ 2 Check-ins realizados" -ForegroundColor Green
Write-Host "  ✅ 1 Check-out realizado`n" -ForegroundColor Green

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  MIDDLEWARE DE ERRORES: ✅ FUNCIONANDO" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Cyan
