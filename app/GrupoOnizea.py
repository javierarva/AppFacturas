import mysql.connector
import os
from alta import alta
from baja import baja
from modificar import modificar
from consulta import consulta

def obtener_datos(tabla):
    try:
        mybasedatos = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="factura2.0"
        )
        cursor = mybasedatos.cursor()
        
        # Ejecutar la consulta para obtener los datos de la tabla
        cursor.execute(f"SELECT * FROM {tabla};")
        registros = cursor.fetchall()
        
        # Obtener los nombres de las columnas
        cursor.execute(f"SHOW COLUMNS FROM {tabla};")
        columnas = cursor.fetchall()
        
        # Mostrar los nombres de las columnas
        print(f"Datos de la tabla '{tabla}':")
        nombres_columnas = [columna[0] for columna in columnas]
        print("\t".join(nombres_columnas))
        
        # Mostrar los registros
        for registro in registros:
            print("\t".join(map(str, registro)))
        
        # Cerrar la conexión
        cursor.close()
        mybasedatos.close()
    except mysql.connector.Error as err:
        print("Error al conectar a la base de datos:", err)

def mostrar_tablas():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
    print("Menú de tablas")
    print("1. Empresa")
    print("2. Cliente")
    print("3. Producto")
    print("4. Cabecera")
    print("5. Lineas")
    print("6. DireccionEnvio")
    print("7. Provincias")
    print("8.CodigoPostal ")
    print("9. Bancos")
    print("10. salir")

def menu_crud(tabla):
    while True:
        print(f"Menú de operaciones para la tabla '{tabla}':")
        print("1. Alta")
        print("2. Baja")
        print("3. Modificar")
        print("4. Consulta")
        print("5. Volver al menú principal")
        opcion = input("Selecciona una opción (1-5): ")
        
        if opcion == '1':
            alta(tabla)
        elif opcion == '2':
            baja(tabla)
        elif opcion == '3':
            modificar(tabla)
        elif opcion == '4':
            consulta(tabla)
        elif opcion == '5':
            break  # Salir del menú CRUD y volver al menú principal
        else:
            print("Opción no válida, por favor selecciona un número entre 1 y 5.")
        print()  # Línea en blanco para mejorar la legibilidad

def opcion_tabla(tabla):
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
    obtener_datos(tabla)
    menu_crud(tabla)

def mostrar_menu():
    print("Menú Principal")
    print("1. Tablas")
    print("2. Factura")
    print("3. Impresión")
    print("4. Listado")
    print("5. Salir")

def mostrar_menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla antes de mostrar el menú
        mostrar_menu()
        opcion = input("Selecciona una opción (1-5): ")

        if opcion == '1':
            mostrar_tablas()
            opcion_tablas = input("Selecciona una tabla (1-10): ")
            if opcion_tablas == '1':
                opcion_tabla("Empresa")
            elif opcion_tablas == '2':
                opcion_tabla("Cliente")
            elif opcion_tablas == '3':
                opcion_tabla("Producto")
            elif opcion_tablas == '4':
                opcion_tabla("Cabecera")
            elif opcion_tablas == '5':
                opcion_tabla("Lineas")
            elif opcion_tablas == '6':
                opcion_tabla("DireccionEnvio")
            elif opcion_tablas == '7':
                opcion_tabla("Provincias")
            elif opcion_tablas == '8':
                opcion_tabla("CodigoPostal")
            elif opcion_tablas == '9':
                opcion_tabla("Bancos")
            elif opcion_tablas == '10':
                continue  # Volver al menú principal
            else:
                print("Opción no válida, por favor selecciona un número entre 1 y 10.")
        elif opcion == '2':
            opcion_factura()
        elif opcion == '3':
            opcion_impresion()
        elif opcion == '4':
            opcion_listado()
        elif opcion == '5':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida, por favor selecciona un número entre 1 y 5.")

        input("Presiona Enter para continuar...")  # Pausar antes de volver al menú principal

def opcion_factura():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
    print("Has seleccionado la opción Factura.")

def opcion_impresion():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
    print("Has seleccionado la opción Impresión.")

def opcion_listado():
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
    print("Has seleccionado la opción Listado.")

def main():
    mostrar_menu_principal()

if __name__ == "__main__":
    main()