from pathlib import Path

# La ruta al directorio actual donde vive el script
# El punto "." hace referencia al directorio actual.
directorio_actual = Path(".")

# Busca todos los archivos que terminan en .csv
for archivo_csv in directorio_actual.glob("*.csv"):
    try:
        # Verifica si es un archivo antes de intentar borrarlo
        if archivo_csv.is_file():
            archivo_csv.unlink()
            print(f"Borrado: {archivo_csv}")
    except Exception as e:
        print(f"Error al borrar {archivo_csv}: {e}")

print("Proceso de limpieza completado.")