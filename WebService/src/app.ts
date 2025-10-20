import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';

// Carga las variables de entorno del archivo .env
dotenv.config();

const app: Express = express();
const port = process.env.PORT || 3000;

app.get('/', (req: Request, res: Response) => {
  res.send('¡El servidor del PMS con TypeScript está funcionando!');
});

app.listen(port, () => {
  console.log(`⚡️ [server]: Servidor corriendo en http://localhost:${port}`);
});