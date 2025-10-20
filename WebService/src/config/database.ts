import mysql from 'mysql2/promise';

// Creamos un "pool" de conexiones con los datos directamente en el código.
export const pool = mysql.createPool({
  host: 'localhost',
  user: 'pms_user',
  password: 'pms_password123',
  database: 'pms_database',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});