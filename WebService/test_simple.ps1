# Test simple de endpoints con middleware
$ErrorActionPreference = "Continue"
$baseUrl = "http://localhost:3000/api"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  TEST DE ENDPOINTS Y MIDDLEWARE" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Contador de éxitos
$exitosos = 0
$totales = 0

function Test-Endpoint {
    param($nombre, $test)
    $script:totales++
    try {
        & $test
        Write-Host "✅ $nombre" -ForegroundColor Green
        $script:exitosos++
    } catch {
        Write-Host "❌ $nombre - $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "--- TESTS DE ERRORES (Middleware) ---`n" -ForegroundColor Yellow

Test-Endpoint "404 - Hotel inexistente" {
    try {
        Invoke-RestMethod -Uri "$baseUrl/hoteles/9999" -Method GET
        throw "Debería dar 404"
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 404) { throw "Código incorrecto" }
    }
}

Test-Endpoint "404 - Reserva inexistente" {
    try {
        Invoke-RestMethod -Uri "$baseUrl/reservas/9999" -Method GET
        throw "Debería dar 404"
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 404) { throw "Código incorrecto" }
    }
}

Test-Endpoint "400 - Validación (sin fechas)" {
    try {
        Invoke-RestMethod -Uri "$baseUrl/disponibilidad?hotel=Test" -Method GET
        throw "Debería dar 400"
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 400) { throw "Código incorrecto" }
    }
}

Test-Endpoint "400 - Fechas inválidas en reserva" {
    $body = @{
        fechaEntrada = "2024-12-31"
        fechaSalida = "2024-12-30"
        tipo = "Reserva"
        clientePaga = @{
            nombre = "Test"
            apellidos = "Error"
            correoElectronico = "test@error.com"
            DNI = "00000000X"
        }
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Doble Estándar"
        regimen = "AD"
    } | ConvertTo-Json -Depth 10
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    try {
        Invoke-RestMethod -Uri "$baseUrl/reservas" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
        throw "Debería dar 400"
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 400) { throw "Código incorrecto" }
    }
}

Write-Host "`n--- TESTS DE FUNCIONALIDAD ---`n" -ForegroundColor Yellow

Test-Endpoint "GET - Listar hoteles" {
    $hoteles = Invoke-RestMethod -Uri "$baseUrl/hoteles" -Method GET
    if ($hoteles.Count -lt 1) { throw "No hay hoteles" }
}

Test-Endpoint "GET - Listar regímenes" {
    $regimenes = Invoke-RestMethod -Uri "$baseUrl/regimenes" -Method GET
    if ($regimenes.Count -lt 1) { throw "No hay regímenes" }
}

Test-Endpoint "GET - Listar tipos de habitación" {
    $tipos = Invoke-RestMethod -Uri "$baseUrl/tipos-habitacion" -Method GET
    if ($tipos.Count -lt 1) { throw "No hay tipos" }
}

Test-Endpoint "GET - Listar reservas" {
    $reservas = Invoke-RestMethod -Uri "$baseUrl/reservas" -Method GET
    # Puede estar vacío, solo verificamos que responda
}

Test-Endpoint "POST - Crear reserva" {
    $body = @{
        fechaEntrada = (Get-Date).AddDays(10).ToString("yyyy-MM-dd")
        fechaSalida = (Get-Date).AddDays(13).ToString("yyyy-MM-dd")
        tipo = "Reserva"
        clientePaga = @{
            nombre = "Test"
            apellidos = "Usuario"
            correoElectronico = "test.usuario@email.com"
            DNI = "99999999Z"
        }
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Doble Estándar"
        regimen = "AD"
    } | ConvertTo-Json -Depth 10
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    $response = Invoke-RestMethod -Uri "$baseUrl/reservas" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
    if (-not $response.reserva.idReserva) { throw "No se creó la reserva" }
    $script:reservaId = $response.reserva.idReserva
}

Test-Endpoint "GET - Obtener reserva por ID" {
    $reserva = Invoke-RestMethod -Uri "$baseUrl/reservas/$script:reservaId" -Method GET
    if ($reserva.idReserva -ne $script:reservaId) { throw "ID no coincide" }
}

Test-Endpoint "POST - Check-in" {
    $body = @{ numeroHabitacion = "H1-101" } | ConvertTo-Json
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    $response = Invoke-RestMethod -Uri "$baseUrl/reservas/$script:reservaId/checkin" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
    if (-not $response.contrato.idContrato) { throw "No se creó el contrato" }
    $script:contratoId = $response.contrato.idContrato
}

Test-Endpoint "409 - Check-in duplicado" {
    $body = @{ numeroHabitacion = "H1-102" } | ConvertTo-Json
    $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    try {
        Invoke-RestMethod -Uri "$baseUrl/reservas/$script:reservaId/checkin" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
        throw "Debería dar 409"
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 409) { throw "Código incorrecto: $($_.Exception.Response.StatusCode.value__)" }
    }
}

Test-Endpoint "POST - Check-out" {
    $response = Invoke-RestMethod -Uri "$baseUrl/contratos/$script:contratoId/checkout" -Method POST -ContentType "application/json; charset=utf-8"
    if (-not $response.contrato.fechaCheckOut) { throw "No se hizo checkout" }
}

Test-Endpoint "409 - Check-out duplicado" {
    try {
        Invoke-RestMethod -Uri "$baseUrl/contratos/$script:contratoId/checkout" -Method POST -ContentType "application/json; charset=utf-8"
        throw "Debería dar 409"
    } catch {
        if ($_.Exception.Response.StatusCode.value__ -ne 409) { throw "Código incorrecto" }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RESULTADO: $exitosos/$totales TESTS PASADOS" -ForegroundColor $(if ($exitosos -eq $totales) { "Green" } else { "Yellow" })
Write-Host "========================================`n" -ForegroundColor Cyan

if ($exitosos -eq $totales) {
    Write-Host "✅ TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE" -ForegroundColor Green
    Write-Host "✅ MIDDLEWARE DE ERRORES FUNCIONANDO" -ForegroundColor Green
} else {
    Write-Host "⚠️  Algunos tests fallaron" -ForegroundColor Yellow
}
