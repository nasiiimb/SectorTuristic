Write-Host "`nTEST DE API - SECTOR TURISTICO`n" -ForegroundColor Cyan

$baseUrl = "http://localhost:3000/api"
$ok = 0
$fail = 0

# 1. GET Hoteles
try { $h = Invoke-RestMethod "$baseUrl/hoteles" ; Write-Host "[OK] GET hoteles ($($h.Count))" -ForegroundColor Green ; $ok++ } catch { Write-Host "[FAIL] GET hoteles" -ForegroundColor Red ; $fail++ }

# 2. GET Regimenes
try { $r = Invoke-RestMethod "$baseUrl/regimenes" ; Write-Host "[OK] GET regimenes ($($r.Count))" -ForegroundColor Green ; $ok++ } catch { Write-Host "[FAIL] GET regimenes" -ForegroundColor Red ; $fail++ }

# 3. GET Tipos Habitacion
try { $t = Invoke-RestMethod "$baseUrl/tipos-habitacion" ; Write-Host "[OK] GET tipos-habitacion ($($t.Count))" -ForegroundColor Green ; $ok++ } catch { Write-Host "[FAIL] GET tipos-habitacion" -ForegroundColor Red ; $fail++ }

# 4. ERROR 404
try { Invoke-RestMethod "$baseUrl/hoteles/9999" ; Write-Host "[FAIL] Error 404 no funciona" -ForegroundColor Red ; $fail++ } catch { if ($_.Exception.Response.StatusCode.value__ -eq 404) { Write-Host "[OK] Error 404 funciona" -ForegroundColor Green ; $ok++ } else { Write-Host "[FAIL] Codigo incorrecto" -ForegroundColor Red ; $fail++ } }

# 5. ERROR 400
try { Invoke-RestMethod "$baseUrl/disponibilidad?hotel=Test" ; Write-Host "[FAIL] Error 400 no funciona" -ForegroundColor Red ; $fail++ } catch { if ($_.Exception.Response.StatusCode.value__ -eq 400) { Write-Host "[OK] Error 400 funciona" -ForegroundColor Green ; $ok++ } else { Write-Host "[FAIL] Codigo incorrecto" -ForegroundColor Red ; $fail++ } }

# 6. POST Reserva
$body = @{ fechaEntrada = "2025-01-10" ; fechaSalida = "2025-01-13" ; tipo = "Reserva" ; clientePaga = @{ nombre = "Test" ; apellidos = "Usuario" ; correoElectronico = "test@email.com" ; DNI = "99999999Z" } ; hotel = "Gran Hotel del Mar" ; tipoHabitacion = "Doble Estandar" ; regimen = "AD" } | ConvertTo-Json -Depth 10
$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
try { $res = Invoke-RestMethod "$baseUrl/reservas" -Method POST -Body $bytes -ContentType "application/json; charset=utf-8" ; $resId = $res.reserva.idReserva ; Write-Host "[OK] POST reserva (ID: $resId)" -ForegroundColor Green ; $ok++ } catch { Write-Host "[FAIL] POST reserva: $($_.Exception.Message)" -ForegroundColor Red ; $fail++ ; $resId = $null }

# 7. POST Check-in
if ($resId) {
  $checkinBody = @{ numeroHabitacion = "H1-101" } | ConvertTo-Json
  $bytes2 = [System.Text.Encoding]::UTF8.GetBytes($checkinBody)
  try { $cont = Invoke-RestMethod "$baseUrl/reservas/$resId/checkin" -Method POST -Body $bytes2 -ContentType "application/json; charset=utf-8" ; $contId = $cont.contrato.idContrato ; Write-Host "[OK] POST check-in (Contrato: $contId)" -ForegroundColor Green ; $ok++ } catch { Write-Host "[FAIL] POST check-in: $($_.Exception.Message)" -ForegroundColor Red ; $fail++ ; $contId = $null }
}

# 8. ERROR 409 Check-in duplicado
if ($resId) {
  $checkinBody2 = @{ numeroHabitacion = "H1-102" } | ConvertTo-Json
  $bytes3 = [System.Text.Encoding]::UTF8.GetBytes($checkinBody2)
  try { Invoke-RestMethod "$baseUrl/reservas/$resId/checkin" -Method POST -Body $bytes3 -ContentType "application/json; charset=utf-8" ; Write-Host "[FAIL] Error 409 no funciona" -ForegroundColor Red ; $fail++ } catch { if ($_.Exception.Response.StatusCode.value__ -eq 409) { Write-Host "[OK] Error 409 check-in duplicado" -ForegroundColor Green ; $ok++ } else { Write-Host "[FAIL] Codigo incorrecto ($($_.Exception.Response.StatusCode.value__))" -ForegroundColor Red ; $fail++ } }
}

# 9. POST Check-out
if ($contId) {
  try { Invoke-RestMethod "$baseUrl/contratos/$contId/checkout" -Method POST -ContentType "application/json; charset=utf-8" | Out-Null ; Write-Host "[OK] POST check-out" -ForegroundColor Green ; $ok++ } catch { Write-Host "[FAIL] POST check-out" -ForegroundColor Red ; $fail++ }
}

# 10. ERROR 409 Check-out duplicado
if ($contId) {
  try { Invoke-RestMethod "$baseUrl/contratos/$contId/checkout" -Method POST -ContentType "application/json; charset=utf-8" ; Write-Host "[FAIL] Error 409 checkout no funciona" -ForegroundColor Red ; $fail++ } catch { if ($_.Exception.Response.StatusCode.value__ -eq 409) { Write-Host "[OK] Error 409 check-out duplicado" -ForegroundColor Green ; $ok++ } else { Write-Host "[FAIL] Codigo incorrecto" -ForegroundColor Red ; $fail++ } }
}

Write-Host "`nRESULTADO: $ok OK / $fail FAIL" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Yellow" })
if ($fail -eq 0) { Write-Host "`nTODOS LOS TESTS PASARON - PROYECTO LISTO`n" -ForegroundColor Green }
