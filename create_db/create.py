import sqlite3

DATABASE = 'db_tiktok_audience.db'
table_name = 'tb_lno_acima_3000'

with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()

    query = f"CREATE TABLE IF NOT EXISTS {table_name} (p1 TEXT,p2 TEXT,p3 TEXT,p4 TEXT,p5 TEXT,p6 TEXT)"

    cursor.execute(query)