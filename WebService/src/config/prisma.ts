import { PrismaClient } from '@prisma/client';

// Creamos una instancia única de PrismaClient para toda la aplicación
// Esto es importante para evitar múltiples conexiones a la base de datos
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'], // Opcional: logs para desarrollo
});

// Ejecutar comando SET NAMES al iniciar la conexión
prisma.$connect().then(async () => {
  await prisma.$executeRawUnsafe('SET NAMES utf8mb4');
  await prisma.$executeRawUnsafe('SET CHARACTER SET utf8mb4');
  await prisma.$executeRawUnsafe('SET character_set_connection=utf8mb4');
  console.log('✅ [prisma]: Conexión establecida con charset UTF-8');
});

export default prisma;
