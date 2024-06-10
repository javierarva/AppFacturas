import mysql.connector
import os
def modificar(tabla):
    try:
        mybasedatos = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="factura2.0"
        )
        cursor = mybasedatos.cursor()

        # Mostrar los registros de la tabla para que el usuario seleccione uno
        cursor.execute(f"SELECT * FROM {tabla};")
        registros = cursor.fetchall()
        cursor.execute(f"SHOW COLUMNS FROM {tabla};")
        columnas = cursor.fetchall()
        nombres_columnas = [columna[0] for columna in columnas]

        print(f"Datos de la tabla '{tabla}':")
        for registro in registros:
            print("\t".join(map(str, registro)))

        # Solicitar el ID del registro a modificar
        id_columna = nombres_columnas[0]
        id_valor = input(f"Introduce el valor del ID del registro a modificar ({id_columna}): ")

        # Mostrar las opciones de campos para modificar
        print("Campos disponibles para modificar:")
        for i, columna in enumerate(nombres_columnas[1:], 1):
            print(f"{i}. {columna}")

        # Solicitar la selección del campo a modificar
        opcion_campo = input("Selecciona el número del campo a modificar: ")
        if not opcion_campo.isdigit() or not (1 <= int(opcion_campo) <= len(nombres_columnas) - 1):
            print("Selección no válida.")
            return
        
        campo = nombres_columnas[int(opcion_campo)]
        nuevo_valor = input(f"Introduce el nuevo valor para '{campo}': ")

        # Crear la consulta de actualización
        consulta = f"UPDATE {tabla} SET {campo} = %s WHERE {id_columna} = %s"

        # Ejecutar la consulta de actualización
        cursor.execute(consulta, (nuevo_valor, id_valor))
        mybasedatos.commit()
        print(f"Registro en la tabla '{tabla}' modificado con éxito.")

        # Cerrar la conexión
        cursor.close()
        mybasedatos.close()
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)


