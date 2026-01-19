import { RowDataPacket } from 'mysql2';
import { Request } from 'express';

// ============================================
// Interfaces de Usuario
// ============================================

export interface Usuario extends RowDataPacket {
  id: number;
  nombre: string;
  apellidos: string;
  email: string;
  dni?: string;
  fecha_nacimiento?: Date;
  password: string;
  created_at: Date;
  updated_at: Date;
  activo: boolean;
}

export interface UsuarioRegistro {
  nombre: string;
  apellidos: string;
  email: string;
  dni?: string;
  fecha_nacimiento?: string;
  password: string;
}

export interface UsuarioLogin {
  email: string;
  password: string;
}

export interface UsuarioResponse {
  id: number;
  nombre: string;
  apellidos: string;
  email: string;
  dni?: string;
  fecha_nacimiento?: string;
}

// ============================================
// Interfaces de Reserva
// ============================================

export interface Reserva extends RowDataPacket {
  id: number;
  usuario_id: number;
  localizador_externo: string;
  origen: 'WebService' | 'Channel';
  hotel_nombre: string;
  habitacion_tipo: string;
  fecha_entrada: Date;
  fecha_salida: Date;
  num_huespedes: number;
  precio_total: number;
  estado: 'confirmada' | 'cancelada' | 'completada';
  datos_adicionales?: any;
  created_at: Date;
  updated_at: Date;
}

export interface ReservaCreate {
  usuario_id: number;
  localizador_externo: string;
  origen: 'WebService' | 'Channel';
  hotel_nombre: string;
  habitacion_tipo: string;
  fecha_entrada: string;
  fecha_salida: string;
  num_huespedes: number;
  precio_total: number;
  datos_adicionales?: any;
}

// ============================================
// Interfaces de Disponibilidad
// ============================================

export interface HabitacionDisponible {
  id: string | number;
  idHotel?: number; // ID del hotel (para WebService, obtener regímenes)
  hotelId?: number; // ID del hotel (para Channel)
  nombre: string;
  hotel: string;
  descripcion?: string;
  capacidad: number;
  precio: number;
  foto_url?: string;
  origen: 'WebService' | 'Channel';
  disponible: boolean;
  servicios?: string[];
}

export interface BusquedaDisponibilidad {
  fecha_entrada: string;
  fecha_salida: string;
  num_huespedes: number;
  ciudad?: string;
}

// ============================================
// Interfaces JWT
// ============================================

export interface JWTPayload {
  id: number;
  email: string;
}

// ============================================
// Interfaces de Request extendidas
// ============================================

export interface AuthRequest extends Request {
  user?: JWTPayload;
}
