🚦 Proyecto de Análisis de Movilidad con Spark y Kafka

Autora: Andrea Gordillo Rojas
Universidad: UNAD – Universidad Nacional Abierta y a Distancia
Asignatura: Big Data y Analítica Avanzada
Entorno de ejecución: Ubuntu (VM en VirtualBox con Apache Spark, Kafka y Zookeeper instalados)

🧩 1. Definición del problema y conjunto de datos

El proyecto tiene como propósito analizar la movilidad urbana en Bogotá, utilizando la Encuesta de Movilidad 2019, con el fin de identificar patrones de viaje, medios de transporte predominantes y tiempos promedio de desplazamiento.

Se emplean herramientas del ecosistema Big Data —Apache Spark y Apache Kafka— para realizar un procesamiento batch y un procesamiento en tiempo real (streaming), demostrando cómo ambos enfoques se complementan en un escenario analítico completo.

🧾 Conjunto de datos

Nombre: Movilidad de Bogotá – Caracterización de Viajes

Archivo: Encuesta_movilidad.csv

Fuente: Kaggle (Encuesta de Movilidad Bogotá 2019)[(https://www.kaggle.com/datasets/eduarmma19/movilidad-de-bogot-caracterizacin-viajes?resource=download)]

Tamaño: ~43 MB

Formato: CSV

Ubicación en la VM:

/home/vboxuser/datasets/Encuesta_movilidad.csv

🗂 2. Estructura de carpetas del proyecto

La organización del proyecto dentro de la VM es la siguiente:

/home/vboxuser/
│
├── spark_output/                      → Resultados del procesamiento en streaming
│
├── datasets/
│   ├── Encuesta_movilidad.csv         → Conjunto de datos original
│   ├── batch_process.py               → Script de procesamiento batch (Spark)
│   └── encuesta_movilidad/
│       └── resultados/
│           ├── promedio_tiempo/       → Resultados del procesamiento batch
│           ├── distribucion/          → Resultados del procesamiento batch
│           └── conteo_viajes/         → Resultados del procesamiento batch
│
├── kafka_producer.py                  → Productor de Kafka (simula flujo de datos)
└── spark_streaming_consumer.py        → Consumidor Spark Streaming (procesamiento en tiempo real)


batch_process.py: Procesamiento batch con Spark (limpieza, análisis y almacenamiento).

kafka_producer.py: Envía los datos del CSV a un tópico Kafka.

spark_streaming_consumer.py: Procesa los datos en tiempo real con Spark Streaming.

resultados/: Contiene los CSV generados por el análisis batch.

⚙️ 3. Procesamiento Batch (Spark)

Script: datasets/batch_process.py

Este script realiza el análisis y transformación inicial del dataset de movilidad:

Funcionalidades principales:

Lectura del archivo CSV con Spark.

Limpieza de datos: eliminación de nulos y registros inconsistentes.

Transformación de columnas y conversión de tipos.

Cálculo de indicadores principales:

Promedio de tiempo de viaje por medio de transporte.

Conteo de viajes por motivo.

Distribución horaria de los desplazamientos.

Almacenamiento de resultados en:

/home/vboxuser/datasets/encuesta_movilidad/resultados/
├── promedio_tiempo/
├── distribucion/
└── conteo_viajes/

Ejecución:
cd /home/vboxuser/datasets
python3 batch_process.py

Ejemplo de salida:
-------------------------------------------
Batch: 5
-------------------------------------------
+------------------+-------------+
|MEDIO_PREDOMINANTE|PROMEDIO_TIEMPO|
+------------------+-------------+
|Transmilenio      |27.35        |
|Bus urbano        |25.10        |
|Bicicleta         |15.87        |
|A pie             |12.43        |
+------------------+-------------+
Streaming (salida en tiempo real):

🔄 4. Procesamiento en Tiempo Real (Streaming + Kafka)
⚙️ Kafka Producer

Script: /home/vboxuser/kafka_producer.py

Simula la llegada de datos en tiempo real, publicando los registros del archivo Encuesta_movilidad.csv al tópico movilidad.

Pasos:

Leer el CSV.

Convertir cada fila en un mensaje JSON.

Enviar los mensajes al tópico Kafka.

Ejecución:

python3 kafka_producer.py

⚙️ Spark Streaming Consumer

Script: /home/vboxuser/spark_streaming_consumer.py

Escucha el tópico movilidad y procesa los mensajes en tiempo real con Spark Structured Streaming.

Tareas:

Conectarse al tópico Kafka movilidad.

Leer los mensajes JSON y estructurarlos como DataFrame.

Calcular conteos en tiempo real por medio de transporte.

Mostrar los resultados en consola y almacenarlos opcionalmente en /spark_output/.

Ejecución:

spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /home/vboxuser/spark_streaming_consumer.py

🧠 5. Arquitectura de la Solución
                ┌──────────────────────────────────┐
                │ Encuesta_movilidad.csv (Kaggle)  │
                └──────────────────┬───────────────┘
                                   │
             ┌─────────────────────▼─────────────────────┐
             │ batch_process.py (Spark - Batch)          │
             │ Limpieza + EDA + Resultados CSV           │
             └──────────────┬────────────────────────────┘
                            │
                Resultados en: resultados/
                            │
                            ▼
             ┌──────────────────────────────────┐
             │ kafka_producer.py                 │
             │ Envía datos JSON a Kafka (topic)  │
             └──────────────────┬───────────────┘
                                │
             ┌──────────────────▼───────────────┐
             │ spark_streaming_consumer.py       │
             │ Procesamiento en tiempo real      │
             └──────────────────┬───────────────┘
                                │
                       Resultados en spark_output/

📊 6. Resultados Esperados
🔹 Procesamiento Batch

Promedio de duración de viaje por medio de transporte.

Conteo de viajes por motivo (MOTIVOVIAJE).

Distribución horaria de viajes (HORA_INICIO, HORA_FIN).

🔹 Procesamiento Streaming

Conteo en tiempo real de viajes según el medio de transporte.

Resultados actualizados en consola o almacenados en /spark_output/.

📸 7. Capturas sugeridas para la presentación

Estructura de carpetas en /home/vboxuser/.

Ejecución del script batch_process.py con Spark.

Productor Kafka enviando datos al tópico movilidad.

Spark Streaming recibiendo y mostrando resultados en tiempo real.

Archivos generados dentro de resultados/.

🔗 8. Enlaces

Repositorio GitHub: Proyecto de Análisis de Movilidad con Spark y Kafka

Video explicativo: (realizado por Andrea Gordillo Rojas, UNAD)

💬 9. Conclusiones

Este proyecto demuestra el potencial del ecosistema Big Data al integrar Spark (para procesamiento masivo y analítico) y Kafka (para transmisión y análisis en tiempo real).

La aplicación permite analizar la movilidad de Bogotá de forma flexible y escalable, aplicando una infraestructura que combina:

Limpieza y análisis batch de grandes volúmenes.

Procesamiento de flujos en tiempo real.

Persistencia de resultados para análisis posteriores.  
