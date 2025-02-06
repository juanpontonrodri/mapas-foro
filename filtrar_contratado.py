import pandas as pd

def filter_columns(input_csv, output_csv):
    # Cargar el archivo CSV
    df = pd.read_csv(input_csv)
    
    # Seleccionar solo las columnas 2 y 12 (índices 1 y 11 en base 0)
    df_filtered = df.iloc[:, [1, 11]]
    
    # Guardar el nuevo CSV
    df_filtered.to_csv(output_csv, index=False)
    
    print(f"Archivo filtrado guardado en {output_csv}")

# Ejemplo de uso
input_csv = "datos.csv"  # Nombre del archivo de entrada
output_csv = "datos_filtrados.csv"  # Nombre del archivo de salida
filter_columns(input_csv, output_csv)
