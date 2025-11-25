from flask import Flask, request, jsonify
import jwt, datetime, bcrypt
import MySQLdb
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
SECRET_KEY = "clave_super_segura"  # Usa una clave segura en producción

# Conexión MySQL usando MySQLdb
db = MySQLdb.connect(
    host="localhost",
    user="tmas",
    passwd="",
    db="turisme"
)
cursor = db.cursor()

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password'].encode('utf-8')

    cursor.execute("SELECT id, password_hash, role FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    if not user or not bcrypt.checkpw(password, user[1].encode('utf-8')):
        return jsonify({"message": "Credenciales inválidas"}), 401

    user_id, _, role = user

    # Generar token JWT
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"user_id": user_id, "role": role, "exp": exp_time}, SECRET_KEY, algorithm="HS256")

    # Guardar token en DB
    cursor.execute("INSERT INTO tokens (user_id, token, expires_at) VALUES (%s, %s, %s)",
                   (user_id, token, exp_time))
    db.commit()

    return jsonify({"token": token})

# Verificar token
@app.route('/verify', methods=['POST'])
def verify():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Token requerido"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        cursor.execute("SELECT id FROM tokens WHERE token=%s", (token,))
        token_record = cursor.fetchone()
        if not token_record:
            return jsonify({"message": "Token no registrado"}), 403
        return jsonify({"message": "Token válido", "role": decoded["role"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 403

if __name__ == '__main__':
    app.run(debug=True)  # HTTP en local
