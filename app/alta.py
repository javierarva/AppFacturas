import mysql.connector
import os
def alta(tabla):
    try:
        mybasedatos = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Facturacion"
        )
        cursor = mybasedatos.cursor()
        
        # Obtener los nombres de las columnas
        cursor.execute(f"SHOW COLUMNS FROM {tabla};")
        columnas = cursor.fetchall()
        
        # Solicitar los valores para cada columna
        valores = []
        for columna in columnas:
            valor = input(f"Introduce el valor para '{columna[0]}': ")
            valores.append(valor)
        
        # Crear la consulta de inserción
        nombres_columnas = [columna[0] for columna in columnas]
        valores_placeholder = ", ".join(["%s"] * len(columnas))
        consulta = f"INSERT INTO {tabla} ({', '.join(nombres_columnas)}) VALUES ({valores_placeholder})"
        
        # Ejecutar la consulta de inserción
        cursor.execute(consulta, valores)
        mybasedatos.commit()
        print(f"Nuevo registro en la tabla '{tabla}' registrado con éxito.")
        
        # Cerrar la conexión
        cursor.close()
        mybasedatos.close()
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)
