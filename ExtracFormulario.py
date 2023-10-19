import json
import os

# Directorio que contiene los archivos JSON
directorio_json = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Json'

# Lista de nombres de archivos JSON en el directorio que contienen "formulario" en su nombre
archivos_json = [archivo for archivo in os.listdir(directorio_json) if archivo.endswith('.json') and ("formulario" in archivo.lower())]

# Definir una función para extraer la información de un archivo JSON
def extraer_informacion(archivo_json):
    try:
        with open(os.path.join(directorio_json, archivo_json), 'r', encoding='utf-8') as archivo_json:
            data = json.load(archivo_json)

        # Variables para controlar la extracción de datos
        extrayendo = False
        textos_extraidos = []

        for obj in data:
            if "text" in obj:
                texto = obj["text"].upper()  # Convertir el texto a mayúsculas para la búsqueda
                if "INFORMACIÓN" in texto:
                    extrayendo = True
                if extrayendo:
                    textos_extraidos.append(obj["text"])
                if "FAMILIAR" in texto:
                    extrayendo = False

        # Crear un diccionario para almacenar los resultados
        resultados = {"textos_extraidos": textos_extraidos}

        return resultados
    except Exception as e:
        return {"error": str(e)}
    
    
# Crear la carpeta "Result" si no existe
carpeta_result = os.path.join(directorio_json, 'Result')
if not os.path.exists(carpeta_result):
    os.makedirs(carpeta_result)

# Procesar cada archivo JSON y guardar los resultados en la carpeta "Result"
for archivo_json in archivos_json:
    resultados = extraer_informacion(archivo_json)
    
    if resultados is not None:  # Verificar si se extrajo información
        nombre_resultado = os.path.splitext(archivo_json)[0] + '_Formulario.json'
        ruta_resultado = os.path.join(carpeta_result, nombre_resultado)
        
        with open(ruta_resultado, "w", encoding='utf-8') as archivo_resultado:
            json.dump(resultados, archivo_resultado, indent=4, ensure_ascii=False)

        print(f"Los textos extraídos del archivo '{archivo_json}' se han guardado en '{ruta_resultado}'")
    else:
        print(f"El archivo '{archivo_json}' no cumple con el criterio y no se procesó.")
