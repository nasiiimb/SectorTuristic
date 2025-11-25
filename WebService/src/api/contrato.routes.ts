import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError, ConflictError } from '../middleware/errorHandler';

const router = Router();

// GET /contratos/buscar/cliente - Buscar contratos por nombre o apellido del cliente
router.get('/buscar/cliente', asyncHandler(async (req, res) => {
  const { nombre, apellido, hotel } = req.query;

  // Validar que al menos un parámetro esté presente
  if (!nombre && !apellido) {
    return res.status(400).json({
      error: 'Debe proporcionar al menos nombre o apellido para buscar',
    });
  }

  // Construir filtro dinámico para el cliente
  const filtroCliente: any = {};
  
  if (nombre) {
    filtroCliente.nombre = {
      contains: nombre as string
    };
  }
  
  if (apellido) {
    filtroCliente.apellidos = {
      contains: apellido as string
    };
  }

  // Construir filtro WHERE para la reserva
  const filtroReserva: any = {
    clientePaga: filtroCliente
  };

  // Filtrar por hotel si se proporciona
  if (hotel) {
    filtroReserva.precioRegimen = {
      idHotel: parseInt(hotel as string)
    };
  }

  const contratos = await prisma.contrato.findMany({
    where: {
      reserva: filtroReserva
    },
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
    filtros: {
      nombre: nombre || null,
      apellido: apellido || null,
    },
  });
}));

// GET /contratos - Obtiene todos los contratos (reservas con check-in)
router.get('/', asyncHandler(async (req, res) => {
  const { hotel } = req.query;

  // Construir filtro WHERE
  const whereClause: any = {};

  // Filtrar por hotel si se proporciona
  if (hotel) {
    whereClause.reserva = {
      precioRegimen: {
        idHotel: parseInt(hotel as string)
      }
    };
  }

  const contratos = await prisma.contrato.findMany({
    where: whereClause,
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

// GET /contratos/:idContrato - Obtiene un contrato específico con sus pernoctaciones y servicios
router.get('/:idContrato', asyncHandler(async (req, res) => {
  const { idContrato } = req.params;

  const contrato = await prisma.contrato.findUnique({
    where: {
      idContrato: parseInt(idContrato),
    },
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
              servicioPernoctacion: {
                include: {
                  servicio: true,
                },
              },
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
  });

  if (!contrato) {
    throw new NotFoundError('Contrato');
  }

  // Formatear la respuesta incluyendo servicios
  const contratoFormateado = {
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
      numeroNoches: contrato.reserva.pernoctaciones.length,
    },
    habitacion: contrato.habitacion,
    pernoctaciones: contrato.reserva.pernoctaciones.map((pern: any) => ({
      idPernoctacion: pern.idPernoctacion,
      fechaPernoctacion: pern.fechaPernoctacion,
      tipoHabitacion: pern.tipoHabitacion,
      servicios: pern.servicioPernoctacion,
    })),
  };

  res.json(contratoFormateado);
}));

// PUT /contratos/{idContrato}/checkout - Realiza el check-out
router.put('/:idContrato/checkout', asyncHandler(async (req, res) => {
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
