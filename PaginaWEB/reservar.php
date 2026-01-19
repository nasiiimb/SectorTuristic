<?php
require_once 'config.php';

// Verificar que el usuario esté logueado
if (!isLoggedIn()) {
    // Guardar datos en sesión y redirigir al login
    $_SESSION['pending_reservation'] = $_POST;
    header('Location: auth.php?redirect=reservar.php');
    exit;
}

// Recuperar datos de la reserva
$datosReserva = $_SESSION['pending_reservation'] ?? $_POST;
$_SESSION['pending_reservation'] = null;

if (empty($datosReserva)) {
    header('Location: index.php');
    exit;
}

$idHotel = $datosReserva['idHotel'] ?? null;
$idTipoHabitacion = $datosReserva['idTipoHabitacion'] ?? null;
$fechaEntrada = $datosReserva['fechaEntrada'] ?? null;
$fechaSalida = $datosReserva['fechaSalida'] ?? null;
$precioTotal = $datosReserva['precioTotal'] ?? null;
$precioPorNoche = $datosReserva['precioPorNoche'] ?? null;
$nombreHotel = $datosReserva['nombreHotel'] ?? 'Hotel';
$categoriaHabitacion = $datosReserva['categoriaHabitacion'] ?? 'Habitación';

// Obtener todos los regímenes disponibles desde la API
$responseRegimenes = apiRequest("/regimenes");
$regimenes = [];

// Mapeo de códigos de régimen a nombres descriptivos
$nombresRegimenes = [
    'SA' => 'Solo Alojamiento',
    'AD' => 'Alojamiento y Desayuno',
    'MP' => 'Media Pensión',
    'PC' => 'Pensión Completa',
    'TI' => 'Todo Incluido'
];

if ($responseRegimenes['success']) {
    $regimenes = $responseRegimenes['data'];
    // Agregar nombres descriptivos a cada régimen
    foreach ($regimenes as &$regimen) {
        $regimen['nombre'] = $nombresRegimenes[$regimen['codigo']] ?? $regimen['codigo'];
    }
    unset($regimen); // Romper la referencia
}

// Calcular noches
$noches = calculateNights($fechaEntrada, $fechaSalida);

// Obtener usuario actual
$user = getCurrentUser();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de Reserva - HotelHub</title>
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

    <div class="container" style="padding: 3rem 0;">
        <div class="auth-container">
            <div class="auth-box" style="max-width: 800px;">
                <h1 class="auth-title">Completa tu Reserva</h1>
                
                <!-- Resumen de la reserva -->
                <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
                    <h3 style="margin-top: 0; color: #333;"><i class="fas fa-clipboard-list"></i> Resumen de la Reserva</h3>
                    <div style="display: grid; gap: 0.75rem;">
                        <p><strong><i class="fas fa-hotel"></i> Hotel:</strong> <?= e($nombreHotel) ?></p>
                        <p><strong><i class="fas fa-bed"></i> Habitación:</strong> <?= e($categoriaHabitacion) ?></p>
                        <p><strong><i class="fas fa-calendar-check"></i> Check-in:</strong> <?= date('d/m/Y', strtotime($fechaEntrada)) ?></p>
                        <p><strong><i class="fas fa-calendar-check"></i> Check-out:</strong> <?= date('d/m/Y', strtotime($fechaSalida)) ?></p>
                        <p><strong><i class="fas fa-moon"></i> Noches:</strong> <?= $noches ?></p>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 0.5rem 0;">
                        <p><strong>Habitación:</strong> <span data-precio-habitacion><?= formatPrice($precioPorNoche * $noches) ?></span></p>
                        <p><strong>Régimen:</strong> <span data-precio-regimen>0,00 €</span> <span style="font-size: 0.85rem; color: #666;">(Selecciona un régimen)</span></p>
                        <hr style="border: none; border-top: 2px solid #ddd; margin: 0.5rem 0;">
                        <p style="font-size: 1.25rem; color: #e74c3c; font-weight: bold;">
                            <strong><i class="fas fa-euro-sign"></i> Precio Total:</strong> <span data-precio-total><?= formatPrice($precioTotal) ?></span>
                        </p>
                        <p style="font-size: 0.85rem; color: #666;">
                            * Selecciona un régimen para ver el precio actualizado
                        </p>
                    </div>
                </div>

                <!-- Formulario de reserva -->
                <form action="confirmar.php" method="POST" class="auth-form">
                    <!-- Campos ocultos con datos de la reserva -->
                    <input type="hidden" name="idHotel" value="<?= $idHotel ?>">
                    <input type="hidden" name="idTipoHabitacion" value="<?= $idTipoHabitacion ?>">
                    <input type="hidden" name="fechaEntrada" value="<?= e($fechaEntrada) ?>">
                    <input type="hidden" name="fechaSalida" value="<?= e($fechaSalida) ?>">
                    <input type="hidden" name="precioTotal" value="<?= $precioTotal ?>">
                    <input type="hidden" name="nombreHotel" value="<?= e($nombreHotel) ?>">
                    <input type="hidden" name="categoriaHabitacion" value="<?= e($categoriaHabitacion) ?>">
                    
                    <!-- Selección de régimen -->
                    <div class="form-group">
                        <label for="regimen">Régimen de Alojamiento *</label>
                        <select id="regimen" name="codigoRegimen" class="form-control" required>
                            <option value="">Selecciona un régimen</option>
                            <?php if (!empty($regimenes)): ?>
                                <?php foreach ($regimenes as $regimen): ?>
                                    <option value="<?= e($regimen['codigo']) ?>">
                                        <?= e($regimen['nombre']) ?> (<?= e($regimen['codigo']) ?>)
                                    </option>
                                <?php endforeach; ?>
                            <?php else: ?>
                                <option value="SA">Solo Alojamiento (SA)</option>
                                <option value="AD">Alojamiento y Desayuno (AD)</option>
                                <option value="MP">Media Pensión (MP)</option>
                                <option value="PC">Pensión Completa (PC)</option>
                                <option value="TI">Todo Incluido (TI)</option>
                            <?php endif; ?>
                        </select>
                    </div>

                    <!-- Información del huésped principal -->
                    <h3 style="margin-top: 2rem; margin-bottom: 1rem;"><i class="fas fa-user"></i> Información del Huésped Principal</h3>
                    <p style="color: #666; font-size: 0.9rem; margin-bottom: 1rem;">
                        Los datos se completarán automáticamente con tu información de usuario.
                    </p>

                    <div class="form-group">
                        <label>Nombre Completo</label>
                        <input type="text" class="form-control" value="<?= e($user['nombre'] . ' ' . $user['apellidos']) ?>" disabled>
                    </div>

                    <div class="form-group">
                        <label>Email</label>
                        <input type="text" class="form-control" value="<?= e($user['email']) ?>" disabled>
                    </div>

                    <!-- Notas adicionales -->
                    <div class="form-group">
                        <label for="notas">Peticiones Especiales (Opcional)</label>
                        <textarea id="notas" name="notas" class="form-control" rows="4" 
                                  placeholder="Ej: Cama supletoria, cuna para bebé, piso alto, etc."></textarea>
                    </div>

                    <!-- Términos y condiciones -->
                    <div class="form-group">
                        <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                            <input type="checkbox" name="terminos" required>
                            <span>Acepto los <a href="#" style="color: #3498db;">términos y condiciones</a> *</span>
                        </label>
                    </div>

                    <!-- Botones -->
                    <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                        <a href="javascript:history.back()" class="btn-secondary" style="flex: 1; text-align: center; text-decoration: none;">
                            Volver
                        </a>
                        <button type="submit" class="btn-primary" style="flex: 1;">
                            Confirmar y Pagar
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 HotelHub - Sector Turístico. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script>
        // Precio base por noche de la habitación
        const precioBaseNoche = <?= $precioPorNoche ?>;
        const noches = <?= $noches ?>;
        const nombreHotel = '<?= addslashes($nombreHotel) ?>';
        
        // Precios de regímenes para este hotel
        const preciosRegimenes = {
            <?php foreach ($regimenes as $reg): ?>
                <?php 
                // Buscar el precio del régimen para este hotel
                $precioRegimen = 0;
                if (!empty($reg['disponibleEn'])) {
                    foreach ($reg['disponibleEn'] as $hotel) {
                        if ($hotel['hotel'] === $nombreHotel) {
                            $precioRegimen = $hotel['precio'];
                            break;
                        }
                    }
                }
                ?>
                '<?= $reg['codigo'] ?>': <?= $precioRegimen ?>,
            <?php endforeach; ?>
        };

        // Función para actualizar el precio total
        function actualizarPrecio() {
            const regimenSelect = document.getElementById('regimen');
            const codigoRegimen = regimenSelect.value;
            
            if (codigoRegimen && preciosRegimenes[codigoRegimen] !== undefined) {
                const precioRegimen = preciosRegimenes[codigoRegimen];
                const precioTotalHabitacion = precioBaseNoche * noches;
                const precioTotalRegimen = precioRegimen * noches;
                const precioTotal = precioTotalHabitacion + precioTotalRegimen;
                
                // Actualizar el precio del régimen
                const precioRegimenElement = document.querySelector('[data-precio-regimen]');
                if (precioRegimenElement) {
                    precioRegimenElement.textContent = precioTotalRegimen.toFixed(2) + ' €';
                    precioRegimenElement.nextElementSibling.textContent = '(' + precioRegimen.toFixed(2) + ' € por noche)';
                }
                
                // Actualizar el precio total en el resumen
                const precioElement = document.querySelector('[data-precio-total]');
                if (precioElement) {
                    precioElement.textContent = precioTotal.toFixed(2) + ' €';
                }
                
                // Actualizar el input hidden del precio total
                const precioInput = document.querySelector('input[name="precioTotal"]');
                if (precioInput) {
                    precioInput.value = precioTotal.toFixed(2);
                }
            } else {
                // Si no hay régimen seleccionado, mostrar solo el precio de la habitación
                const precioRegimenElement = document.querySelector('[data-precio-regimen]');
                if (precioRegimenElement) {
                    precioRegimenElement.textContent = '0,00 €';
                    precioRegimenElement.nextElementSibling.textContent = '(Selecciona un régimen)';
                }
                
                const precioElement = document.querySelector('[data-precio-total]');
                if (precioElement) {
                    const precioHabitacion = precioBaseNoche * noches;
                    precioElement.textContent = precioHabitacion.toFixed(2) + ' €';
                }
            }
        }

        // Escuchar cambios en el select de régimen
        document.addEventListener('DOMContentLoaded', function() {
            const regimenSelect = document.getElementById('regimen');
            if (regimenSelect) {
                regimenSelect.addEventListener('change', actualizarPrecio);
                // Actualizar precio inicial si hay un régimen pre-seleccionado
                actualizarPrecio();
            }
        });
    </script>

    <?php
    // Manejar logout
    if (isset($_GET['logout'])) {
        logout();
    }
    ?>
</body>
</html>
