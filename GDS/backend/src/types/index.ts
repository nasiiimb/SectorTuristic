import { RowDataPacket } from 'mysql2';
import { Request } from 'express';

// ==================== USUARIO ====================
export interface Usuario extends RowDataPacket {
  id: number;
  nombre: string;
  apellidos: string;
  email: string;
  dni?: string;
  fecha_nacimiento?: string;
  password: string;
  created_at: Date;
  updated_at: Date;
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
  created_at: Date;
  updated_at: Date;
}

// ==================== JWT ====================
export interface JWTPayload {
  id: number;
  email: string;
  iat?: number;
  exp?: number;
}

// ==================== RESERVA ====================
export interface Reserva extends RowDataPacket {
  id: number;
  usuario_id: number;
  localizador_externo: string;
  origen: 'WebService' | 'Channel';
  hotel_nombre: string;
  habitacion_tipo: string;
  fecha_entrada: string;
  fecha_salida: string;
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
  estado?: 'confirmada' | 'cancelada' | 'completada';
  datos_adicionales?: any;
}

// ==================== HABITACION ====================
export interface HabitacionDisponible {
  id: number;
  idHotel?: number;  // Para WebService (obtener regímenes)
  hotel_id?: number;  // Para Channel
  nombre: string;  // Nombre del tipo de habitación (era 'tipo')
  hotel: string;  // Nombre del hotel (era 'hotel_nombre')
  ciudad?: string;
  descripcion?: string;
  capacidad: number;
  precio: number;  // Precio por noche (era 'precio_noche')
  foto_url?: string;
  origen: 'WebService' | 'Channel';
  disponible?: boolean;
  servicios?: string[];
}

// ==================== EXPRESS ====================
export interface AuthRequest extends Request {
  user?: JWTPayload;
}
