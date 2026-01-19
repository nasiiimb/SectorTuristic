import express, { Application, Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth';
import bookingRoutes from './routes/booking';

// Cargar variables de entorno
dotenv.config();

const app: Application = express();
const PORT = process.env.PORT || 8010;
const CORS_ORIGIN = process.env.CORS_ORIGIN || 'http://localhost:5174';

// ============================================
// Middlewares
// ============================================

// CORS
app.use(cors({
  origin: CORS_ORIGIN,
  credentials: true
}));

// Parser de JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logger simple
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// ============================================
// Rutas
// ============================================

// Ruta raíz
app.get('/', (req: Request, res: Response) => {
  res.json({
    service: 'Principal - Booking Engine',
    version: '1.0.0',
    status: 'online',
    endpoints: {
      auth: {
        register: 'POST /api/auth/register',
        login: 'POST /api/auth/login',
        profile: 'GET /api/auth/profile'
      },
      booking: {
        search: 'GET /api/search',
        book: 'POST /api/book',
        myReservations: 'GET /api/my-reservations',
        reservationDetail: 'GET /api/reservations/:localizador'
      }
    }
  });
});

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api', bookingRoutes);

// ============================================
// Manejo de errores 404
// ============================================

app.use((req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    message: 'Endpoint no encontrado'
  });
});

// ============================================
// Iniciar servidor
// ============================================

app.listen(PORT, () => {
  console.log('');
  console.log('═══════════════════════════════════════════════════════');
  console.log('Principal Booking Engine');
  console.log('═══════════════════════════════════════════════════════');
  console.log(`Servidor corriendo en: http://localhost:${PORT}`);
  console.log(`CORS habilitado para: ${CORS_ORIGIN}`);
  console.log(`WebService URL: ${process.env.WEBSERVICE_URL || 'http://localhost:3000'}`);
  console.log(`Channel URL: ${process.env.CHANNEL_URL || 'http://localhost:8001'}`);
  console.log('═══════════════════════════════════════════════════════');
  console.log('');
  console.log('Endpoints disponibles:');
  console.log('   POST   /api/auth/register');
  console.log('   POST   /api/auth/login');
  console.log('   GET    /api/auth/profile (auth)');
  console.log('   GET    /api/search');
  console.log('   POST   /api/book (auth)');
  console.log('   GET    /api/my-reservations (auth)');
  console.log('');
});

export default app;
