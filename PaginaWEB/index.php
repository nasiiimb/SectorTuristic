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
            <form action="resultados.php" method="GET" class="search-form" id="searchForm">
                <div class="search-group">
                    <label for="pais">País</label>
                    <select id="pais" name="pais" required>
                        <option value="">Selecciona un país</option>
                    </select>
                </div>
                
                <div class="search-group">
                    <label for="ciudad">Ciudad</label>
                    <select id="ciudad" name="ciudad" required disabled>
                        <option value="">Primero selecciona un país</option>
                    </select>
                </div>
                
                <div class="search-group">
                    <label for="hotel">Hotel (Opcional)</label>
                    <select id="hotel" name="hotel" disabled>
                        <option value="">Todos los hoteles</option>
                    </select>
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

    <script>
    // Cargar países al iniciar
    document.addEventListener('DOMContentLoaded', function() {
        cargarPaises();
        
        // Establecer fechas mínimas
        const hoy = new Date().toISOString().split('T')[0];
        document.getElementById('fechaEntrada').min = hoy;
        document.getElementById('fechaSalida').min = hoy;
        
        // Validar que fecha salida > fecha entrada
        document.getElementById('fechaEntrada').addEventListener('change', function() {
            document.getElementById('fechaSalida').min = this.value;
        });
    });

    function cargarPaises() {
        console.log('🔄 Intentando cargar países...');
        fetch('api.php?action=paises')
            .then(res => {
                console.log('📡 Respuesta recibida, status:', res.status);
                return res.json();
            })
            .then(data => {
                console.log('✅ Países recibidos:', data);
                if (data.success) {
                    const select = document.getElementById('pais');
                    console.log('📝 Añadiendo', data.data.length, 'países al select');
                    data.data.forEach(pais => {
                        const option = document.createElement('option');
                        option.value = pais;
                        option.textContent = pais;
                        select.appendChild(option);
                    });
                    console.log('✨ Países cargados correctamente');
                } else {
                    console.error('❌ Error en respuesta:', data);
                }
            })
            .catch(err => {
                console.error('💥 Error cargando países:', err);
                alert('Error al cargar países. Verifica que el servidor PHP esté corriendo.');
            });
    }

    document.getElementById('pais').addEventListener('change', function() {
        const pais = this.value;
        const ciudadSelect = document.getElementById('ciudad');
        const hotelSelect = document.getElementById('hotel');
        
        // Reset
        ciudadSelect.innerHTML = '<option value="">Cargando ciudades...</option>';
        ciudadSelect.disabled = true;
        hotelSelect.innerHTML = '<option value="">Todos los hoteles</option>';
        hotelSelect.disabled = true;
        
        if (!pais) {
            ciudadSelect.innerHTML = '<option value="">Primero selecciona un país</option>';
            return;
        }
        
        console.log('🌍 Cargando ciudades del país:', pais);
        fetch(`api.php?action=ciudades&pais=${encodeURIComponent(pais)}`)
            .then(res => res.json())
            .then(data => {
                console.log('🏙️ Ciudades recibidas:', data);
                if (data.success) {
                    ciudadSelect.innerHTML = '<option value="">Selecciona una ciudad</option>';
                    data.data.forEach(ciudad => {
                        const option = document.createElement('option');
                        option.value = ciudad.nombre;
                        option.textContent = ciudad.nombre;
                        ciudadSelect.appendChild(option);
                    });
                    ciudadSelect.disabled = false;
                    console.log('✨ Ciudades cargadas:', data.data.length);
                }
            })
            .catch(err => console.error('💥 Error cargando ciudades:', err));
    });

    document.getElementById('ciudad').addEventListener('change', function() {
        const ciudad = this.value;
        const hotelSelect = document.getElementById('hotel');
        
        hotelSelect.innerHTML = '<option value="">Cargando hoteles...</option>';
        hotelSelect.disabled = true;
        
        if (!ciudad) {
            hotelSelect.innerHTML = '<option value="">Todos los hoteles</option>';
            return;
        }
        
        console.log('🏨 Cargando hoteles de la ciudad:', ciudad);
        fetch(`api.php?action=hoteles&ciudad=${encodeURIComponent(ciudad)}`)
            .then(res => res.json())
            .then(data => {
                console.log('🏨 Hoteles recibidos:', data);
                if (data.success) {
                    hotelSelect.innerHTML = '<option value="">Todos los hoteles</option>';
                    data.data.forEach(hotel => {
                        const option = document.createElement('option');
                        option.value = hotel.idHotel;
                        option.textContent = `${hotel.nombre} (${'★'.repeat(hotel.categoria)})`;
                        hotelSelect.appendChild(option);
                    });
                    hotelSelect.disabled = false;
                    console.log('✨ Hoteles cargados:', data.data.length);
                }
            })
            .catch(err => console.error('💥 Error cargando hoteles:', err));
    });
    </script>

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
