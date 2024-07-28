from src.postgres_db import PostgresDatabase
from src.mqtt_subscriber import MQTTSubscriber
import time


time.sleep(2)
postgres_db = PostgresDatabase(sql_path='/app/src/init.sql')
mqtt_subscriber = MQTTSubscriber(postgres_db=postgres_db)

mqtt_subscriber.run()





