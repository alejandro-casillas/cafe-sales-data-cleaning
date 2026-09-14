import pandas as pd

from src.inspeccion import inspeccionar_datos
from src.limpieza import limpiar_datos


RUTA_ORIGINAL = "data/raw/dirty_cafe_sales.csv"
RUTA_LIMPIA = "data/clean/cafe_sales_clean.csv"


def validar_datos(df):
    print("\n===== VALIDACIÓN FINAL =====")
    print("\nDimensiones finales:")
    print(df.shape)

    print("\nValores nulos después de la limpieza:")
    print(df.isnull().sum())

    print("\nFilas duplicadas:")
    print(df.duplicated().sum())

    print("\nIDs duplicados:")
    print(df["Transaction ID"].duplicated().sum())

    validas = (
        df["Quantity"].notna()
        & df["Price Per Unit"].notna()
        & df["Total Spent"].notna()
    )

    coinciden = (
        (
            df.loc[validas, "Quantity"]
            * df.loc[validas, "Price Per Unit"]
            - df.loc[validas, "Total Spent"]
        ).abs() < 0.001
    )

    print("\nRegistros numéricos comprobables:")
    print(validas.sum())

    print("\nCálculos correctos:")
    print(coinciden.sum())

    print("\nCálculos incorrectos:")
    print((~coinciden).sum())


# Cargar dataset
df = pd.read_csv(RUTA_ORIGINAL)

# Inspeccionar datos
print("===== INSPECCIÓN INICIAL =====")
inspeccionar_datos(df)

# Limpiar datos
print("\n===== LIMPIEZA =====")
df_limpio = limpiar_datos(df)

# Validar resultado
validar_datos(df_limpio)

# Exportar dataset limpio
df_limpio.to_csv(RUTA_LIMPIA, index=False)