# 🚦 Proyecto de Análisis de Movilidad con Spark y Kafka

## 📖 Introducción
Este proyecto realiza el **análisis de datos de movilidad en Bogotá** utilizando **Apache Spark** y **Apache Kafka**, aplicando tanto **procesamiento batch** como **procesamiento en tiempo real (streaming)**.  

El objetivo principal es demostrar cómo integrar ambas modalidades de análisis sobre un mismo dominio de datos, partiendo de un conjunto de información pública y simulando el flujo continuo de datos en Kafka.

---

## 🎯 Definición del Problema

La movilidad en Bogotá involucra grandes volúmenes de datos derivados de los viajes diarios de los ciudadanos.  
El reto consiste en **analizar estos datos para obtener patrones de uso de medios de transporte y tiempos de desplazamiento promedio**, tanto de forma histórica (batch) como simulada en tiempo real (streaming).

---

## 🧩 Conjunto de Datos

- **Fuente:** [Kaggle – Encuesta de Movilidad Bogotá](https://www.kaggle.com/)  
- **Archivo:** `Encuesta_movilidad.csv`
- **Ubicación en el entorno:**  
  `/home/vboxuser/datasets/Encuesta_movilidad.csv`
- **Descripción de columnas relevantes:**
  - `MEDIO_PREDOMINANTE`: Medio de transporte principal usado.
  - `TIEMPO_CAMINO`: Tiempo total de desplazamiento.
  - Otras variables relacionadas con los viajes y características de los encuestados.

---

## ⚙️ Tecnologías Utilizadas

- **Apache Spark 3.5.3**
- **Apache Kafka 3.6.2**
- **Python 3.10**
- **Hadoop (modo local)**
- **Sistema Operativo:** Ubuntu (máquina virtual `vboxuser`)

---

## 🧮 Procesamiento Batch (`batch_process.py`)

El procesamiento batch carga y limpia el dataset completo, calcula estadísticas descriptivas y almacena los resultados en formato CSV.

### 🔹 Pasos principales:
1. **Carga del dataset desde la ruta local.**
2. **Limpieza:**  
   - Eliminación de registros nulos.  
   - Filtrado de tiempos de viaje inválidos.
3. **Cálculos realizados:**
   - Conteo de viajes por medio de transporte.
   - Promedio de tiempo de viaje por medio de transporte.
4. **Salida de resultados:**  
   Los resultados se almacenan en:
/home/vboxuser/datasets/encuesta_movilidad/resultados/
├── conteo_viajes/
└── promedio_tiempo/


### 🧠 Ejecución del procesamiento batch
```bash
spark-submit batch_process.py
⚡ Procesamiento en Tiempo Real (Spark Streaming + Kafka)
El flujo en tiempo real simula la llegada continua de datos mediante Kafka y los procesa usando Spark Structured Streaming.

🧱 Arquitectura
java
Copiar código
Kafka Producer  →  Kafka Topic (sensor_data)  →  Spark Streaming Consumer
🚀 Configuración y Ejecución Paso a Paso
💡 Importante: Todos los comandos se ejecutan como usuario vboxuser.

1️⃣ Iniciar servicios

# Iniciar ZooKeeper
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

# Iniciar Kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &

2️⃣ Crear el topic de Kafka

/opt/Kafka/bin/kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic sensor_data

3️⃣ Ejecutar el productor (kafka_producer.py)
Este script genera datos simulados (por ejemplo, sensores o viajes) y los envía al topic sensor_data.

python3 kafka_producer.py
Ejemplo de salida:

yaml
Copiar código
Sent: {'sensor_id': 3, 'temperature': 27.1, 'humidity': 53.4, 'timestamp': 1729282738}

4️⃣ Ejecutar el consumidor (spark_streaming_consumer.py)
En otra terminal:

spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 \
  spark_streaming_consumer.py
Ejemplo de salida en consola:

pgsql
Copiar código
+------------------------------------------+----------+------------------+------------------+
|window                                    |sensor_id |avg(temperature)  |avg(humidity)     |
+------------------------------------------+----------+------------------+------------------+
|{2025-10-26 23:35:00, 2025-10-26 23:36:00}|3         |27.4              |52.8              |
+------------------------------------------+----------+------------------+------------------+
💻 Puedes visualizar los Jobs y Stages activos en Spark en:
http://localhost:4040

📊 Evidencias
En la carpeta /evidencias/ del repositorio se incluyen capturas del procesamiento en:

Modo batch (resultados CSV).

Modo streaming (Kafka + Spark Streaming funcionando en tiempo real).

🧰 Estructura del Repositorio

proyecto_spark_movilidad/
├── batch_process.py
├── kafka_producer.py
├── spark_streaming_consumer.py
├── evidencias/
│   ├── batch_resultados.png
│   ├── streaming_kafka.png
│   └── spark_ui.png
└── README.md
✅ Resultados Obtenidos
Batch: identificación de los medios de transporte más usados y sus tiempos promedio.

Streaming: monitoreo continuo de eventos simulados en tiempo real, cálculo de promedios por ventana temporal.

Integración completa de Spark y Kafka, ejecutada en entorno local (sin Docker).

🧾 Conclusiones
El proyecto demuestra la viabilidad de combinar procesamiento batch y en tiempo real en un entorno de Big Data usando Spark y Kafka.
Además, la arquitectura propuesta puede adaptarse fácilmente a escenarios reales de movilidad o IoT para analizar flujos masivos de información.

👩‍💻 Autora
Andrea Gordillo
Proyecto desarrollado para la asignatura Big Data y Análisis en Tiempo Real.
Universidad Nacional Abierta y a Distancia UNAD — 2025.
