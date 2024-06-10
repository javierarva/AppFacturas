from db.connection import connector
from db.queries import *
from controllers.functions import *

def mostrar_tablas(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        print("\nTablas en la base de datos:")
        for idx, tabla in enumerate(tablas, start=1):
            print(f"{idx}. {tabla[0]}")

        tabla_seleccionada = int(input("\nSelecciona el número de la tabla: "))
        if 1 <= tabla_seleccionada <= len(tablas):
            tabla_seleccionada = tablas[tabla_seleccionada - 1][0]
            submenu_crud(conexion, tabla_seleccionada)
        else:
            print("\nNúmero de tabla no válido.")

    except Error as e:
        print(f"Error al obtener las tablas: {e}")

def datos(conexion):
    while True:
        print("\nSubmenú Datos")
        print("1. Mostrar tablas")
        print("2. Volver al menú principal")

        opcion = input("\nElige una opción: ")
 
        if opcion == '1':
            mostrar_tablas(conexion)
        elif opcion == '2':
            break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")

def submenu_crud(conexion, tabla):
    conexion = connector()
    if conexion is None:
        print("\nNo se pudo establecer conexión con la base de datos.")
        return
    
    opciones = {
        "1": crear,
        "2": leer,
        "3": modificar,
        "4": eliminar
    }

    while True:
        print(f"\nSubmenú CRUD para {tabla}:")
        print("1. Crear registro")
        print("2. Leer registros")
        print("3. Actualizar registro")
        print("4. Eliminar registro")
        print("5. Volver al menú anterior")

        opcion = input("\nElige una opción: ").strip()

        if opcion in opciones:
            opciones[opcion](conexion, tabla)
        elif opcion == "5":
            if confirmar("\n¿Estás seguro de que deseas volver al menú anterior? "):
                break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")

def menu():
    conexion = connector()
    if conexion is None:
        print("\nNo se pudo establecer conexión con la base de datos.")
        return
 
    opciones = {
        "1": datos,
    }

    while True:
        print("\nMenú Principal")
        print("1. Datos")
        
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion in opciones:
            opciones[opcion](conexion)
        elif opcion == "5":
            if confirmar("\n¿Estás seguro de que deseas salir? "):
                break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")
 
    if conexion:
        conexion.close()

if __name__ == "__main__":
    menu()