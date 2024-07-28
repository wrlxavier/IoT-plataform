import os
import psycopg2
import pytz
from datetime import datetime


class PostgresDatabase:

    def __init__(self, sql_path="src/init.sql"):

        self.db_config = {
            'database': "postgres",
            'user': "admin",
            'password': "admin",
            'host': "postgres",
            'port': "5432"
        }

        self.sql_path = sql_path
        self.initialize_database()
        self.tz = pytz.timezone('America/Sao_Paulo')

    def get_connection(self):
        return psycopg2.connect(
            dbname=self.db_config['database'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            host=self.db_config['host'],
            port=self.db_config['port']
        )

    def initialize_database(self):
        try:
            with open(self.sql_path, 'r') as file:
                sql_script = file.read()
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_script)
                conn.commit()
                print('\n\n\n\n\n\nScriopt SQL executado com sucesso!\n\n\n\n\n\n')
        except IOError as e:
            raise RuntimeError(f"Error: {e}")
        except psycopg2.Error as e:
            raise RuntimeError(f"PostgreSQL error: {e}")
        
    def insert_moisture(self, value):
        """Insere dados na tabela 'moisture'."""
        timestamp = datetime.now().astimezone(self.tz)
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO moisture (time, value) VALUES (%s, %s)", (timestamp, value))
                conn.commit()
                #print("Dados de umidade inseridos com sucesso.")
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de umidade: {e}")

    def insert_temperature(self, value):
        """Insere dados na tabela 'temperature'."""
        timestamp = datetime.now().astimezone(self.tz)
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO temperature (time, value) VALUES (%s, %s)", (timestamp, value))
                conn.commit()
                #print("Dados de temperatura inseridos com sucesso.")
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de temperatura: {e}")