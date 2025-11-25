import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import hotelRoutes from './api/hotel.routes';
import ciudadRoutes from './api/ciudad.routes';
import clienteRoutes from './api/cliente.routes';
import reservaRoutes from './api/reserva.routes';
import disponibilidadRoutes from './api/disponibilidad.routes';
import contratoRoutes from './api/contrato.routes';
import pernoctacionRoutes from './api/pernoctacion.routes';
import servicioRoutes from './api/servicio.routes';
import regimenRoutes from './api/regimen.routes';
import tipoHabitacionRoutes from './api/tipoHabitacion.routes';
import habitacionRoutes from './api/habitacion.routes';
import { errorHandler, notFoundHandler } from './middleware/errorHandler';

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

// Middleware para establecer charset UTF-8 en todas las respuestas
app.use((req, res, next) => {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  next();
});

// Middleware for JSON con UTF-8
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Use the routes
app.use('/api/hoteles', hotelRoutes);
app.use('/api/ciudades', ciudadRoutes);
app.use('/api/clientes', clienteRoutes);
app.use('/api/reservas', reservaRoutes);
app.use('/api/disponibilidad', disponibilidadRoutes);
app.use('/api/contratos', contratoRoutes);
app.use('/api/pernoctaciones', pernoctacionRoutes);
app.use('/api/servicios', servicioRoutes);
app.use('/api/regimenes', regimenRoutes);
app.use('/api/tipos-habitacion', tipoHabitacionRoutes);
app.use('/api/habitaciones', habitacionRoutes);

// Default route
app.get('/', (req: Request, res: Response) => {
  res.send('Servidor de Sector Turístico funcionando con Prisma ORM');
});

// Health check route
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'OK',
    message: 'API funcionando correctamente',
    endpoints: {
      catalogs: {
        hoteles: '/api/hoteles',
        ciudades: '/api/ciudades',
        tiposHabitacion: '/api/tipos-habitacion',
        regimenes: '/api/regimenes',
        servicios: '/api/servicios',
      },
      operations: {
        disponibilidad: '/api/disponibilidad?fechaEntrada=YYYY-MM-DD&fechaSalida=YYYY-MM-DD&hotel=NombreHotel',
        crearReserva: 'POST /api/reservas',
        verReservas: 'GET /api/reservas',
        verContratos: 'GET /api/contratos',
        checkin: 'POST /api/reservas/:idReserva/checkin',
        checkout: 'POST /api/contratos/:idContrato/checkout',
        anadirServicio: 'POST /api/pernoctaciones/:idPernoctacion/servicios',
      },
    },
  });
});

// Middleware para rutas no encontradas (debe ir después de todas las rutas)
app.use(notFoundHandler);

// Middleware de manejo de errores (debe ir al final)
app.use(errorHandler);

app.listen(port, () => {
  // Server started - console logs disabled for backend
});

