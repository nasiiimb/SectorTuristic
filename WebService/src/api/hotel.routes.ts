import { Router } from 'express';
import { pool } from '../config/database'; // Importamos nuestra conexión a la BD
import { Hotel } from '../models/hotel.model'; // Importamos el modelo

const router = Router();

// Esta ruta responderá a GET http://localhost:3000/api/hoteles
router.get('/', async (req, res) => {
  try {
    // Ejecutamos una consulta SQL para obtener todos los hoteles
    const [rows] = await pool.query('SELECT * FROM Hotel');

    // Convertimos el resultado a nuestro modelo Hotel
    const hoteles = rows as Hotel[];

    // Enviamos la respuesta como un JSON con código 200 (OK)
    res.status(200).json(hoteles);
  } catch (error) {
    // Si hay un error, lo mostramos en la consola y enviamos un error 500
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener los hoteles' });
  }
});

export default router;