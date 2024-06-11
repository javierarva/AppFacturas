from fpdf import FPDF
from db.connection import connector
import os

conexion = connector()
cursor = conexion.cursor()

def obtener_factura(cursor, id_cliente):
    cursor.execute("SELECT * FROM cabecera WHERE ClienteID = %s", (id_cliente,))
    return cursor.fetchone()

def obtener_cliente(cursor, id_cliente):
    cursor.execute("SELECT * FROM cliente WHERE ClienteID = %s", (id_cliente,))
    return cursor.fetchone()

def obtener_productos(cursor, id_factura):
    cursor.execute("SELECT * FROM producto WHERE ProductoID IN (SELECT ProductoID FROM linea WHERE CabeceraID = %s)", (id_factura,))
    return cursor.fetchall()

def obtener_detalles_factura(cursor, id_factura):
    cursor.execute("SELECT * FROM linea WHERE CabeceraID = %s", (id_factura,))
    return cursor.fetchall()

def crear_pdf_factura(invoice, client, products, details):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Factura', 0, 1, 'C')

    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Factura ID: {invoice["CabeceraID"]}', 0, 1)
    pdf.cell(0, 10, f'Fecha: {invoice["Fecha"]}', 0, 1)
    pdf.cell(0, 10, f'Cliente: {client["Nombre"]}', 0, 1)
    pdf.cell(0, 10, f'Dirección: {client["Direccion"]}', 0, 1)

    pdf.ln(10)

    pdf.set_font('Arial', 'B', 10)
    pdf.cell(80, 10, 'Producto', 1)
    pdf.cell(30, 10, 'Cantidad', 1)
    pdf.cell(30, 10, 'Precio Unitario', 1)
    pdf.cell(30, 10, 'Total', 1)
    pdf.ln()

    total_factura = 0
    for detail in details:
        product = next(p for p in products if p['ProductoID'] == detail['ProductoID'])
        total_producto = detail['Cantidad'] * detail['PrecioUnitario']
        total_factura += total_producto

        pdf.cell(80, 10, product['Descripcion'], 1)
        pdf.cell(30, 10, str(detail['Cantidad']), 1)
        pdf.cell(30, 10, f"{detail['PrecioUnitario']:.2f}", 1)
        pdf.cell(30, 10, f"{total_producto:.2f}", 1)
        pdf.ln()

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(140, 10, 'Total Factura', 1)
    pdf.cell(30, 10, f"{total_factura:.2f}", 1)

    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'invoices')
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f'factura_{client["Nombre"].replace(" ", "_")}.pdf')
    pdf.output(output_file)
    print(f"Factura generada con éxito: {output_file}")