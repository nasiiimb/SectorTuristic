<?php
require_once 'config.php';

// Verificar que el usuario esté logueado
if (!isLoggedIn()) {
    // Guardar datos en sesión y redirigir al login
    $_SESSION['pending_reservation'] = $_POST;
    header('Location: auth.php?redirect=confirmar.php');
    exit;
}

$error = null;
$success = null;
$reservaId = null;

// Recuperar datos de la reserva
$datosReserva = $_SESSION['pending_reservation'] ?? $_POST;
$_SESSION['pending_reservation'] = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($datosReserva)) {
    $idHotel = $datosReserva['idHotel'] ?? null;
    $idTipoHabitacion = $datosReserva['idTipoHabitacion'] ?? null;
    $fechaEntrada = $datosReserva['fechaEntrada'] ?? null;
    $fechaSalida = $datosReserva['fechaSalida'] ?? null;
    $precioTotal = $datosReserva['precioTotal'] ?? null;
    
    if (!$idHotel || !$idTipoHabitacion || !$fechaEntrada || !$fechaSalida) {
        $error = 'Datos de reserva incompletos';
    } else {
        // Obtener usuario actual
        $user = getCurrentUser();
        
        // Buscar el PrecioRegimen correspondiente al hotel
        $responseRegimen = apiRequest("/hoteles/{$idHotel}");
        $idPrecioRegimen = null;
        
        if ($responseRegimen['success'] && !empty($responseRegimen['data']['preciosRegimen'])) {
            // Usar el primer régimen disponible (SA - Solo Alojamiento por defecto)
            $idPrecioRegimen = $responseRegimen['data']['preciosRegimen'][0]['idPrecioRegimen'];
        } else {
            $error = 'No se encontró información de régimen para este hotel';
        }
        
        if (!$error) {
            // Crear la reserva
            $reservaData = [
                'fechaEntrada' => $fechaEntrada,
                'fechaSalida' => $fechaSalida,
                'canalReserva' => 'Web',
                'tipo' => 'Reserva',
                'idCliente_paga' => $user['idCliente'],
                'idPrecioRegimen' => $idPrecioRegimen,
                'tipoHabitacion' => $idTipoHabitacion,
                'huespedes' => [$user['idCliente']]
            ];
            
            $response = apiRequest('/reservas', 'POST', $reservaData);
            
            if ($response['success']) {
                $reservaId = $response['data']['idReserva'] ?? $response['data']['reserva']['idReserva'] ?? null;
                $success = true;
            } else {
                $error = $response['data']['message'] ?? 'Error al crear la reserva';
            }
        }
    }
}

// Calcular noches
$noches = 0;
if (isset($datosReserva['fechaEntrada']) && isset($datosReserva['fechaSalida'])) {
    $noches = calculateNights($datosReserva['fechaEntrada'], $datosReserva['fechaSalida']);
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmar Reserva - HotelHub</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="container">
            <a href="index.php" class="navbar-brand">🏨 HotelHub</a>
            <ul class="navbar-menu">
                <li><a href="index.php">Inicio</a></li>
                <li><a href="?logout=1">Cerrar Sesión</a></li>
            </ul>
        </div>
    </nav>

    <div class="container">
        <?php if ($success): ?>
            <!-- Reserva exitosa -->
            <div class="auth-container">
                <div class="auth-box" style="max-width: 600px;">
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <div style="font-size: 4rem; color: #28a745;">✓</div>
                        <h2 style="color: #28a745; margin: 1rem 0;">¡Reserva Confirmada!</h2>
                    </div>
                    
                    <div class="alert alert-success">
                        Tu reserva se ha realizado correctamente. 
                        <?php if ($reservaId): ?>
                            Tu número de reserva es: <strong>#<?= $reservaId ?></strong>
                        <?php endif; ?>
                    </div>
                    
                    <div class="summary-box">
                        <h3 style="margin-bottom: 1.5rem; color: var(--primary-color);">Detalles de tu reserva</h3>
                        
                        <div class="summary-row">
                            <span class="summary-label">Hotel:</span>
                            <span class="summary-value"><?= e($datosReserva['nombreHotel'] ?? 'N/A') ?></span>
                        </div>
                        
                        <div class="summary-row">
                            <span class="summary-label">Habitación:</span>
                            <span class="summary-value"><?= e($datosReserva['categoriaHabitacion'] ?? 'N/A') ?></span>
                        </div>
                        
                        <div class="summary-row">
                            <span class="summary-label">Entrada:</span>
                            <span class="summary-value"><?= formatDate($datosReserva['fechaEntrada']) ?></span>
                        </div>
                        
                        <div class="summary-row">
                            <span class="summary-label">Salida:</span>
                            <span class="summary-value"><?= formatDate($datosReserva['fechaSalida']) ?></span>
                        </div>
                        
                        <div class="summary-row">
                            <span class="summary-label">Noches:</span>
                            <span class="summary-value"><?= $noches ?></span>
                        </div>
                        
                        <div class="summary-row">
                            <span class="summary-label">Total:</span>
                            <span class="summary-value"><?= formatPrice($datosReserva['precioTotal'] ?? 0) ?></span>
                        </div>
                    </div>
                    
                    <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; margin: 1.5rem 0; border: 1px solid #ffeaa7;">
                        <strong>📌 Importante:</strong> El pago se realizará en el hotel durante el check-in. 
                        Por favor, presenta tu DNI y esta confirmación.
                    </div>
                    
                    <a href="index.php" class="btn-primary">Volver al Inicio</a>
                </div>
            </div>
        <?php elseif ($error): ?>
            <!-- Error -->
            <div class="auth-container">
                <div class="auth-box">
                    <h2 style="color: var(--accent-color);">Error en la Reserva</h2>
                    <div class="alert alert-error">
                        <?= e($error) ?>
                    </div>
                    <a href="index.php" class="btn-primary">Volver al Inicio</a>
                </div>
            </div>
        <?php else: ?>
            <!-- Confirmación de datos -->
            <h1 class="page-title">Confirmar Reserva</h1>
            
            <div style="max-width: 600px; margin: 0 auto;">
                <div class="summary-box">
                    <h3 style="margin-bottom: 1.5rem; color: var(--primary-color);">Resumen de tu reserva</h3>
                    
                    <div class="summary-row">
                        <span class="summary-label">Hotel:</span>
                        <span class="summary-value"><?= e($datosReserva['nombreHotel'] ?? 'N/A') ?></span>
                    </div>
                    
                    <div class="summary-row">
                        <span class="summary-label">Habitación:</span>
                        <span class="summary-value"><?= e($datosReserva['categoriaHabitacion'] ?? 'N/A') ?></span>
                    </div>
                    
                    <div class="summary-row">
                        <span class="summary-label">Entrada:</span>
                        <span class="summary-value"><?= formatDate($datosReserva['fechaEntrada']) ?></span>
                    </div>
                    
                    <div class="summary-row">
                        <span class="summary-label">Salida:</span>
                        <span class="summary-value"><?= formatDate($datosReserva['fechaSalida']) ?></span>
                    </div>
                    
                    <div class="summary-row">
                        <span class="summary-label">Noches:</span>
                        <span class="summary-value"><?= $noches ?></span>
                    </div>
                    
                    <div class="summary-row">
                        <span class="summary-label">Precio por noche:</span>
                        <span class="summary-value"><?= formatPrice($datosReserva['precioPorNoche'] ?? 0) ?></span>
                    </div>
                    
                    <div class="summary-row">
                        <span>Total a pagar en el hotel:</span>
                        <span><?= formatPrice($datosReserva['precioTotal'] ?? 0) ?></span>
                    </div>
                </div>
                
                <div style="background: #e3f2fd; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0; border: 1px solid #90caf9;">
                    <strong>ℹ️ Información importante:</strong>
                    <ul style="margin: 0.5rem 0 0 1.5rem; line-height: 1.8;">
                        <li>El pago se realizará en el hotel durante el check-in</li>
                        <li>No es necesario tarjeta de crédito ahora</li>
                        <li>Puedes cancelar gratuitamente hasta 24h antes</li>
                    </ul>
                </div>
                
                <form method="POST">
                    <input type="hidden" name="idHotel" value="<?= e($datosReserva['idHotel'] ?? '') ?>">
                    <input type="hidden" name="idTipoHabitacion" value="<?= e($datosReserva['idTipoHabitacion'] ?? '') ?>">
                    <input type="hidden" name="fechaEntrada" value="<?= e($datosReserva['fechaEntrada'] ?? '') ?>">
                    <input type="hidden" name="fechaSalida" value="<?= e($datosReserva['fechaSalida'] ?? '') ?>">
                    <input type="hidden" name="precioTotal" value="<?= e($datosReserva['precioTotal'] ?? '') ?>">
                    <input type="hidden" name="precioPorNoche" value="<?= e($datosReserva['precioPorNoche'] ?? '') ?>">
                    <input type="hidden" name="nombreHotel" value="<?= e($datosReserva['nombreHotel'] ?? '') ?>">
                    <input type="hidden" name="categoriaHabitacion" value="<?= e($datosReserva['categoriaHabitacion'] ?? '') ?>">
                    
                    <button type="submit" class="btn-primary">Confirmar Reserva</button>
                    <a href="javascript:history.back()" class="btn-primary" style="background: #6c757d; margin-top: 1rem;">
                        Volver
                    </a>
                </form>
            </div>
        <?php endif; ?>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 HotelHub - Sector Turístico. Todos los derechos reservados.</p>
        </div>
    </footer>

    <?php
    // Manejar logout
    if (isset($_GET['logout'])) {
        logout();
    }
    ?>
</body>
</html>
