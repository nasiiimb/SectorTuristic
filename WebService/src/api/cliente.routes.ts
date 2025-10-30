import { Router } from 'express';
import prisma from '../config/prisma';
import { asyncHandler, NotFoundError } from '../middleware/errorHandler';

const router = Router();

// Obtener todos los clientes
router.get('/', asyncHandler(async (req, res) => {
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
}));

// Obtener un cliente por ID
router.get('/:id', asyncHandler(async (req, res) => {
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
    throw new NotFoundError('Cliente');
  }

  res.status(200).json(cliente);
}));

// Crear un nuevo cliente
router.post('/', asyncHandler(async (req, res) => {
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
}));

// Actualizar un cliente
router.put('/:id', asyncHandler(async (req, res) => {
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
}));

export default router;
