import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// GET /regimenes - Obtener todos los regímenes disponibles
router.get('/', async (req, res) => {
  try {
    const regimenes = await prisma.regimen.findMany({
      include: {
        preciosRegimen: {
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

    // Formatear respuesta para que sea más legible
    const regimenesFormateados = regimenes.map((regimen) => ({
      codigo: regimen.codigo,
      idRegimen: regimen.idRegimen,
      disponibleEn: regimen.preciosRegimen.map((pr) => ({
        hotel: pr.hotel.nombre,
        ciudad: pr.hotel.ciudad.nombre,
        precio: parseFloat(pr.precio.toString()),
      })),
    }));

    res.status(200).json(regimenesFormateados);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener los regímenes' });
  }
});

// GET /regimenes/:codigo - Obtener un régimen específico
router.get('/:codigo', async (req, res) => {
  try {
    const { codigo } = req.params;

    const regimen = await prisma.regimen.findFirst({
      where: {
        codigo: codigo,
      },
      include: {
        preciosRegimen: {
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

    if (!regimen) {
      return res.status(404).json({
        message: `No se encontró ningún régimen con el código "${codigo}"`,
      });
    }

    const regimenFormateado = {
      codigo: regimen.codigo,
      idRegimen: regimen.idRegimen,
      disponibleEn: regimen.preciosRegimen.map((pr) => ({
        hotel: pr.hotel.nombre,
        ciudad: pr.hotel.ciudad.nombre,
        precio: parseFloat(pr.precio.toString()),
      })),
    };

    res.status(200).json(regimenFormateado);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener el régimen' });
  }
});

export default router;
