import time
from src.mqtt_subscriber import MQTTSubscriber

if __name__ == "__main__":

    time.sleep(5)
    
    broker_config = {
        "broker": 'www.maqiatto.com',
        "port": 1883,
        "user": "lucasl050503@gmail.com",
        "password": '123456'
    }


    subscriber = MQTTSubscriber(broker_config)
    subscriber.connect()