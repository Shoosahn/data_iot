import mysql.connector

# Konfigurasi koneksi ke database
config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "db_iot"
}

def create_connection():
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print("Koneksi gagal:", err)
        return None

def close_connection(connection):
    if connection.is_connected():
        connection.close()
