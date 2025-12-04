from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from src.utils.config_manager import load_settings
import io
import os

def generar_receta_pdf(doctor_nombre, paciente_nombre, fecha, diagnostico, medicamentos):
    """
    Genera un archivo PDF en memoria con la receta médica.
    Retorna un objeto BytesIO.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Cargar configuración
    settings = load_settings()

    # --- Cabecera ---
    # Logo
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        try:
            logo = ImageReader(logo_path)
            # Dibujar logo (x, y, width, height)
            c.drawImage(logo, 50, height - 100, width=100, height=50, mask='auto')
        except Exception as e:
            print(f"Error cargando logo: {e}")

    # Info Clínica
    c.setFont("Helvetica-Bold", 16)
    c.drawString(170, height - 60, settings.get("nombre_clinica", "DentalGuard Clinic"))
    c.setFont("Helvetica", 10)
    c.drawString(170, height - 75, settings.get("slogan", "Especialistas en Sonrisas"))
    c.drawString(170, height - 87, settings.get("direccion", "Av. Salud 123"))
    c.drawString(170, height - 99, f"Tel: {settings.get('telefono', '')}")
    
    c.line(50, height - 110, width - 50, height - 110)

    # --- Datos del Doctor y Paciente ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 150, f"Dr(a). {doctor_nombre}")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 180, f"Paciente: {paciente_nombre}")
    c.drawString(400, height - 180, f"Fecha: {fecha}")

    # --- Cuerpo de la Receta ---
    y_position = height - 230
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Diagnóstico:")
    c.setFont("Helvetica", 12)
    c.drawString(150, y_position, diagnostico)
    
    y_position -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Rx / Medicamentos e Indicaciones:")
    
    y_position -= 20
    c.setFont("Helvetica", 11)
    
    # Manejo básico de líneas múltiples para medicamentos
    text_object = c.beginText(50, y_position)
    text_object.setFont("Helvetica", 11)
    
    lines = medicamentos.split('\n')
    for line in lines:
        text_object.textLine(line)
        
    c.drawText(text_object)

    # --- Pie de Página ---
    c.line(50, 100, width - 50, 100)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 80, "Este documento es una receta médica válida generada por DentalGuard ERP.")
    c.drawString(50, 65, "Firma del Doctor: __________________________")

    c.save()
    buffer.seek(0)
    return buffer
