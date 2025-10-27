from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, when

# Crear sesión Spark
spark = SparkSession.builder \
    .appName("Batch_Encuesta_Movilidad") \
    .getOrCreate()

# ===============================
# 1️⃣ Cargar datos desde el CSV
# ===============================
data_path = "/home/vboxuser/datasets/Encuesta_movilidad.csv"

df = spark.read.csv(data_path, header=True, inferSchema=True)

print("✅ Datos cargados desde CSV:")
df.show(5)

# ===============================
# 2️⃣ Limpieza y transformación
# ===============================
# Eliminar filas con valores nulos en campos importantes
df_clean = df.dropna(subset=["MOTIVOVIAJE", "MEDIO_PREDOMINANTE", "TIEMPO_CAMINO"])

# ===============================
# 3️⃣ Análisis exploratorio (EDA)
# ===============================

# 3.1. Promedio de tiempo de camino por medio de transporte
promedio_tiempo = df_clean.groupBy("MEDIO_PREDOMINANTE").agg(
    avg("TIEMPO_CAMINO").alias("PROMEDIO_TIEMPO")
)

# 3.2. Distribución de motivos de viaje
distribucion = df_clean.groupBy("MOTIVOVIAJE").agg(
    count("*").alias("CANTIDAD_VIAJES")
)
# 3.3. Conteo de viajes por departamento de destino
conteo_viajes = df_clean.groupBy("DEPARTAMENTO_DESTINO").agg(
    count("*").alias("TOTAL_VIAJES")
)

# ===============================
# 4️⃣ Guardar resultados
# ===============================
output_base = "/home/vboxuser/datasets/encuesta_movilidad/resultados"

promedio_tiempo.write.mode("overwrite").csv(f"{output_base}/promedio_tiempo", header=True)
distribucion.write.mode("overwrite").csv(f"{output_base}/distribucion", header=True)
conteo_viajes.write.mode("overwrite").csv(f"{output_base}/conteo_viajes", header=True)

print("✅ Resultados almacenados en:")
print(f"  - {output_base}/promedio_tiempo")
print(f"  - {output_base}/distribucion")
print(f"  - {output_base}/conteo_viajes")

spark.stop()
