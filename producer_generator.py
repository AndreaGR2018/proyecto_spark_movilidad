import json, time, random
from kafka import KafkaProducer
from datetime import datetime, timedelta

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

medios = ['bus', 'transmilenio', 'taxi', 'bicicleta', 'peaton']
motivos = ['trabajo', 'estudio', 'ocio', 'compras', 'salud']

while True:
    inicio = datetime.now()
    duracion = random.randint(5, 60)
    mensaje = {
        "ID_ENCUESTA": random.randint(10000, 99999),
        "NUMERO_PERSONA": 1,
        "NUMERO_VIAJE": random.randint(1, 5),
        "MOTIVOVIAJE": random.choice(motivos),
        "MUNICIPIO_DESTINO": "Bogotá",
        "DEPARTAMENTO_DESTINO": "Cundinamarca",
        "TIEMPO_CAMINO": duracion,
        "HORA_INICIO": inicio.strftime("%H:%M:%S"),
        "HORA_FIN": (inicio + timedelta(minutes=duracion)).strftime("%H:%M:%S"),
        "MEDIO_PRE": random.choice(medios)
    }
    producer.send('movilidad_bogota', value=mensaje)
    print("Mensaje enviado:", mensaje)
    time.sleep(2)
