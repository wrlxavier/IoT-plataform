import threading
import time
import paho.mqtt.client as mqtt
import json
import psutil

class Publisher:
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
        while cycle_count < 5 and self.running:
            data = self.data_function()
            self.publisher.publish(self.topic, data)
            print(f"Publicado {data} no tópico {self.topic}")
            time.sleep(5)
            cycle_count += 1

    def stop(self):
        self.running = False

def get_cpu_frequency():
    # Substitua com a coleta real de dados
    return f"{psutil.cpu_freq().current}"

def get_cpu_usage():
    # Substitua com a coleta real de dados
    return f"{psutil.cpu_percent(interval=0.5)}"

def get_memory_usage():
    # Substitua com a coleta real de dados
    return f"{psutil.virtual_memory().percent}"

def get_network_io():
    # Substitua com a coleta real de dados
    return json.dumps({"n_input": 1024, "n_output": 2048})