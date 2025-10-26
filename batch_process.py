from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, round, desc

# 1️⃣ Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("ProcesamientoBatch_EncuestaMovilidad") \
    .getOrCreate()

print("\n🚀 Iniciando procesamiento batch...")

# 2️⃣ Cargar el archivo CSV
df = spark.read.csv("/home/vboxuser/datasets/Encuesta_movilidad.csv", header=True, inferSchema=True)

# 3️⃣ Mostrar estructura inicial
print("\n📋 Columnas del DataFrame:")
print(df.columns)
print(f"\n📊 Total de registros iniciales: {df.count()}")

# 4️⃣ Mostrar muestra aleatoria
print("\n🔍 Muestra aleatoria de registros:")
df.sample(fraction=0.01, seed=42).show(5, truncate=False)

# 5️⃣ Resumen estadístico del tiempo de camino
print("\n📈 Resumen estadístico de 'TIEMPO_CAMINO':")
df.select("TIEMPO_CAMINO").describe().show()  
# 6️⃣ Limpieza de datos
df_limpio = df.filter(
    (col("MEDIO_PREDOMINANTE").isNotNull()) &
    (col("TIEMPO_CAMINO").isNotNull()) &
    (col("TIEMPO_CAMINO") > 0)
)

print(f"\n🧹 Total de registros después de limpieza: {df_limpio.count()}")

# 7️⃣ Transformaciones y análisis
# Conteo de viajes por medio de transporte
conteo = df_limpio.groupBy("MEDIO_PREDOMINANTE") \
    .agg(count("*").alias("NUM_VIAJES")) \
    .orderBy(desc("NUM_VIAJES"))

# Promedio de tiempo de viaje
promedios = df_limpio.groupBy("MEDIO_PREDOMINANTE") \
    .agg(round(avg("TIEMPO_CAMINO"), 2).alias("PROMEDIO_TIEMPO")) \
    .orderBy(col("PROMEDIO_TIEMPO").asc())

# 8️⃣ Distribución porcentual de medios de transporte
total_viajes = df_limpio.count()
distribucion = conteo.withColumn("PORCENTAJE", round((col("NUM_VIAJES") / total_viajes) * 100, 2))

# 9️⃣ Mostrar resultados en consola
print("\n🚗 --- Conteo de viajes por medio de transporte ---")
conteo.show(truncate=False)

print("\n🕒 --- Tiempo promedio de viaje por medio de transporte ---")
promedios.show(truncate=False)
 print("\n📊 --- Distribución porcentual de medios de transporte ---")
distribucion.show(truncate=False)

# 🔟 Guardar resultados
output_dir = "/home/vboxuser/datasets/encuesta_movilidad/resultados"
conteo.write.mode("overwrite").csv(f"{output_dir}/conteo_viajes", header=True)
promedios.write.mode("overwrite").csv(f"{output_dir}/promedio_tiempo", header=True)
distribucion.write.mode("overwrite").csv(f"{output_dir}/distribucion", header=True)

print("\n✅ Procesamiento batch completado correctamente.")
print(f"📂 Resultados guardados en: {output_dir}")

# 🔚 Cerrar sesión
spark.stop()
