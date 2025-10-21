import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// GET /tipos-habitacion - Obtener todos los tipos de habitación
router.get('/', async (req, res) => {
  try {
    const tiposHabitacion = await prisma.tipoHabitacion.findMany({
      include: {
        habitaciones: {
          include: {
            hotel: {
              include: {
                ciudad: true,
              },
            },
          },
        },
      },
    });

    // Formatear respuesta
    const tiposFormateados = tiposHabitacion.map((tipo) => {
      // Agrupar hoteles únicos
      const hotelesUnicos = new Map();
      tipo.habitaciones.forEach((hab) => {
        const hotelId = hab.hotel.idHotel;
        if (!hotelesUnicos.has(hotelId)) {
          hotelesUnicos.set(hotelId, {
            hotel: hab.hotel.nombre,
            ciudad: hab.hotel.ciudad.nombre,
            cantidad: 1,
          });
        } else {
          const hotel = hotelesUnicos.get(hotelId);
          hotel.cantidad++;
        }
      });

      return {
        categoria: tipo.categoria,
        camasIndividuales: tipo.camasIndividuales,
        camasDobles: tipo.camasDobles,
        disponibleEn: Array.from(hotelesUnicos.values()),
      };
    });

    res.status(200).json(tiposFormateados);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener los tipos de habitación' });
  }
});

// GET /tipos-habitacion/:categoria - Obtener un tipo específico
router.get('/:categoria', async (req, res) => {
  try {
    const { categoria } = req.params;

    const tipo = await prisma.tipoHabitacion.findFirst({
      where: {
        categoria: {
          contains: categoria,
        },
      },
      include: {
        habitaciones: {
          include: {
            hotel: {
              include: {
                ciudad: true,
              },
            },
          },
        },
      },
    });

    if (!tipo) {
      return res.status(404).json({
        message: `No se encontró ningún tipo de habitación "${categoria}"`,
      });
    }

    // Agrupar hoteles únicos
    const hotelesUnicos = new Map();
    tipo.habitaciones.forEach((hab) => {
      const hotelId = hab.hotel.idHotel;
      if (!hotelesUnicos.has(hotelId)) {
        hotelesUnicos.set(hotelId, {
          hotel: hab.hotel.nombre,
          ciudad: hab.hotel.ciudad.nombre,
          cantidad: 1,
        });
      } else {
        const hotel = hotelesUnicos.get(hotelId);
        hotel.cantidad++;
      }
    });

    const tipoFormateado = {
      categoria: tipo.categoria,
      camasIndividuales: tipo.camasIndividuales,
      camasDobles: tipo.camasDobles,
      disponibleEn: Array.from(hotelesUnicos.values()),
    };

    res.status(200).json(tipoFormateado);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener el tipo de habitación' });
  }
});

export default router;
