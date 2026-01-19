<?php
require_once 'config.php';

// Verificar que el usuario esté logueado
if (!isLoggedIn()) {
    header('Location: auth.php');
    exit;
}

$user = getCurrentUser();
$error = null;
$success = null;

// Obtener datos completos del cliente
$responseCliente = apiRequest('/clientes/' . $user['idCliente']);
$clienteCompleto = $responseCliente['success'] ? $responseCliente['data'] : null;

// Procesar actualización de datos
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = trim($_POST['nombre'] ?? '');
    $apellidos = trim($_POST['apellidos'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $dni = trim($_POST['dni'] ?? '');
    $telefono = trim($_POST['telefono'] ?? '');
    $direccion = trim($_POST['direccion'] ?? '');
    $fechaNacimiento = $_POST['fecha_nacimiento'] ?? null;
    
    // Cambio de contraseña (opcional)
    $passwordActual = $_POST['password_actual'] ?? '';
    $passwordNueva = $_POST['password_nueva'] ?? '';
    $passwordConfirm = $_POST['password_confirm'] ?? '';
    
    // Validaciones
    if (empty($nombre) || empty($apellidos) || empty($email) || empty($dni)) {
        $error = 'Por favor completa todos los campos obligatorios';
    } elseif (!empty($passwordNueva)) {
        // Si quiere cambiar contraseña
        if (empty($passwordActual)) {
            $error = 'Debes ingresar tu contraseña actual para cambiarla';
        } elseif (strlen($passwordNueva) < 6) {
            $error = 'La nueva contraseña debe tener al menos 6 caracteres';
        } elseif ($passwordNueva !== $passwordConfirm) {
            $error = 'Las contraseñas nuevas no coinciden';
        }
    }
    
    if (!$error) {
        // Preparar datos para actualizar
        $datosActualizados = [
            'nombre' => $nombre,
            'apellidos' => $apellidos,
            'correoElectronico' => $email,
            'DNI' => $dni
        ];
        
        if (!empty($telefono)) $datosActualizados['telefono'] = $telefono;
        if (!empty($direccion)) $datosActualizados['direccion'] = $direccion;
        if (!empty($fechaNacimiento)) $datosActualizados['fechaDeNacimiento'] = $fechaNacimiento;
        
        // Si hay cambio de contraseña, incluirla
        if (!empty($passwordNueva)) {
            $datosActualizados['password'] = $passwordNueva;
            $datosActualizados['passwordActual'] = $passwordActual;
        }
        
        // Actualizar cliente
        $response = apiRequest('/clientes/' . $user['idCliente'], 'PUT', $datosActualizados);
        
        if ($response['success']) {
            $success = 'Datos actualizados correctamente';
            
            // Actualizar sesión
            $_SESSION['user']['nombre'] = $nombre;
            $_SESSION['user']['apellidos'] = $apellidos;
            $_SESSION['user']['email'] = $email;
            
            // Recargar datos completos
            $responseCliente = apiRequest('/clientes/' . $user['idCliente']);
            $clienteCompleto = $responseCliente['success'] ? $responseCliente['data'] : null;
        } else {
            $error = $response['error'] ?? 'Error al actualizar los datos';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Perfil - HotelHub</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        .perfil-container {
            max-width: 900px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        
        .perfil-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px 12px 0 0;
            text-align: center;
        }
        
        .perfil-avatar {
            width: 100px;
            height: 100px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            margin-bottom: 1rem;
            border: 3px solid rgba(255,255,255,0.3);
        }
        
        .perfil-nombre {
            font-size: 1.8rem;
            font-weight: 600;
            margin: 0;
        }
        
        .perfil-email {
            opacity: 0.9;
            margin-top: 0.3rem;
        }
        
        .perfil-body {
            background: white;
            padding: 2rem;
            border-radius: 0 0 12px 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .perfil-section {
            margin-bottom: 2rem;
        }
        
        .perfil-section h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e9ecef;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .perfil-section h3 i {
            color: #667eea;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .password-toggle {
            cursor: pointer;
            margin-top: 0.5rem;
            color: #667eea;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }
        
        .password-toggle:hover {
            text-decoration: underline;
        }
        
        .password-section {
            display: none;
            margin-top: 1rem;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        
        .password-section.active {
            display: block;
        }
        
        .info-box {
            background: #e3f2fd;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #90caf9;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        
        .info-box i {
            color: #1976d2;
            margin-right: 0.5rem;
        }
        
        .form-actions {
            display: flex;
            gap: 1rem;
            justify-content: flex-end;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 2px solid #e9ecef;
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
                <li><a href="mis-reservas.php">Mis Reservas</a></li>
                <li><a href="perfil.php" class="active"><i class="fas fa-user-circle"></i> Mi Perfil</a></li>
                <li><a href="?logout=1">Cerrar Sesión</a></li>
            </ul>
        </div>
    </nav>

    <div class="perfil-container">
        <div class="perfil-header">
            <div class="perfil-avatar">
                <i class="fas fa-user"></i>
            </div>
            <h1 class="perfil-nombre"><?= e($user['nombre'] . ' ' . $user['apellidos']) ?></h1>
            <p class="perfil-email"><?= e($user['email']) ?></p>
        </div>
        
        <div class="perfil-body">
            <?php if ($error): ?>
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i> <?= e($error) ?>
                </div>
            <?php endif; ?>

            <?php if ($success): ?>
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i> <?= e($success) ?>
                </div>
            <?php endif; ?>

            <form method="POST" action="perfil.php">
                <!-- Datos personales -->
                <div class="perfil-section">
                    <h3><i class="fas fa-user"></i> Datos Personales</h3>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Nombre *</label>
                            <input type="text" name="nombre" class="form-control" 
                                   value="<?= e($clienteCompleto['nombre'] ?? '') ?>" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Apellidos *</label>
                            <input type="text" name="apellidos" class="form-control" 
                                   value="<?= e($clienteCompleto['apellidos'] ?? '') ?>" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>DNI/NIE *</label>
                            <input type="text" name="dni" class="form-control" 
                                   value="<?= e($clienteCompleto['DNI'] ?? '') ?>" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Fecha de Nacimiento</label>
                            <input type="date" name="fecha_nacimiento" class="form-control" 
                                   value="<?= e($clienteCompleto['fechaDeNacimiento'] ? date('Y-m-d', strtotime($clienteCompleto['fechaDeNacimiento'])) : '') ?>">
                        </div>
                    </div>
                </div>

                <!-- Datos de contacto -->
                <div class="perfil-section">
                    <h3><i class="fas fa-envelope"></i> Datos de Contacto</h3>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Email *</label>
                            <input type="email" name="email" class="form-control" 
                                   value="<?= e($clienteCompleto['correoElectronico'] ?? '') ?>" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Teléfono</label>
                            <input type="tel" name="telefono" class="form-control" 
                                   value="<?= e($clienteCompleto['telefono'] ?? '') ?>">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Dirección</label>
                        <input type="text" name="direccion" class="form-control" 
                               value="<?= e($clienteCompleto['direccion'] ?? '') ?>">
                    </div>
                </div>

                <!-- Cambiar contraseña -->
                <div class="perfil-section">
                    <h3><i class="fas fa-lock"></i> Seguridad</h3>
                    
                    <div class="password-toggle" onclick="togglePasswordSection()">
                        <i class="fas fa-key"></i> 
                        <span id="passwordToggleText">Cambiar contraseña</span>
                    </div>
                    
                    <div class="password-section" id="passwordSection">
                        <div class="info-box">
                            <i class="fas fa-info-circle"></i>
                            Deja estos campos vacíos si no deseas cambiar tu contraseña
                        </div>
                        
                        <div class="form-group">
                            <label>Contraseña Actual</label>
                            <input type="password" name="password_actual" class="form-control">
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label>Nueva Contraseña</label>
                                <input type="password" name="password_nueva" class="form-control" 
                                       minlength="6">
                                <small style="color: #6c757d;">Mínimo 6 caracteres</small>
                            </div>
                            
                            <div class="form-group">
                                <label>Confirmar Nueva Contraseña</label>
                                <input type="password" name="password_confirm" class="form-control">
                            </div>
                        </div>
                    </div>
                </div>

                <div class="form-actions">
                    <a href="index.php" class="button button-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="button button-primary">
                        <i class="fas fa-save"></i> Guardar Cambios
                    </button>
                </div>
            </form>
        </div>
    </div>

    <footer style="text-align: center; padding: 2rem; color: #6c757d; margin-top: 3rem;">
        <p>&copy; 2025 HotelHub - Todos los derechos reservados</p>
    </footer>

    <script>
        function togglePasswordSection() {
            const section = document.getElementById('passwordSection');
            const text = document.getElementById('passwordToggleText');
            
            if (section.classList.contains('active')) {
                section.classList.remove('active');
                text.textContent = 'Cambiar contraseña';
            } else {
                section.classList.add('active');
                text.textContent = 'Ocultar cambio de contraseña';
            }
        }
    </script>
</body>
</html>
