import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// Obtener todas las ciudades
router.get('/', async (req, res) => {
  try {
    const ciudades = await prisma.ciudad.findMany({
      include: {
        hoteles: true, // Incluye los hoteles de cada ciudad
      },
    });

    res.status(200).json(ciudades);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener las ciudades' });
  }
});

// Obtener una ciudad por ID
router.get('/:id', async (req, res) => {
  try {
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
      return res.status(404).json({ message: 'Ciudad no encontrada' });
    }

    res.status(200).json(ciudad);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener la ciudad' });
  }
});

// Crear una nueva ciudad
router.post('/', async (req, res) => {
  try {
    const { nombre, pais } = req.body;

    const nuevaCiudad = await prisma.ciudad.create({
      data: {
        nombre,
        pais,
      },
    });

    res.status(201).json(nuevaCiudad);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al crear la ciudad' });
  }
});

export default router;
