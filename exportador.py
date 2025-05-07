import os

def guardar_proyecto_en_txt(ruta_proyecto, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(ruta_proyecto):
            for file in files:
                if file.endswith(('.py', '.html', '.css', '.js')):
                    ruta_archivo = os.path.join(root, file)
                    f.write(f'\n\n# === [ {ruta_archivo} ] ===\n\n')
                    try:
                        with open(ruta_archivo, 'r', encoding='utf-8') as code_file:
                            contenido = code_file.read()
                            f.write(contenido)
                    except Exception as e:
                        f.write(f'[ERROR al leer archivo: {e}]\n')

# Cambia esta ruta a la carpeta raíz de tu proyecto
ruta = r"C:\Users\mateo\OneDrive\Desktop\Cannabia Gem\mi_cultivo_app"
salida = "proyecto_cannabia.txt"

guardar_proyecto_en_txt(ruta, salida)
