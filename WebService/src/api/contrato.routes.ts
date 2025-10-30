import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError, ConflictError } from '../middleware/errorHandler';

const router = Router();

// GET /contratos - Obtiene todos los contratos (reservas con check-in)
router.get('/', asyncHandler(async (req, res) => {
  const contratos = await prisma.contrato.findMany({
    include: {
      reserva: {
        include: {
          clientePaga: true,
          precioRegimen: {
            include: {
              hotel: true,
              regimen: true,
            },
          },
          pernoctaciones: {
            include: {
              tipoHabitacion: true,
            },
          },
        },
      },
      habitacion: {
        include: {
          hotel: true,
          tipoHabitacion: true,
        },
      },
    },
    orderBy: {
      fechaCheckIn: 'desc',
    },
  });

  // Formatear la respuesta
  const contratosFormateados = contratos.map((contrato) => ({
    idContrato: contrato.idContrato,
    montoTotal: contrato.montoTotal,
    fechaCheckIn: contrato.fechaCheckIn,
    fechaCheckOut: contrato.fechaCheckOut,
    numeroHabitacion: contrato.numeroHabitacion,
    estado: contrato.fechaCheckOut ? 'Finalizado' : 'Activo',
    reserva: {
      idReserva: contrato.reserva.idReserva,
      fechaEntrada: contrato.reserva.fechaEntrada,
      fechaSalida: contrato.reserva.fechaSalida,
      canalReserva: contrato.reserva.canalReserva,
      tipo: contrato.reserva.tipo,
      clientePaga: contrato.reserva.clientePaga,
      hotel: contrato.reserva.precioRegimen.hotel,
      regimen: contrato.reserva.precioRegimen.regimen,
      tipoHabitacion: contrato.reserva.pernoctaciones[0]?.tipoHabitacion,
      numeroNoches: contrato.reserva.pernoctaciones.length,
    },
    habitacion: contrato.habitacion,
  }));

  res.json({
    total: contratosFormateados.length,
    activos: contratosFormateados.filter((c) => c.estado === 'Activo').length,
    finalizados: contratosFormateados.filter((c) => c.estado === 'Finalizado').length,
    contratos: contratosFormateados,
  });
}));

// POST /contratos/{idContrato}/checkout - Realiza el check-out
router.post('/:idContrato/checkout', asyncHandler(async (req, res) => {
  const { idContrato } = req.params;

  // Verificar que el contrato existe
  const contrato = await prisma.contrato.findUnique({
    where: {
      idContrato: parseInt(idContrato),
    },
    include: {
      reserva: true,
    },
  });

  if (!contrato) {
    throw new NotFoundError('Contrato');
  }

  // Verificar que no se haya hecho check-out previamente
  if (contrato.fechaCheckOut) {
    throw new ConflictError('Ya se ha realizado el check-out de este contrato');
  }

  // Verificar que se haya hecho check-in
  if (!contrato.fechaCheckIn) {
    throw new ConflictError('No se puede hacer check-out sin haber hecho check-in');
  }

  // Realizar el check-out
  const contratoActualizado = await prisma.contrato.update({
    where: {
      idContrato: parseInt(idContrato),
    },
    data: {
      fechaCheckOut: new Date(),
    },
    include: {
      reserva: {
        include: {
          clientePaga: true,
          precioRegimen: {
            include: {
              regimen: true,
              hotel: true,
            },
          },
        },
      },
      habitacion: {
        include: {
          tipoHabitacion: true,
        },
      },
    },
  });

  res.status(200).json({
    message: 'Check-out realizado exitosamente',
    contrato: contratoActualizado,
  });
}));

export default router;
