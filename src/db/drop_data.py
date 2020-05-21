# -*- coding: utf-8 -*-
import db
import sql
conn = db.conn
try:
    with conn.cursor() as cursor:
        for query in sql.drop_index:
            cursor.execute(query)
        for query in sql.drop_tables:
            cursor.execute(query)
finally:
    conn.close()

print("Done Drop tables! [stock, stock_price]")