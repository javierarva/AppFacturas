import os
from db.connection import *
from db.queries import *
from controllers.functions import *
from controllers.print import *

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPresiona Enter para continuar...")

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

def factura(conexion):
    while True:
        clear_terminal()
        check_connection(conexion)
        
        print("\nGenerar factura en Cabecera o Línea:")
        print("1. Cabecera")
        print("2. Linea")
        print("3. Salir al menú anterior")

        opcion = input("\nElige una opción: ").strip()

        try:
            if opcion == "1":
                crear(conexion, "Cabecera")
            elif opcion == "2":
                crear(conexion, "Linea")
            elif opcion == "3":
                if confirmar("\n¿Estás seguro de que deseas volver al menú anterior? "):
                    break
            else:
                print("Opción no válida. Por favor, seleccione una opción del menú.")
        except Error as e:
            print(f"Error al ejecutar la operación {opcion} en la tabla: {e}")
        
def impresion(conexion):
    clear_terminal()
    check_connection(conexion)
    
    cursor = conexion.cursor(dictionary=True)

    id_factura = int(input("Ingrese el ID de la factura que desea imprimir: "))

    try:
        invoice = obtener_factura(cursor, id_factura)
        if not invoice:
            raise ValueError(f"No se encontró ninguna factura con ID {id_factura}")

        client = obtener_cliente(cursor, invoice['ClienteID'])
        if not client:
            raise ValueError(f"No se encontró ningún cliente con el ID {invoice['ClienteID']}")
        
        products = obtener_productos(cursor, invoice['CabeceraID'])
        if not products:
            raise ValueError("No se encontraron productos para esta factura")

        details = obtener_detalles_factura(cursor, invoice['CabeceraID'])
        if not details:
            raise ValueError("No se encontraron detalles de factura para esta factura")

        crear_pdf_factura(invoice, client, products, details)
    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conexion.close()

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

        if opcion in opciones:
            try:
                opciones[opcion](conexion, tabla)
                if opcion == "2":
                    pause()
            except Error as e:
                print(f"Error al ejecutar la operación {opcion} en la tabla {tabla}: {e}")
        elif opcion == "5":
            if confirmar("\n¿Estás seguro de que deseas volver al menú anterior? "):
                break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")

def menu():
    while True:
        clear_terminal()
        try:
            check_connection(conexion)
        except Error as e:
            print(f"Error de conexión: {e}")
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
                print(f"Error al ejecutar la opción {opcion}: {e}")
        elif opcion == "5":
            if confirmar("\n¿Estás seguro de que deseas salir? "):
                break
        else:
            print("\nOpción no válida, por favor elige de nuevo.")
 
    if conexion:
        conexion.close()

if __name__ == "__main__":
    menu()
