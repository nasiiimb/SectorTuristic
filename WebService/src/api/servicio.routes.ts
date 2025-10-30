import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// GET /servicios - Obtener todos los servicios disponibles
router.get('/', asyncHandler(async (req, res) => {
  const servicios = await prisma.servicio.findMany({
    orderBy: {
      codigoServicio: 'asc',
    },
  });

  res.status(200).json(servicios);
}));

// GET /servicios/:codigo - Obtener un servicio específico
router.get('/:codigo', asyncHandler(async (req, res) => {
  const { codigo } = req.params;

  const servicio = await prisma.servicio.findUnique({
    where: {
      codigoServicio: codigo,
    },
  });

  if (!servicio) {
    throw new NotFoundError('Servicio');
  }

  res.status(200).json(servicio);
}));

export default router;
