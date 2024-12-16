import happybase
import pandas as pd
from datetime import datetime

# Establecer conexión con HBase
connection = happybase.Connection('localhost')
print("Admin: Yerelin Marcela Valencia Posada")
print("Conexión establecida con HBase")
table_name = 'juventud'
families = {
    'info': dict()
}

# Eliminar la tabla si ya existe
if table_name.encode() in connection.tables():
    print(f"Eliminando tabla existente - {table_name}")
    connection.delete_table(table_name, disable=True)

# Crear nueva tabla
connection.create_table(table_name, families)
table = connection.table(table_name)
print("Tabla 'juventud' creada exitosamente")

# Leer el archivo CSV
csv_file = 'data/juventud.csv'
df = pd.read_csv(csv_file, encoding='utf-8')

# Cargar los datos en la tabla HBase juventud
for index, row in df.iterrows():
    row_key = f'juventud_{index}'.encode()
    data = {
        b'info:a_o': str(row['a_o']).encode(),
        b'info:edad': str(row['edad']).encode(),
        b'info:zona': row['zona'].encode(),
        b'info:genero': row['genero'].encode(),
        b'info:etnia': row['etnia'].encode(),
        b'info:discapacidad': row['discapacidad'].encode(),
        b'info:escolaridad': row['escolaridad'].encode() if pd.notnull(row['escolaridad']) else b''
    }
    table.put(row_key, data)

print("Datos cargados exitosamente")

connection.close()
print("Conexión cerrada")