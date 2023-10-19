from PIL import Image, ImageSequence
from google.cloud import vision_v1p3beta1 as vision
import os

# Ruta del archivo GIF de entrada
input_gif_path = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Login\Generate.gif'

# Ruta de la carpeta de salida para las imágenes JPG
output_image_dir = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Login\output_images'

# Ruta del archivo de texto de salida
output_txt_path = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Login\output.txt'

# Función para extraer texto de las imágenes JPG utilizando Google Cloud Vision
def extract_text_from_jpg_images(image_dir, output_txt_path):
    try:
        # Inicializa un cliente de Google Cloud Vision
        client = vision.ImageAnnotatorClient()

        # Inicializa un texto vacío
        extracted_text = ""

        # Procesa cada imagen JPG en busca de texto
        for filename in os.listdir(image_dir):
            if filename.endswith('.jpg'):
                image_path = os.path.join(image_dir, filename)
                with open(image_path, 'rb') as image_file:
                    # Lee el contenido de la imagen
                    content = image_file.read()

                # Utiliza Google Cloud Vision para extraer texto de la imagen
                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations

                if texts:
                    # El primer texto es el resultado completo
                    extracted_text += texts[0].description + "\n"

        # Guarda los datos de texto en un archivo
        with open(output_txt_path, 'w') as txt_file:
            txt_file.write(extracted_text)

        print(f"Texto extraído de las imágenes JPG y guardado en {output_txt_path} con éxito.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Llama a la función para extraer texto de las imágenes JPG
extract_text_from_jpg_images(output_image_dir, output_txt_path)
