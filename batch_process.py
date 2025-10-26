from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, round

# 1️⃣ Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("ProcesamientoBatch_EncuestaMovilidad") \
    .getOrCreate()

# 2️⃣ Cargar el archivo CSV (ruta absoluta para evitar errores)
df = spark.read.csv("/home/vboxuser/datasets/Encuesta_movilidad.csv", header=True, inferSchema=True)

# 3️⃣ Mostrar columnas para confirmar que se cargó correctamente
print("\n📋 Columnas del DataFrame:")
print(df.columns)

# 4️⃣ Limpieza básica
#   - Eliminar filas con valores nulos
#   - Filtrar tiempos no válidos (<= 0)
df_limpio = df.filter(
    (col("MEDIO_PREDOMINANTE").isNotNull()) &
    (col("TIEMPO_CAMINO").isNotNull()) &
    (col("TIEMPO_CAMINO") > 0)
)

# 5️⃣ Conteo de viajes por medio de transporte
conteo = df_limpio.groupBy("MEDIO_PREDOMINANTE") \
    .agg(count("*").alias("NUM_VIAJES")) \
    .orderBy(col("NUM_VIAJES").desc())

# 6️⃣ Calcular el tiempo promedio de viaje por medio de transporte
promedios = df_limpio.groupBy("MEDIO_PREDOMINANTE") \
    .agg(round(avg("TIEMPO_CAMINO"), 2).alias("PROMEDIO_TIEMPO")) \
    .orderBy(col("PROMEDIO_TIEMPO").asc())

# 7️⃣ Mostrar resultados en consola
print("\n🚗 --- Conteo de viajes por medio de transporte ---")
conteo.show(truncate=False)

print("\n🕒 --- Tiempo promedio de viaje por medio de transporte ---")
promedios.show(truncate=False)

# 8️⃣ Guardar resultados en carpeta de salida (rutas absolutas)
output_dir = "/home/vboxuser/datasets/encuesta_movilidad/resultados"
conteo.write.mode("overwrite").csv(f"{output_dir}/conteo_viajes", header=True)
promedios.write.mode("overwrite").csv(f"{output_dir}/promedio_tiempo", header=True)

# 9️⃣ Finalizar sesión
spark.stop()

print("\n✅ Procesamiento batch completado correctamente.")
print(f"📂 Resultados guardados en: {output_dir}")
