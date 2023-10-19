import os
import fitz  # PyMuPDF
from PIL import Image

# Ruta de la carpeta que contiene los archivos PDF
carpeta_pdf = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Archivos'

# Obtén la lista de archivos PDF en la carpeta
archivos_pdf = [archivo for archivo in os.listdir(carpeta_pdf) if archivo.endswith('.pdf')]

# Ordena los archivos PDF alfabéticamente (cambiar a la lógica de orden deseada)
archivos_pdf.sort()

# Carpeta de salida para las imágenes JPEG
carpeta_salida = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Imagenes'

# Asegúrate de que la carpeta de salida exista, o créala si no existe
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Convierte cada archivo PDF a imágenes JPEG utilizando PyMuPDF (Fitz)
for archivo_pdf in archivos_pdf:
    pdf_path = os.path.join(carpeta_pdf, archivo_pdf)

    try:
        pdf_document = fitz.open(pdf_path)

        # Recorre las páginas del PDF y guarda cada página como una imagen JPEG
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            image = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [image.width, image.height], image.samples)

            nombre_salida = f'{os.path.splitext(archivo_pdf)[0]}_pagina{page_num + 1}.jpg'
            ruta_salida = os.path.join(carpeta_salida, nombre_salida)
            img.save(ruta_salida, 'JPEG')
            print(f"Saved {ruta_salida}")

        pdf_document.close()

    except Exception as e:
        print(f"Error al procesar el archivo {archivo_pdf}: {e}")
