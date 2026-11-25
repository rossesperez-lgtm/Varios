import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

carpeta = Path(__file__).parent

# Leer Datos.csv: Pandas usa ";" porque ese es el separador del archivo.
df = pd.read_csv(carpeta / "Datos.csv", sep=";", encoding="utf-8-sig")

print("=== Analisis de Datos.csv ===")
print("\nPrimeras filas:")
print(df.head())

# Consultar el tamano y los tipos de datos.
print(f"\nFilas y columnas: {df.shape}")
print("\nInformacion de las columnas:")
df.info()

# Calcular estadisticas solo para las columnas numericas.
columnas_numericas = df.select_dtypes(include="number")
estadisticas = pd.DataFrame(
    {
        "media": columnas_numericas.mean(),
        "mediana": columnas_numericas.median(),
        "desviacion estandar": columnas_numericas.std(),
        "minimo": columnas_numericas.min(),
        "maximo": columnas_numericas.max(),
    }
)
print("\nEstadisticas:")
print(estadisticas)

# Ventas.csv incluye texto, fechas, numeros y algunos datos faltantes para
# practicar operaciones comunes con tablas de datos.
ventas = pd.read_csv(
    carpeta / "Ventas.csv",
    sep=";",
    encoding="utf-8-sig",
    parse_dates=["Fecha"],
)

print("\n=== Ejemplos con Ventas.csv ===")
print("\nPrimeras filas:")
print(ventas.head())

# Seleccionar columnas especificas.
print("\nProducto, categoria y precio:")
print(ventas[["Producto", "Categoria", "Precio"]].head())

# Filtrar filas con mas de una condicion usando &.
bebidas = ventas[(ventas["Categoria"] == "Bebidas") & (ventas["Cantidad"] >= 2)]
print("\nBebidas con cantidad igual o mayor que 2:")
print(bebidas)

# Ordenar desde el precio mas alto al mas bajo.
ordenadas = ventas.sort_values("Precio", ascending=False)
print("\nProductos ordenados por precio (descendente):")
print(ordenadas[["Producto", "Precio"]].head())

# Crear una copia y agregar una columna calculada.
ventas_con_total = ventas.copy()
ventas_con_total["Total"] = ventas_con_total["Cantidad"] * ventas_con_total["Precio"]
print("\nTotal por venta (cantidad por precio):")
print(ventas_con_total[["Producto", "Cantidad", "Precio", "Total"]].head())

# Detectar datos faltantes y reemplazarlos en una copia de la tabla.
print("\nDatos faltantes por columna:")
print(ventas_con_total.isna().sum())

ventas_limpias = ventas_con_total.copy()
ventas_limpias["Region"] = ventas_limpias["Region"].fillna("Sin especificar")
print("\nRegiones despues de completar los datos faltantes:")
print(ventas_limpias[["Producto", "Region"]].tail())

# Contar y quitar filas duplicadas. Se agrega una copia temporal de una fila
# para que se pueda observar el efecto de drop_duplicates().
datos_con_duplicado = pd.concat(
    [ventas_limpias, ventas_limpias.head(1)],
    ignore_index=True,
)
print(
    "\nFilas duplicadas en el ejemplo:",
    datos_con_duplicado.duplicated().sum(),
)
datos_sin_duplicados = datos_con_duplicado.drop_duplicates()
print("Filas despues de quitar duplicados:", len(datos_sin_duplicados))

# Agrupar por categoria y resumir varias columnas.
resumen = ventas_limpias.groupby("Categoria", as_index=False).agg(
    Unidades=("Cantidad", "sum"),
    Ventas_totales=("Total", "sum"),
    Precio_promedio=("Precio", "mean"),
)
print("\nResumen por categoria:")
print(resumen)

# Guardar el resumen en un nuevo CSV, sin incluir el indice de Pandas.
archivo_salida = carpeta / "Resumen_por_categoria.csv"
resumen.to_csv(archivo_salida, sep=";", index=False, encoding="utf-8-sig")
print(f"\nResumen guardado en: {archivo_salida}")

# Mostrar el grafico al final para que no interrumpa los ejemplos anteriores.
if columnas_numericas.shape[1] >= 2:
    eje_x = columnas_numericas.columns[0]
    eje_y = columnas_numericas.columns[1]

    plt.scatter(columnas_numericas[eje_x], columnas_numericas[eje_y])
    plt.xlabel(eje_x)
    plt.ylabel(eje_y)
    plt.title(f"{eje_y} vs {eje_x}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("\nSe necesitan dos columnas numericas para crear el grafico.")
