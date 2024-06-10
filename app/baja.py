import mysql.connector
import os
def baja(tabla):
    print(f"Has seleccionado 'Baja' en la tabla '{tabla}'.")
    id_registro = input("Introduce el ID del registro que deseas eliminar: ")

    try:
        mybasedatos = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Facturacion"
        )
        cursor = mybasedatos.cursor()

        # Crear la consulta de eliminación
        consulta = f"DELETE FROM {tabla} WHERE id = %s"

        # Ejecutar la consulta de eliminación
        cursor.execute(consulta, (id_registro,))
        mybasedatos.commit()
        print(f"Registro con ID {id_registro} eliminado de la tabla '{tabla}' con éxito.")

        # Cerrar la conexión
        cursor.close()
        mybasedatos.close()
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)

