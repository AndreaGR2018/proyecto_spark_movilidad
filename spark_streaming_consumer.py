from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, from_unixtime
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, TimestampType
import logging

# Reducir los mensajes de log
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Definir el esquema de los datos
schema = StructType([
    StructField("sensor_id", IntegerType()),
    StructField("temperature", FloatType()),
    StructField("humidity", FloatType()),
    StructField("timestamp", IntegerType())
])

# Leer datos en streaming desde Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

# Parsear el JSON
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Convertir el timestamp Unix a tipo Timestamp
parsed_df = parsed_df.withColumn("timestamp", from_unixtime(col("timestamp")).cast(TimestampType()))

# Calcular promedios por minuto y sensor
windowed_stats = parsed_df \
    .groupBy(window(col("timestamp"), "1 minute"), "sensor_id") \
    .agg({"temperature": "avg", "humidity": "avg"}) \
    .orderBy("window")

# Mostrar resultados en la consola
query = windowed_stats \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
