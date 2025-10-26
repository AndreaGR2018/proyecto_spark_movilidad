from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, TimestampType

# Crear sesión Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming_Movilidad") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Esquema del JSON que llega desde el producer
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
    StructField("MEDIO_PRE", StringType()),
    StructField("timestamp", TimestampType())
])

# Leer datos del topic 'movilidad'
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "movilidad") \
    .option("startingOffsets", "latest") \
    .load()

# Parsear los JSON
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Ejemplo de análisis: tiempo promedio por medio de transporte cada minuto
stats = parsed_df \
    .groupBy(window(col("timestamp"), "1 minute"), "MEDIO_PRE") \
    .agg({"TIEMPO_CAMINO": "avg"}) \
    .withColumnRenamed("avg(TIEMPO_CAMINO)", "PROMEDIO_TIEMPO")

# Mostrar resultados en consola
query = stats \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
