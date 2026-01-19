import axios from 'axios';
import mysql from 'mysql2/promise';
import { HabitacionDisponible } from '../types';

const CHANNEL_URL = process.env.CHANNEL_URL || 'http://localhost:8001';

// Pool de conexión a la BD de Channel (SQLite)
const channelDbPath = process.env.CHANNEL_DB_PATH || '../Channel/channel.db';

export class ChannelClient {
  // Consultar disponibilidad directamente en la BD de Channel
  static async buscarDisponibilidad(
    fechaEntrada: string,
    fechaSalida: string,
    numHuespedes: number
  ): Promise<HabitacionDisponible[]> {
    try {
      console.log(`[Channel] Consultando disponibilidad...`);
      console.log(`[Channel] URL: ${CHANNEL_URL}/api/disponibilidad/buscar`);
      console.log(`[Channel] Params:`, { fecha_inicio: fechaEntrada, fecha_fin: fechaSalida, num_huespedes: numHuespedes });
      
      // Opción 1: Consultar vía HTTP endpoint (más limpio)
      // Si Channel tiene endpoint de disponibilidad, usar este approach
      const response = await axios.get(`${CHANNEL_URL}/api/disponibilidad/buscar`, {
        params: {
          fecha_inicio: fechaEntrada,
          fecha_fin: fechaSalida,
          num_huespedes: numHuespedes
        }
      });

      console.log(`[Channel] Status: ${response.status}`);
      console.log(`[Channel] Data type: ${Array.isArray(response.data) ? 'Array' : typeof response.data}`);
      console.log(`[Channel] Items count: ${Array.isArray(response.data) ? response.data.length : 'N/A'}`);

      if (!response.data || !Array.isArray(response.data)) {
        console.log('[Channel] WARNING - Respuesta no es array, retornando []');
        return [];
      }

      // Transformar datos de Channel al formato común
      const habitaciones = response.data.map((item: any) => ({
        id: item.tipo_habitacion_id || item.id,
        hotelId: item.hotel_id, // ⬅️ Agregar hotel_id para usar en reserva
        nombre: item.tipo_nombre || item.nombre || 'Habitación',
        hotel: item.hotel_nombre || 'Hotel Channel',
        descripcion: item.descripcion || '',
        capacidad: item.capacidad_max || 2,
        precio: parseFloat(item.precio || 0),
        foto_url: item.foto_url,
        origen: 'Channel' as const,
        disponible: item.cantidad_disponible > 0,
        servicios: item.servicios ? item.servicios.split(',') : []
      }));
      
      console.log(`[Channel] Transformadas ${habitaciones.length} habitaciones`);
      return habitaciones;
      
    } catch (error: any) {
      console.error('[Channel] Error:', error.message);
      if (error.response) {
        console.error('[Channel] Response status:', error.response.status);
        console.error('[Channel] Response data:', error.response.data);
      }
      return [];
    }
  }

  // Crear reserva en Channel
  static async crearReserva(data: {
    hotel_id: number;
    tipo_habitacion_id: number;
    fecha_entrada: string;
    fecha_salida: string;
    num_habitaciones: number;
    num_huespedes: number;
    cliente_nombre: string;
    cliente_email: string;
    cliente_telefono?: string;
  }): Promise<{ localizador: string; precio: number; reserva: any }> {
    try {
      console.log('[Channel] Creando reserva con datos:', data);
      const response = await axios.post(`${CHANNEL_URL}/api/reservas/reserve`, data);

      return {
        localizador: response.data.localizador || response.data.id.toString(),
        precio: response.data.precio_total || 0,
        reserva: response.data
      };
    } catch (error: any) {
      console.error('Error al crear reserva en Channel:', error.response?.data || error.message);
      throw new Error(error.response?.data?.detail || 'Error al crear reserva en Channel');
    }
  }

  // Obtener detalles de una habitación específica
  static async obtenerDetallesHabitacion(tipoHabitacionId: number): Promise<any> {
    try {
      const response = await axios.get(`${CHANNEL_URL}/api/habitaciones/${tipoHabitacionId}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener detalles de habitación:', error);
      return null;
    }
  }
}
