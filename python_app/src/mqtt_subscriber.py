import paho.mqtt.client as mqtt
import threading
import queue
import json  # Importa o módulo JSON para processar as mensagens

class MQTTSubscriber:

    def __init__(self, broker_config, db):
        self.broker = broker_config['broker']
        self.port = broker_config['port']
        self.user = broker_config['user']
        self.password = broker_config['password']
        self.db = db
        self.client = mqtt.Client()

        self.client.username_pw_set(self.user, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self.process_queue)
        self.worker_thread.start()

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("lucasl050503@gmail.com/UPI1/moisture")
        client.subscribe("lucasl050503@gmail.com/UPI1/temperature")
        client.subscribe("lucasl050503@gmail.com/UPI2/moisture")
        client.subscribe("lucasl050503@gmail.com/UPI2/temperature")
        client.subscribe("lucasl050503@gmail.com/alarm")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        print(f"Received message on topic {topic}: {payload}")
        
        # Enfileira a mensagem para processamento posterior
        self.queue.put((topic, payload))

    def process_queue(self):
        while True:
            topic, payload = self.queue.get()
            try:
                # Decodifica o JSON da carga útil
                message = json.loads(payload)
                timestamp = message.get("timestamp")
                value = message.get("value")

                if timestamp and value is not None:

                    if topic == "lucasl050503@gmail.com/UPI1/moisture":
                        self.db.insert_moisture(timestamp, 1, value)
                    elif topic == "lucasl050503@gmail.com/UPI1/temperature":
                        self.db.insert_temperature(timestamp, 1, value)
                    elif topic == "lucasl050503@gmail.com/UPI2/moisture":
                        self.db.insert_moisture(timestamp, 2, value)
                    elif topic == "lucasl050503@gmail.com/UPI2/temperature":
                        self.db.insert_temperature(timestamp, 2, value)
                    elif topic == "lucasl050503@gmail.com/alarm":
                        upi = message.get('upi')
                        alarm_type = message.get('alarm_type')
                        self.db.insert_alarm(timestamp, upi, alarm_type, value)
                    
                else:
                    print(f"Mensagem inválida: {payload}")
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
            except ValueError as e:
                print(f"Erro ao processar valor: {e}")
            except Exception as e:
                print(f"Erro inesperado: {e}")
            finally:
                self.queue.task_done()
