import { Router } from 'express';
import { AuthController } from '../controllers/AuthController';
import { authMiddleware } from '../middleware/auth';

const router = Router();

// POST /api/auth/register - Registro de usuario
router.post('/register', AuthController.register);

// POST /api/auth/login - Login de usuario
router.post('/login', AuthController.login);

// GET /api/auth/profile - Obtener perfil del usuario autenticado (requiere auth)
router.get('/profile', authMiddleware, AuthController.getProfile);

export default router;
