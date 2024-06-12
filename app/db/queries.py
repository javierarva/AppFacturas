from mysql.connector import Error
from tabulate import tabulate
from controllers.functions import confirmar, valor_valido

def crear(conexion, tabla):
    try:
        cursor = conexion.cursor()

        cursor.execute(f"SHOW COLUMNS FROM {tabla}")
        columnas_info = cursor.fetchall()

        columnas = []
        tipos = []
        not_nulls = []

        for columna_info in columnas_info:
            columna = columna_info[0]
            tipo = columna_info[1]
            extra = columna_info[5]
            is_nullable = columna_info[2]

            if 'auto_increment' not in extra:
                columnas.append(columna)
                tipos.append(tipo)
                not_nulls.append(is_nullable == "NO")

        valores = []
        for columna, tipo, not_null in zip(columnas, tipos, not_nulls):
            while True:
                valor = input(f"Ingrese el valor para la columna '{columna}' (tipo {tipo}): ").strip()
                if valor_valido(valor, tipo) and (not not_null or valor):
                    valores.append(valor)
                    break
                else:
                    if not not_null and not valor:
                        valores.append('NULL')
                        break
                    print(f"Valor no válido para la columna '{columna}' (tipo {tipo}). Por favor, ingrese un valor válido.")
                    if not_null:
                        print(f"Este campo no puede estar vacío.")

        valores_str = ', '.join(["'" + valor + "'" if valor != 'NULL' else valor for valor in valores])
        columnas_str = ', '.join(columnas)
        consulta = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({valores_str})"
        cursor.execute(consulta)
        conexion.commit()

        print("\nRegistro creado exitosamente.")
    except Error as e:
        print(f"Error al crear el registro: {e}")

def leer(conexion, tabla):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {tabla}")
        registros = cursor.fetchall()
        if registros:
            headers = [i[0] for i in cursor.description]
            print(f"\nRegistros en la tabla {tabla}:")
            print(tabulate(registros, headers=headers, tablefmt="grid"))
        else:
            print(f"\nNo hay registros en la tabla {tabla}.")
    except Error as e:
        print(f"Error al leer los registros: {e}")

def modificar(conexion, tabla):
    try:
        cursor = conexion.cursor()

        leer(conexion, tabla)

        id_registro = input("\nIngrese el ID del registro que desea modificar: ").strip()

        cursor.execute(f"SHOW COLUMNS FROM {tabla}")
        columnas = [columna[0] for columna in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {tabla} WHERE {tabla}ID = %s", (id_registro,))
        registro = cursor.fetchone()

        if registro:
            print(f"\nRegistro seleccionado para modificar (ID: {id_registro}):")
            print(tabulate([registro], headers=columnas, tablefmt="grid"))
        else:
            print(f"\nNo se encontró ningún registro con ID {id_registro}.")
            return

        nuevos_valores = []
        for columna in columnas[1:]:
            nuevo_valor = input(f"Ingrese el nuevo valor para la columna '{columna}': ").strip()
            nuevos_valores.append(nuevo_valor)

        sets = ', '.join([f"{columna} = %s" for columna in columnas[1:]])
        consulta = f"UPDATE {tabla} SET {sets} WHERE {tabla}ID = %s"
        cursor.execute(consulta, nuevos_valores + [id_registro])
        conexion.commit()

        print("\nRegistro modificado exitosamente.")
    except Error as e:
        print(f"Error al modificar el registro: {e}")

def eliminar(conexion, tabla):
    try:
        cursor = conexion.cursor()

        leer(conexion, tabla)

        id_registro = input("\nIngrese el ID del registro que desea eliminar: ").strip()

        cursor.execute(f"SELECT * FROM {tabla} WHERE {tabla}ID = %s", (id_registro,))
        registro = cursor.fetchone()

        if registro:
            if confirmar("\n¿Estás seguro de que deseas eliminar este registro? "):
                cursor.execute(f"DELETE FROM {tabla} WHERE {tabla}ID = %s", (id_registro,))
                conexion.commit()
                print("\nRegistro eliminado exitosamente.")
            else:
                print("\nEliminación cancelada.")
        else:
            print(f"\nNo se encontró un registro con el ID: {id_registro}")

    except Error as e:
        print(f"Error al eliminar el registro: {e}")

def mostrar_listado(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM cabecera")
        registros = cursor.fetchall()
        if registros:
            headers = [i[0] for i in cursor.description]
            print(f"\nRegistros en la tabla cabecera:")
            print(tabulate(registros, headers=headers, tablefmt="grid"))
        else:
            print(f"\nNo hay registros en la tabla cabecera.")
    except Error as e:
        print(f"Error al leer los registros: {e}")