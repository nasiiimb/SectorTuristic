import { Router } from 'express';
import { BookingController } from '../controllers/BookingController';
import { authMiddleware } from '../middleware/auth';

const router = Router();

// GET /api/search - Buscar disponibilidad (público)
router.get('/search', BookingController.search);

// POST /api/book - Crear reserva (requiere autenticación)
router.post('/book', authMiddleware, BookingController.book);

// GET /api/my-reservations - Obtener reservas del usuario (requiere autenticación)
router.get('/my-reservations', authMiddleware, BookingController.getMyReservations);

// GET /api/reservations/:localizador - Obtener detalle de reserva (requiere autenticación)
router.get('/reservations/:localizador', authMiddleware, BookingController.getReservationByLocalizador);

export default router;
