import { Router } from 'express';
import prisma from '../config/prisma';

const router = Router();

// Obtener todos los clientes
router.get('/', async (req, res) => {
  try {
    const clientes = await prisma.cliente.findMany({
      include: {
        reservasPagadas: true,
        reservasHuespedes: {
          include: {
            reserva: true,
          },
        },
      },
    });

    res.status(200).json(clientes);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener los clientes' });
  }
});

// Obtener un cliente por ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    const cliente = await prisma.cliente.findUnique({
      where: {
        idCliente: parseInt(id),
      },
      include: {
        reservasPagadas: {
          include: {
            precioRegimen: {
              include: {
                hotel: true,
                regimen: true,
              },
            },
          },
        },
        reservasHuespedes: {
          include: {
            reserva: {
              include: {
                precioRegimen: {
                  include: {
                    hotel: true,
                  },
                },
              },
            },
          },
        },
      },
    });

    if (!cliente) {
      return res.status(404).json({ message: 'Cliente no encontrado' });
    }

    res.status(200).json(cliente);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al obtener el cliente' });
  }
});

// Crear un nuevo cliente
router.post('/', async (req, res) => {
  try {
    const { nombre, apellidos, correoElectronico, fechaDeNacimiento, DNI } = req.body;

    const nuevoCliente = await prisma.cliente.create({
      data: {
        nombre,
        apellidos,
        correoElectronico,
        fechaDeNacimiento: fechaDeNacimiento ? new Date(fechaDeNacimiento) : null,
        DNI,
      },
    });

    res.status(201).json(nuevoCliente);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al crear el cliente' });
  }
});

// Actualizar un cliente
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { nombre, apellidos, correoElectronico, fechaDeNacimiento } = req.body;

    const clienteActualizado = await prisma.cliente.update({
      where: {
        idCliente: parseInt(id),
      },
      data: {
        ...(nombre && { nombre }),
        ...(apellidos && { apellidos }),
        ...(correoElectronico && { correoElectronico }),
        ...(fechaDeNacimiento && { fechaDeNacimiento: new Date(fechaDeNacimiento) }),
      },
    });

    res.status(200).json(clienteActualizado);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error en el servidor al actualizar el cliente' });
  }
});

export default router;
