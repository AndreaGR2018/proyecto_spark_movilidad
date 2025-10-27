from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

# Crear sesión de Spark con soporte Kafka
spark = SparkSession.builder \
    .appName("StreamingMovilidad") \
    .master("local[*]") \
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Definir esquema de los datos (ajustado a tu JSON)
schema = StructType([
    StructField("ID_ENCUESTA", LongType(), True),
    StructField("NUMERO_PERSONA", IntegerType(), True),
    StructField("NUMERO_VIAJE", IntegerType(), True),
    StructField("MOTIVOVIAJE", StringType(), True),
    StructField("DEPARTAMENTO_DESTINO", StringType(), True),
    StructField("TIEMPO_CAMINO", FloatType(), True),
    StructField("HORA_INICIO", StringType(), True),
    StructField("HORA_FIN", StringType(), True),
    StructField("MEDIO_PREDOMINANTE", StringType(), True)
])

# Leer el stream desde Kafka
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "movilidad") \
    .option("startingOffsets", "latest") \
    .load()

# Convertir value a string y aplicar el esquema
df = df_raw.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
# Procesamiento simple: calcular promedio de tiempo por departamento
resultado = df.groupBy("DEPARTAMENTO_DESTINO").avg("TIEMPO_CAMINO")

# Mostrar resultados en consola (en lugar de CSV)
query = resultado.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
