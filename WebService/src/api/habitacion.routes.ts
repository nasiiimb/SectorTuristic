import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// GET /habitaciones?hotel={idHotel} - Obtener habitaciones, opcionalmente filtradas por hotel
router.get('/', asyncHandler(async (req, res) => {
  const { hotel } = req.query;

  const whereClause: any = {};
  
  if (hotel) {
    whereClause.idHotel = parseInt(hotel as string);
  }

  const habitaciones = await prisma.habitacion.findMany({
    where: whereClause,
    include: {
      hotel: {
        select: {
          idHotel: true,
          nombre: true,
        },
      },
      tipoHabitacion: {
        select: {
          idTipoHabitacion: true,
          categoria: true,
        },
      },
    },
    orderBy: {
      numeroHabitacion: 'asc',
    },
  });

  res.status(200).json({ habitaciones });
}));

// GET /habitaciones/:numeroHabitacion - Obtener una habitación específica
router.get('/:numeroHabitacion', asyncHandler(async (req, res) => {
  const { numeroHabitacion } = req.params;

  const habitacion = await prisma.habitacion.findUnique({
    where: {
      numeroHabitacion,
    },
    include: {
      hotel: true,
      tipoHabitacion: true,
      contratos: {
        include: {
          reserva: {
            include: {
              clientePaga: true,
            },
          },
        },
      },
    },
  });

  if (!habitacion) {
    throw new NotFoundError('Habitación');
  }

  res.status(200).json(habitacion);
}));

// GET /habitaciones/disponibles?hotel={idHotel}&tipoHabitacion={categoria} - Obtener habitaciones disponibles
router.get('/disponibles/list', asyncHandler(async (req, res) => {
  const { hotel, tipoHabitacion } = req.query;

  if (!hotel) {
    return res.status(400).json({ 
      error: 'Parámetro requerido', 
      message: 'Se requiere el parámetro hotel' 
    });
  }

  const whereClause: any = {
    idHotel: parseInt(hotel as string),
  };

  if (tipoHabitacion) {
    whereClause.tipoHabitacion = {
      categoria: tipoHabitacion as string,
    };
  }

  // Obtener todas las habitaciones del hotel
  const habitaciones = await prisma.habitacion.findMany({
    where: whereClause,
    include: {
      tipoHabitacion: true,
      contratos: {
        where: {
          fechaCheckOut: null, // Solo contratos activos
        },
        select: {
          idContrato: true,
          numeroHabitacion: true,
        },
      },
    },
  });

  // Filtrar habitaciones que no tienen contratos activos
  const habitacionesDisponibles = habitaciones.filter(
    (hab: any) => hab.contratos.length === 0
  );

  res.status(200).json({ habitaciones: habitacionesDisponibles });
}));

// POST /habitaciones - Crear una nueva habitación
router.post('/', asyncHandler(async (req, res) => {
  const { numeroHabitacion, idHotel, idTipoHabitacion } = req.body;

  // Verificar que el hotel existe
  const hotel = await prisma.hotel.findUnique({
    where: { idHotel },
  });

  if (!hotel) {
    throw new NotFoundError('Hotel');
  }

  // Verificar que el tipo de habitación existe
  const tipoHabitacion = await prisma.tipoHabitacion.findUnique({
    where: { idTipoHabitacion },
  });

  if (!tipoHabitacion) {
    throw new NotFoundError('Tipo de habitación');
  }

  const nuevaHabitacion = await prisma.habitacion.create({
    data: {
      numeroHabitacion,
      idHotel,
      idTipoHabitacion,
    },
    include: {
      hotel: true,
      tipoHabitacion: true,
    },
  });

  res.status(201).json(nuevaHabitacion);
}));

export default router;
