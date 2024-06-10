import mysql.connector
from mysql.connector import Error

def connector():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='Facturacion'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"\nError al conectar a la base de datos: {e}")
    return None