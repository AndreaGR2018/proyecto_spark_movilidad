from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

# Crear sesión Spark con soporte de streaming
spark = SparkSession.builder \
    .appName("StreamingMovilidadBogota") \
    .getOrCreate()

# Leer desde Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "movilidad") \
    .option("startingOffsets", "latest") \
    .load()

# Esquema de los datos que envías desde el producer
schema = StructType() \
    .add("ID_ENCUESTA", StringType()) \
    .add("NUMERO_PERSONA", StringType()) \
    .add("NUMERO_VIAJE", StringType()) \
    .add("MOTIVOVIAJE", StringType()) \
    .add("MUNICIPIO_DESTINO", StringType()) \
    .add("DEPARTAMENTO_DESTINO", StringType()) \
    .add("TIEMPO_CAMINO", StringType()) \
    .add("HORA_INICIO", StringType()) \
    .add("HORA_FIN", StringType()) \
    .add("MEDIO_PRE", StringType())

# Convertir el valor (JSON string) a columnas
df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Procesamiento en tiempo real: contar viajes por medio de transporte
conteo = df_parsed.groupBy("MEDIO_PRE").count()

# Mostrar resultados en consola en tiempo real
query = conteo.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
