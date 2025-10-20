import { Router } from 'express';
import prisma from '../config/prisma'; // Importamos Prisma Client

const router = Router();

// Esta ruta responderá a GET http://localhost:3000/api/hoteles
router.get('/', async (req, res) => {
  try {
    // Usamos Prisma para obtener todos los hoteles con su relación de ciudad
    const hoteles = await prisma.hotel.findMany({
      include: {
        ciudad: true, // Incluye información de la ciudad relacionada
      },
    });

    // Enviamos la respuesta como un JSON con código 200 (OK)
    res.status(200).json(hoteles);
  } catch (error) {
    // Si hay un error, lo mostramos en la consola y enviamos un error 500
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener los hoteles' });
  }
});

// Obtener un hotel específico por ID
router.get('/:id', async (req, res) => {
  try {
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
      return res.status(404).json({ message: 'Hotel no encontrado' });
    }

    res.status(200).json(hotel);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener el hotel' });
  }
});

// Crear un nuevo hotel
router.post('/', async (req, res) => {
  try {
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
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al crear el hotel' });
  }
});

// Actualizar un hotel
router.put('/:id', async (req, res) => {
  try {
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
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al actualizar el hotel' });
  }
});

// Eliminar un hotel
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    await prisma.hotel.delete({
      where: {
        idHotel: parseInt(id),
      },
    });

    res.status(200).json({ message: 'Hotel eliminado correctamente' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al eliminar el hotel' });
  }
});

export default router;