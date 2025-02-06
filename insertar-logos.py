import pandas as pd
import os
import re
import unicodedata

def remove_accents(input_str):
    return ''.join(
        c for c in unicodedata.normalize('NFD', input_str) if unicodedata.category(c) != 'Mn'
    )

def update_map_files(csv_path, mapas_folder, logos_folder):
    # Cargar el CSV
    df = pd.read_csv(csv_path)
    
    # Convertir la columna "Empresa" a string y manejar valores nulos
    df["Empresa"] = df["Empresa"].astype(str).fillna("").str.lower()
    
    # Crear un diccionario de stand -> empresa con espacios reemplazados por guiones y sin tildes
    stand_dict = {str(row["Nº Stand"]): remove_accents(row["Empresa"]).replace(" ", "-") + ".png" for _, row in df.iterrows()}
    
    # Prefijo de la URL de imágenes
    img_prefix = "https://www.forotecnoloxico.net/wp-content/uploads/2025/02/"
    
    # Obtener archivos en la carpeta mapas
    for filename in os.listdir(mapas_folder):
        file_path = os.path.join(mapas_folder, filename)
        
        # Leer el contenido del archivo
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Buscar y reemplazar valores en alt="x"
        def replace_alt(match):
            stand_number = match.group(1)
            if stand_number in stand_dict:
                corrected_url = re.sub(r'\.\.png$', '.png', f'{img_prefix}{stand_dict[stand_number]}')
                return f'alt="{corrected_url}"'
            return match.group(0)
        
        updated_content = re.sub(r'alt="(\d+)"', replace_alt, content)
        
        # Escribir el archivo actualizado
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        print(f"Archivo actualizado: {filename}")
    
    # Normalizar nombres de logos
    for logo in os.listdir(logos_folder):
        old_path = os.path.join(logos_folder, logo)
        new_name = remove_accents(logo.lower().replace(" ", "-"))
        new_path = os.path.join(logos_folder, new_name)
        os.rename(old_path, new_path)
        print(f"Logo renombrado: {logo} -> {new_name}")
    
    # Guardar el CSV actualizado con nombres en minúsculas y sin tildes
    df["Empresa"] = df["Empresa"].apply(remove_accents)
    df.to_csv(csv_path, index=False)
    print(f"CSV actualizado con nombres en minúsculas y sin tildes: {csv_path}")

# Ejemplo de uso
csv_path = "datos_filtrados.csv"  # Nombre del archivo CSV con datos de empresas
mapas_folder = "./mapas"  # Carpeta donde están los archivos de mapa
logos_folder = "./logos"  # Carpeta donde están los logos

update_map_files(csv_path, mapas_folder, logos_folder)
