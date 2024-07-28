import threading
import time
import paho.mqtt.client as mqtt
import json
import psutil
from datetime import datetime
from postgres_db import PostgresDatabase


class MQTTPublisher:
    def __init__(self, broker, port, user, password):
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.client = mqtt.Client()
        self.client.username_pw_set(self.user, self.password)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com sucesso. Código de resultado:", rc)

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


class DataPublisher(threading.Thread):
    def __init__(self, publisher, topic, data_function):
        super().__init__()
        self.publisher = publisher
        self.topic = topic
        self.data_function = data_function
        self.running = True

    def run(self):
        cycle_count = 0
        while cycle_count < 5000 and self.running:
            data = self.data_function()
            self.publisher.publish(self.topic, data)
            print(f"Publicado {data} no tópico {self.topic}")
            time.sleep(1)
            cycle_count += 1

    def stop(self):
        self.running = False

# Funções de coleta de dados
def get_cpu_frequency():
    return f"{psutil.cpu_freq().current}"

def get_cpu_usage():
    return f"{psutil.cpu_percent(interval=1)}"

def get_memory_usage():
    return f"{psutil.virtual_memory().percent}"

def get_network_io():
    return json.dumps({"n_input": 1024, "n_output": 2048})


class MQTTSubscriber(threading.Thread):
    def __init__(self, broker, port, user, password, topics, db_handler):
        super().__init__()
        self.broker = broker
        self.port = port
        self.user = user
        self.password = password
        self.topics = topics
        self.db_handler = db_handler
        self.client = mqtt.Client()
        self.client.username_pw_set(self.user, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.running = True

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com sucesso. Código de resultado:", rc)
        for topic in self.topics:
            client.subscribe(topic)
            print(f"Inscrito no tópico: {topic}")

    def on_message(self, client, userdata, msg):
        if self.running:
            timestamp = datetime.now()
            payload = msg.payload.decode()
            print(f"Recebido {payload} do tópico {msg.topic}")

            if msg.topic.endswith("cpu_frequency"):
                self.db_handler.insert_cpu_frequency(timestamp, payload)
            elif msg.topic.endswith("cpu_usage"):
                self.db_handler.insert_cpu_usage(timestamp, payload)
            elif msg.topic.endswith("memory_usage"):
                self.db_handler.insert_memory_usage(timestamp, payload)
            elif msg.topic.endswith("network_io"):
                data = json.loads(payload)
                self.db_handler.insert_network_io(timestamp, data["n_input"], data["n_output"])

    def run(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

    def stop(self):
        self.running = False
        self.client.disconnect()

# Função principal
if __name__ == "__main__":
    # Configurações do MQTT
    MQTT_BROKER = 'www.maqiatto.com'
    MQTT_PORT = 1883
    MQTT_USER = 'warleyxavier.fernandes@gmail.com'
    MQTT_PASSWORD = 'wZn&y6Pt'

    # Configuração do Banco de Dados PostgreSQL
    db_handler = PostgresDatabase("init.sql")

    # Criar instância do Publisher
    publisher = MQTTPublisher(MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
    publisher.connect()

    # Tópicos e funções de dados para publicação
    topics = [
        "warleyxavier.fernandes@gmail.com/device_1/cpu_frequency",
        "warleyxavier.fernandes@gmail.com/device_1/cpu_usage",
        "warleyxavier.fernandes@gmail.com/device_1/memory_usage",
        "warleyxavier.fernandes@gmail.com/device_1/network_io"
    ]
    data_functions = [get_cpu_frequency, get_cpu_usage, get_memory_usage, get_network_io]

    # Criar e iniciar threads de publicação
    publisher_threads = []
    for topic, data_function in zip(topics, data_functions):
        thread = DataPublisher(publisher, topic, data_function)
        publisher_threads.append(thread)
        thread.start()

    # Criar e iniciar o subscriber
    subscriber = MQTTSubscriber(MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, topics, db_handler)
    subscriber.start()

    try:
        # Manter o programa em execução
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
        # Parar threads de publicação
        for thread in publisher_threads:
            thread.stop()
        # Parar o subscriber
        subscriber.stop()

    finally:
        # Desconectar o publisher
        publisher.disconnect()
        # Fechar a conexão com o banco de dados
        db_handler.close()
