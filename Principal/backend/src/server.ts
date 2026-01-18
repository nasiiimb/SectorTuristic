import express, { Request, Response, NextFunction } from 'express';import express, { Application, Request, Response } from 'express';

import cors from 'cors';import cors from 'cors';

import dotenv from 'dotenv';import dotenv from 'dotenv';

import authRoutes from './routes/auth';import authRoutes from './routes/auth';

import bookingRoutes from './routes/booking';import bookingRoutes from './routes/booking';



// Cargar variables de entorno// Cargar variables de entorno

dotenv.config();dotenv.config();



const app = express();const app: Application = express();

const PORT = process.env.PORT || 8010;const PORT = process.env.PORT || 8010;

const CORS_ORIGIN = process.env.CORS_ORIGIN || 'http://localhost:5174';const CORS_ORIGIN = process.env.CORS_ORIGIN || 'http://localhost:5174';



// ============================================// ============================================

// Middlewares// Middlewares

// ============================================// ============================================



// CORS// CORS

app.use(cors({app.use(cors({

  origin: CORS_ORIGIN,  origin: CORS_ORIGIN,

  credentials: true  credentials: true

}));}));



// Parser de JSON// Parser de JSON

app.use(express.json());app.use(express.json());

app.use(express.urlencoded({ extended: true }));app.use(express.urlencoded({ extended: true }));



// Logger simple// Logger simple

app.use((req: Request, res: Response, next: NextFunction) => {app.use((req, res, next) => {

  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);

  next();  next();

});});



// ============================================// ============================================

// Rutas// Rutas

// ============================================// ============================================



// Ruta raíz// Ruta raíz

app.get('/', (req: Request, res: Response) => {app.get('/', (req: Request, res: Response) => {

  res.json({  res.json({

    service: 'Principal - Booking Engine',    service: 'Principal - Booking Engine',

    version: '1.0.0',    version: '1.0.0',

    status: 'online',    status: 'online',

    endpoints: {    endpoints: {

      auth: {      auth: {

        register: 'POST /api/auth/register',        register: 'POST /api/auth/register',

        login: 'POST /api/auth/login',        login: 'POST /api/auth/login',

        profile: 'GET /api/auth/profile'        profile: 'GET /api/auth/profile'

      },      },

      booking: {      booking: {

        search: 'GET /api/search',        search: 'GET /api/search',

        book: 'POST /api/book',        book: 'POST /api/book',

        myReservations: 'GET /api/my-reservations',        myReservations: 'GET /api/my-reservations',

        reservationDetail: 'GET /api/reservations/:localizador'        reservationDetail: 'GET /api/reservations/:localizador'

      }      }

    }    }

  });  });

});});



// Health check// Health check

app.get('/health', (req: Request, res: Response) => {app.get('/health', (req: Request, res: Response) => {

  res.json({  res.json({

    status: 'ok',    status: 'ok',

    timestamp: new Date().toISOString()    timestamp: new Date().toISOString()

  });  });

});});



// API Routes// API Routes

app.use('/api/auth', authRoutes);app.use('/api/auth', authRoutes);

app.use('/api', bookingRoutes);app.use('/api', bookingRoutes);



// ============================================// ============================================

// Manejo de errores 404// Manejo de errores 404

// ============================================// ============================================

app.use((req: Request, res: Response) => {

  res.status(404).json({app.use((req: Request, res: Response) => {

    success: false,  res.status(404).json({

    message: 'Endpoint no encontrado'    success: false,

  });    message: 'Endpoint no encontrado'

});  });

});

// ============================================

// Iniciar servidor// ============================================

// ============================================// Iniciar servidor

app.listen(PORT, () => {// ============================================

  console.log('');

  console.log('═══════════════════════════════════════════════════════');app.listen(PORT, () => {

  console.log('[PRINCIPAL] Booking Engine');  console.log('');

  console.log('═══════════════════════════════════════════════════════');  console.log('═══════════════════════════════════════════════════════');

  console.log(`[SERVER] Corriendo en: http://localhost:${PORT}`);  console.log('Principal Booking Engine');

  console.log(`[CORS] Habilitado para: ${CORS_ORIGIN}`);  console.log('═══════════════════════════════════════════════════════');

  console.log(`[WEBSERVICE] URL: ${process.env.WEBSERVICE_URL || 'http://localhost:3000'}`);  console.log(`Servidor corriendo en: http://localhost:${PORT}`);

  console.log(`[CHANNEL] URL: ${process.env.CHANNEL_URL || 'http://localhost:8001'}`);  console.log(`CORS habilitado para: ${CORS_ORIGIN}`);

  console.log('═══════════════════════════════════════════════════════');  console.log(`WebService URL: ${process.env.WEBSERVICE_URL || 'http://localhost:3000'}`);

  console.log('');  console.log(`Channel URL: ${process.env.CHANNEL_URL || 'http://localhost:8001'}`);

  console.log('[ENDPOINTS] Disponibles:');  console.log('═══════════════════════════════════════════════════════');

  console.log('   POST   /api/auth/register');  console.log('');

  console.log('   POST   /api/auth/login');  console.log('Endpoints disponibles:');

  console.log('   GET    /api/auth/profile (auth)');  console.log('   POST   /api/auth/register');

  console.log('   GET    /api/search');  console.log('   POST   /api/auth/login');

  console.log('   POST   /api/book (auth)');  console.log('   GET    /api/auth/profile (auth)');

  console.log('   GET    /api/my-reservations (auth)');  console.log('   GET    /api/search');

  console.log('');  console.log('   POST   /api/book (auth)');

});  console.log('   GET    /api/my-reservations (auth)');

  console.log('');

export default app;});


export default app;
