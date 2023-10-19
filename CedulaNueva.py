import json
import os
from unidecode import unidecode

# Directorio que contiene los archivos JSON
directorio_json = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Json'

# Lista de nombres de archivos JSON en el directorio que no contienen "Formulario" en su nombre
archivos_json = [archivo for archivo in os.listdir(directorio_json) if archivo.endswith('.json') and "Formulario" not in archivo]

def cumple_criterios(archivo_json):
    try:
        with open(os.path.join(directorio_json, archivo_json), 'r', encoding='utf-8') as archivo_json:
            data = json.load(archivo_json)

        tiene_cedula = False
        tiene_nuip = False

        for obj in data:
            if "text" in obj:
                texto = obj["text"].strip().lower()

                # Elimina las tildes de "CEDULA" y ".CO"
                texto_sin_tildes = unidecode(texto)

                if texto_sin_tildes == "cedula":
                    tiene_cedula = True
                elif texto_sin_tildes == "nuip":
                    tiene_nuip = True

        return tiene_cedula and tiene_nuip

    except Exception as e:
        return False

# Definir una función para extraer la información de un archivo JSON
def cedula_nueva_completa(archivo_json):
    try:
        with open(os.path.join(directorio_json, archivo_json), 'r', encoding='utf-8') as archivo_json:
            data = json.load(archivo_json)

        resultados = {}
        i = 0

        while i < len(data):
            obj = data[i]

            if "text" in obj:
                texto = unidecode(obj["text"].strip().lower())

                if texto == "nuip":
                    resultados["Cedula"] = encontrar_primer_numero(data, i + 1)
                elif texto == "apellidos":
                    # Extraer todo entre "apellidos" y "nombres"
                    resultados["Apellido"] = extraer_texto_entre_palabras_clave(data, "apellidos", "nombres", i)
                    i += 1  # Avanzar después de "apellidos"
                elif texto == "nombres":
                    # Extraer todo entre "nombres" y "nacionalidad"
                    resultados["Nombre"] = extraer_texto_entre_palabras_clave(data, "nombres", "nacionalidad", i)
                    i += 1  # Avanzar después de "nombres"
                elif texto == "col" and i + 4 < len(data):
                    resultados["Fecha de Nacimiento"] = " ".join(data[j]["text"] for j in range(i + 4, i + 7))
                    i += 3
                elif texto == "expedicion" and i + 4 < len(data):
                    resultados["Fecha de Expedicion"] = " ".join(data[j]["text"] for j in range(i + 1, i + 4))
                    i += 3

            i += 1

        return resultados

    except Exception as e:
        return {"error": str(e)}

def encontrar_primer_numero(data, start_index):
    # Buscar el primer índice que contenga un número en el texto
    for i in range(start_index, len(data)):
        obj = data[i]
        if "text" in obj:
            texto = obj["text"]
            # Verificar si el texto contiene un número
            if any(char.isdigit() for char in texto):
                return texto
    return ""

def extraer_texto_entre_palabras_clave(data, palabra_clave_inicio, palabra_clave_fin, indice_inicio):
    texto_extraido = []
    i = indice_inicio  # Empezar después de la palabra clave de inicio

    # Buscar el inicio de la sección
    while i < len(data):
        obj = data[i]
        if "text" in obj:
            texto = obj["text"].strip().lower()
            if texto == palabra_clave_inicio:
                break
        i += 1

    # Verificar si se encontró la palabra clave de inicio
    if i >= len(data):
        return None

    # Continuar buscando hasta encontrar el final de la sección
    i += 1
    while i < len(data):
        obj = data[i]
        if "text" in obj:
            texto = obj["text"].strip().lower()
            if texto == palabra_clave_fin:
                break
            texto_extraido.append(obj["text"])
        i += 1

    return " ".join(texto_extraido)

   
# Crear la carpeta "Result" si no existe
carpeta_result = os.path.join(directorio_json, 'Result')
if not os.path.exists(carpeta_result):
    os.makedirs(carpeta_result)

# Procesar cada archivo JSON y guardar los resultados en la carpeta "Result" solo si cumple con los criterios
for archivo_json in archivos_json:
    if cumple_criterios(archivo_json):
        resultados = cedula_nueva_completa(archivo_json)
        nombre_resultado = os.path.splitext(archivo_json)[0] + '_CCNueva.json'
        ruta_resultado = os.path.join(carpeta_result, nombre_resultado)
        
        with open(ruta_resultado, "w", encoding='utf-8') as archivo_resultado:
            json.dump(resultados, archivo_resultado, indent=4, ensure_ascii=False)

        print(f"La información relevante del archivo '{archivo_json}' se ha guardado en '{ruta_resultado}'")
    else:
        print(f"El archivo '{archivo_json}' no cumple con los criterios y no se procesará.")
