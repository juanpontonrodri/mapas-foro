import pandas as pd
import os
import shutil

def filter_columns(input_csv, output_csv):
    # Cargar el archivo CSV
    df = pd.read_csv(input_csv)
    
    # Seleccionar solo las columnas 2 y 12 (índices 1 y 11 en base 0)
    df_filtered = df.iloc[:, [1, 11]]
    
    # Guardar el nuevo CSV
    df_filtered.to_csv(output_csv, index=False)
    
    print(f"Archivo filtrado guardado en {output_csv}")

def rename_logos(csv_path, logos_folder):
    # Cargar el CSV
    df = pd.read_csv(csv_path)
    
    # Obtener lista de archivos en la carpeta de logos
    logos_files = os.listdir(logos_folder)
    
    # Normalizar nombres de archivos y empresas para comparación
    def normalize_name(name):
        return str(name).lower().replace(" ", "").replace("-", "").replace("_", "").replace(".", "")
    
    # Crear un diccionario con los nombres de empresas normalizados
    empresa_dict = {normalize_name(empresa): empresa for empresa in df["Empresa"].dropna()}
    
    # Renombrar los archivos de logos
    for logo in logos_files:
        normalized_logo = normalize_name(logo.replace("removebgpreview", "").replace(".png", ""))
        
        for norm_empresa, empresa_real in empresa_dict.items():
            if norm_empresa in normalized_logo:
                new_filename = f"{empresa_real}.png"
                old_path = os.path.join(logos_folder, logo)
                new_path = os.path.join(logos_folder, new_filename)
                
                shutil.move(old_path, new_path)
                print(f"Renombrado: {logo} -> {new_filename}")
                break

# Ejemplo de uso
input_csv = "datos.csv"  # Nombre del archivo de entrada
output_csv = "datos_filtrados.csv"  # Nombre del archivo de salida
logos_folder = "./Logos"  # Carpeta donde están los logos

filter_columns(input_csv, output_csv)
rename_logos(output_csv, logos_folder)