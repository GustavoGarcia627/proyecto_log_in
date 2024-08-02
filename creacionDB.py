import mysql.connector

class Clientes:
    def __init__(self,host,user,password,database):

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.cursor = self.conn.cursor(dictionary=True)

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
	        Usuario varchar(255) PRIMARY KEY,
	        Contraseña varchar(255) NOT NULL
            )''')
        
        self.conn.commit()
    
    def log_in(self,usuario,contraseña):
        existe = self.consultar_cliente(usuario)
        if existe == False:
            sql = "INSERT INTO clientes (Usuario, Contraseña) VALUES (%s, %s)"
            valores = (usuario, contraseña)
            self.cursor.execute(sql,valores)
            self.conn.commit()
            return self.cursor.fetchone()
        else:
            print(f'El usuario {usuario} ya existe')

    def sign_in(self,usuario,contraseña):
        existe = self.consultar_cliente(usuario)

        if existe == True:
            self.cursor.execute(f"SELECT * FROM clientes WHERE Usuario='{usuario}';")
            x =  self.cursor.fetchall()
            if x[0]['Contraseña'] == contraseña:
                print('Acceso concedido')
                return True
            else: 
                print('Acceso denegado')
                return False
        else:
            print('El usuario no existe')
            return False


    def consultar_cliente(self,usuario):
        '''
        Precondicion: Recibe el usuario (ID)
        PosCondicion: Si el usuario existe devuelve True, sino False
        '''
        self.cursor.execute(f"SELECT * FROM clientes WHERE Usuario='{usuario}';")
        x =  self.cursor.fetchall()
        if len(x)==0:
            return False
        elif x[0]['Usuario'] == usuario:
            return True
        else: 
            return False

afaClientes = Clientes("localhost","root","","basededatos")

afaClientes.sign_in("Elssa","1234")