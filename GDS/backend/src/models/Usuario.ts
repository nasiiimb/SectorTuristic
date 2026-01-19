import pool from '../config/database';
import { Usuario, UsuarioRegistro, UsuarioResponse } from '../types';
import { ResultSetHeader } from 'mysql2';

export class UsuarioModel {
  // Crear usuario
  static async crear(datos: UsuarioRegistro): Promise<number> {
    const query = `
      INSERT INTO usuarios (nombre, apellidos, email, dni, fecha_nacimiento, password)
      VALUES (?, ?, ?, ?, ?, ?)
    `;

    const [result] = await pool.execute<ResultSetHeader>(query, [
      datos.nombre,
      datos.apellidos,
      datos.email,
      datos.dni || null,
      datos.fecha_nacimiento || null,
      datos.password
    ]);

    return result.insertId;
  }

  // Buscar por email
  static async buscarPorEmail(email: string): Promise<Usuario | null> {
    const query = 'SELECT * FROM usuarios WHERE email = ?';
    const [rows] = await pool.execute<Usuario[]>(query, [email]);
    return rows.length > 0 ? rows[0] : null;
  }

  // Buscar por DNI
  static async buscarPorDNI(dni: string): Promise<Usuario | null> {
    const query = 'SELECT * FROM usuarios WHERE dni = ?';
    const [rows] = await pool.execute<Usuario[]>(query, [dni]);
    return rows.length > 0 ? rows[0] : null;
  }

  // Buscar por ID
  static async buscarPorId(id: number): Promise<Usuario | null> {
    const query = 'SELECT * FROM usuarios WHERE id = ?';
    const [rows] = await pool.execute<Usuario[]>(query, [id]);
    return rows.length > 0 ? rows[0] : null;
  }

  // Convertir a respuesta (sin password)
  static toResponse(usuario: Usuario): UsuarioResponse {
    return {
      id: usuario.id,
      nombre: usuario.nombre,
      apellidos: usuario.apellidos,
      email: usuario.email,
      dni: usuario.dni,
      fecha_nacimiento: usuario.fecha_nacimiento,
      created_at: usuario.created_at,
      updated_at: usuario.updated_at
    };
  }
}
