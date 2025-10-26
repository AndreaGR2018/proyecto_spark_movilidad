from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, count, date_format
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, TimestampType

# Crear sesión Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming_Movilidad") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Esquema de los datos JSON (debe coincidir con el formato del producer)
schema = StructType([
    StructField("ID_ENCUESTA", IntegerType()),
    StructField("NUMERO_PERSONA", IntegerType()),
    StructField("NUMERO_VIAJE", IntegerType()),
    StructField("MOTIVOVIAJE", StringType()),
    StructField("MUNICIPIO_DESTINO", StringType()),
    StructField("DEPARTAMENTO_DESTINO", StringType()),
    StructField("TIEMPO_CAMINO", FloatType()),
    StructField("HORA_INICIO", StringType()),
    StructField("HORA_FIN", StringType()),
    StructField("MEDIO_PREDOMINANTE", StringType()),
    StructField("timestamp", TimestampType())
])

# Leer flujo de datos desde Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "movilidad") \
    .option("startingOffsets", "latest") \
    .load()

# Extraer y parsear los datos JSON desde el campo "value"
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Reemplazar valores nulos
parsed_df = parsed_df.na.fill({"TIEMPO_CAMINO": 0.0, "MEDIO_PREDOMINANTE": "Desconocido"})

# Cálculo de estadísticas por ventana de tiempo (1 minuto)
stats = parsed_df \
    .groupBy(
        window(col("timestamp"), "1 minute"),
        col("MEDIO_PREDOMINANTE")
    ) \
    .agg(
        avg("TIEMPO_CAMINO").alias("PROMEDIO_TIEMPO"),
        count("*").alias("TOTAL_VIAJES")
    ) \
    .withColumn("INICIO_VENTANA", date_format(col("window.start"), "HH:mm:ss")) \
    .withColumn("FIN_VENTANA", date_format(col("window.end"), "HH:mm:ss")) \
    .select("INICIO_VENTANA", "FIN_VENTANA", "MEDIO_PREDOMINANTE", "PROMEDIO_TIEMPO", "TOTAL_VIAJES")

# Mostrar los resultados en consola
console_query = stats \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Guardar los resultados como archivos CSV en HDFS o en tu sistema local
file_query = stats \
    .writeStream \
    .outputMode("complete") \
    .format("csv") \
    .option("path", "file:///home/vboxuser/spark_output/movilidad") \
    .option("checkpointLocation", "file:///home/vboxuser/spark_output/checkpoints") \
    .start()

# Esperar la terminación del streaming
spark.streams.awaitAnyTermination()
