import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from PIL import Image
import io

# Configuración de la conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host='localhost',
    user='Raymundo',
    password='raymundo1234',
    database='imagenes_db'
)

def guardar_imagen(nombre, ruta):
    try:
        with open(ruta, 'rb') as imagen_file:
            imagen_binaria = imagen_file.read()

        cursor = conexion.cursor()
        insert_query = "INSERT INTO fotografia (nombre, imagen) VALUES (%s, %s)"
        cursor.execute(insert_query, (nombre, imagen_binaria))
        conexion.commit()
        print("Imagen guardada con éxito.")
    except Error as e:
        print("Error al guardar la imagen:", e)

def mostrar_imagen(nombre, imagen_binaria):
    try:
        img = Image.open(io.BytesIO(imagen_binaria))
        img.show()
        print(f"Mostrando la imagen '{nombre}' en una ventana.")
    except Exception as e:
        print("Error al mostrar la imagen:", e)

def recuperar_imagen(id):
    try:
        cursor = conexion.cursor()
        select_query = "SELECT nombre, imagen FROM fotografia WHERE id = %s"
        cursor.execute(select_query, (id,))
        fila = cursor.fetchone()

        if fila:
            nombre, imagen_binaria = fila
            mostrar_imagen(nombre, imagen_binaria)
        else:
            print("No se encontró ninguna imagen con el ID proporcionado.")
    except Error as e:
        print("Error al recuperar la imagen:", e)

if __name__ == '__main__':
    try:
        cursor = conexion.cursor()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS fotografia (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                imagen LONGBLOB
            )
        '''
        cursor.execute(create_table_query)
        conexion.commit()

        opcion = input("¿Deseas guardar una imagen (1) o recuperar una imagen (2)? ")

        if opcion == '1':
            nombre = input("Ingrese el nombre de la imagen: ")
            ruta = input("Ingrese la ruta de la imagen: ")
            guardar_imagen(nombre, ruta)
        elif opcion == '2':
            id = int(input("Ingrese el ID de la imagen a recuperar: "))
            recuperar_imagen(id)
        else:
            print("Opción no válida.")
    except Error as e:
        print("Error en la operación:", e)
    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión a la base de datos cerrada.")
