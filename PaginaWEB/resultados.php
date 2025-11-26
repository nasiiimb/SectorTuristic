<?php
require_once 'config.php';

// Obtener parámetros de búsqueda
$ciudad = $_GET['ciudad'] ?? '';
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
    
    if ($response['success'] && !empty($response['data'])) {
        $hoteles = $response['data'];
    } else {
        $error = 'No se encontraron hoteles disponibles para las fechas seleccionadas';
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
    <title>Resultados de Búsqueda - HotelHub</title>
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
                <?php if (isLoggedIn()): ?>
                    <li><a href="#">Mis Reservas</a></li>
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
                                        <?= str_repeat('⭐', $hotel['categoria']) ?>
                                    </p>
                                    
                                    <h3 class="room-title"><?= e($tipo['categoria']) ?></h3>
                                    
                                    <p class="room-description">
                                        <?= e($hotel['ubicacion']) ?>
                                    </p>
                                    
                                    <div class="room-features">
                                        <?php if ($tipo['camasIndividuales'] > 0): ?>
                                            <span>🛏️ <?= $tipo['camasIndividuales'] ?> cama(s) individual(es)</span>
                                        <?php endif; ?>
                                        <?php if ($tipo['camasDobles'] > 0): ?>
                                            <span>🛏️ <?= $tipo['camasDobles'] ?> cama(s) doble(s)</span>
                                        <?php endif; ?>
                                    </div>
                                    
                                    <p style="font-size: 0.9rem; color: #28a745; font-weight: 500;">
                                        ✅ <?= $tipo['disponibles'] ?> habitaciones disponibles
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
                                        
                                        <form action="confirmar.php" method="POST">
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
