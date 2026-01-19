<?php
require_once 'config.php';

// Verificar que el usuario esté logueado
if (!isLoggedIn()) {
    header('Location: auth.php');
    exit;
}

$user = getCurrentUser();
$error = null;
$reservas = [];

// Buscar reservas del cliente por nombre y apellido
$response = apiRequest('/reservas/buscar/cliente/activas?nombre=' . urlencode($user['nombre']) . '&apellido=' . urlencode($user['apellidos']));

// Log para debug
error_log("Reservas response: " . json_encode($response));

if ($response['success'] && !empty($response['data']) && is_array($response['data'])) {
    // Filtrar solo arrays válidos
    $reservas = array_filter($response['data'], function($item) {
        return is_array($item) && !empty($item['idReserva']);
    });
} else {
    $reservas = [];
}

// Función para formatear fecha
function formatearFecha($fecha) {
    if (!$fecha) {
        return 'N/A';
    }
    $timestamp = strtotime($fecha);
    return $timestamp ? date('d/m/Y', $timestamp) : 'N/A';
}

// Función para calcular noches
function calcularNoches($fechaEntrada, $fechaSalida) {
    $entrada = strtotime($fechaEntrada);
    $salida = strtotime($fechaSalida);
    $diff = $salida - $entrada;
    return round($diff / (60 * 60 * 24));
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mis Reservas - HotelHub</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        .reservas-container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        
        .reserva-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            overflow: hidden;
            transition: transform 0.2s;
        }
        
        .reserva-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .reserva-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .reserva-id {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        .reserva-estado {
            background: rgba(255,255,255,0.2);
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .reserva-body {
            padding: 1.5rem;
        }
        
        .hotel-info {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #e9ecef;
        }
        
        .hotel-imagen {
            width: 120px;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
        }
        
        .hotel-detalles {
            flex: 1;
        }
        
        .hotel-nombre {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .hotel-ubicacion {
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }
        
        .hotel-estrellas {
            color: #ffc107;
            font-size: 0.9rem;
        }
        
        .reserva-detalles {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .detalle-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .detalle-item i {
            color: #667eea;
            width: 20px;
            text-align: center;
        }
        
        .detalle-label {
            font-size: 0.85rem;
            color: #6c757d;
            display: block;
        }
        
        .detalle-valor {
            font-weight: 500;
            color: #2c3e50;
        }
        
        .precio-total {
            text-align: right;
            font-size: 1.5rem;
            font-weight: 700;
            color: #667eea;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 2px solid #e9ecef;
        }
        
        .no-reservas {
            text-align: center;
            padding: 3rem 1rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .no-reservas i {
            font-size: 4rem;
            color: #dee2e6;
            margin-bottom: 1rem;
        }
        
        .no-reservas h3 {
            color: #6c757d;
            margin-bottom: 1rem;
        }
        
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }
        
        .page-header h1 {
            color: #2c3e50;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .page-header h1 i {
            color: #667eea;
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar">
        <div class="container">
            <a href="index.php" class="navbar-brand"><i class="fas fa-hotel"></i> HotelHub</a>
            <ul class="navbar-menu">
                <li><a href="index.php">Inicio</a></li>
                <li><a href="mis-reservas.php" class="active">Mis Reservas</a></li>
                <li><a href="perfil.php"><i class="fas fa-user-circle"></i> Mi Perfil</a></li>
                <li><a href="?logout=1">Cerrar Sesión</a></li>
            </ul>
        </div>
    </nav>

    <div class="reservas-container">
        <div class="page-header">
            <h1><i class="fas fa-calendar-check"></i> Mis Reservas</h1>
        </div>

        <?php if ($error): ?>
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle"></i> <?= e($error) ?>
            </div>
        <?php endif; ?>

        <?php if (empty($reservas)): ?>
            <div class="no-reservas">
                <i class="fas fa-calendar-times"></i>
                <h3>No tienes reservas activas</h3>
                <p style="color: #6c757d; margin-bottom: 1.5rem;">
                    Comienza a explorar nuestros hoteles y haz tu primera reserva
                </p>
                <a href="index.php" class="button button-primary">
                    <i class="fas fa-search"></i> Buscar Hoteles
                </a>
            </div>
        <?php else: ?>
            <?php foreach ($reservas as $reserva): ?>
                <?php
                    // Validar que sea un array antes de acceder
                    if (!is_array($reserva)) {
                        continue;
                    }

                    $hotel = $reserva['precioRegimen']['hotel'] ?? null;
                    $regimen = $reserva['precioRegimen']['regimen'] ?? null;
                    
                    // Manejar pernoctaciones de forma segura
                    $pernoctaciones = $reserva['pernoctaciones'] ?? [];
                    $tipoHabitacion = null;
                    $fechaEntrada = null;
                    $fechaSalida = null;
                    $noches = 0;
                    
                    if (is_array($pernoctaciones) && !empty($pernoctaciones)) {
                        $tipoHabitacion = $pernoctaciones[0]['tipoHabitacion'] ?? null;
                        $fechaEntrada = $pernoctaciones[0]['fecha'] ?? null;
                        $fechaSalida = $pernoctaciones[count($pernoctaciones) - 1]['fecha'] ?? null;
                        $noches = count($pernoctaciones);
                    }
                    
                    // Intentar obtener precio de diferentes ubicaciones
                    $precioTotal = 0;
                    if (isset($reserva['detallesPrecio']['precioTotal'])) {
                        $precioTotal = $reserva['detallesPrecio']['precioTotal'];
                    } elseif (isset($reserva['precioTotal'])) {
                        $precioTotal = $reserva['precioTotal'];
                    }
                    
                    $huespedes = (is_array($reserva['reservaHuespedes'] ?? null)) ? count($reserva['reservaHuespedes']) + 1 : 1;
                ?>
                <div class="reserva-card">
                    <div class="reserva-header">
                        <div>
                            <div class="reserva-id">Reserva #<?= !empty($reserva['idReserva']) ? e($reserva['idReserva']) : 'N/A' ?></div>
                            <h3 style="margin: 0.3rem 0 0 0; font-size: 1.1rem;">
                                <?= $hotel ? e($hotel['nombre'] ?? 'Hotel') : 'Hotel' ?>
                            </h3>
                        </div>
                        <div class="reserva-estado">
                            <i class="fas fa-check-circle"></i> <?= !empty($reserva['estado']) ? e($reserva['estado']) : 'Activa' ?>
                        </div>
                    </div>
                    
                    <div class="reserva-body">
                        <div class="hotel-info">
                            <img src="<?= $tipoHabitacion && !empty($tipoHabitacion['foto_url']) ? e($tipoHabitacion['foto_url']) : 'https://placehold.co/120x120?text=Hotel' ?>" 
                                 alt="<?= $hotel ? e($hotel['nombre'] ?? 'Hotel') : 'Hotel' ?>"
                                 class="hotel-imagen"
                                 onerror="this.src='https://placehold.co/120x120?text=Hotel'">
                            
                            <div class="hotel-detalles">
                                <div class="hotel-nombre"><?= $hotel ? e($hotel['nombre'] ?? 'Hotel') : 'Hotel' ?></div>
                                <div class="hotel-ubicacion">
                                    <i class="fas fa-map-marker-alt"></i> <?= $hotel ? e($hotel['ubicacion'] ?? 'Ubicación no disponible') : 'Ubicación no disponible' ?>
                                </div>
                                <div class="hotel-estrellas">
                                    <?= $hotel ? str_repeat('★', $hotel['categoria'] ?? 0) : '' ?>
                                </div>
                            </div>
                        </div>
                        
                        <div class="reserva-detalles">
                            <div class="detalle-item">
                                <i class="fas fa-bed"></i>
                                <div>
                                    <span class="detalle-label">Habitación</span>
                                    <div class="detalle-valor"><?= $tipoHabitacion ? e($tipoHabitacion['categoria'] ?? 'N/A') : 'N/A' ?></div>
                                </div>
                            </div>
                            
                            <div class="detalle-item">
                                <i class="fas fa-utensils"></i>
                                <div>
                                    <span class="detalle-label">Régimen</span>
                                    <div class="detalle-valor"><?= $regimen ? e($regimen['nombre'] ?? $regimen['codigo'] ?? 'N/A') : 'N/A' ?></div>
                                </div>
                            </div>
                            
                            <div class="detalle-item">
                                <i class="fas fa-calendar-check"></i>
                                <div>
                                    <span class="detalle-label">Check-in</span>
                                    <div class="detalle-valor"><?= $fechaEntrada ? formatearFecha($fechaEntrada) : 'N/A' ?></div>
                                </div>
                            </div>
                            
                            <div class="detalle-item">
                                <i class="fas fa-calendar-times"></i>
                                <div>
                                    <span class="detalle-label">Check-out</span>
                                    <div class="detalle-valor"><?= $fechaSalida ? formatearFecha($fechaSalida) : 'N/A' ?></div>
                                </div>
                            </div>
                            
                            <div class="detalle-item">
                                <i class="fas fa-moon"></i>
                                <div>
                                    <span class="detalle-label">Noches</span>
                                    <div class="detalle-valor"><?= $noches > 0 ? $noches : 'N/A' ?></div>
                                </div>
                            </div>
                            
                            <div class="detalle-item">
                                <i class="fas fa-users"></i>
                                <div>
                                    <span class="detalle-label">Huéspedes</span>
                                    <div class="detalle-valor"><?= $huespedes > 0 ? $huespedes : 'N/A' ?></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="precio-total">
                            Total: <?= $precioTotal > 0 ? formatPrice($precioTotal) : 'N/A' ?>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>
    </div>

    <footer style="text-align: center; padding: 2rem; color: #6c757d; margin-top: 3rem;">
        <p>&copy; 2025 HotelHub - Todos los derechos reservados</p>
    </footer>
</body>
</html>
