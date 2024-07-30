import psycopg2
from datetime import datetime
import pytz

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
        self.tz = pytz.timezone('America/Sao_Paulo')
        self.initialize_database()

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
        except IOError as e:
            raise RuntimeError(f"Error: {e}")
        except psycopg2.Error as e:
            raise RuntimeError(f"PostgreSQL error: {e}")

    def insert_moisture(self, timestamp, upi_id, value):
        """Insere dados na tabela 'moisture'."""
        #timestamp = datetime.fromisoformat(timestamp).astimezone(self.tz)
        timestamp = datetime.fromisoformat(timestamp)
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO moisture (time, upi_id, value) VALUES (%s, %s, %s)",
                    (timestamp, upi_id, value)
                )
                conn.commit()
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de umidade: {e}")

    def insert_temperature(self, timestamp, upi_id, value):
        """Insere dados na tabela 'temperature'."""
        #timestamp = datetime.fromisoformat(timestamp).astimezone(self.tz)
        timestamp = datetime.fromisoformat(timestamp)
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO temperature (time, upi_id, value) VALUES (%s, %s, %s)",
                    (timestamp, upi_id, value)
                )
                conn.commit()
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de temperatura: {e}")

    def insert_upi(self, upi_name):
        """Insere dados na tabela 'upis'."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO upis (upi_name) VALUES (%s) RETURNING id",
                    (upi_name,)
                )
                upi_id = cursor.fetchone()[0]
                conn.commit()
                return upi_id
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de UPI: {e}")
        
    def insert_alarm(self, timestamp, upi, alarm_type, value):
            """Insere dados na tabela 'alarm'."""
            timestamp = datetime.fromisoformat(timestamp)
            try:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO alarm (time, upi, alarm_type, value) VALUES (%s, %s, %s, %s)",
                        (timestamp, upi, alarm_type, value)
                    )
                    conn.commit()
            except psycopg2.Error as e:
                raise RuntimeError(f"Erro ao inserir dados de alarme: {e}")