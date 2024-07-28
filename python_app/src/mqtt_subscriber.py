import paho.mqtt.client as mqtt
from src.postgres_db import PostgresDatabase



class MQTTSubscriber:

    def __init__(self, postgres_db: PostgresDatabase):

        self.client = mqtt.Client()
        self.postgres_db = postgres_db

        self.broker_config = {
            "broker": 'www.maqiatto.com',
            "port": 1883,
            "user": "lucasl050503@gmail.com",
            "password": '123456'
        }

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado com sucesso. Código de resultado:", rc)
        client.subscribe("lucasl050503@gmail.com/UPI1/moisture")
        client.subscribe("lucasl050503@gmail.com/UPI1/temperature")


    def on_message(self, client, userdata, msg):
        print(f"Recebido mensagem em {msg.topic}: {msg.payload.decode()}")
        if msg.topic == "lucasl050503@gmail.com/UPI1/moisture":
            self.postgres_db.insert_moisture(msg.payload.decode())
            #insert_data("moisture", msg.payload.decode())
        elif msg.topic == "lucasl050503@gmail.com/UPI1/temperature":
            self.postgres_db.insert_temperature(msg.payload.decode())
            #insert_data("temperature", msg.payload.decode())


    def run(self):

        self.client.username_pw_set(self.broker_config['user'], 
                                    self.broker_config['password'])

        self.client.connect(self.broker_config['broker'], 
                            self.broker_config['port'], 60)
        
        self.client.loop_forever()