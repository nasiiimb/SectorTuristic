import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, ValidationError, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// GET /disponibilidad - Busca tipos de habitación disponibles
router.get('/', asyncHandler(async (req, res) => {
  const { fechaEntrada, fechaSalida, hotel, ciudad, pais } = req.query;

  // Validación de parámetros requeridos
  if (!fechaEntrada || !fechaSalida) {
    throw new ValidationError('Los parámetros fechaEntrada y fechaSalida son requeridos');
  }

  // Validar que al menos se proporcione un filtro de ubicación
  if (!hotel && !ciudad && !pais) {
    throw new ValidationError('Se debe proporcionar al menos un filtro de ubicación: hotel (nombre), ciudad o pais');
  }

  const entrada = new Date(fechaEntrada as string);
  const salida = new Date(fechaSalida as string);

  // Validar que las fechas sean válidas
  if (isNaN(entrada.getTime()) || isNaN(salida.getTime())) {
    throw new ValidationError('Las fechas proporcionadas no son válidas');
  }

  // Validar que la fecha de salida sea posterior a la de entrada
  if (salida <= entrada) {
    throw new ValidationError('La fecha de salida debe ser posterior a la fecha de entrada');
  }

    // Caso 1: Búsqueda por hotel específico (por ID o nombre)
    if (hotel) {
      // Intentar parsear como ID numérico
      const hotelId = parseInt(hotel as string);
      const isId = !isNaN(hotelId);
      
      // Buscar el hotel por ID o por nombre
      const hotelEncontrado = await prisma.hotel.findFirst({
        where: isId 
          ? { idHotel: hotelId }  // Buscar por ID
          : {                     // Buscar por nombre
              nombre: {
                contains: hotel as string,
              },
            },
        include: {
          ciudad: true,
        },
      });

      if (!hotelEncontrado) {
        throw new NotFoundError(`Hotel con ${isId ? 'ID' : 'nombre'} "${hotel}"`);
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

      // Obtener las reservas que se solapan con el rango de fechas
      // IMPORTANTE: Solo contar reservas ACTIVAS (no canceladas)
      const whereReservas: any = {
        estado: 'Activa', // Solo considerar reservas activas
        precioRegimen: {
          idHotel: hotelEncontrado.idHotel,
        },
        AND: [
          { fechaEntrada: { lt: salida } },
          { fechaSalida: { gt: entrada } },
        ],
      };
      
      const reservasEnRango = await prisma.reserva.findMany({
        where: whereReservas,
        include: {
          pernoctaciones: {
            select: {
              idTipoHabitacion: true,
            },
            take: 1, // Solo necesitamos saber el tipo, todas las pernoctaciones de una reserva tienen el mismo tipo
          },
        },
      });

      // Contar cuántas reservas hay por tipo de habitación
      const reservasPorTipoMap = new Map<number, number>();
      reservasEnRango.forEach((reserva) => {
        const idTipo = reserva.pernoctaciones[0]?.idTipoHabitacion;
        if (idTipo) {
          reservasPorTipoMap.set(idTipo, (reservasPorTipoMap.get(idTipo) || 0) + 1);
        }
      });

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

        // Obtener las reservas que se solapan con el rango de fechas
        // IMPORTANTE: Solo contar reservas ACTIVAS (no canceladas)
        const whereReservas: any = {
          estado: 'Activa', // Solo considerar reservas activas
          precioRegimen: {
            idHotel: hotel.idHotel,
          },
          AND: [
            { fechaEntrada: { lt: salida } },
            { fechaSalida: { gt: entrada } },
          ],
        };
        
        const reservasEnRango = await prisma.reserva.findMany({
          where: whereReservas,
          include: {
            pernoctaciones: {
              select: {
                idTipoHabitacion: true,
              },
              take: 1, // Solo necesitamos saber el tipo
            },
          },
        });

        // Contar cuántas reservas hay por tipo de habitación
        const reservasPorTipoMap = new Map<number, number>();
        reservasEnRango.forEach((reserva) => {
          const idTipo = reserva.pernoctaciones[0]?.idTipoHabitacion;
          if (idTipo) {
            reservasPorTipoMap.set(idTipo, (reservasPorTipoMap.get(idTipo) || 0) + 1);
          }
        });

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
}));

export default router;
