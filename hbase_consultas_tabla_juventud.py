import happybase
import pandas as pd

# Establecer conexión con HBase
connection = happybase.Connection('localhost')
print("Admin: Yerelin Marcela Valencia Posada")
print("Conexión establecida con HBase")
table_name = 'juventud'
table = connection.table(table_name)

# Leer el archivo CSV
csv_file = 'data/juventud.csv'
df = pd.read_csv(csv_file, encoding='utf-8')

# Cargar los datos en la tabla HBase
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

# Consultas de selección, filtrado y recorrido
print("\n=== Primeros 5 registros ===")
for key, data in table.scan(limit=5):
    print(f"Row key: {key.decode()}")
    for column, value in data.items():
        print(f"{column.decode()}: {value.decode()}")
    print()

# Encontrar registros con edad menor a 18
print("\n=== Registros con edad menor a 18 ===")
for key, data in table.scan():
    if int(data[b'info:edad'].decode()) < 18:
        print(f"\nID: {key.decode()}")
        print(f"Edad: {data[b'info:edad'].decode()}")
        print(f"Nombre: {data[b'info:genero'].decode()}")

# Análisis de registros por zona
print("\n=== Registros por zona ===")
zona_counts = {}

for key, data in table.scan():
    zona = data[b'info:zona'].decode()
    zona_counts[zona] = zona_counts.get(zona, 0) + 1

for zona, count in zona_counts.items():
    print(f"Zona {zona}: {count}")

# Operaciones de escritura (inserción, actualización y eliminación)

# Inserción de un nuevo registro
new_row_key = b'juventud_new'
new_data = {
    b'info:a_o': b'2024',
    b'info:edad': b'18',
    b'info:zona': b'Urbana',
    b'info:genero': b'Masculino',
    b'info:etnia': b'Mestizo',
    b'info:discapacidad': b'Ninguna',
    b'info:escolaridad': b'Bachiller'
}
table.put(new_row_key, new_data)
print("Nuevo registro insertado")

# Actualización de un registro
update_row_key = b'juventud_0'
update_data = {b'info:escolaridad': b'Profesional'}
table.put(update_row_key, update_data)
print("Registro actualizado")

# Eliminación de un registro
delete_row_key = b'juventud_new'
table.delete(delete_row_key)
print("Registro eliminado")

connection.close()