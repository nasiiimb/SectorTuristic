<?php
require_once 'config.php';
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HotelHub - Encuentra tu Hotel Perfecto</title>
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

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1>Descubre tu próxima escapada</h1>
            <p>Miles de hoteles al mejor precio. Reserva ahora y paga en el hotel.</p>
        </div>
    </section>

    <!-- Buscador -->
    <div class="container">
        <div class="search-bar">
            <form action="resultados.php" method="GET" class="search-form">
                <div class="search-group">
                    <label for="ciudad">Destino</label>
                    <input type="text" id="ciudad" name="ciudad" placeholder="¿A dónde viajas?" required>
                </div>
                
                <div class="search-group">
                    <label for="fechaEntrada">Entrada</label>
                    <input type="date" id="fechaEntrada" name="fechaEntrada" required>
                </div>
                
                <div class="search-group">
                    <label for="fechaSalida">Salida</label>
                    <input type="date" id="fechaSalida" name="fechaSalida" required>
                </div>
                
                <button type="submit" class="btn-search">Buscar</button>
            </form>
        </div>
    </div>

    <!-- Contenido adicional -->
    <div class="container">
        <h2 class="page-title">Destinos Populares</h2>
        <div class="rooms-grid">
            <div class="room-card">
                <img src="https://images.unsplash.com/photo-1540541338287-41700207dee6?w=600" alt="Palma de Mallorca" class="room-image">
                <div class="room-content">
                    <h3 class="room-title">Palma de Mallorca</h3>
                    <p class="room-description">Playas paradisíacas, cultura mediterránea y gastronomía única.</p>
                </div>
            </div>
            
            <div class="room-card">
                <img src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600" alt="Barcelona" class="room-image">
                <div class="room-content">
                    <h3 class="room-title">Barcelona</h3>
                    <p class="room-description">Arte, arquitectura modernista y vida mediterránea vibrante.</p>
                </div>
            </div>
            
            <div class="room-card">
                <img src="https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=600" alt="Madrid" class="room-image">
                <div class="room-content">
                    <h3 class="room-title">Madrid</h3>
                    <p class="room-description">Capital con museos de clase mundial y vida nocturna animada.</p>
                </div>
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
        // Establecer fechas mínimas
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('fechaEntrada').min = today;
        document.getElementById('fechaSalida').min = today;
        
        // Validar que la fecha de salida sea posterior a la de entrada
        document.getElementById('fechaEntrada').addEventListener('change', function() {
            const fechaEntrada = this.value;
            document.getElementById('fechaSalida').min = fechaEntrada;
            
            // Si la fecha de salida es anterior, resetearla
            const fechaSalida = document.getElementById('fechaSalida').value;
            if (fechaSalida && fechaSalida <= fechaEntrada) {
                document.getElementById('fechaSalida').value = '';
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
