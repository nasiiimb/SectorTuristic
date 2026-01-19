import pool from '../config/database';
import { Reserva, ReservaCreate } from '../types';
import { ResultSetHeader } from 'mysql2';

export class ReservaModel {
  // Crear reserva
  static async crear(datos: ReservaCreate): Promise<number> {
    const query = `
      INSERT INTO reservas (
        usuario_id, localizador_externo, origen, hotel_nombre,
        habitacion_tipo, fecha_entrada, fecha_salida,
        num_huespedes, precio_total, estado, datos_adicionales
      )
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    const [result] = await pool.execute<ResultSetHeader>(query, [
      datos.usuario_id,
      datos.localizador_externo,
      datos.origen,
      datos.hotel_nombre,
      datos.habitacion_tipo,
      datos.fecha_entrada,
      datos.fecha_salida,
      datos.num_huespedes,
      datos.precio_total,
      datos.estado || 'confirmada',
      datos.datos_adicionales ? JSON.stringify(datos.datos_adicionales) : null
    ]);

    return result.insertId;
  }

  // Buscar reservas por usuario
  static async buscarPorUsuario(usuarioId: number): Promise<Reserva[]> {
    const query = `
      SELECT * FROM reservas 
      WHERE usuario_id = ? 
      ORDER BY created_at DESC
    `;
    const [rows] = await pool.execute<Reserva[]>(query, [usuarioId]);
    return rows;
  }

  // Buscar por localizador externo
  static async buscarPorLocalizador(localizador: string): Promise<Reserva | null> {
    const query = 'SELECT * FROM reservas WHERE localizador_externo = ?';
    const [rows] = await pool.execute<Reserva[]>(query, [localizador]);
    return rows.length > 0 ? rows[0] : null;
  }

  // Buscar por localizador y usuario (para seguridad)
  static async buscarPorLocalizadorYUsuario(
    localizador: string,
    usuarioId: number
  ): Promise<Reserva | null> {
    const query = 'SELECT * FROM reservas WHERE localizador_externo = ? AND usuario_id = ?';
    const [rows] = await pool.execute<Reserva[]>(query, [localizador, usuarioId]);
    return rows.length > 0 ? rows[0] : null;
  }
}
