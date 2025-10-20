import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import hotelRoutes from './api/hotel.routes';
import ciudadRoutes from './api/ciudad.routes';
import clienteRoutes from './api/cliente.routes';
import reservaRoutes from './api/reserva.routes';

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

// Middleware for JSON
app.use(express.json());

// Use the routes
app.use('/api/hoteles', hotelRoutes);
app.use('/api/ciudades', ciudadRoutes);
app.use('/api/clientes', clienteRoutes);
app.use('/api/reservas', reservaRoutes);

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
      hoteles: '/api/hoteles',
      ciudades: '/api/ciudades',
      clientes: '/api/clientes',
      reservas: '/api/reservas',
    },
  });
});

app.listen(port, () => {
  console.log(`⚡️ [server]: Servidor corriendo en http://localhost:${port}`);
  console.log(`📊 [prisma]: Usando Prisma ORM con MySQL`);
});
