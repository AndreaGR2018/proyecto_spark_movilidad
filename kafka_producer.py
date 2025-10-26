import time
import json
import pandas as pd
from kafka import KafkaProducer

# Ruta de tu CSV
csv_file = "Encuesta_movilidad.csv"

# Leer el CSV con pandas
df = pd.read_csv(csv_file)

# Convertir filas a diccionarios
rows = df.to_dict(orient='records')

# Configuración del producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Nombre del topic existente
topic_name = 'movilidad'

# Enviar datos fila por fila
for row in rows:
    producer.send(topic_name, value=row)
    print(f"Sent: {row}")
    time.sleep(1)  # espera 1 segundo entre envíos
