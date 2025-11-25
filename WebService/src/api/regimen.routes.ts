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

// GET /regimenes/hotel/:idHotel - Obtener regímenes disponibles en un hotel con sus precios
router.get('/hotel/:idHotel', asyncHandler(async (req, res) => {
  const idHotel = parseInt(req.params.idHotel);

  if (isNaN(idHotel)) {
    res.status(400).json({ error: 'El ID del hotel debe ser un número válido' });
    return;
  }

  // Verificar que el hotel existe
  const hotel = await prisma.hotel.findUnique({
    where: { idHotel },
    include: { ciudad: true },
  });

  if (!hotel) {
    throw new NotFoundError(`Hotel con ID ${idHotel}`);
  }

  // Obtener los precios de régimen del hotel
  const preciosRegimen = await prisma.precioRegimen.findMany({
    where: {
      idHotel: idHotel,
    },
    include: {
      regimen: true,
    },
  });

  // Formatear respuesta
  const regimenesConPrecios = preciosRegimen.map((pr) => ({
    idPrecioRegimen: pr.idPrecioRegimen,
    regimen: {
      idRegimen: pr.regimen.idRegimen,
      codigo: pr.regimen.codigo,
    },
    precio: parseFloat(pr.precio.toString()),
  }));

  res.status(200).json({
    hotel: {
      idHotel: hotel.idHotel,
      nombre: hotel.nombre,
      ubicacion: hotel.ubicacion,
      ciudad: hotel.ciudad.nombre,
    },
    regimenes: regimenesConPrecios,
  });
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
