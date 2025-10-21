import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// GET /servicios - Obtener todos los servicios disponibles
router.get('/', async (req, res) => {
  try {
    const servicios = await prisma.servicio.findMany({
      orderBy: {
        codigoServicio: 'asc',
      },
    });

    res.status(200).json(servicios);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener los servicios' });
  }
});

// GET /servicios/:codigo - Obtener un servicio específico
router.get('/:codigo', async (req, res) => {
  try {
    const { codigo } = req.params;

    const servicio = await prisma.servicio.findUnique({
      where: {
        codigoServicio: codigo,
      },
    });

    if (!servicio) {
      return res.status(404).json({
        message: 'Servicio no encontrado',
      });
    }

    res.status(200).json(servicio);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener el servicio' });
  }
});

export default router;
