import { Request, Response } from 'express';
import { UsuarioModel } from '../models/Usuario';
import { AuthService } from '../services/AuthService';
import { UsuarioRegistro, UsuarioLogin } from '../types';

export class AuthController {
  // Registro de usuario
  static async register(req: Request, res: Response): Promise<void> {
    try {
      const { nombre, apellidos, email, dni, fecha_nacimiento, password }: UsuarioRegistro = req.body;

      // Validaciones
      if (!nombre || !apellidos || !email || !password) {
        res.status(400).json({
          success: false,
          message: 'Faltan campos obligatorios: nombre, apellidos, email, password'
        });
        return;
      }

      if (password.length < 6) {
        res.status(400).json({
          success: false,
          message: 'La contraseña debe tener al menos 6 caracteres'
        });
        return;
      }

      // Verificar si el email ya existe
      const usuarioExistente = await UsuarioModel.buscarPorEmail(email);
      if (usuarioExistente) {
        res.status(409).json({
          success: false,
          message: 'Este email ya está registrado'
        });
        return;
      }

      // Verificar si el DNI ya existe (si se proporcionó)
      if (dni) {
        const dniExistente = await UsuarioModel.buscarPorDNI(dni);
        if (dniExistente) {
          res.status(409).json({
            success: false,
            message: 'Este DNI ya está registrado'
          });
          return;
        }
      }

      // Hash de la contraseña
      const hashedPassword = await AuthService.hashPassword(password);

      // Crear usuario
      const usuarioId = await UsuarioModel.crear({
        nombre,
        apellidos,
        email,
        dni,
        fecha_nacimiento,
        password: hashedPassword
      });

      // Buscar el usuario creado
      const nuevoUsuario = await UsuarioModel.buscarPorId(usuarioId);
      
      if (!nuevoUsuario) {
        throw new Error('Error al crear usuario');
      }

      // Generar token
      const token = AuthService.generateToken({
        id: nuevoUsuario.id,
        email: nuevoUsuario.email
      });

      res.status(201).json({
        success: true,
        message: 'Usuario registrado exitosamente',
        data: {
          user: UsuarioModel.toResponse(nuevoUsuario),
          token
        }
      });
    } catch (error) {
      console.error('Error en register:', error);
      res.status(500).json({
        success: false,
        message: 'Error al registrar usuario',
        error: error instanceof Error ? error.message : 'Error desconocido'
      });
    }
  }

  // Login de usuario
  static async login(req: Request, res: Response): Promise<void> {
    try {
      const { email, password }: UsuarioLogin = req.body;

      // Validaciones
      if (!email || !password) {
        res.status(400).json({
          success: false,
          message: 'Email y contraseña son obligatorios'
        });
        return;
      }

      // Buscar usuario
      const usuario = await UsuarioModel.buscarPorEmail(email);
      
      if (!usuario) {
        res.status(401).json({
          success: false,
          message: 'Email o contraseña incorrectos'
        });
        return;
      }

      // Verificar contraseña
      const passwordValida = await AuthService.verifyPassword(password, usuario.password);
      
      if (!passwordValida) {
        res.status(401).json({
          success: false,
          message: 'Email o contraseña incorrectos'
        });
        return;
      }

      // Generar token
      const token = AuthService.generateToken({
        id: usuario.id,
        email: usuario.email
      });

      res.json({
        success: true,
        message: 'Login exitoso',
        data: {
          user: UsuarioModel.toResponse(usuario),
          token
        }
      });
    } catch (error) {
      console.error('Error en login:', error);
      res.status(500).json({
        success: false,
        message: 'Error al iniciar sesión',
        error: error instanceof Error ? error.message : 'Error desconocido'
      });
    }
  }

  // Obtener perfil del usuario autenticado
  static async getProfile(req: Request, res: Response): Promise<void> {
    try {
      if (!req.user) {
        res.status(401).json({
          success: false,
          message: 'No autenticado'
        });
        return;
      }

      const usuario = await UsuarioModel.buscarPorId(req.user.id);
      
      if (!usuario) {
        res.status(404).json({
          success: false,
          message: 'Usuario no encontrado'
        });
        return;
      }

      res.json({
        success: true,
        data: UsuarioModel.toResponse(usuario)
      });
    } catch (error) {
      console.error('Error en getProfile:', error);
      res.status(500).json({
        success: false,
        message: 'Error al obtener perfil',
        error: error instanceof Error ? error.message : 'Error desconocido'
      });
    }
  }
}
