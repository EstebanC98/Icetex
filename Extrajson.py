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

        tiene_republica = False
        tiene_numero = False

        for obj in data:
            if "text" in obj:
                texto = obj["text"].strip().lower()

                # Elimina las tildes de "REPUBLICA" y "NUMERO"
                texto_sin_tildes = unidecode(texto)

                if texto_sin_tildes == "republica":
                    tiene_republica = True
                elif texto_sin_tildes == "numero":
                    tiene_numero = True

        return tiene_republica and tiene_numero

    except Exception as e:
        return False

# Definir una función para extraer la información de un archivo JSON
def cedula_vieja_completa(archivo_json):
    try:
        with open(os.path.join(directorio_json, archivo_json), 'r', encoding='utf-8') as archivo_json:
            data = json.load(archivo_json)

        # Crear un diccionario para almacenar la información extraída
        resultados = {}

        # Recorrer todos los objetos en la data
        i = 0
        while i < len(data):
            obj = data[i]
            if "text" in obj:
                texto = obj["text"].lower()  # Convertir el texto a minúsculas para la búsqueda

                # Comprobar si el texto coincide con un caso y llamar a la función correspondiente
                if "ciudadania" in texto:
                    resultados["Cedula"] = encontrar_primer_numero(data, i + 1)
                    # Detener la búsqueda cuando se encuentra "apellidos"
                    while i < len(data) and "apellidos" not in data[i]["text"].lower():
                        i += 1
                elif "nombre" in texto:
                    data_nombre = " ".join(data[j]["text"] for j in range(max(0, i - 2), i))
                    resultados["Nombre"] = data_nombre.strip()
                    i += 1  # Avanzar un paso después de nombre
                elif "apellido" in texto:
                    data_apellido = " ".join(data[j]["text"] for j in range(max(0, i - 2), i))
                    resultados["Apellido"] = data_apellido.strip()  
                    i += 1  # Avanzar un paso después de apellido
                elif "derecho" in texto:
                    resultados["Fecha de Nacimiento"] = "".join(data[j]["text"] for j in range(i + 4, i + 9))
                    i += 9  # Saltar al siguiente conjunto de datos después de fecha
                elif "sexo" in texto:
                    resultados["Fecha de Expedicion"] = "".join(data[j]["text"] for j in range(i + 1, i + 6))
                    i += 5
                else:
                    i += 1  # Avanzar un paso si no se encuentra una coincidencia
            else:
                i += 1  # Avanzar un paso si no hay "text" en el objeto

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

# Crear la carpeta "Result" si no existe
carpeta_result = os.path.join(directorio_json, 'Result')
if not os.path.exists(carpeta_result):
    os.makedirs(carpeta_result)

# Procesar cada archivo JSON y guardar los resultados en la carpeta "Result" solo si cumple con los criterios
for archivo_json in archivos_json:
    if cumple_criterios(archivo_json):
        resultados = cedula_vieja_completa(archivo_json)
        nombre_resultado = os.path.splitext(archivo_json)[0] + '_CCAntigua.json'
        ruta_resultado = os.path.join(carpeta_result, nombre_resultado)
        
        with open(ruta_resultado, "w", encoding='utf-8') as archivo_resultado:
            json.dump(resultados, archivo_resultado, indent=4, ensure_ascii=False)

        print(f"La información relevante del archivo '{archivo_json}' se ha guardado en '{ruta_resultado}'")
    else:
        print(f"El archivo '{archivo_json}' no cumple con los criterios y no se procesará.")
