from db.connection import connector
from datetime import datetime

conexion = connector()
cursor = conexion.cursor()

def generar_numero_factura(cursor):
    try:
        cursor.execute("SELECT NumeroFactura FROM Cabecera ORDER BY CabeceraID DESC LIMIT 1")
        ultimo_numero = cursor.fetchone()
        if ultimo_numero:
            ultimo_numero = int(ultimo_numero[0][1:])
            nuevo_numero = ultimo_numero + 1
        else:
            nuevo_numero = 1
        return f"F{nuevo_numero:04d}"
    except Exception as e:
        print(f"\nError al generar el número de factura: {e}")

def insertar_factura(cursor, conexion):
    try:
        numero_factura = generar_numero_factura(cursor)
        fecha = datetime.today().strftime('%Y-%m-%d')
        empresa_id = int(input("\nIngrese el ID de la empresa: "))
        cliente_id = int(input("Ingrese el ID del cliente: "))
        direccion_envio_id = int(input("Ingrese el ID de la dirección de envío: "))
        banco_id = int(input("Ingrese el ID del banco: "))
        iva_percent = float(input("Ingrese el porcentaje de IVA (ej. 21 para 21%): ")) / 100
    except ValueError as e:
        print(f"\nEntrada inválida: {e}")

    try:
        cursor.execute("SELECT Nombre, Direccion, Telefono, Email FROM Empresa WHERE EmpresaID = %s", (empresa_id,))
        empresa = cursor.fetchone()

        cursor.execute("SELECT CodigoCliente, NIF_NIE, Nombre, Apellido, Direccion, Telefono, Email FROM Cliente WHERE ClienteID = %s", (cliente_id,))
        cliente = cursor.fetchone()

        cursor.execute("SELECT Calle, Numero, Ciudad, ProvinciaID, CodigoPostalID FROM DireccionEnvio WHERE DireccionEnvioID = %s", (direccion_envio_id,))
        direccion_envio = cursor.fetchone()

        cursor.execute("SELECT Nombre FROM Provincia WHERE ProvinciaID = %s", (direccion_envio[3],))
        provincia = cursor.fetchone()[0]

        cursor.execute("SELECT Codigo FROM CodigoPostal WHERE CodigoPostalID = %s", (direccion_envio[4],))
        codigo_postal = cursor.fetchone()[0]

        cursor.execute("SELECT Nombre, NumeroCuenta, Sucursal FROM Banco WHERE BancoID = %s", (banco_id,))
        banco = cursor.fetchone()
    except Exception as e:
        print(f"\nError al obtener datos de la base de datos: {e}")

    try:
        add_cabecera = ("INSERT INTO Cabecera "
                        "(NumeroFactura, Fecha, EmpresaNombre, EmpresaDireccion, EmpresaTelefono, EmpresaEmail, "
                        "ClienteCodigoCliente, ClienteNIF_NIE, ClienteNombre, ClienteApellido, ClienteDireccion, ClienteTelefono, ClienteEmail, "
                        "DireccionEnvioCalle, DireccionEnvioNumero, DireccionEnvioCiudad, DireccionEnvioProvincia, DireccionEnvioCodigoPostal, "
                        "BancoNombre, BancoNumeroCuenta, BancoSucursal) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        data_cabecera = (numero_factura, fecha, empresa[0], empresa[1], empresa[2], empresa[3], 
                         cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5], cliente[6],
                         direccion_envio[0], direccion_envio[1], direccion_envio[2], provincia, codigo_postal,
                         banco[0], banco[1], banco[2])

        cursor.execute(add_cabecera, data_cabecera)
        conexion.commit()
        cabecera_id = cursor.lastrowid

        print(f"\nRegistro insertado en la tabla Cabecera con Número de Factura: {numero_factura}")
    except Exception as e:
        print(f"\nError al insertar datos en la tabla Cabecera: {e}")
        conexion.rollback()
        
    try:
        total = 0
        producto_id = int(input("\nIngrese el ID del producto: "))
        cantidad = int(input("Ingrese la cantidad: "))
    except ValueError as e:
        print(f"\nEntrada inválida: {e}")

    try:
        cursor.execute("SELECT Precio FROM Producto WHERE ProductoID = %s", (producto_id,))
        producto = cursor.fetchone()
        
        if producto:
            precio_unitario = producto[0]
            subtotal = cantidad * precio_unitario
            total += subtotal

            add_linea = ("INSERT INTO Linea (NumeroFactura, CabeceraID, ProductoID, Cantidad, PrecioUnitario, Subtotal) "
                         "VALUES (%s, %s, %s, %s, %s, %s)")
            data_linea = (numero_factura, cabecera_id, producto_id, cantidad, precio_unitario, subtotal)

            cursor.execute(add_linea, data_linea)
            conexion.commit()

            print("\nRegistro insertado en la tabla Linea.")
        else:
            print(f"\nNo se encontró ningún producto con ID {producto_id}. Inténtelo de nuevo.")
    except Exception as e:
        print(f"\nError al insertar datos en la tabla Linea: {e}")
        conexion.rollback()

    try:
        iva = total * iva_percent
        update_cabecera = ("UPDATE Cabecera SET Total = %s, IVA = %s WHERE CabeceraID = %s")
        cursor.execute(update_cabecera, (total, iva, cabecera_id))
        conexion.commit()

    except Exception as e:
        print(f"\nError al actualizar la tabla Cabecera: {e}")
        conexion.rollback()