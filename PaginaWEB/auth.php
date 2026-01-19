<?php
require_once 'config.php';

$error = null;
$success = null;

// Procesar login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if (empty($email) || empty($password)) {
        $error = 'Por favor completa todos los campos';
    } else {
        // Llamar al endpoint de login
        $response = apiRequest('/clientes/login', 'POST', [
            'correoElectronico' => $email,
            'password' => $password
        ]);
        
        if ($response['success'] && isset($response['data'])) {
            $cliente = $response['data'];
            
            // Login exitoso
            $_SESSION['user'] = [
                'idCliente' => $cliente['idCliente'],
                'nombre' => $cliente['nombre'],
                'apellidos' => $cliente['apellidos'],
                'email' => $cliente['correoElectronico']
            ];
            
            // Redirigir a la página anterior o al inicio
            $redirect = $_GET['redirect'] ?? 'index.php';
            header('Location: ' . $redirect);
            exit;
        } else {
            $error = $response['error'] ?? 'Email o contraseña incorrectos';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión - HotelHub</title>
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
                <li><a href="registro.php">Registrarse</a></li>
            </ul>
        </div>
    </nav>

    <div class="auth-container">
        <div class="auth-box">
            <h2>Iniciar Sesión</h2>
            
            <?php if ($error): ?>
                <div class="alert alert-error">
                    <?= e($error) ?>
                </div>
            <?php endif; ?>
            
            <?php if ($success): ?>
                <div class="alert alert-success">
                    <?= e($success) ?>
                </div>
            <?php endif; ?>
            
            <form method="POST">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required 
                           value="<?= e($_POST['email'] ?? '') ?>">
                </div>
                
                <div class="form-group">
                    <label for="password">Contraseña</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn-primary">Iniciar Sesión</button>
            </form>
            
            <div class="form-footer">
                ¿No tienes cuenta? <a href="registro.php">Regístrate aquí</a>
            </div>
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
