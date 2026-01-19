import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();

// Configuración del pool de conexiones MySQL
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '3306'),
  user: process.env.DB_USER || 'pms_user',
  password: process.env.DB_PASSWORD || 'pms_password123',
  database: process.env.DB_NAME || 'principal_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  charset: 'utf8mb4'
});

// Test de conexión
pool.getConnection()
  .then((connection) => {
    console.log('Conexión a MySQL establecida correctamente');
    connection.release();
  })
  .catch((err) => {
    console.error('Error al conectar con MySQL:', err.message);
  });

export default pool;
