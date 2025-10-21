import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// Función auxiliar para calcular el precio de una reserva
async function calcularPrecioReserva(reserva: any) {
  // Obtener tarifa de la habitación
  const tarifaHabitacion = await prisma.hotel_Tarifa.findFirst({
    where: {
      idHotel: reserva.precioRegimen.idHotel,
      idTipoHabitacion: reserva.pernoctaciones[0]?.idTipoHabitacion,
    },
    include: {
      tarifa: true,
    },
  });

  const precioHabitacionPorNoche = Number(tarifaHabitacion?.tarifa.precio || 0);
  const precioRegimenPorNoche = Number(reserva.precioRegimen.precio);
  const numeroNoches = reserva.pernoctaciones.length;

  // Calcular descuentos si existen
  const descuentoTotal = reserva.reservaDescuento?.reduce((total: number, rd: any) => {
    return total + Number(rd.descuento.monto);
  }, 0) || 0;

  const subtotalHabitacion = precioHabitacionPorNoche * numeroNoches;
  const subtotalRegimen = precioRegimenPorNoche * numeroNoches;
  const precioTotal = subtotalHabitacion + subtotalRegimen - descuentoTotal;

  return {
    precioHabitacionPorNoche,
    precioRegimenPorNoche,
    numeroNoches,
    subtotalHabitacion,
    subtotalRegimen,
    descuentos: descuentoTotal,
    precioTotal,
  };
}

// Buscar reservas por nombre/apellido del cliente
router.get('/buscar/cliente', async (req, res) => {
  try {
    const { nombre, apellido } = req.query;

    if (!nombre && !apellido) {
      return res.status(400).json({ 
        message: 'Debes proporcionar al menos nombre o apellido para buscar' 
      });
    }

    // Construir filtro dinámico
    const filtroCliente: any = {};
    if (nombre) {
      filtroCliente.nombre = {
        contains: nombre as string,
        mode: 'insensitive' as const
      };
    }
    if (apellido) {
      filtroCliente.apellidos = {
        contains: apellido as string,
        mode: 'insensitive' as const
      };
    }

    const reservas = await prisma.reserva.findMany({
      where: {
        clientePaga: filtroCliente
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
        reservaDescuento: {
          include: {
            descuento: true,
          },
        },
      },
      orderBy: {
        fechaEntrada: 'desc'
      }
    });

    // Calcular precio para cada reserva
    const reservasConPrecio = await Promise.all(
      reservas.map(async (reserva) => {
        const precioDetalle = await calcularPrecioReserva(reserva);
        return {
          ...reserva,
          precioDetalle,
        };
      })
    );

    res.status(200).json({
      reservas: reservasConPrecio,
      total: reservasConPrecio.length,
      filtros: {
        nombre: nombre || null,
        apellido: apellido || null
      }
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al buscar reservas' });
  }
});

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
        contrato: true,
        reservaDescuento: {
          include: {
            descuento: true,
          },
        },
      },
    });

    // Calcular precio para cada reserva
    const reservasConPrecio = await Promise.all(
      reservas.map(async (reserva) => {
        const precioDetalle = await calcularPrecioReserva(reserva);
        return {
          ...reserva,
          precioDetalle,
        };
      })
    );

    res.status(200).json(reservasConPrecio);
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
        reservaDescuento: {
          include: {
            descuento: true,
          },
        },
      },
    });

    if (!reserva) {
      return res.status(404).json({ message: 'Reserva no encontrada' });
    }

    // Calcular precio
    const precioDetalle = await calcularPrecioReserva(reserva);

    res.status(200).json({
      ...reserva,
      precioDetalle,
    });
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
      clientePaga, // Objeto con datos del cliente que paga
      hotel, // Nombre del hotel
      tipoHabitacion, // Nombre del tipo de habitación
      regimen, // Código del régimen
      huespedes, // Array de objetos con datos de huéspedes
    } = req.body;

    // Validación de parámetros requeridos
    if (!fechaEntrada || !fechaSalida || !tipo || !clientePaga || !hotel || !tipoHabitacion || !regimen) {
      return res.status(400).json({
        message: 'Faltan parámetros requeridos: fechaEntrada, fechaSalida, tipo, clientePaga (objeto), hotel (nombre), tipoHabitacion (nombre), regimen (código)',
      });
    }

    // Validar datos del cliente que paga
    if (!clientePaga.nombre || !clientePaga.apellidos || !clientePaga.correoElectronico || !clientePaga.DNI) {
      return res.status(400).json({
        message: 'El cliente que paga debe incluir: nombre, apellidos, correoElectronico, DNI',
      });
    }

    const entrada = new Date(fechaEntrada);
    const salida = new Date(fechaSalida);

    // Validar fechas
    if (isNaN(entrada.getTime()) || isNaN(salida.getTime())) {
      return res.status(400).json({
        message: 'Las fechas proporcionadas no son válidas',
      });
    }

    if (salida <= entrada) {
      return res.status(400).json({
        message: 'La fecha de salida debe ser posterior a la fecha de entrada',
      });
    }

    // Buscar o crear el cliente que paga
    let cliente = await prisma.cliente.findUnique({
      where: { DNI: clientePaga.DNI },
    });

    if (!cliente) {
      // Crear el cliente si no existe
      cliente = await prisma.cliente.create({
        data: {
          nombre: clientePaga.nombre,
          apellidos: clientePaga.apellidos,
          correoElectronico: clientePaga.correoElectronico,
          DNI: clientePaga.DNI,
          fechaDeNacimiento: clientePaga.fechaDeNacimiento ? new Date(clientePaga.fechaDeNacimiento) : null,
        },
      });
    }

    // Buscar el hotel por nombre
    const hotelEncontrado = await prisma.hotel.findFirst({
      where: {
        nombre: {
          contains: hotel,
        },
      },
    });

    if (!hotelEncontrado) {
      return res.status(404).json({
        message: `No se encontró ningún hotel con el nombre "${hotel}"`,
      });
    }

    // Buscar el tipo de habitación por nombre
    const tipoHabitacionEncontrado = await prisma.tipoHabitacion.findFirst({
      where: {
        categoria: {
          contains: tipoHabitacion,
        },
      },
    });

    if (!tipoHabitacionEncontrado) {
      return res.status(404).json({
        message: `No se encontró ningún tipo de habitación con el nombre "${tipoHabitacion}"`,
      });
    }

    // Buscar el régimen por código
    const regimenEncontrado = await prisma.regimen.findFirst({
      where: {
        codigo: regimen,
      },
    });

    if (!regimenEncontrado) {
      return res.status(404).json({
        message: `No se encontró ningún régimen con el código "${regimen}"`,
      });
    }

    // Buscar el precio del régimen para este hotel
    const precioRegimen = await prisma.precioRegimen.findFirst({
      where: {
        idHotel: hotelEncontrado.idHotel,
        idRegimen: regimenEncontrado.idRegimen,
      },
      include: {
        hotel: true,
        regimen: true,
      },
    });

    if (!precioRegimen) {
      return res.status(404).json({
        message: `El hotel "${hotel}" no ofrece el régimen "${regimen}"`,
      });
    }

    // Verificar disponibilidad: obtener habitaciones del hotel del tipo solicitado
    const habitacionesDisponibles = await prisma.habitacion.findMany({
      where: {
        idHotel: hotelEncontrado.idHotel,
        idTipoHabitacion: tipoHabitacionEncontrado.idTipoHabitacion,
      },
    });

    if (habitacionesDisponibles.length === 0) {
      return res.status(409).json({
        message: `No hay habitaciones de tipo "${tipoHabitacion}" en el hotel "${hotel}"`,
      });
    }

    // Verificar que hay disponibilidad en las fechas
    const reservasOcupadas = await prisma.reserva.findMany({
      where: {
        AND: [
          { fechaEntrada: { lt: salida } },
          { fechaSalida: { gt: entrada } },
        ],
        contrato: {
          habitacion: {
            idHotel: hotelEncontrado.idHotel,
            idTipoHabitacion: tipoHabitacionEncontrado.idTipoHabitacion,
          },
        },
      },
      include: {
        contrato: true,
      },
    });

    const habitacionesOcupadas = new Set(
      reservasOcupadas.map((r) => r.contrato?.numeroHabitacion).filter(Boolean)
    );

    const habitacionesLibres = habitacionesDisponibles.filter(
      (hab) => !habitacionesOcupadas.has(hab.numeroHabitacion)
    );

    if (habitacionesLibres.length === 0) {
      return res.status(409).json({
        message: 'No hay disponibilidad para las fechas seleccionadas',
      });
    }

    // Calcular número de noches
    const diffTime = Math.abs(salida.getTime() - entrada.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    // Crear la reserva con pernoctaciones
    const pernoctaciones = [];
    for (let i = 0; i < diffDays; i++) {
      const fecha = new Date(entrada);
      fecha.setDate(fecha.getDate() + i);
      pernoctaciones.push({
        fechaPernoctacion: fecha,
        idTipoHabitacion: tipoHabitacionEncontrado.idTipoHabitacion,
      });
    }

    // Procesar huéspedes (buscar o crear)
    const huespedesIds = [];
    if (huespedes && Array.isArray(huespedes)) {
      for (const huesped of huespedes) {
        if (!huesped.DNI || !huesped.nombre || !huesped.apellidos || !huesped.correoElectronico) {
          return res.status(400).json({
            message: 'Cada huésped debe incluir: nombre, apellidos, correoElectronico, DNI',
          });
        }

        let huespedExistente = await prisma.cliente.findUnique({
          where: { DNI: huesped.DNI },
        });

        if (!huespedExistente) {
          huespedExistente = await prisma.cliente.create({
            data: {
              nombre: huesped.nombre,
              apellidos: huesped.apellidos,
              correoElectronico: huesped.correoElectronico,
              DNI: huesped.DNI,
              fechaDeNacimiento: huesped.fechaDeNacimiento ? new Date(huesped.fechaDeNacimiento) : null,
            },
          });
        }

        huespedesIds.push(huespedExistente.idCliente);
      }
    }

    // Buscar el precio de la tarifa de habitación
    const tarifaHabitacion = await prisma.hotel_Tarifa.findFirst({
      where: {
        idHotel: hotelEncontrado.idHotel,
        idTipoHabitacion: tipoHabitacionEncontrado.idTipoHabitacion,
      },
      include: {
        tarifa: true,
      },
    });

    const precioHabitacionPorNoche = tarifaHabitacion?.tarifa.precio || 0;

    const nuevaReserva = await prisma.reserva.create({
      data: {
        fechaEntrada: entrada,
        fechaSalida: salida,
        canalReserva: canalReserva || null,
        tipo,
        idCliente_paga: cliente.idCliente,
        idPrecioRegimen: precioRegimen.idPrecioRegimen,
        pernoctaciones: {
          create: pernoctaciones,
        },
        reservaHuespedes: {
          create: huespedesIds.map((idCliente) => ({
            idCliente,
          })),
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
        reservaDescuento: {
          include: {
            descuento: true,
          },
        },
      },
    });

    // Calcular precio total
    const numeroNoches = diffDays;
    const precioRegimenPorNoche = Number(precioRegimen.precio);
    const precioHabitacion = Number(precioHabitacionPorNoche);
    
    // Calcular descuentos
    const descuentoTotal = nuevaReserva.reservaDescuento.reduce((total, rd) => {
      return total + Number(rd.descuento.monto);
    }, 0);

    const precioTotal = (precioHabitacion * numeroNoches) + (precioRegimenPorNoche * numeroNoches) - descuentoTotal;

    res.status(201).json({
      message: 'Reserva creada exitosamente',
      reserva: nuevaReserva,
      precioDetalle: {
        precioHabitacionPorNoche: precioHabitacion,
        precioRegimenPorNoche: precioRegimenPorNoche,
        numeroNoches: numeroNoches,
        subtotalHabitacion: precioHabitacion * numeroNoches,
        subtotalRegimen: precioRegimenPorNoche * numeroNoches,
        descuentos: descuentoTotal,
        precioTotal: precioTotal,
      },
      clienteCreado: cliente.idCliente !== undefined ? 'El cliente fue registrado en el sistema' : undefined,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al crear la reserva' });
  }
});

// Actualizar una reserva
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { fechaEntrada, fechaSalida, canalReserva, tipo, idTipoHabitacion } = req.body;

    // Verificar que la reserva existe
    const reservaExistente = await prisma.reserva.findUnique({
      where: { idReserva: parseInt(id) },
      include: {
        contrato: true,
        precioRegimen: {
          include: {
            hotel: true,
          },
        },
        pernoctaciones: true,
      },
    });

    if (!reservaExistente) {
      return res.status(404).json({
        message: 'Reserva no encontrada',
      });
    }

    // Verificar que no se ha hecho check-in
    if (reservaExistente.contrato?.fechaCheckIn) {
      return res.status(409).json({
        message: 'No se puede modificar una reserva después del check-in',
      });
    }

    // Si se cambian las fechas, validar disponibilidad
    const nuevaEntrada = fechaEntrada ? new Date(fechaEntrada) : reservaExistente.fechaEntrada;
    const nuevaSalida = fechaSalida ? new Date(fechaSalida) : reservaExistente.fechaSalida;

    if (nuevaSalida <= nuevaEntrada) {
      return res.status(400).json({
        message: 'La fecha de salida debe ser posterior a la fecha de entrada',
      });
    }

    const tipoHabitacionId = idTipoHabitacion || reservaExistente.pernoctaciones[0]?.idTipoHabitacion;

    // Verificar disponibilidad si se cambian fechas o tipo de habitación
    if (fechaEntrada || fechaSalida || idTipoHabitacion) {
      const reservasOcupadas = await prisma.reserva.findMany({
        where: {
          AND: [
            { idReserva: { not: parseInt(id) } }, // Excluir la reserva actual
            { fechaEntrada: { lt: nuevaSalida } },
            { fechaSalida: { gt: nuevaEntrada } },
          ],
          contrato: {
            habitacion: {
              idHotel: reservaExistente.precioRegimen.idHotel,
              idTipoHabitacion: tipoHabitacionId,
            },
          },
        },
        include: {
          contrato: true,
        },
      });

      const habitacionesDisponibles = await prisma.habitacion.findMany({
        where: {
          idHotel: reservaExistente.precioRegimen.idHotel,
          idTipoHabitacion: tipoHabitacionId,
        },
      });

      const habitacionesOcupadas = new Set(
        reservasOcupadas.map((r) => r.contrato?.numeroHabitacion).filter(Boolean)
      );

      const habitacionesLibres = habitacionesDisponibles.filter(
        (hab) => !habitacionesOcupadas.has(hab.numeroHabitacion)
      );

      if (habitacionesLibres.length === 0) {
        return res.status(409).json({
          message: 'No hay disponibilidad para las fechas o tipo de habitación solicitados',
        });
      }
    }

    // Si se cambian las fechas, actualizar pernoctaciones
    if (fechaEntrada || fechaSalida || idTipoHabitacion) {
      // Eliminar pernoctaciones existentes
      await prisma.pernoctacion.deleteMany({
        where: {
          idReserva: parseInt(id),
        },
      });

      // Crear nuevas pernoctaciones
      const diffTime = Math.abs(nuevaSalida.getTime() - nuevaEntrada.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      const pernoctaciones = [];
      for (let i = 0; i < diffDays; i++) {
        const fecha = new Date(nuevaEntrada);
        fecha.setDate(fecha.getDate() + i);
        pernoctaciones.push({
          fechaPernoctacion: fecha,
          idTipoHabitacion: tipoHabitacionId,
        });
      }

      await prisma.pernoctacion.createMany({
        data: pernoctaciones.map((p) => ({
          ...p,
          idReserva: parseInt(id),
        })),
      });
    }

    const reservaActualizada = await prisma.reserva.update({
      where: {
        idReserva: parseInt(id),
      },
      data: {
        ...(fechaEntrada && { fechaEntrada: nuevaEntrada }),
        ...(fechaSalida && { fechaSalida: nuevaSalida }),
        ...(canalReserva && { canalReserva }),
        ...(tipo && { tipo }),
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
          },
        },
        reservaHuespedes: {
          include: {
            cliente: true,
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

    // Verificar que la reserva existe
    const reserva = await prisma.reserva.findUnique({
      where: { idReserva: parseInt(id) },
      include: {
        contrato: true,
      },
    });

    if (!reserva) {
      return res.status(404).json({
        message: 'Reserva no encontrada',
      });
    }

    // Verificar que no se ha hecho check-in
    if (reserva.contrato?.fechaCheckIn) {
      return res.status(409).json({
        message: 'No se puede cancelar una reserva después del check-in',
      });
    }

    await prisma.reserva.delete({
      where: {
        idReserva: parseInt(id),
      },
    });

    res.status(204).send();
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al cancelar la reserva' });
  }
});

// POST /reservas/{idReserva}/checkin - Realizar check-in
router.post('/:id/checkin', async (req, res) => {
  try {
    const { id } = req.params;
    const { numeroHabitacion } = req.body;

    // Validar parámetros
    if (!numeroHabitacion) {
      return res.status(400).json({
        message: 'El numeroHabitacion es requerido',
      });
    }

    // Verificar que la reserva existe
    const reserva = await prisma.reserva.findUnique({
      where: { idReserva: parseInt(id) },
      include: {
        contrato: true,
        pernoctaciones: {
          include: {
            tipoHabitacion: true,
          },
        },
        precioRegimen: {
          include: {
            regimen: true,
            hotel: true,
          },
        },
        clientePaga: true,
      },
    });

    if (!reserva) {
      return res.status(404).json({
        message: 'Reserva no encontrada',
      });
    }

    // Verificar que no se ha hecho check-in previamente
    if (reserva.contrato) {
      return res.status(409).json({
        message: 'Ya se ha realizado el check-in de esta reserva',
      });
    }

    // Verificar que la habitación existe
    const habitacion = await prisma.habitacion.findUnique({
      where: { numeroHabitacion },
      include: {
        tipoHabitacion: true,
        hotel: true,
      },
    });

    if (!habitacion) {
      return res.status(404).json({
        message: 'Habitación no encontrada',
      });
    }

    // Verificar que la habitación pertenece al hotel correcto
    if (habitacion.idHotel !== reserva.precioRegimen.idHotel) {
      return res.status(400).json({
        message: 'La habitación no pertenece al hotel de la reserva',
      });
    }

    // Verificar que el tipo de habitación coincide
    const tipoReservado = reserva.pernoctaciones[0]?.idTipoHabitacion;
    if (habitacion.idTipoHabitacion !== tipoReservado) {
      return res.status(400).json({
        message: 'El tipo de habitación no coincide con el reservado',
      });
    }

    // Verificar que la habitación no esté ocupada
    const habitacionOcupada = await prisma.contrato.findFirst({
      where: {
        numeroHabitacion,
        fechaCheckIn: { not: null },
        fechaCheckOut: null,
      },
    });

    if (habitacionOcupada) {
      return res.status(409).json({
        message: 'La habitación está ocupada actualmente',
      });
    }

    // Calcular monto total
    const numNoches = reserva.pernoctaciones.length;
    const precioRegimen = parseFloat(reserva.precioRegimen.precio.toString());
    const montoTotal = numNoches * precioRegimen;

    // Crear el contrato
    const contrato = await prisma.contrato.create({
      data: {
        montoTotal,
        fechaCheckIn: new Date(),
        idReserva: parseInt(id),
        numeroHabitacion,
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
            pernoctaciones: {
              include: {
                tipoHabitacion: true,
              },
            },
          },
        },
        habitacion: {
          include: {
            tipoHabitacion: true,
            hotel: true,
          },
        },
      },
    });

    res.status(201).json({
      message: 'Check-in realizado exitosamente',
      contrato,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al realizar el check-in' });
  }
});

export default router;
