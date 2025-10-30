import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// Obtener todas las ciudades
router.get('/', asyncHandler(async (req, res) => {
  const ciudades = await prisma.ciudad.findMany({
    include: {
      hoteles: true, // Incluye los hoteles de cada ciudad
    },
  });

  res.status(200).json(ciudades);
}));

// Obtener una ciudad por ID
router.get('/:id', asyncHandler(async (req, res) => {
  const { id } = req.params;

  const ciudad = await prisma.ciudad.findUnique({
    where: {
      idCiudad: parseInt(id),
    },
    include: {
      hoteles: true,
    },
  });

  if (!ciudad) {
    throw new NotFoundError('Ciudad');
  }

  res.status(200).json(ciudad);
}));

// Crear una nueva ciudad
router.post('/', asyncHandler(async (req, res) => {
  const { nombre, pais } = req.body;

  const nuevaCiudad = await prisma.ciudad.create({
    data: {
      nombre,
      pais,
    },
  });

  res.status(201).json(nuevaCiudad);
}));

export default router;
