import MySQLdb
import bcrypt

# Configuración de conexión a la base de datos
DB_HOST = "localhost"
DB_USER = "tmas"
DB_PASS = ""
DB_NAME = "turisme"

# Datos del usuario a insertar
email = "test@demo.com"
password = "123456"
role = "user"  # Puede ser 'admin' o 'user'

try:
    # Conexión a la base de datos
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
    cursor = db.cursor()

    # Cifrar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insertar usuario
    query = "INSERT INTO users (email, password_hash, role) VALUES (%s, %s, %s)"
    cursor.execute(query, (email, hashed_password, role))
    db.commit()

    print(f"Usuario {email} insertado correctamente.")

except MySQLdb.Error as e:
    print(f"Error en la base de datos: {e}")
finally:
    cursor.close()
    db.close()
