import pandas as pd


def obtener_precios_por_producto(df):
    registros_validos = df.loc[
        df["Item"].notna() & df["Price Per Unit"].notna(),
        ["Item", "Price Per Unit"]
    ]

    return registros_validos.groupby("Item")["Price Per Unit"].first()


def recuperar_valores_numericos(df):
    mascara = (
        df["Total Spent"].isna()
        & df["Quantity"].notna()
        & df["Price Per Unit"].notna()
    )

    df.loc[mascara, "Total Spent"] = (
        df.loc[mascara, "Quantity"]
        * df.loc[mascara, "Price Per Unit"]
    )

    mascara = (
        df["Quantity"].isna()
        & df["Total Spent"].notna()
        & df["Price Per Unit"].notna()
    )

    df.loc[mascara, "Quantity"] = (
        df.loc[mascara, "Total Spent"]
        / df.loc[mascara, "Price Per Unit"]
    )

    mascara = (
        df["Price Per Unit"].isna()
        & df["Total Spent"].notna()
        & df["Quantity"].notna()
    )

    df.loc[mascara, "Price Per Unit"] = (
        df.loc[mascara, "Total Spent"]
        / df.loc[mascara, "Quantity"]
    )

    return df


def limpiar_datos(df):
    df = df.copy()

    # Normalizar valores inválidos
    df.replace(["ERROR", "UNKNOWN"], pd.NA, inplace=True)

    # Convertir tipos de datos
    columnas_numericas = [
        "Quantity",
        "Price Per Unit",
        "Total Spent"
    ]

    for columna in columnas_numericas:
        df[columna] = pd.to_numeric(
            df[columna],
            errors="coerce"
        )

    df["Transaction Date"] = pd.to_datetime(
        df["Transaction Date"],
        errors="coerce"
    )

    # Recuperar valores numéricos
    df = recuperar_valores_numericos(df)

    # Obtener precios conocidos por producto
    precios_por_producto = obtener_precios_por_producto(df)
    mascara = df["Price Per Unit"].isna() & df["Item"].notna()
    df.loc[mascara, "Price Per Unit"] = (
        df.loc[mascara, "Item"].map(precios_por_producto)
    )

    df = recuperar_valores_numericos(df)

    return df