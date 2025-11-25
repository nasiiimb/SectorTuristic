import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// GET /tipos-habitacion/hotel/:idHotel - Obtener tipos de habitación de un hotel específico
router.get('/hotel/:idHotel', asyncHandler(async (req, res) => {
  const idHotel = parseInt(req.params.idHotel);

  if (isNaN(idHotel)) {
    return res.status(400).json({
      message: 'El ID del hotel debe ser un número válido',
    });
  }

  // Verificar que el hotel existe
  const hotelExiste = await prisma.hotel.findUnique({
    where: { idHotel },
  });

  if (!hotelExiste) {
    return res.status(404).json({
      message: `No se encontró el hotel con ID ${idHotel}`,
    });
  }

  // Obtener habitaciones del hotel con sus tipos
  const habitaciones = await prisma.habitacion.findMany({
    where: {
      idHotel: idHotel,
    },
    include: {
      tipoHabitacion: true,
    },
  });

  // Extraer tipos únicos usando un Map
  const tiposMap = new Map();
  habitaciones.forEach((hab) => {
    const idTipo = hab.tipoHabitacion.idTipoHabitacion;
    if (!tiposMap.has(idTipo)) {
      tiposMap.set(idTipo, {
        idTipoHabitacion: hab.tipoHabitacion.idTipoHabitacion,
        nombreTipo: hab.tipoHabitacion.categoria,
        camasIndividuales: hab.tipoHabitacion.camasIndividuales,
        camasDobles: hab.tipoHabitacion.camasDobles,
      });
    }
  });

  const tiposHabitacion = Array.from(tiposMap.values());

  res.status(200).json({
    hotel: hotelExiste.nombre,
    tiposHabitacion,
  });
}));

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
