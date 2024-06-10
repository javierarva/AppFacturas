import mysql.connector
import os

def consulta(tabla):
    try:
        mybasedatos = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="factura2.0"
        )
        cursor = mybasedatos.cursor()

        # Mostrar los registros de la tabla
        cursor.execute(f"SELECT * FROM {tabla};")
        registros = cursor.fetchall()
        cursor.execute(f"SHOW COLUMNS FROM {tabla};")
        columnas = cursor.fetchall()
        nombres_columnas = [columna[0] for columna in columnas]

        # Mostrar los registros de la tabla con los IDs
        print(f"Datos de la tabla '{tabla}':")
        for registro in registros:
            print("\t".join(map(str, registro)))
        
        # Solicitar el ID del registro a consultar
        id_valor = input(f"Introduce el valor del ID del registro a consultar: ")

        # Crear la consulta de selección
        consulta = f"SELECT * FROM {tabla} WHERE id = %s"

        # Ejecutar la consulta de selección
        cursor.execute(consulta, (id_valor,))
        resultado = cursor.fetchone()
        if resultado:
            # Mostrar la información de la fila sin incluir el ID
            print(f"Información del registro con ID = {id_valor}:")
            for i in range(1, len(resultado)):
                print(f"{nombres_columnas[i]}: {resultado[i]}")
        else:
            print(f"No se encontró ningún registro con ID = {id_valor}")

        # Cerrar la conexión
        cursor.close()
        mybasedatos.close()
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)


