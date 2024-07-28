from src.postgres_db import PostgresDatabase
import time
import psutil


time.sleep(2)
postgres_db = PostgresDatabase(sql_path='/app/src/init.sql')



print("Frequência da CPU (MHz):", psutil.cpu_freq().current)
print("Uso da CPU (%):", psutil.cpu_percent(interval=0.5))
print("Uso da Memória (%):", psutil.virtual_memory().percent)

io_counters = psutil.net_io_counters()



cpu_frequency = psutil.cpu_freq().current
cpu_usage = psutil.cpu_percent(interval=0.5)
memory_usage = psutil.virtual_memory().percent
n_input = psutil.net_io_counters().bytes_recv
n_output = psutil.net_io_counters().bytes_sent


