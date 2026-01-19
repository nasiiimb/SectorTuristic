<?php
require_once 'config.php';

// Verificar que el usuario esté logueado
if (!isLoggedIn()) {
    header('Location: auth.php');
    exit;
}

$error = null;
$success = null;
$reservaId = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $idHotel = $_POST['idHotel'] ?? null;
    $idTipoHabitacion = $_POST['idTipoHabitacion'] ?? null;
    $fechaEntrada = $_POST['fechaEntrada'] ?? null;
    $fechaSalida = $_POST['fechaSalida'] ?? null;
    $codigoRegimen = $_POST['codigoRegimen'] ?? null;
    $precioTotal = $_POST['precioTotal'] ?? null;
    $nombreHotel = $_POST['nombreHotel'] ?? 'Hotel';
    $categoriaHabitacion = $_POST['categoriaHabitacion'] ?? 'Habitación';
    
    if (!$idHotel || !$idTipoHabitacion || !$fechaEntrada || !$fechaSalida || !$codigoRegimen) {
        $error = 'Faltan parámetros requeridos: fechaEntrada, fechaSalida, tipo, clientePaga (objeto), hotel (nombre), tipoHabitacion (nombre), regimen (código)';
    } else {
        // Obtener usuario actual
        $user = getCurrentUser();
        
        // Crear la reserva con el formato esperado por el endpoint
        $reservaData = [
            'fechaEntrada' => $fechaEntrada,
            'fechaSalida' => $fechaSalida,
            'tipo' => 'Reserva',
            'clientePaga' => [
                'nombre' => $user['nombre'],
                'apellidos' => $user['apellidos'],
                'correoElectronico' => $user['email'],
                'DNI' => $user['DNI'] ?? '00000000X'
            ],
            'hotel' => $nombreHotel,
            'tipoHabitacion' => $categoriaHabitacion,
            'regimen' => $codigoRegimen
        ];
        
        $response = apiRequest('/reservas', 'POST', $reservaData);
        
        if ($response['success']) {
            $reservaId = $response['data']['idReserva'] ?? $response['data']['reserva']['idReserva'] ?? null;
            $success = true;
            
            // Guardar datos para mostrar en la confirmación
            $datosReserva = [
                'nombreHotel' => $nombreHotel,
                'categoriaHabitacion' => $categoriaHabitacion,
                'fechaEntrada' => $fechaEntrada,
                'fechaSalida' => $fechaSalida,
                'precioTotal' => $precioTotal
            ];
        } else {
            $error = $response['error'] ?? ($response['data']['message'] ?? 'Error al crear la reserva');
        }
    }
} else {
    header('Location: index.php');
    exit;
}

// Calcular noches
$noches = 0;
if (isset($fechaEntrada) && isset($fechaSalida)) {
    $noches = calculateNights($fechaEntrada, $fechaSalida);
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="container">
            <a href="index.php" class="navbar-brand"><i class="fas fa-hotel"></i> HotelHub</a>
            <ul class="navbar-menu">
                <li><a href="index.php">Inicio</a></li>
                <li><a href="mis-reservas.php">Mis Reservas</a></li>
                <li><a href="perfil.php"><i class="fas fa-user-circle"></i> Mi Perfil</a></li>
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
                        <strong>Importante:</strong> El pago se realizará en el hotel durante el check-in. 
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
                    <strong><i class="fas fa-info-circle"></i> Información importante:</strong>
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
