import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import hotelRoutes from './api/hotel.routes'; // <-- Keep this import

dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

// Middleware for JSON
app.use(express.json());

// Use the hotel routes
app.use('/api/hoteles', hotelRoutes);

// Default route
app.get('/', (req: Request, res: Response) => {
  res.send('¡El servidor del PMS con TypeScript está funcionando!');
});

app.listen(port, () => {
  console.log(`⚡️ [server]: Servidor corriendo en http://localhost:${port}`);
});