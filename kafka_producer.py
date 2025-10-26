import pandas as pd
import json
import time
from kafka import KafkaProducer
from datetime import datetime

# Cargar datos desde el CSV original
df = pd.read_csv("/home/vboxuser/datasets/Encuesta_movilidad.csv")

# Crear productor Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("📤 Iniciando envío de datos al topic 'movilidad'...\n")

# Enviar cada fila del DataFrame como un mensaje JSON
for _, row in df.iterrows():
    try:
        data = {
            "ID_ENCUESTA": int(row["ID_ENCUESTA"]),
            "NUMERO_PERSONA": int(row["NUMERO_PERSONA"]),
            "NUMERO_VIAJE": int(row["NUMERO_VIAJE"]),
            "MOTIVOVIAJE": str(row["MOTIVOVIAJE"]),
            "MUNICIPIO_DESTINO": str(row["MUNICIPIO_DESTINO"]),
            "DEPARTAMENTO_DESTINO": str(row["DEPARTAMENTO_DESTINO"]),
            "TIEMPO_CAMINO": float(row["TIEMPO_CAMINO"]) if not pd.isna(row["TIEMPO_CAMINO"]) else 0.0,
            "HORA_INICIO": str(row["HORA_INICIO"]),
            "HORA_FIN": str(row["HORA_FIN"]),
            "MEDIO_PREDOMINANTE": str(row.get("MEDIO_PREDOMINANTE", "Desconocido")),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        producer.send('movilidad', value=data)
        print(f"Enviado correctamente: {data}")
        time.sleep(0.5)  # Pausa para simular flujo en tiempo real
    except Exception as e:
        print(f"⚠️ Error enviando fila: {e}")

print("\n✅ Envío de datos completado.")
