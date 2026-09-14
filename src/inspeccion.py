import pandas as pd


def inspeccionar_datos(df):
    columnas_categoricas = [
        "Item",
        "Payment Method",
        "Location",
    ]
    columnas_numericas = [
        "Quantity",
        "Price Per Unit",
        "Total Spent",
    ]

    # Resumen general
    print("Primeras filas:")
    print(df.head())

    print("\nDimensiones del dataset:")
    print(df.shape)

    print("\nColumnas:")
    print(df.columns.tolist())

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nValores nulos por columna:")
    print(df.isnull().sum())

    print("\nValores únicos por columna:")
    print(df.nunique())

    # Revisar variables categóricas
    for columna in columnas_categoricas:
        print(f"\nValores de {columna}:")
        print(df[columna].value_counts(dropna=False))

    # Detectar valores numéricos inválidos
    for columna in columnas_numericas:
        convertida = pd.to_numeric(
            df[columna],
            errors="coerce"
        )

        invalidos = df[
            df[columna].notna() & convertida.isna()
        ][columna]

        print(f"\nValores no numéricos en {columna}:")
        print(invalidos.value_counts())

    # Revisar fechas
    fechas_convertidas = pd.to_datetime(
        df["Transaction Date"],
        errors="coerce"
    )

    fechas_invalidas = df[
        df["Transaction Date"].notna()
        & fechas_convertidas.isna()
    ]["Transaction Date"]

    print("\nValores no válidos en Transaction Date:")
    print(fechas_invalidas.value_counts())

    print("\nRango de fechas válidas:")
    print("Fecha mínima:", fechas_convertidas.min())
    print("Fecha máxima:", fechas_convertidas.max())

    # Validar duplicados
    print("\nFilas duplicadas:")
    print(df.duplicated().sum())

    print("\nTransaction ID duplicados:")
    print(df["Transaction ID"].duplicated().sum())

    # Validar relaciones entre columnas
    print("\nRelación entre producto y precio:")

    precios_convertidos = pd.to_numeric(
        df["Price Per Unit"],
        errors="coerce"
    )
    productos_precios = df.loc[
        df["Item"].notna()
        & ~df["Item"].isin(["ERROR", "UNKNOWN"])
        & precios_convertidos.notna(),
        ["Item", "Price Per Unit"]
    ]

    print(productos_precios.groupby("Item")["Price Per Unit"].value_counts())

    print("\nComprobación de Quantity × Price Per Unit = Total Spent:")

    q = pd.to_numeric(df["Quantity"], errors="coerce")
    p = pd.to_numeric(df["Price Per Unit"], errors="coerce")
    t = pd.to_numeric(df["Total Spent"], errors="coerce")

    validas = q.notna() & p.notna() & t.notna()

    coinciden = ((q[validas] * p[validas]) - t[validas]).abs() < 0.001

    print("Registros comprobables:", validas.sum())
    print("Cálculo correcto:", coinciden.sum())
    print("Cálculo incorrecto:", (~coinciden).sum())