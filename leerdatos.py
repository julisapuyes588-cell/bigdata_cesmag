import pandas as pd
import numpy as np

# Leer el archivo CSV
df = pd.read_csv('datos_sinteticos.csv')

# Convertir columnas de fecha a datetime
df['fecha_campana'] = pd.to_datetime(df['fecha_campana'])

# Mostrar información básica
print("=" * 50)
print("INFORMACIÓN DEL DATASET")
print("=" * 50)
print(f"\nForma del dataset: {df.shape}")
print(f"\nPrimeras filas:\n{df.head()}")

# Información general
print(f"\nTipos de datos:\n{df.dtypes}")
print(f"\nValores nulos:\n{df.isnull().sum()}")

# Estadísticas descriptivas (solo columnas numéricas)
print(f"\nEstadísticas descriptivas:\n{df.describe()}")

# Información de columnas
print(f"\nNombres de columnas: {df.columns.tolist()}")
print(f"\nTotal de registros: {len(df)}")

# ANÁLISIS AVANZADO PARA TOMA DE DECISIONES
print("\n" + "=" * 50)
print("INDICADORES CLAVE DE DESEMPEÑO (KPIs)")
print("=" * 50)

# 1. Análisis de distribución y variabilidad
print("\n1. MEDIDAS DE DISPERSIÓN:")
numeric_df = df.select_dtypes(include=[np.number])
print(f"Desviación estándar:\n{numeric_df.std().round(3)}")
print(f"\nCoeficiente de variación (%):\n{(numeric_df.std() / numeric_df.mean() * 100).round(2)}")

# 2. Detección de outliers
print("\n2. ANÁLISIS DE OUTLIERS (IQR):")
for col in df.select_dtypes(include=[np.number]).columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
    print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")

# 3. Correlación entre variables
print("\n3. CORRELACIÓN ENTRE VARIABLES:")
numeric_df = df.select_dtypes(include=[np.number])
if len(numeric_df.columns) > 1:
    print(numeric_df.corr().round(3))

# 4. Análisis de frecuencias (variables categóricas)
print("\n4. DISTRIBUCIÓN DE VARIABLES CATEGÓRICAS:")
for col in df.select_dtypes(include=['object']).columns:
    print(f"\n{col}:")
    print(df[col].value_counts())

# 5. Indicadores de calidad de datos
print("\n5. CALIDAD DE DATOS:")
completitud = (1 - df.isnull().sum() / len(df)) * 100
print(f"Completitud por columna (%):\n{completitud.round(2)}")
print(f"\nTasa de duplicados: {df.duplicated().sum()} ({df.duplicated().sum()/len(df)*100:.2f}%)")

# 6. Resumen ejecutivo
print("\n" + "=" * 50)
print("RESUMEN EJECUTIVO")
print("=" * 50)
print(f"Registros válidos: {len(df)}")
print(f"Completitud promedio: {completitud.mean():.2f}%")
print(f"Dimensionalidad: {len(df.columns)} variables")