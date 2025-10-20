import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// Obtener todas las reservas
router.get('/', async (req, res) => {
  try {
    const reservas = await prisma.reserva.findMany({
      include: {
        clientePaga: true,
        precioRegimen: {
          include: {
            regimen: true,
            hotel: true,
          },
        },
        pernoctaciones: {
          include: {
            tipoHabitacion: true,
          },
        },
        reservaHuespedes: {
          include: {
            cliente: true,
          },
        },
      },
    });

    res.status(200).json(reservas);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener las reservas' });
  }
});

// Obtener una reserva por ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const reserva = await prisma.reserva.findUnique({
      where: {
        idReserva: parseInt(id),
      },
      include: {
        clientePaga: true,
        precioRegimen: {
          include: {
            regimen: true,
            hotel: true,
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
        reservaHuespedes: {
          include: {
            cliente: true,
          },
        },
        contrato: {
          include: {
            habitacion: true,
          },
        },
      },
    });

    if (!reserva) {
      return res.status(404).json({ message: 'Reserva no encontrada' });
    }

    res.status(200).json(reserva);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener la reserva' });
  }
});

// Crear una nueva reserva
router.post('/', async (req, res) => {
  try {
    const {
      fechaEntrada,
      fechaSalida,
      canalReserva,
      tipo,
      idCliente_paga,
      idPrecioRegimen,
      huespedes, // Array de IDs de clientes huéspedes
    } = req.body;

    const nuevaReserva = await prisma.reserva.create({
      data: {
        fechaEntrada: new Date(fechaEntrada),
        fechaSalida: new Date(fechaSalida),
        canalReserva,
        tipo,
        idCliente_paga,
        idPrecioRegimen,
        // Crear las relaciones con los huéspedes
        reservaHuespedes: {
          create: huespedes?.map((idCliente: number) => ({
            idCliente,
          })) || [],
        },
      },
      include: {
        clientePaga: true,
        precioRegimen: {
          include: {
            regimen: true,
            hotel: true,
          },
        },
        reservaHuespedes: {
          include: {
            cliente: true,
          },
        },
      },
    });

    res.status(201).json(nuevaReserva);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al crear la reserva' });
  }
});

// Actualizar una reserva
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { fechaEntrada, fechaSalida, canalReserva, tipo } = req.body;

    const reservaActualizada = await prisma.reserva.update({
      where: {
        idReserva: parseInt(id),
      },
      data: {
        ...(fechaEntrada && { fechaEntrada: new Date(fechaEntrada) }),
        ...(fechaSalida && { fechaSalida: new Date(fechaSalida) }),
        ...(canalReserva && { canalReserva }),
        ...(tipo && { tipo }),
      },
      include: {
        clientePaga: true,
        precioRegimen: {
          include: {
            regimen: true,
          },
        },
      },
    });

    res.status(200).json(reservaActualizada);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al actualizar la reserva' });
  }
});

// Cancelar (eliminar) una reserva
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    await prisma.reserva.delete({
      where: {
        idReserva: parseInt(id),
      },
    });

    res.status(200).json({ message: 'Reserva cancelada correctamente' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al cancelar la reserva' });
  }
});

export default router;
