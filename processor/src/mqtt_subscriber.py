import paho.mqtt.client as mqtt
import threading
import queue
import json  # Importa o módulo JSON para processar as mensagens


MOISTURE_LIMIT_1 = 20
MOISTURE_LIMIT_2 = 80
TEMPERATURE_LIMIT_1 = 25
TEMPERATURE_LIMIT_2 = 30


class MQTTSubscriber:

    def __init__(self, broker_config):
        self.broker = broker_config['broker']
        self.port = broker_config['port']
        self.user = broker_config['user']
        self.password = broker_config['password']
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
                        if value < MOISTURE_LIMIT_1 or value > MOISTURE_LIMIT_2:
                            alarm_message = json.dumps({
                                "timestamp": timestamp,
                                "upi": 1,
                                "alarm_type": "moisture",
                                "value": value
                            })
                            self.client.publish("lucasl050503@gmail.com/alarm", alarm_message)
                        
                    elif topic == "lucasl050503@gmail.com/UPI1/temperature":
                        if value < TEMPERATURE_LIMIT_1 or value > TEMPERATURE_LIMIT_2:
                            alarm_message = json.dumps({
                                "timestamp": timestamp,
                                "upi": 1,
                                "alarm_type": "temperature",
                                "value": value
                            })
                            self.client.publish("lucasl050503@gmail.com/alarm", alarm_message)
                        
                    elif topic == "lucasl050503@gmail.com/UPI2/moisture":
                        if value < MOISTURE_LIMIT_1 or value > MOISTURE_LIMIT_2:
                            alarm_message = json.dumps({
                                "timestamp": timestamp,
                                "upi": 2,
                                "alarm_type": "moisture",
                                "value": value
                            })
                            self.client.publish("lucasl050503@gmail.com/alarm", alarm_message)
                        
                    elif topic == "lucasl050503@gmail.com/UPI2/temperature":
                        if value < TEMPERATURE_LIMIT_1 or value > TEMPERATURE_LIMIT_2:
                            alarm_message = json.dumps({
                                "timestamp": timestamp,
                                "upi": 2,
                                "alarm_type": "temperature",
                                "value": value
                            })
                            self.client.publish("lucasl050503@gmail.com/alarm", alarm_message)
                        
                    
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
