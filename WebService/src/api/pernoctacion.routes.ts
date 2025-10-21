import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// POST /pernoctaciones/{idPernoctacion}/servicios - Añade un servicio a una pernoctación
router.post('/:idPernoctacion/servicios', async (req, res) => {
  try {
    const { idPernoctacion } = req.params;
    const { codigoServicio } = req.body;

    // Validar parámetros
    if (!codigoServicio) {
      return res.status(400).json({
        message: 'El codigoServicio es requerido',
      });
    }

    // Verificar que la pernoctación existe
    const pernoctacion = await prisma.pernoctacion.findUnique({
      where: {
        idPernoctacion: parseInt(idPernoctacion),
      },
    });

    if (!pernoctacion) {
      return res.status(404).json({
        message: 'Pernoctación no encontrada',
      });
    }

    // Verificar que el servicio existe
    const servicio = await prisma.servicio.findUnique({
      where: {
        codigoServicio: codigoServicio,
      },
    });

    if (!servicio) {
      return res.status(404).json({
        message: 'Servicio no encontrado',
      });
    }

    // Verificar si el servicio ya está asociado
    const servicioExistente = await prisma.servicio_Pernoctacion.findUnique({
      where: {
        idPernoctacion_codigoServicio: {
          idPernoctacion: parseInt(idPernoctacion),
          codigoServicio: codigoServicio,
        },
      },
    });

    if (servicioExistente) {
      return res.status(409).json({
        message: 'Este servicio ya está asociado a la pernoctación',
      });
    }

    // Asociar el servicio a la pernoctación
    const servicioAnadido = await prisma.servicio_Pernoctacion.create({
      data: {
        idPernoctacion: parseInt(idPernoctacion),
        codigoServicio: codigoServicio,
      },
      include: {
        servicio: true,
        pernoctacion: {
          include: {
            reserva: true,
            tipoHabitacion: true,
          },
        },
      },
    });

    res.status(201).json({
      message: 'Servicio añadido exitosamente',
      servicio: servicioAnadido,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al añadir el servicio' });
  }
});

export default router;
