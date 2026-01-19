<?php
require_once 'config.php';

// Obtener parámetros de búsqueda
$ciudad = $_GET['ciudad'] ?? '';
$hotel = $_GET['hotel'] ?? ''; // Nuevo parámetro
$fechaEntrada = $_GET['fechaEntrada'] ?? '';
$fechaSalida = $_GET['fechaSalida'] ?? '';

$error = null;
$hoteles = [];

// Validar parámetros
if (empty($ciudad) || empty($fechaEntrada) || empty($fechaSalida)) {
    $error = 'Por favor completa todos los campos de búsqueda';
} else {
    // Construir query para la API
    $queryParams = http_build_query([
        'ciudad' => $ciudad,
        'fechaEntrada' => $fechaEntrada,
        'fechaSalida' => $fechaSalida
    ]);
    
    // Llamar a la API
    $response = apiRequest('/disponibilidad?' . $queryParams);
    
    // Debug: mostrar respuesta
    error_log("Disponibilidad Response: " . print_r($response, true));
    
    if ($response['success'] && !empty($response['data'])) {
        $hoteles = $response['data'];
        
        // Filtrar por hotel si se especificó
        if (!empty($hotel)) {
            $hoteles = array_filter($hoteles, function($h) use ($hotel) {
                return $h['idHotel'] == $hotel;
            });
        }
    } else {
        $error = 'No se encontraron hoteles disponibles para las fechas seleccionadas';
        error_log("Error en disponibilidad: " . ($response['error'] ?? 'Unknown'));
    }
}

// Calcular número de noches
$noches = 0;
if ($fechaEntrada && $fechaSalida) {
    $noches = calculateNights($fechaEntrada, $fechaSalida);
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados - HotelHub</title>
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
                <?php if (isLoggedIn()): ?>
                    <li><a href="mis-reservas.php">Mis Reservas</a></li>
                    <li><a href="perfil.php"><i class="fas fa-user-circle"></i> Mi Perfil</a></li>
                    <li><a href="?logout=1">Cerrar Sesión</a></li>
                <?php else: ?>
                    <li><a href="auth.php">Iniciar Sesión</a></li>
                    <li><a href="registro.php">Registrarse</a></li>
                <?php endif; ?>
            </ul>
        </div>
    </nav>

    <div class="container">
        <h1 class="page-title">Hoteles en <?= e($ciudad) ?></h1>
        
        <!-- DEBUG: Mostrar respuesta completa de la API -->
        <?php if (isset($_GET['debug'])): ?>
            <div style="background: #f8f9fa; border: 2px solid #dee2e6; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; font-family: monospace; font-size: 12px;">
                <h3 style="margin-top: 0; color: #495057;"><i class="fas fa-bug"></i> Debug - Respuesta de la API</h3>
                <div style="margin-bottom: 1rem;">
                    <strong>Endpoint:</strong> /disponibilidad?ciudad=<?= urlencode($ciudad) ?>&fechaEntrada=<?= $fechaEntrada ?>&fechaSalida=<?= $fechaSalida ?>
                </div>
                <div style="margin-bottom: 1rem;">
                    <strong>HTTP Code:</strong> <span style="color: <?= $response['httpCode'] >= 200 && $response['httpCode'] < 300 ? 'green' : 'red' ?>"><?= $response['httpCode'] ?? 'N/A' ?></span>
                </div>
                <div style="margin-bottom: 1rem;">
                    <strong>Success:</strong> <?= $response['success'] ? '<i class="fas fa-check-circle" style="color: green;"></i> true' : '<i class="fas fa-times-circle" style="color: red;"></i> false' ?>
                </div>
                <details style="margin-top: 1rem;">
                    <summary style="cursor: pointer; color: #007bff; font-weight: bold;">Ver respuesta completa (JSON)</summary>
                    <pre style="background: white; padding: 1rem; border-radius: 4px; overflow-x: auto; max-height: 400px;"><?= htmlspecialchars(json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) ?></pre>
                </details>
                <details style="margin-top: 1rem;">
                    <summary style="cursor: pointer; color: #007bff; font-weight: bold;">Ver datos procesados</summary>
                    <pre style="background: white; padding: 1rem; border-radius: 4px; overflow-x: auto; max-height: 400px;"><?= htmlspecialchars(print_r($hoteles, true)) ?></pre>
                </details>
                <p style="margin-top: 1rem; color: #6c757d; font-size: 11px;">
                    💡 Quita <code>?debug</code> de la URL para ocultar este panel
                </p>
            </div>
        <?php else: ?>
            <div style="text-align: center; margin-bottom: 1rem;">
                <a href="?<?= http_build_query(array_merge($_GET, ['debug' => '1'])) ?>" style="color: #6c757d; font-size: 12px; text-decoration: none;">
                    🐛 Activar modo debug
                </a>
            </div>
        <?php endif; ?>
        
        <div style="text-align: center; margin-bottom: 2rem; color: #666;">
            <p>
                <?= formatDate($fechaEntrada) ?> - <?= formatDate($fechaSalida) ?> 
                (<?= $noches ?> <?= $noches === 1 ? 'noche' : 'noches' ?>)
            </p>
            <a href="index.php" style="color: #3498db;">← Modificar búsqueda</a>
        </div>

        <?php if ($error): ?>
            <div class="alert alert-info">
                <?= e($error) ?>
                <br><br>
                <a href="index.php" class="btn-primary" style="display: inline-block; padding: 0.75rem 2rem; width: auto;">
                    Volver a buscar
                </a>
            </div>
        <?php else: ?>
            <div class="rooms-grid">
                <?php foreach ($hoteles as $hotel): ?>
                    <?php if (!empty($hotel['tiposDisponibles'])): ?>
                        <?php foreach ($hotel['tiposDisponibles'] as $tipo): ?>
                            <div class="room-card">
                                <img src="<?= e($tipo['foto_url'] ?? 'https://placehold.co/600x400?text=Sin+Imagen') ?>" 
                                     alt="<?= e($tipo['categoria']) ?>" 
                                     class="room-image"
                                     onerror="this.src='https://placehold.co/600x400?text=Sin+Imagen'">
                                
                                <div class="room-content">
                                    <p class="room-hotel">
                                        <?= e($hotel['nombre']) ?> 
                                        <?= str_repeat('★', $hotel['categoria']) ?>
                                    </p>
                                    
                                    <h3 class="room-title"><?= e($tipo['categoria']) ?></h3>
                                    
                                    <p class="room-description">
                                        <?= e($hotel['ubicacion']) ?>
                                    </p>
                                    
                                    <div class="room-features">
                                        <?php if ($tipo['camasIndividuales'] > 0): ?>
                                            <span><i class="fas fa-bed"></i> <?= $tipo['camasIndividuales'] ?> cama(s) individual(es)</span>
                                        <?php endif; ?>
                                        <?php if ($tipo['camasDobles'] > 0): ?>
                                            <span><i class="fas fa-bed"></i> <?= $tipo['camasDobles'] ?> cama(s) doble(s)</span>
                                        <?php endif; ?>
                                    </div>
                                    
                                    <p style="font-size: 0.9rem; color: #28a745; font-weight: 500;">
                                        <i class="fas fa-check-circle"></i> <?= $tipo['disponibles'] ?> habitaciones disponibles
                                    </p>
                                    
                                    <div class="room-footer">
                                        <div>
                                            <div class="room-price">
                                                <?= formatPrice($tipo['precioPorNoche'] * $noches) ?>
                                            </div>
                                            <span class="room-price-label">
                                                <?= formatPrice($tipo['precioPorNoche']) ?> / noche
                                            </span>
                                        </div>
                                        
                                        <form action="reservar.php" method="POST">
                                            <input type="hidden" name="idHotel" value="<?= $hotel['idHotel'] ?>">
                                            <input type="hidden" name="idTipoHabitacion" value="<?= $tipo['idTipoHabitacion'] ?>">
                                            <input type="hidden" name="fechaEntrada" value="<?= e($fechaEntrada) ?>">
                                            <input type="hidden" name="fechaSalida" value="<?= e($fechaSalida) ?>">
                                            <input type="hidden" name="precioTotal" value="<?= $tipo['precioPorNoche'] * $noches ?>">
                                            <input type="hidden" name="precioPorNoche" value="<?= $tipo['precioPorNoche'] ?>">
                                            <input type="hidden" name="nombreHotel" value="<?= e($hotel['nombre']) ?>">
                                            <input type="hidden" name="categoriaHabitacion" value="<?= e($tipo['categoria']) ?>">
                                            <button type="submit" class="btn-reserve">Reservar</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        <?php endforeach; ?>
                    <?php endif; ?>
                <?php endforeach; ?>
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
