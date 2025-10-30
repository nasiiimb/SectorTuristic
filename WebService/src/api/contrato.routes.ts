import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// GET /contratos - Obtiene todos los contratos (reservas con check-in)
router.get('/', async (req, res) => {
  try {
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
  } catch (error) {
    console.error('Error al obtener contratos:', error);
    res.status(500).json({
      message: 'Error al obtener los contratos',
      error: error instanceof Error ? error.message : 'Error desconocido',
    });
  }
});

// POST /contratos/{idContrato}/checkout - Realiza el check-out
router.post('/:idContrato/checkout', async (req, res) => {
  try {
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
      return res.status(404).json({
        message: 'Contrato no encontrado',
      });
    }

    // Verificar que no se haya hecho check-out previamente
    if (contrato.fechaCheckOut) {
      return res.status(409).json({
        message: 'Ya se ha realizado el check-out de este contrato',
      });
    }

    // Verificar que se haya hecho check-in
    if (!contrato.fechaCheckIn) {
      return res.status(409).json({
        message: 'No se puede hacer check-out sin haber hecho check-in',
      });
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
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al realizar el check-out' });
  }
});

export default router;
