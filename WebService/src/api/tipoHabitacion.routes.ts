import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// GET /tipos-habitacion - Obtener todos los tipos de habitación
router.get('/', asyncHandler(async (req, res) => {
  const tiposHabitacion = await prisma.tipoHabitacion.findMany({
    include: {
      habitaciones: {
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

  // Formatear respuesta
  const tiposFormateados = tiposHabitacion.map((tipo) => {
    // Agrupar hoteles únicos
    const hotelesUnicos = new Map();
    tipo.habitaciones.forEach((hab) => {
      const hotelId = hab.hotel.idHotel;
      if (!hotelesUnicos.has(hotelId)) {
        hotelesUnicos.set(hotelId, {
          hotel: hab.hotel.nombre,
          ciudad: hab.hotel.ciudad.nombre,
          cantidad: 1,
        });
      } else {
        const hotel = hotelesUnicos.get(hotelId);
        hotel.cantidad++;
      }
    });

    return {
      categoria: tipo.categoria,
      camasIndividuales: tipo.camasIndividuales,
      camasDobles: tipo.camasDobles,
      disponibleEn: Array.from(hotelesUnicos.values()),
    };
  });

  res.status(200).json(tiposFormateados);
}));

// GET /tipos-habitacion/:categoria - Obtener un tipo específico
router.get('/:categoria', asyncHandler(async (req, res) => {
  const { categoria } = req.params;

  const tipo = await prisma.tipoHabitacion.findFirst({
    where: {
      categoria: {
        contains: categoria,
      },
    },
    include: {
      habitaciones: {
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

  if (!tipo) {
    throw new NotFoundError(`Tipo de habitación "${categoria}"`);
  }

  // Agrupar hoteles únicos
  const hotelesUnicos = new Map();
  tipo.habitaciones.forEach((hab) => {
    const hotelId = hab.hotel.idHotel;
    if (!hotelesUnicos.has(hotelId)) {
      hotelesUnicos.set(hotelId, {
        hotel: hab.hotel.nombre,
        ciudad: hab.hotel.ciudad.nombre,
        cantidad: 1,
      });
    } else {
      const hotel = hotelesUnicos.get(hotelId);
      hotel.cantidad++;
    }
  });

  const tipoFormateado = {
    categoria: tipo.categoria,
    camasIndividuales: tipo.camasIndividuales,
    camasDobles: tipo.camasDobles,
    disponibleEn: Array.from(hotelesUnicos.values()),
  };

  res.status(200).json(tipoFormateado);
}));

export default router;
