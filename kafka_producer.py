from kafka import KafkaProducer
import json
import time
import pandas as pd

# Configurar Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Leer archivo CSV
file_path = "/home/vboxuser/datasets/Encuesta_movilidad.csv"
df = pd.read_csv(file_path)

print(f"🚀 Enviando {len(df)} registros a Kafka...")

for i, row in df.iterrows():
    message = row.to_dict()
    producer.send("movilidad", value=message)
    print(f"📤 Enviado ({i+1}/{len(df)}): {message}")
    time.sleep(0.5)  # simular llegada de datos en tiempo real

producer.flush()
producer.close()

print("✅ Envío completo.")
