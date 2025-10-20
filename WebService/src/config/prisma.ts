import { PrismaClient } from '@prisma/client';

// Creamos una instancia única de PrismaClient para toda la aplicación
// Esto es importante para evitar múltiples conexiones a la base de datos
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'], // Opcional: logs para desarrollo
});

export default prisma;
