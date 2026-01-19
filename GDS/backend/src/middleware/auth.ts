import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/AuthService';
import { JWTPayload } from '../types';

// Extender el tipo Request de Express para incluir el usuario
declare global {
  namespace Express {
    interface Request {
      user?: JWTPayload;
    }
  }
}

export const authMiddleware = (req: Request, res: Response, next: NextFunction): void => {
  try {
    const authHeader = req.headers.authorization;
    const token = AuthService.extractToken(authHeader);

    if (!token) {
      res.status(401).json({
        success: false,
        message: 'No se proporcionó token de autenticación'
      });
      return;
    }

    // Verificar y decodificar el token
    const payload = AuthService.verifyToken(token);
    
    // Añadir el usuario al request
    req.user = payload;
    
    next();
  } catch (error) {
    res.status(401).json({
      success: false,
      message: 'Token inválido o expirado'
    });
  }
};

// Middleware opcional - no falla si no hay token
export const optionalAuthMiddleware = (req: Request, res: Response, next: NextFunction): void => {
  try {
    const authHeader = req.headers.authorization;
    const token = AuthService.extractToken(authHeader);

    if (token) {
      const payload = AuthService.verifyToken(token);
      req.user = payload;
    }
    
    next();
  } catch (error) {
    // Si el token es inválido, simplemente continuamos sin usuario
    next();
  }
};
