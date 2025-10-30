import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// Esta ruta responderá a GET http://localhost:3000/api/hoteles
router.get('/', asyncHandler(async (req, res) => {
  // Usamos Prisma para obtener todos los hoteles con su relación de ciudad
  const hoteles = await prisma.hotel.findMany({
    include: {
      ciudad: true, // Incluye información de la ciudad relacionada
    },
  });

  // Enviamos la respuesta como un JSON con código 200 (OK)
  res.status(200).json(hoteles);
}));

// Obtener un hotel específico por ID
router.get('/:id', asyncHandler(async (req, res) => {
  const { id } = req.params;
  
  const hotel = await prisma.hotel.findUnique({
    where: {
      idHotel: parseInt(id),
    },
    include: {
      ciudad: true,
      habitaciones: {
        include: {
          tipoHabitacion: true,
        },
      },
      preciosRegimen: {
        include: {
          regimen: true,
        },
      },
    },
  });

  if (!hotel) {
    throw new NotFoundError('Hotel');
  }

  res.status(200).json(hotel);
}));

// Crear un nuevo hotel
router.post('/', asyncHandler(async (req, res) => {
  const { nombre, ubicacion, categoria, idCiudad } = req.body;

  const nuevoHotel = await prisma.hotel.create({
    data: {
      nombre,
      ubicacion,
      categoria,
      idCiudad,
    },
    include: {
      ciudad: true,
    },
  });

  res.status(201).json(nuevoHotel);
}));

// Actualizar un hotel
router.put('/:id', asyncHandler(async (req, res) => {
  const { id } = req.params;
  const { nombre, ubicacion, categoria, idCiudad } = req.body;

  const hotelActualizado = await prisma.hotel.update({
    where: {
      idHotel: parseInt(id),
    },
    data: {
      nombre,
      ubicacion,
      categoria,
      idCiudad,
    },
    include: {
      ciudad: true,
    },
  });

  res.status(200).json(hotelActualizado);
}));

// Eliminar un hotel
router.delete('/:id', asyncHandler(async (req, res) => {
  const { id } = req.params;

  await prisma.hotel.delete({
    where: {
      idHotel: parseInt(id),
    },
  });

  res.status(200).json({ message: 'Hotel eliminado correctamente' });
}));

// GET /hoteles/{idHotel}/tiposHabitacion - Obtener tipos de habitación de un hotel
router.get('/:id/tiposHabitacion', asyncHandler(async (req, res) => {
  const { id } = req.params;

  // Verificar que el hotel existe
  const hotel = await prisma.hotel.findUnique({
    where: {
      idHotel: parseInt(id),
    },
  });

  if (!hotel) {
    throw new NotFoundError('Hotel');
  }

  // Obtener los tipos de habitación del hotel
  const tiposHabitacion = await prisma.tipoHabitacion.findMany({
    where: {
      habitaciones: {
        some: {
          idHotel: parseInt(id),
        },
      },
    },
    include: {
      habitaciones: {
        where: {
          idHotel: parseInt(id),
        },
      },
    },
  });

  // Agregar conteo de habitaciones por tipo
  const tiposConConteo = tiposHabitacion.map((tipo: any) => ({
    ...tipo,
    cantidadHabitaciones: tipo.habitaciones.length,
  }));

  res.status(200).json(tiposConConteo);
}));

export default router;