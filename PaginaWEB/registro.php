<?php
require_once 'config.php';

$error = null;
$success = null;

// Procesar registro
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = $_POST['nombre'] ?? '';
    $apellidos = $_POST['apellidos'] ?? '';
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    $confirmPassword = $_POST['confirm_password'] ?? '';
    $dni = $_POST['dni'] ?? '';
    $fechaNacimiento = $_POST['fecha_nacimiento'] ?? null;
    
    // Validaciones
    if (empty($nombre) || empty($apellidos) || empty($email) || empty($password) || empty($dni)) {
        $error = 'Por favor completa todos los campos obligatorios';
    } elseif ($password !== $confirmPassword) {
        $error = 'Las contraseñas no coinciden';
    } elseif (strlen($password) < 6) {
        $error = 'La contraseña debe tener al menos 6 caracteres';
    } else {
        // Crear cliente
        $clienteData = [
            'nombre' => $nombre,
            'apellidos' => $apellidos,
            'correoElectronico' => $email,
            'DNI' => $dni,
            'email' => $email,  // Para el login
            'password' => password_hash($password, PASSWORD_DEFAULT)
        ];
        
        if ($fechaNacimiento) {
            $clienteData['fechaDeNacimiento'] = $fechaNacimiento;
        }
        
        $response = apiRequest('/clientes', 'POST', $clienteData);
        
        if ($response['success']) {
            $success = 'Registro exitoso. Ya puedes iniciar sesión.';
            // Limpiar el formulario
            $_POST = [];
        } else {
            $errorMsg = $response['data']['message'] ?? 'Error al registrar el usuario';
            if (strpos($errorMsg, 'Duplicate entry') !== false) {
                if (strpos($errorMsg, 'correoElectronico') !== false) {
                    $error = 'Este email ya está registrado';
                } elseif (strpos($errorMsg, 'DNI') !== false) {
                    $error = 'Este DNI ya está registrado';
                } else {
                    $error = 'Este usuario ya está registrado';
                }
            } else {
                $error = $errorMsg;
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registrarse - HotelHub</title>
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
                <li><a href="auth.php">Iniciar Sesión</a></li>
            </ul>
        </div>
    </nav>

    <div class="auth-container">
        <div class="auth-box">
            <h2>Crear Cuenta</h2>
            
            <?php if ($error): ?>
                <div class="alert alert-error">
                    <?= e($error) ?>
                </div>
            <?php endif; ?>
            
            <?php if ($success): ?>
                <div class="alert alert-success">
                    <?= e($success) ?>
                    <br><br>
                    <a href="auth.php" class="btn-primary" style="display: inline-block; padding: 0.75rem 2rem;">
                        Iniciar Sesión
                    </a>
                </div>
            <?php else: ?>
                <form method="POST">
                    <div class="form-group">
                        <label for="nombre">Nombre *</label>
                        <input type="text" id="nombre" name="nombre" required 
                               value="<?= e($_POST['nombre'] ?? '') ?>">
                    </div>
                    
                    <div class="form-group">
                        <label for="apellidos">Apellidos *</label>
                        <input type="text" id="apellidos" name="apellidos" required 
                               value="<?= e($_POST['apellidos'] ?? '') ?>">
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Email *</label>
                        <input type="email" id="email" name="email" required 
                               value="<?= e($_POST['email'] ?? '') ?>">
                    </div>
                    
                    <div class="form-group">
                        <label for="dni">DNI/NIE *</label>
                        <input type="text" id="dni" name="dni" required 
                               value="<?= e($_POST['dni'] ?? '') ?>"
                               placeholder="12345678A">
                    </div>
                    
                    <div class="form-group">
                        <label for="fecha_nacimiento">Fecha de Nacimiento</label>
                        <input type="date" id="fecha_nacimiento" name="fecha_nacimiento" 
                               value="<?= e($_POST['fecha_nacimiento'] ?? '') ?>">
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Contraseña * (mínimo 6 caracteres)</label>
                        <input type="password" id="password" name="password" required minlength="6">
                    </div>
                    
                    <div class="form-group">
                        <label for="confirm_password">Confirmar Contraseña *</label>
                        <input type="password" id="confirm_password" name="confirm_password" required minlength="6">
                    </div>
                    
                    <button type="submit" class="btn-primary">Registrarse</button>
                </form>
                
                <div class="form-footer">
                    ¿Ya tienes cuenta? <a href="auth.php">Inicia sesión aquí</a>
                </div>
            <?php endif; ?>
        </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 HotelHub - Sector Turístico. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>
