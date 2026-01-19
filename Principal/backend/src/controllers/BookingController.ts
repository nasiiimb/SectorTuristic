import { Request, Response } from 'express';
import { WebServiceClient } from '../services/WebServiceClient';
import { ChannelClient } from '../services/ChannelClient';
import { ReservaModel } from '../models/Reserva';
import { UsuarioModel } from '../models/Usuario';

export class BookingController {
  // GET /api/search - Buscar disponibilidad unificada (WebService + Channel)
  static async search(req: Request, res: Response): Promise<void> {
    try {
      console.log('[DEBUG] Búsqueda iniciada');
      console.log('[DEBUG] Query params:', req.query);
      
      const { fecha_entrada, fecha_salida, personas, num_huespedes, ciudad } = req.query;
      const numPersonas = personas || num_huespedes;

      // Validaciones
      if (!fecha_entrada || !fecha_salida || !numPersonas) {
        console.log('[DEBUG] ERROR - Parámetros faltantes');
        console.log('[DEBUG] Recibido:', { fecha_entrada, fecha_salida, personas, num_huespedes });
        res.status(400).json({
          success: false,
          message: 'fecha_entrada, fecha_salida y personas son obligatorios'
        });
        return;
      }

      console.log('[DEBUG] Consultando proveedores en paralelo...');
      
      // Consultar ambos proveedores en paralelo
      const [habitacionesWebService, habitacionesChannel] = await Promise.all([
        WebServiceClient.buscarDisponibilidad(
          fecha_entrada as string,
          fecha_salida as string,
          parseInt(numPersonas as string),
          ciudad as string
        ).then(result => {
          console.log(`[DEBUG] WebService respondió: ${result.length} habitaciones`);
          return result;
        }).catch(error => {
          console.error('[DEBUG] ERROR - WebService:', error.message);
          return [];
        }),
        ChannelClient.buscarDisponibilidad(
          fecha_entrada as string,
          fecha_salida as string,
          parseInt(numPersonas as string)
        ).then(result => {
          console.log(`[DEBUG] Channel respondió: ${result.length} habitaciones`);
          return result;
        }).catch(error => {
          console.error('[DEBUG] ERROR - Channel:', error.message);
          return [];
        })
      ]);

      // Unificar resultados
      const habitacionesDisponibles = [
        ...habitacionesWebService,
        ...habitacionesChannel
      ];

      console.log(`[DEBUG] Total habitaciones: ${habitacionesDisponibles.length}`);

      res.status(200).json({
        success: true,
        data: {
          habitaciones: habitacionesDisponibles,
          total: habitacionesDisponibles.length,
          fuentes: {
            webservice: habitacionesWebService.length,
            channel: habitacionesChannel.length
          }
        }
      });
    } catch (error) {
      console.error('[DEBUG] ERROR CRITICO en búsqueda:', error);
      res.status(500).json({
        success: false,
        message: 'Error al buscar disponibilidad'
      });
    }
  }

  // POST /api/book - Crear reserva (delega a WebService o Channel)
  static async book(req: Request, res: Response): Promise<void> {
    try {
      if (!req.user) {
        res.status(401).json({
          success: false,
          message: 'Debe estar autenticado para reservar'
        });
        return;
      }

      const { origen } = req.body;

      // Validar origen
      if (!origen || (origen !== 'WebService' && origen !== 'Channel')) {
        res.status(400).json({
          success: false,
          message: 'Origen debe ser WebService o Channel'
        });
        return;
      }

      // Obtener datos del usuario
      const usuario = await UsuarioModel.buscarPorId(req.user.id);
      if (!usuario) {
        res.status(404).json({
          success: false,
          message: 'Usuario no encontrado'
        });
        return;
      }

      let localizador: string;
      let reservaExterna: any;

      // === RESERVA CHANNEL ===
      if (origen === 'Channel') {
        const {
          habitacion_id,
          hotel_id,
          hotel_nombre,
          habitacion_tipo,
          fecha_entrada,
          fecha_salida,
          num_huespedes,
          precio_total
        } = req.body;

        // Validaciones básicas para Channel
        if (!hotel_id || !habitacion_id || !fecha_entrada || !fecha_salida || !num_huespedes) {
          res.status(400).json({
            success: false,
            message: 'Faltan campos obligatorios para Channel: hotel_id, habitacion_id, fecha_entrada, fecha_salida, num_huespedes'
          });
          return;
        }

        console.log('[Channel Reserva] Datos recibidos:', {
          hotel_id,
          habitacion_id,
          fecha_entrada,
          fecha_salida,
          num_huespedes,
          usuario: `${usuario.nombre} ${usuario.apellidos}`
        });

        // Llamar a Channel para crear la reserva
        const resultado = await ChannelClient.crearReserva({
          hotel_id: parseInt(hotel_id),
          tipo_habitacion_id: parseInt(habitacion_id),
          fecha_entrada: fecha_entrada,
          fecha_salida: fecha_salida,
          num_habitaciones: 1,
          num_huespedes: parseInt(num_huespedes),
          cliente_nombre: `${usuario.nombre} ${usuario.apellidos}`,
          cliente_email: usuario.email
        });

        localizador = resultado.localizador;
        reservaExterna = resultado.reserva;

        console.log('[Channel Reserva] Reserva creada con localizador:', localizador);

        // Guardar en BD de Principal
        const reservaId = await ReservaModel.crear({
          usuario_id: req.user.id,
          localizador_externo: localizador,
          origen: 'Channel',
          hotel_nombre: hotel_nombre || 'Hotel Channel',
          habitacion_tipo: habitacion_tipo || 'Habitación',
          fecha_entrada: fecha_entrada,
          fecha_salida: fecha_salida,
          num_huespedes: parseInt(num_huespedes),
          precio_total: parseFloat(precio_total) || 0,
          datos_adicionales: reservaExterna
        });

        const reserva = await ReservaModel.obtenerPorId(reservaId);

        res.status(201).json({
          success: true,
          message: 'Reserva en Channel creada exitosamente',
          data: {
            reserva: reserva,
            localizador: localizador
          }
        });
        return;
      }

      // === RESERVA WEBSERVICE ===
      if (origen === 'WebService') {
        const {
          habitacion_id,
          hotel_nombre,
          habitacion_tipo,
          fecha_entrada,
          fecha_salida,
          num_huespedes,
          precio_total,
          regimen,
          idHotel,
          idPrecioRegimen
        } = req.body;

        // Validar campos específicos de WebService
        if (!regimen) {
          res.status(400).json({
            success: false,
            message: 'El campo regimen es obligatorio para WebService'
          });
          return;
        }

        const resultado = await WebServiceClient.crearReserva({
          fechaEntrada: fecha_entrada,
          fechaSalida: fecha_salida,
          hotel: hotel_nombre,
          tipoHabitacion: habitacion_tipo,
          regimen: regimen,
          clientePaga: {
            nombre: usuario.nombre,
            apellidos: usuario.apellidos,
            correoElectronico: usuario.email,
            DNI: usuario.dni || 'N/A',
            fechaDeNacimiento: usuario.fecha_nacimiento?.toISOString().split('T')[0]
          }
        });

        const localizador = resultado.localizador;
        const reservaExterna = resultado.reserva;

        // Guardar en BD de Principal
        const reservaId = await ReservaModel.crear({
          usuario_id: req.user.id,
          localizador_externo: localizador,
          origen: 'WebService',
          hotel_nombre: hotel_nombre,
          habitacion_tipo: habitacion_tipo,
          fecha_entrada: fecha_entrada,
          fecha_salida: fecha_salida,
          num_huespedes: parseInt(num_huespedes),
          precio_total: parseFloat(precio_total),
          datos_adicionales: reservaExterna
        });

        const reserva = await ReservaModel.obtenerPorId(reservaId);

        res.status(201).json({
          success: true,
          message: 'Reserva en WebService creada exitosamente',
          data: {
            reserva: reserva,
            localizador: localizador
          }
        });
        return;
      }

    } catch (error: any) {
      console.error('Error al crear reserva:', error);
      res.status(500).json({
        success: false,
        message: error.message || 'Error al crear la reserva'
      });
    }
  }

  // GET /api/my-reservations - Obtener reservas del usuario autenticado
  static async getMyReservations(req: Request, res: Response): Promise<void> {
    try {
      if (!req.user) {
        res.status(401).json({
          success: false,
          message: 'Debe estar autenticado'
        });
        return;
      }

      const reservas = await ReservaModel.obtenerPorUsuario(req.user.id);

      res.status(200).json({
        success: true,
        data: {
          reservas: reservas,
          total: reservas.length
        }
      });
    } catch (error) {
      console.error('Error al obtener reservas:', error);
      res.status(500).json({
        success: false,
        message: 'Error al obtener las reservas'
      });
    }
  }

  // GET /api/reservations/:localizador - Obtener detalle de una reserva por localizador
  static async getReservationByLocalizador(req: Request, res: Response): Promise<void> {
    try {
      if (!req.user) {
        res.status(401).json({
          success: false,
          message: 'Debe estar autenticado'
        });
        return;
      }

      const { localizador } = req.params;
      const reserva = await ReservaModel.obtenerPorLocalizador(localizador);

      if (!reserva) {
        res.status(404).json({
          success: false,
          message: 'Reserva no encontrada'
        });
        return;
      }

      // Verificar que la reserva pertenece al usuario
      if (reserva.usuario_id !== req.user.id) {
        res.status(403).json({
          success: false,
          message: 'No tiene permiso para ver esta reserva'
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: reserva
      });
    } catch (error) {
      console.error('Error al obtener reserva:', error);
      res.status(500).json({
        success: false,
        message: 'Error al obtener la reserva'
      });
    }
  }
}
