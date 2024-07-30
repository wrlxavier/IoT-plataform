from src.postgres_db import PostgresDatabase
from src.mqtt_subscriber import MQTTSubscriber
import time

if __name__ == "__main__":

    time.sleep(5)
    
    broker_config = {
        "broker": 'www.maqiatto.com',
        "port": 1883,
        "user": "lucasl050503@gmail.com",
        "password": '123456'
    }

    db = PostgresDatabase('/app/src/init.sql')

    subscriber = MQTTSubscriber(broker_config, db)
    subscriber.connect()