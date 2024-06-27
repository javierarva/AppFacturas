from fpdf import FPDF
from db.connection import connector
import os
import datetime
from controllers.functions import pause

conexion = connector()
cursor = conexion.cursor()

def obtener_factura(cursor, id_factura):
    cursor.execute("SELECT c.*, b.Nombre AS BancoNombre, b.NumeroCuenta, b.Sucursal FROM cabecera c JOIN banco b ON c.BancoNombre = b.Nombre WHERE c.CabeceraID = %s", (id_factura,))
    return cursor.fetchone()

def obtener_productos(cursor, id_factura):
    cursor.execute("SELECT * FROM producto WHERE ProductoID IN (SELECT ProductoID FROM linea WHERE CabeceraID = %s)", (id_factura,))
    return cursor.fetchall()

def obtener_detalles_factura(cursor, id_factura):
    cursor.execute("SELECT * FROM linea WHERE CabeceraID = %s", (id_factura,))
    return cursor.fetchall()

def crear_pdf_factura(invoice, products, details):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Factura', 0, 1, 'C')

    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Factura ID: {invoice["CabeceraID"]}', 0, 1)
    pdf.cell(0, 10, f'Número de Factura: {invoice["NumeroFactura"]}', 0, 1)
    pdf.cell(0, 10, f'Fecha: {invoice["Fecha"]}', 0, 1)
    pdf.cell(0, 10, f'Cliente: {invoice["ClienteNombre"]} {invoice["ClienteApellido"]}', 0, 1)
    pdf.cell(0, 10, f'Código Cliente: {invoice["ClienteCodigoCliente"]}', 0, 1)
    pdf.cell(0, 10, f'NIF/NIE: {invoice["ClienteNIF_NIE"]}', 0, 1)
    pdf.cell(0, 10, f'Dirección: {invoice["ClienteDireccion"]}', 0, 1)

    pdf.ln(10)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(80, 10, 'Producto', 1)
    pdf.cell(30, 10, 'Cantidad', 1)
    pdf.cell(30, 10, 'Precio Unitario', 1)
    pdf.cell(30, 10, 'Total', 1)
    pdf.ln()

    subtotal_factura = 0
    for detail in details:
        product = next((p for p in products if p['ProductoID'] == detail['ProductoID']), None)
        if product:
            total_producto = detail['Cantidad'] * detail['PrecioUnitario']
            subtotal_factura += total_producto

            pdf.cell(80, 10, product['Nombre'], 1)
            pdf.cell(30, 10, str(detail['Cantidad']), 1)
            pdf.cell(30, 10, f"{detail['PrecioUnitario']:.2f}", 1)
            pdf.cell(30, 10, f"{total_producto:.2f}", 1)
            pdf.ln()

    pdf.ln(10)

    iva = invoice['IVA']
    total_iva = subtotal_factura * (iva / 100)
    total_factura = subtotal_factura + total_iva

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(140, 10, 'Subtotal', 1)
    pdf.cell(30, 10, f"{subtotal_factura:.2f}", 1)
    pdf.ln()

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(140, 10, f'IVA ({iva}%)', 1)
    pdf.cell(30, 10, f"{total_iva:.2f}", 1)
    pdf.ln()

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(140, 10, 'Total Factura', 1)
    pdf.cell(30, 10, f"{total_factura:.2f}", 1)

    pdf.ln(10)

    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Nombre del Banco: {invoice["BancoNombre"]}', 0, 1)
    pdf.cell(0, 10, f'Número de Cuenta: {invoice["NumeroCuenta"]}', 0, 1)
    pdf.cell(0, 10, f'Sucursal: {invoice["Sucursal"]}', 0, 1)

    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'invoices')
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    client_name_cleaned = invoice["ClienteNombre"].replace(" ", "_")
    output_file = os.path.join(output_dir, f'factura_{client_name_cleaned}_{timestamp}.pdf')

    pdf.output(output_file)
    print(f"Factura generada con éxito: {output_file}")

def crear_impresion():
    cursor = conexion.cursor(dictionary=True)

    while True:
        try:
            id_factura = int(input("\nIngrese el ID de la factura que desea imprimir: "))
            
            invoice = obtener_factura(cursor, id_factura)
            if not invoice:
                raise ValueError(f"No se encontró ninguna factura con ID {id_factura}")
            
            products = obtener_productos(cursor, invoice['CabeceraID'])
            if not products:
                raise ValueError("No se encontraron productos para esta factura")

            details = obtener_detalles_factura(cursor, invoice['CabeceraID'])
            if not details:
                raise ValueError("No se encontraron detalles de factura para esta factura")

            crear_pdf_factura(invoice, products, details)

            pause()
            break

        except ValueError as e:
            print(f"\nPor favor, intente de nuevo con una ID válida.")
            pause()
            break

        except Exception as e:
            print(f"\nError inesperado: {e}")
            pause()
            break