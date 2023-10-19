import json
import os

# Directorio que contiene los archivos JSON
directorio_json = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Json'

# Definir una función para determinar el tipo de cédula
def determinar_tipo_cedula(data):
    if data and len(data) > 0 and "text" in data[0]:
        indice_inicial = data[0]["text"].strip().lower()
        if indice_inicial == "republica":
            return "Cedula Antigua Completa"
        elif indice_inicial == "cedula":
            return "Cedula Nueva Completa"
    return "Tipo de cédula desconocido"

# Definir una función para extraer la información de un archivo JSON
def cedula_antigua_completa(archivo_json):
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
                if "cedula" in texto:
                    resultados["Cedula"] = data[i + 3]["text"]
                    i += 6  # Saltar al siguiente conjunto de datos después de cedula
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

# Definir una función para extraer la información de un archivo JSON (Cedula Nueva Completa)
def cedula_nueva_completa(archivo_json):
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
                if "nuip" in texto:
                    resultados["Cedula"] = data[i + 1]["text"]
                    i += 6  # Saltar al siguiente conjunto de datos después de cedula
                elif "nombres" in texto:
                    data_nombre = " ".join(data[j]["text"] for j in range(max(0, i + 1), i))
                    resultados["Nombre"] = data_nombre.strip()
                    i += 1  # Avanzar un paso después de nombre
                elif "apellidos" in texto:
                    data_apellido = " ".join(data[j]["text"] for j in range(max(0, i + 1), i))
                    resultados["Apellido"] = data_apellido.strip()
                    i += 1  # Avanzar un paso después de apellido
                elif "sexo" in texto:
                    resultados["Fecha de Nacimiento"] = "".join(data[j]["text"] for j in range(i + 5, i + 8))
                    i += 9  # Saltar al siguiente conjunto de datos después de fecha
                elif "expedición" in texto:
                    resultados["Fecha de Expedicion"] = "".join(data[j]["text"] for j in range(i + 1, i + 4))
                    i += 5
                else:
                    i += 1  # Avanzar un paso si no se encuentra una coincidencia
            else:
                i += 1  # Avanzar un paso si no hay "text" en el objeto


        return resultados
    except Exception as e:
        return {"error": str(e)}

# Crear la carpeta "Result" si no existe
carpeta_result = os.path.join(directorio_json, 'Result')
if not os.path.exists(carpeta_result):
    os.makedirs(carpeta_result)

# Procesar cada archivo JSON en el directorio
for archivo_json in os.listdir(directorio_json):
    if archivo_json.endswith('.json'):
        try:
            # Construir la ruta completa del archivo
            ruta_archivo_json = os.path.join(directorio_json, archivo_json)

            # Abrir y cargar el archivo JSON
            with open(ruta_archivo_json, 'r', encoding='utf-8') as archivo_json:
                data = json.load(archivo_json)

            # Determinar el tipo de cédula
            tipo_cedula = determinar_tipo_cedula(data)

            # Procesar el archivo en función del tipo de cédula
            if tipo_cedula == "Cedula Antigua Completa":
                resultados = cedula_antigua_completa(data)
            elif tipo_cedula == "Cedula Nueva Completa":
                resultados = cedula_nueva_completa(data)
            else:
                print(f"El archivo '{archivo_json}' tiene un tipo de cédula desconocido.")

            nombre_resultado = os.path.splitext(archivo_json)[0] + '_result.json'
            ruta_resultado = os.path.join(carpeta_result, nombre_resultado)
            
            with open(ruta_resultado, "w", encoding='utf-8') as archivo_resultado:
                json.dump(resultados, archivo_resultado, indent=4, ensure_ascii=False)

            print(f"La información relevante del archivo '{archivo_json}' se ha guardado en '{ruta_resultado}'")
        except Exception as e:
            print(f"Error al procesar el archivo '{archivo_json}': {str(e)}")