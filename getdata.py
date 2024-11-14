import mysql
from koneksi import create_connection, close_connection


def get_data():
    # Membuat koneksi
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        try:
            # Query untuk mengambil data maksimum suhu, minimum suhu, dan rata-rata suhu
            query_summary = "SELECT MAX(suhu) AS suhu_max, MIN(suhu) AS suhu_min, AVG(suhu) AS suhu_avg FROM tb_cuaca"
            cursor.execute(query_summary)
            row = cursor.fetchone()

            # Array untuk menyimpan data output
            data_output = {}
            if row:
                data_output['suhu_max'] = row['suhu_max']
                data_output['suhu_min'] = row['suhu_min']
                data_output['suhu_avg'] = round(row['suhu_avg'], 2)

            # Query untuk mendapatkan data di mana suhu dan humid berada di nilai maksimum bersamaan
            query_max_data = """
                SELECT id, suhu, humid, lux, ts 
                FROM tb_cuaca 
                WHERE suhu = %s AND humid = (SELECT MAX(humid) FROM tb_cuaca)
            """
            cursor.execute(query_max_data, (data_output['suhu_max'],))
            nilai_suhu_max_humid_max = cursor.fetchall()

            # Memasukkan data hasil query ke dalam data_output
            if nilai_suhu_max_humid_max:
                data_output['nilai_suhu_max_humid_max'] = [
                    {
                        'id': item['id'],
                        'suhu': item['suhu'],
                        'humid': item['humid'],
                        'lux': item['lux'],
                        'timestamp': item['ts']
                    }
                    for item in nilai_suhu_max_humid_max
                ]

            # Query untuk mendapatkan dua data month_year dalam format yang diinginkan
            query_month_year_max = """
                SELECT DISTINCT DATE_FORMAT(ts, '%c-%Y') AS month_year 
                FROM tb_cuaca 
                WHERE suhu = %s AND humid = (SELECT MAX(humid) FROM tb_cuaca) 
                LIMIT 2
            """
            cursor.execute(query_month_year_max, (data_output['suhu_max'],))
            month_year_max = cursor.fetchall()

            # Memasukkan month_year_max ke dalam data_output
            data_output['month_year_max'] = [
                {"month_year": item['month_year']} for item in month_year_max]

            # Mengembalikan data dalam format dictionary
            return data_output

        except mysql.connector.Error as err:
            print("Error saat mengambil data:", err)
            return {"error": str(err)}

        finally:
            cursor.close()
            close_connection(conn)

    else:
        print("Tidak dapat terhubung ke database.")
        return {"error": "Tidak dapat terhubung ke database"}


# Jika file ini dijalankan langsung, tampilkan data ke konsol
if __name__ == "__main__":
    print(get_data())
