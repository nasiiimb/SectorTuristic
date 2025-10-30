import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// GET /regimenes - Obtener todos los regímenes disponibles
router.get('/', asyncHandler(async (req, res) => {
  const regimenes = await prisma.regimen.findMany({
    include: {
      preciosRegimen: {
        include: {
          hotel: {
            include: {
              ciudad: true,
            },
          },
        },
      },
    },
  });

  // Formatear respuesta para que sea más legible
  const regimenesFormateados = regimenes.map((regimen) => ({
    codigo: regimen.codigo,
    idRegimen: regimen.idRegimen,
    disponibleEn: regimen.preciosRegimen.map((pr) => ({
      hotel: pr.hotel.nombre,
      ciudad: pr.hotel.ciudad.nombre,
      precio: parseFloat(pr.precio.toString()),
    })),
  }));

  res.status(200).json(regimenesFormateados);
}));

// GET /regimenes/:codigo - Obtener un régimen específico
router.get('/:codigo', asyncHandler(async (req, res) => {
  const { codigo } = req.params;

  const regimen = await prisma.regimen.findFirst({
    where: {
      codigo: codigo,
    },
    include: {
      preciosRegimen: {
        include: {
          hotel: {
            include: {
              ciudad: true,
            },
          },
        },
      },
    },
  });

  if (!regimen) {
    throw new NotFoundError(`Régimen con código "${codigo}"`);
  }

  const regimenFormateado = {
    codigo: regimen.codigo,
    idRegimen: regimen.idRegimen,
    disponibleEn: regimen.preciosRegimen.map((pr) => ({
      hotel: pr.hotel.nombre,
      ciudad: pr.hotel.ciudad.nombre,
      precio: parseFloat(pr.precio.toString()),
    })),
  };

  res.status(200).json(regimenFormateado);
}));

export default router;
