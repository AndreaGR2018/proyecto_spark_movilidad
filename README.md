# 🚦 Proyecto de Análisis de Movilidad con Spark y Kafka

## 📘 Introducción
Este proyecto tiene como objetivo analizar datos de movilidad de los ciudadanos de Bogotá mediante el uso de **Apache Spark** para el procesamiento masivo de datos y **Apache Kafka** para el procesamiento en tiempo real.  
El flujo completo incluye procesamiento **batch** (análisis exploratorio y limpieza de datos históricos) y **streaming** (análisis en tiempo real de los datos enviados a un topic de Kafka).

---

## 🎯 Definición del Problema
El propósito es analizar los patrones de movilidad en la ciudad, específicamente:
- Identificar los **medios de transporte más utilizados**.  
- Calcular el **tiempo promedio de viaje** según el medio de transporte.  
- Observar cómo varían estos datos en tiempo real al simular la llegada de nuevos registros.

El análisis permite comprender mejor los hábitos de transporte y puede apoyar la toma de decisiones en materia de movilidad urbana.

---

## 📊 Conjunto de Datos
- **Nombre:** `Encuesta_movilidad.csv`  
- **Fuente:** [Kaggle – Encuesta de Movilidad en Bogotá](https://www.kaggle.com)  
- **Ubicación local:** `/home/vboxuser/datasets/Encuesta_movilidad.csv`  
- **Descripción:** Contiene información sobre los viajes diarios realizados por los ciudadanos: motivos del viaje, municipio y departamento de destino, medio de transporte, tiempos de desplazamiento y horarios.

---

## ⚙️ Tecnologías Utilizadas
- **Apache Spark 3.5.x**
- **Apache Kafka 3.6.x**
- **Hadoop (instalado en la VM de Big Data)**
- **Python 3**
- **Librería:** `kafka-python`

---

## 🧠 Arquitectura del Proyecto

Kafka Producer ---> Kafka Topic "movilidad" ---> Spark Streaming Consumer
│
▼
Procesamiento en tiempo real
│
▼
Resultados en consola y CSV


---

## 🧩 Estructura del Repositorio

proyecto_spark_movilidad/
│
├── batch_process.py # Procesamiento batch (EDA y análisis)
├── kafka_producer.py # Productor de datos para Kafka
├── spark_streaming_consumer.py # Consumidor Spark Streaming
└── README.md

---

## 🧹 Procesamiento Batch (Análisis Exploratorio y Limpieza)

El script [`batch_process.py`](batch_process.py) realiza operaciones de limpieza, transformación y **análisis exploratorio de datos (EDA)** usando **DataFrames de Spark**.

### 🔍 Funcionalidades
- Carga del dataset con inferencia de esquema.
- Muestra aleatoria de registros para ver el contenido.
- Estadísticas descriptivas (`describe()`).
- Filtrado de valores nulos o inválidos.
- Cálculo de:
  - Conteo de viajes por medio de transporte.
  - Tiempo promedio de viaje.
  - Distribución porcentual de los medios utilizados.
- Exporta los resultados a:
/home/vboxuser/datasets/encuesta_movilidad/resultados/


### ▶️ Ejecución
```bash
spark-submit batch_process.py
⚡ Procesamiento en Tiempo Real (Kafka + Spark Streaming)

1️⃣ Iniciar los servicios
En la máquina virtual con Ubuntu (usuario: vboxuser, contraseña: bigdata):

Iniciar ZooKeeper
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &
Iniciar Kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
Crear el topic
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic movilidad

2️⃣ Ejecutar el Productor
El script kafka_producer.py envía los registros del archivo CSV al topic movilidad en formato JSON, simulando la llegada continua de datos.

python3 kafka_producer.py
Cada mensaje enviado se muestra en consola, con un pequeño retardo (time.sleep(0.5)) para simular un flujo en tiempo real.

3️⃣ Ejecutar el Consumidor (Spark Streaming)
El script spark_streaming_consumer.py lee los datos del topic movilidad, los procesa y calcula estadísticas agregadas cada minuto, mostrando resultados en consola y guardándolos como CSV.

Ejecución:
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumer.py

Resultados:
Se muestran en la consola de Spark Streaming.

También se guardan automáticamente en:

/home/vboxuser/spark_output/movilidad/
📈 Ejemplo de Resultados
Batch (promedios y conteos):

+------------------+-------------+
|MEDIO_PREDOMINANTE|PROMEDIO_TIEMPO|
+------------------+-------------+
|Transmilenio      |27.35        |
|Bus urbano        |25.10        |
|Bicicleta         |15.87        |
|A pie             |12.43        |
+------------------+-------------+
Streaming (salida en tiempo real):

-------------------------------------------
Batch: 5
-------------------------------------------
|INICIO_VENTANA|FIN_VENTANA|MEDIO_PREDOMINANTE|PROMEDIO_TIEMPO|TOTAL_VIAJES|
|00:01:00       |00:02:00  |Transmilenio      |26.7           |45          |
|00:01:00       |00:02:00  |Bicicleta         |14.3           |12          |
-------------------------------------------
🌐 Interfaz Web de Spark
Durante la ejecución de Spark Streaming, puedes acceder al panel de monitoreo en tu navegador:

perl
Copiar código
http://<IP-local>:4040
Ejemplo:

http://192.168.1.7:4040
📦 Evidencias y Resultados
En la carpeta del repositorio encontrarás capturas de pantalla que evidencian:

Ejecución del productor Kafka.

Procesamiento en tiempo real con Spark Streaming.

Resultados batch y streaming almacenados correctamente.

✅ Conclusiones
Se logró integrar Apache Kafka con Apache Spark Streaming para el procesamiento en tiempo real.

Se realizaron operaciones de limpieza, transformación y EDA sobre el dataset en modo batch.

El sistema permite analizar la movilidad urbana tanto históricamente como en tiempo real.

Los resultados se visualizan en consola y se guardan en formato CSV.

👩‍💻 Autor
Andrea Gordillo
Proyecto: Análisis de Movilidad con Spark y Kafka
Universidad Nacional Abierta y a Distancia UNAD
Asignatura: Big Data
Año: 2025
