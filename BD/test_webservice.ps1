# =====================================================
# SCRIPT DE PRUEBA DEL WEB SERVICE - API REST
# =====================================================
# Este script prueba el API REST haciendo:
# 1. Consultar disponibilidad
# 2. Crear 10 reservas distintas
# 3. Hacer 5 check-ins
# 4. Hacer 3 check-outs
# =====================================================

# IMPORTANTE: Configurar encoding UTF-8 para PowerShell
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$baseUrl = "http://localhost:3000/api"
$resultados = @()

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  PRUEBA COMPLETA DEL WEB SERVICE - API REST" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

# =====================================================
# PARTE 1: CONSULTAR DISPONIBILIDAD
# =====================================================

Write-Host "PASO 1: Consultando disponibilidad..." -ForegroundColor Yellow
Write-Host ""

# Disponibilidad para diferentes fechas y hoteles
$consultas = @(
    @{ fechaEntrada = "2025-11-01"; fechaSalida = "2025-11-06"; hotel = "Gran" },
    @{ fechaEntrada = "2025-11-10"; fechaSalida = "2025-11-17"; hotel = "Palma" },
    @{ fechaEntrada = "2025-11-15"; fechaSalida = "2025-11-21"; ciudad = "Palma" }
)

foreach ($consulta in $consultas) {
    $params = ""
    foreach ($key in $consulta.Keys) {
        if ($params -ne "") { $params += [char]38 }
        $params += "$key=$($consulta[$key])"
    }
    
    Write-Host "  -> Consultando: $params" -ForegroundColor Gray
    $response = Invoke-RestMethod -Uri "$baseUrl/disponibilidad?$params" -Method GET
    Write-Host "    OK Disponibilidad encontrada: $($response.disponibles.Count) opciones" -ForegroundColor Green
}

Write-Host ""

# =====================================================
# PARTE 2: CREAR 10 RESERVAS DISTINTAS
# =====================================================

Write-Host "PASO 2: Creando 10 reservas..." -ForegroundColor Yellow
Write-Host ""

$reservas = @(
    # RESERVA 1: Maria Garcia - Suite Junior - Pension Completa
    @{
        fechaEntrada = "2025-11-01"
        fechaSalida = "2025-11-06"
        tipo = "Reserva"
        canalReserva = "Web"
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Suite Junior"
        regimen = "PC"
        clientePaga = @{
            nombre = "Maria"
            apellidos = "Garcia Lopez"
            correoElectronico = "maria.garcia@email.com"
            DNI = "11111111A"
            fechaDeNacimiento = "1985-03-15"
        }
        huespedes = @(
            @{
                nombre = "Maria"
                apellidos = "Garcia Lopez"
                correoElectronico = "maria.garcia@email.com"
                DNI = "11111111A"
                fechaDeNacimiento = "1985-03-15"
            },
            @{
                nombre = "Elena"
                apellidos = "Garcia Lopez"
                correoElectronico = "elena.garcia@email.com"
                DNI = "11111112A"
                fechaDeNacimiento = "1987-03-15"
            }
        )
    },
    
    # RESERVA 2: Jose Martinez - Doble Estandar - Alojamiento y Desayuno
    @{
        fechaEntrada = "2025-11-02"
        fechaSalida = "2025-11-05"
        tipo = "Reserva"
        canalReserva = "Telefono"
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Doble Estandar"
        regimen = "AD"
        clientePaga = @{
            nombre = "Jose"
            apellidos = "Martinez Sanchez"
            correoElectronico = "jose.martinez@email.com"
            DNI = "22222222B"
            fechaDeNacimiento = "1990-07-22"
        }
        huespedes = @(
            @{
                nombre = "Jose"
                apellidos = "Martinez Sanchez"
                correoElectronico = "jose.martinez@email.com"
                DNI = "22222222B"
                fechaDeNacimiento = "1990-07-22"
            },
            @{
                nombre = "Carmen"
                apellidos = "Martinez Sanchez"
                correoElectronico = "carmen.martinez@email.com"
                DNI = "22222223B"
                fechaDeNacimiento = "1992-07-22"
            }
        )
    },
    
    # RESERVA 3: Ana Rodriguez - Doble Superior - Media Pension
    @{
        fechaEntrada = "2025-11-03"
        fechaSalida = "2025-11-05"
        tipo = "Reserva"
        canalReserva = "Web"
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Doble Superior"
        regimen = "MP"
        clientePaga = @{
            nombre = "Ana"
            apellidos = "Rodriguez Perez"
            correoElectronico = "ana.rodriguez@email.com"
            DNI = "33333333C"
            fechaDeNacimiento = "1988-11-30"
        }
        huespedes = @(
            @{
                nombre = "Ana"
                apellidos = "Rodriguez Perez"
                correoElectronico = "ana.rodriguez@email.com"
                DNI = "33333333C"
                fechaDeNacimiento = "1988-11-30"
            }
        )
    },
    
    # RESERVA 4: Carlos Fernandez - Doble Superior - Solo Alojamiento (Hotel 2)
    @{
        fechaEntrada = "2025-11-05"
        fechaSalida = "2025-11-09"
        tipo = "Reserva"
        canalReserva = "Email"
        hotel = "Hotel Palma Centro"
        tipoHabitacion = "Doble Superior"
        regimen = "SA"
        clientePaga = @{
            nombre = "Carlos"
            apellidos = "Fernandez Gomez"
            correoElectronico = "carlos.fernandez@email.com"
            DNI = "44444444D"
            fechaDeNacimiento = "1982-05-10"
        }
        huespedes = @(
            @{
                nombre = "Carlos"
                apellidos = "Fernandez Gomez"
                correoElectronico = "carlos.fernandez@email.com"
                DNI = "44444444D"
                fechaDeNacimiento = "1982-05-10"
            }
        )
    },
    
    # RESERVA 5: Laura Lopez - Individual - Alojamiento y Desayuno (Hotel 2)
    @{
        fechaEntrada = "2025-11-06"
        fechaSalida = "2025-11-07"
        tipo = "Reserva"
        canalReserva = "Web"
        hotel = "Hotel Palma Centro"
        tipoHabitacion = "Individual"
        regimen = "AD"
        clientePaga = @{
            nombre = "Laura"
            apellidos = "Lopez Martin"
            correoElectronico = "laura.lopez@email.com"
            DNI = "55555555E"
            fechaDeNacimiento = "1995-09-18"
        }
        huespedes = @(
            @{
                nombre = "Laura"
                apellidos = "Lopez Martin"
                correoElectronico = "laura.lopez@email.com"
                DNI = "55555555E"
                fechaDeNacimiento = "1995-09-18"
            }
        )
    },
    
    # RESERVA 6: Sophie Dubois - Doble Superior - Pension Completa
    @{
        fechaEntrada = "2025-11-10"
        fechaSalida = "2025-11-17"
        tipo = "Reserva"
        canalReserva = "Agencia"
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Doble Superior"
        regimen = "PC"
        clientePaga = @{
            nombre = "Sophie"
            apellidos = "Dubois"
            correoElectronico = "sophie.dubois@email.fr"
            DNI = "66666666F"
            fechaDeNacimiento = "1987-02-28"
        }
        huespedes = @(
            @{
                nombre = "Sophie"
                apellidos = "Dubois"
                correoElectronico = "sophie.dubois@email.fr"
                DNI = "66666666F"
                fechaDeNacimiento = "1987-02-28"
            }
        )
    },
    
    # RESERVA 7: Hans Muller - Suite Junior - Media Pension
    @{
        fechaEntrada = "2025-11-08"
        fechaSalida = "2025-11-11"
        tipo = "Reserva"
        canalReserva = "Web"
        hotel = "Gran Hotel del Mar"
        tipoHabitacion = "Suite Junior"
        regimen = "MP"
        clientePaga = @{
            nombre = "Hans"
            apellidos = "Muller"
            correoElectronico = "hans.muller@email.de"
            DNI = "77777777G"
            fechaDeNacimiento = "1980-12-05"
        }
        huespedes = @(
            @{
                nombre = "Hans"
                apellidos = "Muller"
                correoElectronico = "hans.muller@email.de"
                DNI = "77777777G"
                fechaDeNacimiento = "1980-12-05"
            }
        )
    },
    
    # RESERVA 8: Emma Smith - Doble Estandar - Pension Completa (Hotel 3)
    @{
        fechaEntrada = "2025-11-12"
        fechaSalida = "2025-11-14"
        tipo = "Reserva"
        canalReserva = "Telefono"
        hotel = "Boutique Hotel Casco Antiguo"
        tipoHabitacion = "Doble Estandar"
        regimen = "PC"
        clientePaga = @{
            nombre = "Emma"
            apellidos = "Smith"
            correoElectronico = "emma.smith@email.uk"
            DNI = "88888888H"
            fechaDeNacimiento = "1992-06-14"
        }
        huespedes = @(
            @{
                nombre = "Emma"
                apellidos = "Smith"
                correoElectronico = "emma.smith@email.uk"
                DNI = "88888888H"
                fechaDeNacimiento = "1992-06-14"
            },
            @{
                nombre = "Michael"
                apellidos = "Smith"
                correoElectronico = "michael.smith@email.uk"
                DNI = "88888889H"
                fechaDeNacimiento = "1993-06-14"
            }
        )
    },
    
    # RESERVA 9: Luca Rossi - Doble Superior - Alojamiento y Desayuno (Hotel 3)
    @{
        fechaEntrada = "2025-11-15"
        fechaSalida = "2025-11-21"
        tipo = "Reserva"
        canalReserva = "Web"
        hotel = "Boutique Hotel Casco Antiguo"
        tipoHabitacion = "Doble Superior"
        regimen = "AD"
        clientePaga = @{
            nombre = "Luca"
            apellidos = "Rossi"
            correoElectronico = "luca.rossi@email.it"
            DNI = "99999999I"
            fechaDeNacimiento = "1989-04-20"
        }
        huespedes = @(
            @{
                nombre = "Luca"
                apellidos = "Rossi"
                correoElectronico = "luca.rossi@email.it"
                DNI = "99999999I"
                fechaDeNacimiento = "1989-04-20"
            },
            @{
                nombre = "Isabella"
                apellidos = "Rossi"
                correoElectronico = "isabella.rossi@email.it"
                DNI = "99999998I"
                fechaDeNacimiento = "1990-04-20"
            }
        )
    },
    
    # RESERVA 10: Pierre Lefebvre - Doble Estándar - Media Pensión (Hotel 2)
    @{
        fechaEntrada = "2025-11-18"
        fechaSalida = "2025-11-22"
        tipo = "Reserva"
        canalReserva = "Email"
        hotel = "Hotel Palma Centro"
        tipoHabitacion = "Doble Estandar"
        regimen = "MP"
        clientePaga = @{
            nombre = "Pierre"
            apellidos = "Lefebvre"
            correoElectronico = "pierre.lefebvre@email.fr"
            DNI = "10101010J"
            fechaDeNacimiento = "1991-08-25"
        }
        huespedes = @(
            @{
                nombre = "Pierre"
                apellidos = "Lefebvre"
                correoElectronico = "pierre.lefebvre@email.fr"
                DNI = "10101010J"
                fechaDeNacimiento = "1991-08-25"
            }
        )
    }
)

$reservasCreadas = @()
$contador = 1

foreach ($reserva in $reservas) {
    Write-Host "  -> Reserva $contador : $($reserva.clientePaga.nombre) $($reserva.clientePaga.apellidos) - $($reserva.hotel)" -ForegroundColor Gray
    
    try {
        $json = $reserva | ConvertTo-Json -Depth 10
        $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
        $response = Invoke-RestMethod -Uri "$baseUrl/reservas" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
        $reservasCreadas += $response.reserva.idReserva
        Write-Host "    OK Reserva creada ID: $($response.reserva.idReserva) - Precio: EUR$($response.precioDetalle.precioTotal)" -ForegroundColor Green
    }
    catch {
        Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    $contador++
}

Write-Host ""
Write-Host "  Total de reservas creadas: $($reservasCreadas.Count)" -ForegroundColor Cyan
Write-Host ""

# =====================================================
# PARTE 3: HACER 5 CHECK-INS
# =====================================================

Write-Host "PASO 3: Haciendo 5 check-ins..." -ForegroundColor Yellow
Write-Host ""

$checkIns = @(
    @{ idReserva = $reservasCreadas[0]; numeroHabitacion = "H1-301" },  # María - Suite Junior (correcto)
    @{ idReserva = $reservasCreadas[1]; numeroHabitacion = "H1-101" },  # José - Doble Estándar (correcto)
    @{ idReserva = $reservasCreadas[2]; numeroHabitacion = "H1-201" },  # Ana - Doble Superior (correcto)
    @{ idReserva = $reservasCreadas[3]; numeroHabitacion = "H2-301" },  # Carlos - Doble Superior (correcto)
    @{ idReserva = $reservasCreadas[4]; numeroHabitacion = "H2-101" }   # Laura - Individual (correcto)
)

$contratosCreados = @()

foreach ($checkin in $checkIns) {
    Write-Host "  -> Check-in Reserva ID: $($checkin.idReserva) - Habitacion: $($checkin.numeroHabitacion)" -ForegroundColor Gray
    
    try {
        $json = @{ numeroHabitacion = $checkin.numeroHabitacion } | ConvertTo-Json
        $utf8Bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
        $response = Invoke-RestMethod -Uri "$baseUrl/reservas/$($checkin.idReserva)/checkin" -Method POST -Body $utf8Bytes -ContentType "application/json; charset=utf-8"
        $contratosCreados += $response.contrato.idContrato
        Write-Host "    OK Check-in exitoso - Contrato ID: $($response.contrato.idContrato)" -ForegroundColor Green
    }
    catch {
        Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "  Total de check-ins realizados: $($contratosCreados.Count)" -ForegroundColor Cyan
Write-Host ""

# =====================================================
# PARTE 4: HACER 3 CHECK-OUTS
# =====================================================

Write-Host "PASO 4: Haciendo 3 check-outs..." -ForegroundColor Yellow
Write-Host ""

# Vamos a hacer check-out de los 3 primeros contratos
$checkOutsRealizados = 0

for ($i = 0; $i -lt 3 -and $i -lt $contratosCreados.Count; $i++) {
    $contratoId = $contratosCreados[$i]
    Write-Host "  -> Check-out Contrato ID: $contratoId" -ForegroundColor Gray
    
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/contratos/$contratoId/checkout" -Method POST -ContentType "application/json; charset=utf-8"
        Write-Host "    OK Check-out exitoso - Total pagado: EUR$($response.contrato.montoTotal)" -ForegroundColor Green
        $checkOutsRealizados++
    }
    catch {
        Write-Host "    ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "  Total de check-outs realizados: $checkOutsRealizados" -ForegroundColor Cyan
Write-Host ""

# =====================================================
# RESUMEN FINAL
# =====================================================

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE OPERACIONES" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  OK Reservas creadas:        $($reservasCreadas.Count)/10" -ForegroundColor Green
Write-Host "  OK Check-ins realizados:    $($contratosCreados.Count)/5" -ForegroundColor Green
Write-Host "  OK Check-outs realizados:   $checkOutsRealizados/3" -ForegroundColor Green
Write-Host ""

# Consultar estado actual
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  ESTADO ACTUAL DEL SISTEMA" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""

try {
    $todasReservas = Invoke-RestMethod -Uri "$baseUrl/reservas" -Method GET
    Write-Host "  Total de reservas en sistema: $($todasReservas.Count)" -ForegroundColor White
    
    $reservasConContrato = $todasReservas | Where-Object { $null -ne $_.contrato }
    $reservasConCheckIn = $reservasConContrato | Where-Object { $null -ne $_.contrato.fechaCheckIn }
    $reservasConCheckOut = $reservasConCheckIn | Where-Object { $null -ne $_.contrato.fechaCheckOut }
    
    Write-Host "  Reservas con check-in:        $($reservasConCheckIn.Count)" -ForegroundColor White
    Write-Host "  Reservas con check-out:       $($reservasConCheckOut.Count)" -ForegroundColor White
    Write-Host "  Habitaciones ocupadas:        $($reservasConCheckIn.Count - $reservasConCheckOut.Count)" -ForegroundColor Yellow
}
catch {
    Write-Host "  Error al obtener estado: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "  OK PRUEBA COMPLETADA" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host ""
