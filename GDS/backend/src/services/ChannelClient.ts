import axios from 'axios';
import { HabitacionDisponible } from '../types';

const CHANNEL_URL = process.env.CHANNEL_URL || 'http://localhost:8001';

export class ChannelClient {
  // Consultar disponibilidad en Channel
  static async buscarDisponibilidad(
    fechaEntrada: string,
    fechaSalida: string,
    numHuespedes: number
  ): Promise<HabitacionDisponible[]> {
    try {
      console.log(`[Channel] Consultando disponibilidad...`);
      console.log(`[Channel] URL: ${CHANNEL_URL}/api/disponibilidad/buscar`);
      console.log(`[Channel] Params:`, { fecha_inicio: fechaEntrada, fecha_fin: fechaSalida, num_huespedes: numHuespedes });
      
      const params = {
        fecha_inicio: fechaEntrada,
        fecha_fin: fechaSalida,
        num_huespedes: numHuespedes
      };

      const response = await axios.get(`${CHANNEL_URL}/api/disponibilidad/buscar`, {
        params
      });

      console.log(`[Channel] Status: ${response.status}`);
      console.log(`[Channel] Data type: ${Array.isArray(response.data) ? 'Array' : typeof response.data}`);
      console.log(`[Channel] Items count: ${Array.isArray(response.data) ? response.data.length : 'N/A'}`);

      if (!response.data || !Array.isArray(response.data)) {
        console.log('[Channel] WARNING - Respuesta no es array, retornando []');
        return [];
      }

      if (response.data.length > 0) {
        console.log('[Channel] Sample response item:', JSON.stringify(response.data[0], null, 2));
      }

      // Transformar datos de Channel al formato común
      const habitaciones = response.data.map((item: any) => ({
        id: item.tipo_habitacion_id || item.id,
        hotelId: item.hotel_id, // ⬅️ Importante para usar en reserva
        nombre: item.tipo_nombre || item.nombre || 'Habitación',
        hotel: item.hotel_nombre || 'Hotel Channel',
        descripcion: item.descripcion || '',
        capacidad: item.capacidad_max || 2,
        precio: parseFloat(item.precio || 0),
        foto_url: item.foto_url || 'https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800',
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
      const response = await axios.post(`${CHANNEL_URL}/api/reservas/crear`, data);

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
}
