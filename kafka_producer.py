import pandas as pd
import json
import time
from kafka import KafkaProducer

# Cargar datos del CSV
df = pd.read_csv("/home/vboxuser/datasets/Encuesta_movilidad.csv")

# Crear el productor Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Enviar cada fila como un mensaje JSON
for _, row in df.iterrows():
    data = {
        "ID_ENCUESTA": int(row["ID_ENCUESTA"]),
        "NUMERO_PERSONA": int(row["NUMERO_PERSONA"]),
        "NUMERO_VIAJE": int(row["NUMERO_VIAJE"]),
        "MOTIVOVIAJE": str(row["MOTIVOVIAJE"]),
        "MUNICIPIO_DESTINO": str(row["MUNICIPIO_DESTINO"]),
        "DEPARTAMENTO_DESTINO": str(row["DEPARTAMENTO_DESTINO"]),
        "TIEMPO_CAMINO": float(row["TIEMPO_CAMINO"]),
        "HORA_INICIO": str(row["HORA_INICIO"]),
        "HORA_FIN": str(row["HORA_FIN"]),
        "MEDIO_PRE": str(row["MEDIO_PRE"]),
        "timestamp": int(time.time())
    }
    producer.send('movilidad', value=data)
    print(f"Enviado: {data}")
    time.sleep(0.5)  # Pausa entre envíos para simular flujo en tiempo real
