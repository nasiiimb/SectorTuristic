import axios from 'axios';
import { HabitacionDisponible } from '../types';

const WEBSERVICE_URL = process.env.WEBSERVICE_URL || 'http://localhost:3000';

export class WebServiceClient {
  // Consultar disponibilidad en WebService
  static async buscarDisponibilidad(
    fechaEntrada: string,
    fechaSalida: string,
    numHuespedes: number,
    ciudad?: string
  ): Promise<HabitacionDisponible[]> {
    try {
      console.log(`[WebService] Consultando disponibilidad...`);
      console.log(`[WebService] URL: ${WEBSERVICE_URL}/api/disponibilidad`);
      
      const params: any = {
        fechaEntrada,
        fechaSalida,
        personas: numHuespedes
      };
      
      // WebService requiere al menos un filtro de ubicación
      if (ciudad) {
        params.ciudad = ciudad;
      } else {
        // Si no hay ciudad, buscar en todas las ubicaciones usando un wildcard o sin filtro
        params.ciudad = ''; // Buscar en todas las ciudades
      }
      
      console.log(`[WebService] Params:`, params);
      
      const response = await axios.get(`${WEBSERVICE_URL}/api/disponibilidad`, {
        params
      });

      console.log(`[WebService] Status: ${response.status}`);
      console.log(`[WebService] Data type: ${Array.isArray(response.data) ? 'Array' : typeof response.data}`);
      console.log(`[WebService] Items count: ${Array.isArray(response.data) ? response.data.length : 'N/A'}`);

      if (!response.data || !Array.isArray(response.data)) {
        console.log('[WebService] WARNING - Respuesta no es array, retornando []');
        return [];
      }

      if (response.data.length > 0) {
        console.log('[WebService] Sample response item:', JSON.stringify(response.data[0], null, 2));
      }

      // Transformar datos de WebService al formato común
      // WebService devuelve un array de hoteles, cada uno con tiposDisponibles[]
      const habitaciones: HabitacionDisponible[] = [];
      
      response.data.forEach((hotel: any) => {
        if (hotel.tiposDisponibles && Array.isArray(hotel.tiposDisponibles)) {
          hotel.tiposDisponibles.forEach((tipo: any) => {
            habitaciones.push({
              id: tipo.idTipoHabitacion,
              idHotel: hotel.idHotel, // ⬅️ Agregar idHotel para obtener regímenes
              nombre: tipo.categoria || 'Habitación',
              hotel: hotel.nombre || 'Hotel',
              descripcion: `Habitación ${tipo.categoria} en ${hotel.nombre}`,
              capacidad: (tipo.camasDobles || 0) * 2 + (tipo.camasIndividuales || 0),
              precio: parseFloat(tipo.precioPorNoche || tipo.precio || 0),
              foto_url: tipo.foto_url || 'https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800',
              origen: 'WebService' as const,
              disponible: tipo.disponibles > 0,
              servicios: []
            });
          });
        }
      });
      
      console.log(`[WebService] Transformadas ${habitaciones.length} habitaciones de ${response.data.length} hoteles`);
      return habitaciones;
      
    } catch (error: any) {
      console.error('[WebService] Error:', error.message);
      if (error.response) {
        console.error('[WebService] Response status:', error.response.status);
        console.error('[WebService] Response data:', error.response.data);
      }
      return [];
    }
  }

  // Crear reserva en WebService
  static async crearReserva(data: {
    fechaEntrada: string;
    fechaSalida: string;
    hotel: string;
    tipoHabitacion: string;
    regimen: string;
    clientePaga: {
      nombre: string;
      apellidos: string;
      correoElectronico: string;
      DNI: string;
      fechaDeNacimiento?: string;
    };
    huespedes?: any[];
  }): Promise<{ localizador: string; precio: number; reserva: any }> {
    try {
      const response = await axios.post(`${WEBSERVICE_URL}/api/reservas`, {
        fechaEntrada: data.fechaEntrada,
        fechaSalida: data.fechaSalida,
        tipo: 'Reserva',
        hotel: data.hotel,
        tipoHabitacion: data.tipoHabitacion,
        regimen: data.regimen,
        clientePaga: data.clientePaga,
        huespedes: data.huespedes || []
      });

      const reserva = response.data.reserva;
      
      return {
        localizador: reserva.localizador || reserva.idReserva.toString(),
        precio: response.data.precioDetalle?.precioTotal || 0,
        reserva: response.data
      };
    } catch (error: any) {
      console.error('Error al crear reserva en WebService:', error.response?.data || error.message);
      throw new Error(error.response?.data?.message || 'Error al crear reserva en WebService');
    }
  }
}
