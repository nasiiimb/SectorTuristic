import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// GET /disponibilidad - Busca tipos de habitación disponibles
router.get('/', async (req, res) => {
  try {
    const { fechaEntrada, fechaSalida, hotel, ciudad, pais } = req.query;

    // Validación de parámetros requeridos
    if (!fechaEntrada || !fechaSalida) {
      return res.status(400).json({
        message: 'Los parámetros fechaEntrada y fechaSalida son requeridos',
      });
    }

    // Validar que al menos se proporcione un filtro de ubicación
    if (!hotel && !ciudad && !pais) {
      return res.status(400).json({
        message: 'Se debe proporcionar al menos un filtro de ubicación: hotel (nombre), ciudad o pais',
      });
    }

    const entrada = new Date(fechaEntrada as string);
    const salida = new Date(fechaSalida as string);

    // Validar que las fechas sean válidas
    if (isNaN(entrada.getTime()) || isNaN(salida.getTime())) {
      return res.status(400).json({
        message: 'Las fechas proporcionadas no son válidas',
      });
    }

    // Validar que la fecha de salida sea posterior a la de entrada
    if (salida <= entrada) {
      return res.status(400).json({
        message: 'La fecha de salida debe ser posterior a la fecha de entrada',
      });
    }

    // Caso 1: Búsqueda por hotel específico (por nombre)
    if (hotel) {
      // Buscar el hotel por nombre
      const hotelEncontrado = await prisma.hotel.findFirst({
        where: {
          nombre: {
            contains: hotel as string,
          },
        },
        include: {
          ciudad: true,
        },
      });

      if (!hotelEncontrado) {
        return res.status(404).json({
          message: `No se encontró ningún hotel con el nombre "${hotel}"`,
        });
      }

      // Contar el total de habitaciones de cada tipo en el hotel
      const habitacionesPorTipo = await prisma.habitacion.groupBy({
        by: ['idTipoHabitacion'],
        where: {
          idHotel: hotelEncontrado.idHotel,
        },
        _count: {
          numeroHabitacion: true,
        },
      });

      // Obtener los IDs de tipos de habitación que existen en este hotel
      const tiposEnHotel = new Set(
        habitacionesPorTipo.map((h) => h.idTipoHabitacion)
      );

      // Contar las pernoctaciones (reservas) para cada tipo de habitación en el rango de fechas
      // Solo contamos las que pertenecen a tipos de habitación de este hotel
      const pernoctacionesPorTipo = await prisma.pernoctacion.groupBy({
        by: ['idTipoHabitacion'],
        where: {
          idTipoHabitacion: {
            in: Array.from(tiposEnHotel),
          },
          reserva: {
            AND: [
              { fechaEntrada: { lt: salida } },
              { fechaSalida: { gt: entrada } },
            ],
          },
        },
        _count: {
          idPernoctacion: true,
        },
      });

      // Crear un mapa de reservas por tipo
      const reservasPorTipoMap = new Map(
        pernoctacionesPorTipo.map((p) => [p.idTipoHabitacion, p._count.idPernoctacion])
      );

      // Calcular disponibilidad para cada tipo de habitación
      const tiposDisponibles = await Promise.all(
        habitacionesPorTipo
          .filter((hab) => {
            const totalHabitaciones = hab._count.numeroHabitacion;
            const reservasActuales = reservasPorTipoMap.get(hab.idTipoHabitacion) || 0;
            return totalHabitaciones > reservasActuales; // Hay disponibilidad si hay más habitaciones que reservas
          })
          .map(async (hab) => {
            const totalHabitaciones = hab._count.numeroHabitacion;
            const reservasActuales = reservasPorTipoMap.get(hab.idTipoHabitacion) || 0;
            const disponibles = totalHabitaciones - reservasActuales;

            // Obtener la información del tipo de habitación
            const tipoHabitacion = await prisma.tipoHabitacion.findUnique({
              where: { idTipoHabitacion: hab.idTipoHabitacion },
            });

            // Obtener la tarifa
            const hotelTarifa = await prisma.hotel_Tarifa.findFirst({
              where: {
                idHotel: hotelEncontrado.idHotel,
                idTipoHabitacion: hab.idTipoHabitacion,
              },
              include: {
                tarifa: true,
              },
            });

            return {
              ...tipoHabitacion,
              precioPorNoche: hotelTarifa?.tarifa.precio || null,
              codigoTarifa: hotelTarifa?.tarifa.codigo || null,
              disponibles, // Cantidad de habitaciones disponibles de este tipo
              totalHabitaciones,
              reservasActuales,
            };
          })
      );

      console.log(hotelEncontrado);

      return res.status(200).json({
        hotel: {
          nombre: hotelEncontrado.nombre,
          ubicacion: hotelEncontrado.ubicacion,
          categoria: hotelEncontrado.categoria,
          ciudad: hotelEncontrado.ciudad.nombre,
          pais: hotelEncontrado.ciudad.pais,
        },
        tiposDisponibles,
        totalTiposDisponibles: tiposDisponibles.length,
      });
    }

    // Caso 2: Búsqueda por ciudad o país
    const whereClause: any = {};
    
    if (ciudad) {
      whereClause.ciudad = {
        nombre: {
          contains: ciudad as string,
        },
      };
    }

    if (pais) {
      whereClause.ciudad = {
        ...whereClause.ciudad,
        pais: {
          contains: pais as string,
        },
      };
    }

    // Obtener hoteles que coincidan con el filtro
    const hoteles = await prisma.hotel.findMany({
      where: whereClause,
      include: {
        ciudad: true,
        habitaciones: {
          include: {
            tipoHabitacion: true,
          },
        },
      },
    });

    // Para cada hotel, calcular disponibilidad
    const hotelesConDisponibilidad = await Promise.all(
      hoteles.map(async (hotel) => {
        // Contar el total de habitaciones de cada tipo en el hotel
        const habitacionesPorTipo = await prisma.habitacion.groupBy({
          by: ['idTipoHabitacion'],
          where: {
            idHotel: hotel.idHotel,
          },
          _count: {
            numeroHabitacion: true,
          },
        });

        // Obtener los IDs de tipos de habitación que existen en este hotel
        const tiposEnHotel = new Set(
          habitacionesPorTipo.map((h) => h.idTipoHabitacion)
        );

        // Contar las pernoctaciones (reservas) para cada tipo de habitación en el rango de fechas
        const pernoctacionesPorTipo = await prisma.pernoctacion.groupBy({
          by: ['idTipoHabitacion'],
          where: {
            idTipoHabitacion: {
              in: Array.from(tiposEnHotel),
            },
            reserva: {
              AND: [
                { fechaEntrada: { lt: salida } },
                { fechaSalida: { gt: entrada } },
              ],
            },
          },
          _count: {
            idPernoctacion: true,
          },
        });

        // Crear un mapa de reservas por tipo
        const reservasPorTipoMap = new Map(
          pernoctacionesPorTipo.map((p) => [p.idTipoHabitacion, p._count.idPernoctacion])
        );

        // Calcular disponibilidad para cada tipo de habitación
        const tiposDisponibles = await Promise.all(
          habitacionesPorTipo
            .filter((hab) => {
              const totalHabitaciones = hab._count.numeroHabitacion;
              const reservasActuales = reservasPorTipoMap.get(hab.idTipoHabitacion) || 0;
              return totalHabitaciones > reservasActuales;
            })
            .map(async (hab) => {
              const totalHabitaciones = hab._count.numeroHabitacion;
              const reservasActuales = reservasPorTipoMap.get(hab.idTipoHabitacion) || 0;
              const disponibles = totalHabitaciones - reservasActuales;

              // Obtener la información del tipo de habitación
              const tipoHabitacion = await prisma.tipoHabitacion.findUnique({
                where: { idTipoHabitacion: hab.idTipoHabitacion },
              });

              // Obtener la tarifa
              const hotelTarifa = await prisma.hotel_Tarifa.findFirst({
                where: {
                  idHotel: hotel.idHotel,
                  idTipoHabitacion: hab.idTipoHabitacion,
                },
                include: {
                  tarifa: true,
                },
              });

              return {
                ...tipoHabitacion,
                precioPorNoche: hotelTarifa?.tarifa.precio || null,
                codigoTarifa: hotelTarifa?.tarifa.codigo || null,
                disponibles,
                totalHabitaciones,
                reservasActuales,
              };
            })
        );

        return {
          idHotel: hotel.idHotel,
          nombre: hotel.nombre,
          ubicacion: hotel.ubicacion,
          categoria: hotel.categoria,
          ciudad: hotel.ciudad,
          tiposDisponibles,
          totalTiposDisponibles: tiposDisponibles.length,
        };
      })
    );

    // Filtrar hoteles que tengan disponibilidad
    const hotelesConHabitaciones = hotelesConDisponibilidad.filter(
      (h) => h.totalTiposDisponibles > 0
    );

    res.status(200).json(hotelesConHabitaciones);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al buscar disponibilidad' });
  }
});

export default router;
