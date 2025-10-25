from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg

# 1️⃣ Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("ProcesamientoBatch_EncuestaMovilidad") \
    .getOrCreate()

# 2️⃣ Cargar el archivo CSV
df = spark.read.csv("Encuesta_movilidad.csv", header=True, inferSchema=True)

# 3️⃣ Mostrar columnas para confirmar que se cargó correctamente
print("Columnas del DataFrame:")
print(df.columns)

# 4️⃣ Limpieza básica: eliminar filas con valores nulos en columnas clave
df = df.filter(col("MEDIO_PREDOMINANTE").isNotNull() & col("TIEMPO_CAMINO").isNotNull())

# 5️⃣ Conteo de viajes por medio de transporte
conteo = df.groupBy("MEDIO_PREDOMINANTE") \
    .agg(count("*").alias("num_viajes")) \
    .orderBy(col("num_viajes").desc())

# 6️⃣ Calcular el tiempo promedio de viaje por medio de transporte
promedios = df.groupBy("MEDIO_PREDOMINANTE") \
    .agg(avg("TIEMPO_CAMINO").alias("promedio_tiempo")) \
    .orderBy(col("promedio_tiempo").asc())

# 7️⃣ Mostrar resultados en consola
print("\n--- Conteo de viajes por medio de transporte ---")
conteo.show(truncate=False)

print("\n--- Tiempo promedio de viaje por medio de transporte ---")
promedios.show(truncate=False)

# 8️⃣ Guardar resultados en carpeta de salida
conteo.write.mode("overwrite").csv("resultados/conteo_viajes", header=True)
promedios.write.mode("overwrite").csv("resultados/promedio_tiempo", header=True)

# 9️⃣ Finalizar sesión
spark.stop()

print("\n✅ Procesamiento batch completado. Archivos guardados en la carpeta 'resultados/'")
