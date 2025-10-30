import { Request, Response, NextFunction } from 'express';
import { Prisma } from '@prisma/client';

// Tipos de error personalizados
export class AppError extends Error {
  statusCode: number;
  isOperational: boolean;

  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} no encontrado`, 404);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400);
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 409);
  }
}

// Middleware para capturar errores asíncronos
export const asyncHandler = (fn: Function) => {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

// Middleware de manejo de errores global
export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // Error de Prisma - clave duplicada
  if (err instanceof Prisma.PrismaClientKnownRequestError) {
    if (err.code === 'P2002') {
      return res.status(409).json({
        error: 'Conflicto',
        message: 'Ya existe un registro con esos datos únicos',
        details: err.meta
      });
    }
    if (err.code === 'P2025') {
      return res.status(404).json({
        error: 'No encontrado',
        message: 'El registro solicitado no existe'
      });
    }
    if (err.code === 'P2003') {
      return res.status(400).json({
        error: 'Error de validación',
        message: 'Referencia a un registro inexistente',
        details: err.meta
      });
    }
  }

  // Error de validación de Prisma
  if (err instanceof Prisma.PrismaClientValidationError) {
    return res.status(400).json({
      error: 'Error de validación',
      message: 'Los datos proporcionados no son válidos',
      details: err.message
    });
  }

  // Errores personalizados de la aplicación
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.name,
      message: err.message
    });
  }

  // Error genérico
  console.error('Error no manejado:', err);
  return res.status(500).json({
    error: 'Error interno del servidor',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Ha ocurrido un error inesperado'
  });
};

// Middleware para rutas no encontradas
export const notFoundHandler = (req: Request, res: Response) => {
  res.status(404).json({
    error: 'Ruta no encontrada',
    message: `No se encontró la ruta: ${req.method} ${req.originalUrl}`
  });
};
