# Limpieza de datos de ventas de cafetería

Práctica de limpieza y transformación de datos utilizando Python y Pandas sobre el dataset **Cafe Sales - Dirty Data for Cleaning Training**.

## Procedimiento

Se realizó una inspección inicial para identificar valores nulos, valores inválidos (`ERROR` y `UNKNOWN`), tipos de datos incorrectos y posibles duplicados.

Durante la limpieza se realizaron las siguientes acciones:

- Se reemplazaron `ERROR` y `UNKNOWN` por valores nulos.
- Se convirtieron las columnas de cantidad, precio y total a valores numéricos.
- Se convirtió la fecha de transacción a tipo fecha.
- Se reconstruyeron valores faltantes utilizando la relación `Total Spent = Quantity × Price Per Unit`.
- Se utilizaron los precios conocidos de los productos para recuperar algunos precios faltantes.
- Los datos que no podían recuperarse de forma confiable se conservaron como nulos.

## Resultados

El dataset original contiene **10,000 registros**. Después de la limpieza se conservaron los 10,000 registros, sin filas ni identificadores duplicados.

| Columna | Faltantes antes | Faltantes después |
|---|---:|---:|
| Quantity | 479 | 23 |
| Price Per Unit | 533 | 6 |
| Total Spent | 502 | 23 |

Al finalizar, se pudieron comprobar **9,974 registros** mediante la relación entre cantidad, precio y total, sin encontrar inconsistencias.

## Tabla resumen

| Problema encontrado | Registros afectados | Acción realizada | Justificación |
|---|---:|---|---|
| `ERROR` y `UNKNOWN` | Varias columnas | Reemplazar por nulos | No representan valores válidos |
| Valores faltantes en Quantity | 479 | Reconstrucción cuando fue posible | Puede calcularse con total y precio |
| Valores faltantes en Price Per Unit | 533 | Reconstrucción y precio del producto | Los productos presentan precios consistentes |
| Valores faltantes en Total Spent | 502 | Reconstrucción cuando fue posible | Se puede calcular con cantidad × precio |
| Tipos de datos incorrectos | 4 columnas | Conversión de tipos | Facilita los cálculos y el análisis |
| Datos que no pueden inferirse | Varias columnas | Conservar como nulos | Evita inventar información |
| Registros duplicados | 0 | Sin cambios | No se encontraron duplicados |

## Ejecución

Instalar Pandas:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python main.py
```

La base procesada se guarda en `data/clean/cafe_sales_clean.csv`.