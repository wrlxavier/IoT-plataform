import os
import psycopg2



class PostgresDatabase:

    def __init__(self, sql_path="src/init.sql"):

        self.db_config = {
            'database': "postgres",
            'user': "admin",
            'password': "admin",
            'host': "localhost",
            'port': "5432"
        }

        self.sql_path = sql_path
        #self.initialize_database()

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
        

    def insert_cpu_frequency(self, timestamp, value):
        """Insere dados na tabela 'cpu_frequency'."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cpu_frequency (time, value) VALUES (%s, %s)", (timestamp, value))
                conn.commit()
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de frequência: {e}")
        
    def insert_cpu_usage(self, timestamp, value):
        """Insere dados na tabela 'cpu_usage'."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cpu_usage (time, value) VALUES (%s, %s)", (timestamp, value))
                conn.commit()
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de uso de CPU: {e}")
        
    def insert_memory_usage(self, timestamp, value):
        """Insere dados na tabela 'memory_usage'."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO memory_usage (time, value) VALUES (%s, %s)", (timestamp, value))
                conn.commit()
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de uso de memória: {e}")
        
    def insert_network_io(self, timestamp, n_input, n_output):
        """Insere dados na tabela 'network_io'."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO network_io (time, n_input, n_output) VALUES (%s, %s, %s)", (timestamp, n_input, n_output))
                conn.commit()
        except psycopg2.Error as e:
            raise RuntimeError(f"Erro ao inserir dados de uso de input e output de rede: {e}")