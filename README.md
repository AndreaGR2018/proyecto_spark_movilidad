🚦 Proyecto Spark Movilidad

Análisis de movilidad en Bogotá con Apache Spark y Kafka

🧩 Introducción

Este proyecto analiza datos de movilidad en Bogotá utilizando Apache Spark y Apache Kafka para el procesamiento tanto batch como en tiempo real.
El conjunto de datos contiene información sobre los medios de transporte utilizados por los ciudadanos en sus viajes diarios, permitiendo identificar patrones de desplazamiento y comportamientos de movilidad urbana.

🗺️ Definición del problema y conjunto de datos

El propósito de este proyecto es analizar los patrones de movilidad de los ciudadanos de Bogotá a partir de datos de encuestas sobre viajes, con el fin de identificar:

Los medios de transporte más utilizados.

Los horarios de mayor flujo de viajes.

Los tiempos promedio de desplazamiento según el medio de transporte.

El conjunto de datos utilizado proviene de la Encuesta de Movilidad de Bogotá (Encuesta_movilidad.csv), disponible públicamente en fuentes abiertas como Kaggle y el portal de datos abiertos de Colombia.
Este dataset contiene información de viajes con campos como:
ID_ENCUESTA, NUMERO_PERSONA, MOTIVOVIAJE, MUNICIPIO_DESTINO, HORA_INICIO, HORA_FIN, TIEMPO_CAMINO y MEDIO_PRE.

⚙️ Arquitectura de la Solución

La arquitectura incluye los siguientes componentes principales:

Kafka 📨: para la transmisión de mensajes en tiempo real.

Spark Structured Streaming ⚙️: para el procesamiento continuo de los datos recibidos desde Kafka.

Docker Compose 🐳: para levantar los servicios de Kafka y Zookeeper fácilmente.

Python 🐍: para generar los mensajes (productor) y procesarlos (consumidor).

📁 Archivos Principales
Archivo	Descripción
batch_process.py	Realiza el análisis inicial del dataset en modo batch (limpieza, transformación y cálculo de promedios).
producer_generator.py	Envía los registros del dataset al tópico de Kafka (movilidad_bogota).
streaming_kafka.py	Consume los mensajes desde Kafka y los procesa en tiempo real con Spark.
docker-compose.yml	Define los contenedores de Kafka y Zookeeper.
Encuesta_movilidad.csv	Dataset base con la información de los registros.
🚀 Ejecución del procesamiento batch (Apache Spark)
📌 Descripción

El procesamiento batch se encarga de analizar los datos históricos de movilidad ciudadana en Bogotá, obtenidos de la encuesta de movilidad.
Este proceso permite identificar patrones de uso de transporte, horarios de mayor flujo y tiempos promedio de desplazamiento.

El script principal es:

batch_process.py

⚙️ Ejecución del script

Para ejecutar el procesamiento batch desde el entorno Hadoop/Spark (en la máquina virtual Ubuntu Server), se usa el siguiente comando:

cd ~/datasets/encuesta_movilidad
spark-submit batch_process.py


💡 Asegúrate de haber iniciado los servicios de Hadoop y configurado correctamente las variables de entorno de Spark antes de ejecutar el comando.

🧮 Proceso realizado

El script realiza las siguientes operaciones:

Carga del dataset desde un archivo CSV (encuesta de movilidad).

Limpieza y transformación de datos, eliminando valores nulos y columnas innecesarias.

Agrupación y análisis de los viajes por medio de transporte, hora y duración promedio.

Generación de resultados en consola o archivos CSV, listos para visualización y análisis posterior.

📸 Ejemplo de salida

Evidencia de la ejecución del procesamiento batch en la consola de Spark:

+------------------+-------------+-------------------+
|medio_transporte  |cantidad_viajes|tiempo_promedio_min|
+------------------+-------------+-------------------+
|Transmilenio      |  14532      |       43.2        |
|Bus Urbano        |   9560      |       39.7        |
|Automóvil Particular |  7843     |       35.4        |
|Bicicleta         |   3241      |       27.1        |
+------------------+-------------+-------------------+

📁 Resultados

Los resultados generados se almacenan en la carpeta local:

~/datasets/encuesta_movilidad/output_batch/


Cada archivo contiene los datos procesados por Spark listos para análisis o visualización.

🧠 Conclusiones

El procesamiento batch permitió obtener una visión general de los patrones de movilidad, destacando los medios de transporte con mayor uso y los tiempos promedio de desplazamiento.
Estos resultados sirven como base para comparar con el análisis en tiempo real (streaming) mediante Apache Kafka y Spark Streaming.

🔁 Procesamiento en Tiempo Real (Streaming)

El procesamiento en tiempo real se realiza con Kafka + Spark Streaming:

1️⃣ Kafka recibe los mensajes generados por el productor (producer_generator.py).
2️⃣ Spark Streaming (en streaming_kafka.py) consume esos mensajes desde el tópico.
3️⃣ Los datos se agrupan por tipo de medio de transporte (MEDIO_PRE) y se muestran los resultados en tiempo real.

▶️ Ejecución del Proyecto
1️⃣ Levantar los contenedores de Kafka y Zookeeper

Desde el directorio del proyecto:

sudo docker-compose up -d

2️⃣ Ejecutar el Productor (envía datos a Kafka)
python3 producer_generator.py

3️⃣ Ejecutar el Consumidor (procesa los datos en Spark)

En otra terminal:

spark-submit streaming_kafka.py

📊 Visualización de Resultados

El sistema imprime en consola los resultados en tiempo real, mostrando el conteo de viajes por tipo de medio de transporte.

📸 Ejemplo de salida del streaming:

+-------------+-----+
| MEDIO_PRE   |count|
+-------------+-----+
| transmilenio| 235 |
| bus         | 204 |
| bicicleta   | 128 |
| peaton      | 226 |
| carro       | 142 |
| taxi        | 80  |
| moto        | 135 |
+-------------+-----+


Además, el procesamiento batch genera archivos CSV con resultados agregados en la carpeta resultados/.
---

## 📸 Evidencias del Proyecto

A continuación, se presentan las principales evidencias del funcionamiento del proyecto, desde el procesamiento batch hasta el flujo de datos en tiempo real con Kafka y Spark Streaming.

### 🧾 1. Procesamiento Batch
Ejecución del script `batch_process.py` para procesar el conjunto de datos y generar los resultados agregados.
  
![Procesamiento Batch](evidencias/01_datos_batch_process.png)

---

### 📊 2. Resultados del Procesamiento Batch
Visualización del archivo generado con los conteos por tipo de medio de transporte.

![Resultados CSV](evidencias/02_resultados_batch_csv.png)

---

### 🚀 3. Productor Kafka Enviando Datos
Simulación del flujo de datos en tiempo real desde el productor hacia el tópico de Kafka.

![Productor Kafka](evidencias/03_kafka_productor.png)

---

### ⚙️ 4. Spark Streaming en Ejecución
Ejecución del proceso `streaming_kafka.py` mostrando los resultados del análisis en tiempo real.

![Spark Streaming](evidencias/04_spark_streaming.png)

---

### 💻 5. Repositorio en GitHub
Estructura final del repositorio con el código fuente, scripts y documentación del proyecto.

![Repositorio GitHub](evidencias/05_github_repo.png)

---

🔗 Enlaces

📂 Repositorio del proyecto: GitHub - Proyecto Spark Movilidad

🎥 Video explicativo: (pendiente de grabar)

🧑‍💻 Autores

Proyecto desarrollado por:
Andrea Gordillo Rojas
Universidad Nacional Abierta y a Distancia (UNAD)
Curso: Big Data – 2025
