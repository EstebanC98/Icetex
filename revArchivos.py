import os

# Ruta de la carpeta que contiene los archivos
carpeta = r'C:\Users\CLARO\Documents\ElectroNeek\Icetex\Imagenes'

# Obtén la lista de archivos en la carpeta
archivos = os.listdir(carpeta)

# Ordena los archivos alfabéticamente
archivos.sort()

# Procesa los archivos en el orden deseado
for archivo in archivos:
    # Aquí puedes realizar acciones con cada archivo, por ejemplo, imprimir su nombre
    print(archivo)
    # O abrir el archivo, leer su contenido, etc.
    # Para abrir el archivo puedes usar, por ejemplo:
    # with open(os.path.join(carpeta, archivo), 'r') as f:
    #     contenido = f.read()
