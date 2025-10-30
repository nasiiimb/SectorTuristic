import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, ValidationError, NotFoundError, ConflictError } from '../middleware/errorHandler';

const router = Router();

// POST /pernoctaciones/{idPernoctacion}/servicios - Añade un servicio a una pernoctación
router.post('/:idPernoctacion/servicios', asyncHandler(async (req, res) => {
  const { idPernoctacion } = req.params;
  const { codigoServicio } = req.body;

  // Validar parámetros
  if (!codigoServicio) {
    throw new ValidationError('El codigoServicio es requerido');
  }

  // Verificar que la pernoctación existe
  const pernoctacion = await prisma.pernoctacion.findUnique({
    where: {
      idPernoctacion: parseInt(idPernoctacion),
    },
  });

  if (!pernoctacion) {
    throw new NotFoundError('Pernoctación');
  }

  // Verificar que el servicio existe
  const servicio = await prisma.servicio.findUnique({
    where: {
      codigoServicio: codigoServicio,
    },
  });

  if (!servicio) {
    throw new NotFoundError('Servicio');
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
    throw new ConflictError('Este servicio ya está asociado a la pernoctación');
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
}));

export default router;
