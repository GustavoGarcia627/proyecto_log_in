from flask import Flask, request, jsonify, render_template, redirect, url_for
from user import User  # Asegúrate de que esta clase esté correctamente definida
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)  # Esto habilitará CORS para todas las rutas
app.secret_key = 'your_secret_key'
CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app, resources={r"/signin": {"origins": "*"}})



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

class Clientes(UserMixin):
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
            User_id INT AUTO_INCREMENT PRIMARY KEY,
            Usuario VARCHAR(255) NOT NULL,
            Contraseña VARCHAR(255) NOT NULL
        )''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM clientes WHERE Usuario = %s", (user_id,))
        return self.cursor.fetchone()

    def log_in(self, usuario, contraseña):
        if not self.consultar_cliente(usuario):
            sql = "INSERT INTO clientes (Usuario, Contraseña) VALUES (%s, %s)"
            contraseña_encriptada = generate_password_hash(contraseña)
            valores = (usuario, contraseña_encriptada)
            self.cursor.execute(sql, valores)
            self.conn.commit()
            return jsonify({"mensaje": "Cliente agregado correctamente."})
        else:
            return jsonify({"mensaje": "El usuario ya existe."})

    def sign_in(self, usuario, contraseña):
        if self.consultar_cliente(usuario):
            self.cursor.execute("SELECT * FROM clientes WHERE Usuario=%s;", (usuario,))
            x = self.cursor.fetchall()
            if (check_password_hash(x[0]['Contraseña'], contraseña)):
                # Asegúrate de que User sea una clase válida
                login_user(User(usuario))
                return True
            else:
                return False
        else:
            return False

    def consultar_cliente(self, usuario):
        self.cursor.execute("SELECT * FROM clientes WHERE Usuario=%s;", (usuario,))
        x = self.cursor.fetchall()
        return len(x) > 0

# Crear una instancia de la clase clientes
clientes = Clientes(host='localhost', user='root', password='', database='basededatos')

ruta_destino = './static/imagenes/'


@login_manager.user_loader
def load_user(usuario):
    return User(usuario)  # Asegúrate de que User sea una clase válida que implemente UserMixin



@app.route('/login', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        condition = clientes.sign_in(usuario, contraseña)
        if condition:
            
            return jsonify({"mensaje": "Cliente agregado correctamente."}),200
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@app.route('/protected',methods=['GET', 'POST'])
@login_required
def protected():
    return render_template('index.html')

@app.route('/profile',methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')

@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' http://127.0.0.1:5500; script-src 'self'; style-src 'self';"
    return response



if __name__ == "__main__":
    app.run(debug=True)
