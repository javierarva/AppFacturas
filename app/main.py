from db.connection import *
from db.queries import *
from controllers.functions import *
from controllers.print import *
from controllers.billing import *

def mostrar_tablas(conexion):
    clear_terminal()
    try:
        cursor = conexion.cursor()
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()

        tablas_excluidas = {'cabecera', 'linea'}
        tablas_filtradas = [tabla for tabla in tablas if tabla[0] not in tablas_excluidas]

        if not tablas_filtradas:
            print("\nNo hay tablas disponibles para mostrar.")
            return

        print("\nTablas en la base de datos:")
        for idx, tabla in enumerate(tablas_filtradas, start=1):
            print(f"{idx}. {tabla[0]}")

        while True:
            try:
                tabla_seleccionada = int(input("\nSelecciona el número de la tabla: "))
                if 1 <= tabla_seleccionada <= len(tablas_filtradas):
                    tabla_seleccionada = tablas_filtradas[tabla_seleccionada - 1][0]
                    submenu_crud(conexion, tabla_seleccionada)
                    break
                else:
                    print("\nNúmero de tabla no válido. Por favor, ingrese un número válido.")
            except ValueError:
                print("\nEntrada no válida. Por favor, ingrese un número.")

    except Error as e:
        print(f"Error al obtener las tablas: {e}")

def datos(conexion):
    while True:
        clear_terminal()
        print("\nSubmenú Datos")
        print("1. Mostrar tablas")
        print("2. Volver al menú principal")

        opcion = input("\nElige una opción: ")
 
        if opcion == '1':
            mostrar_tablas(conexion)
        elif opcion == '2':
            if confirmar("\n¿Estás seguro de que deseas volver al menú anterior? "):
                break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")
            pause()

def factura(conexion):
    clear_terminal()
    check_connection(conexion)

    insertar_factura(cursor, conexion)
    pause()

def impresion(conexion):
    clear_terminal()
    check_connection(conexion)

    mostrar_listado(conexion)

    crear_impresion()

def listado(conexion):
    clear_terminal()
    check_connection(conexion)
    
    mostrar_listado(conexion)
    pause()

def submenu_crud(conexion, tabla):
    while True:
        clear_terminal()

        check_connection(conexion)
        
        opciones = {
            "1": crear,
            "2": leer,
            "3": modificar,
            "4": eliminar
        }

        print(f"\nSubmenú CRUD para {tabla}:")
        print("1. Crear registro")
        print("2. Leer registros")
        print("3. Actualizar registro")
        print("4. Eliminar registro")
        print("5. Volver al menú anterior")

        opcion = input("\nElige una opción: ").strip()

        clear_terminal()

        if opcion in opciones:
            try:
                opciones[opcion](conexion, tabla)
                pause()
            except Error as e:
                print(f"\nError al ejecutar la operación {opcion} en la tabla {tabla}: {e}")
                pause()
        elif opcion == "5":
            if confirmar("\n¿Estás seguro de que deseas volver al menú anterior? "):
                break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")
            pause()

def menu():
    while True:
        clear_terminal()
        try:
            check_connection(conexion)
        except Error as e:
            print(f"\nError de conexión: {e}")
            break
 
        opciones = {
            "1": datos,
            "2": factura,
            "3": impresion,
            "4": listado,
        }

        print("\nMenú Principal")
        print("1. Datos")
        print("2. Factura")
        print("3. Impresión")
        print("4. Listado")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion in opciones:
            try:
                opciones[opcion](conexion)
            except Error as e:
                print(f"\nError al ejecutar la opción {opcion}: {e}")
                pause()
        elif opcion == "5":
            if confirmar("\n¿Estás seguro de que deseas salir? "):
                break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")
            pause()
 
    if conexion:
        conexion.close()
        cursor.close()

if __name__ == "__main__":
    menu()
