import json
import os

# Directorio que contiene los archivos JSON
directorio_json = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Json'

# Función para determinar el tipo de cédula
def determinar_tipo_cedula(data):
    if data and len(data) > 0 and "text" in data[0]:
        indice_inicial = data[0]["text"].strip().lower()
        if indice_inicial == "republica":
            return "Cedula Antigua Completa"
        elif indice_inicial == "cedula":
            return "Cedula Nueva Completa"
    return "Tipo de cédula desconocido"

# Función para extraer la información de un archivo JSON
def extraer_informacion(archivo_json):
    try:
        with open(os.path.join(directorio_json, archivo_json), 'r', encoding='utf-8') as archivo_json:
            data = json.load(archivo_json)

        # Crear un diccionario para almacenar la información extraída
        resultados = {"Cedula": "", "Nombre": "", "Apellido": "", "Fecha de Nacimiento": "", "Fecha de Expedicion": ""}
        i = 0

        while i < len(data):
            obj = data[i]
            if "text" in obj:
                texto = obj["text"].lower()
                if "apellidos" in texto:
                    resultados["Cedula"] = data[i + 3]["text"]
                    i += 6
                elif "nombre" in texto:
                    resultados["Nombre"] = " ".join(data[j]["text"] for j in range(max(0, i - 2), i)).strip()
                    i += 1
                elif "apellido" in texto:
                    resultados["Apellido"] = " ".join(data[j]["text"] for j in range(max(0, i - 2), i)).strip()
                    i += 1
                elif "derecho" in texto:
                    resultados["Fecha de Nacimiento"] = "".join(data[j]["text"] for j in range(i + 4, i + 9))
                    i += 9
                elif "sexo" in texto:
                    resultados["Fecha de Expedicion"] = "".join(data[j]["text"] for j in range(i + 1, i + 6))
                    i += 5
                else:
                    i += 1
            else:
                i += 1

        return resultados
    except Exception as e:
        return {"error": str(e)}

# Crear la carpeta "Result" si no existe
carpeta_result = os.path.join(directorio_json, 'Result')
if not os.path.exists(carpeta_result):
    os.makedirs(carpeta_result)

# Procesar cada archivo JSON y guardar los resultados en la carpeta "Result"
for archivo_json in os.listdir(directorio_json):
    if archivo_json.endswith('.json'):
        try:
            resultados = extraer_informacion(archivo_json)
            nombre_resultado = os.path.splitext(archivo_json)[0] + '_Ejemplo.json'
            ruta_resultado = os.path.join(carpeta_result, nombre_resultado)
            
            with open(ruta_resultado, "w", encoding='utf-8') as archivo_resultado:
                json.dump(resultados, archivo_resultado, indent=4, ensure_ascii=False)

            print(f"La información relevante del archivo '{archivo_json}' se ha guardado en '{ruta_resultado}'")
        except Exception as e:
            print(f"Error al procesar el archivo '{archivo_json}': {str(e)}")
