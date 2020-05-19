# -*- coding: utf-8 -*-
import db
import sql
conn = db.conn

try:
    with conn.cursor() as cursor:
        cursor.execute(sql.create_stock_table)
        for stock_index in sql.create_stock_indexs:
            cursor.execute(stock_index)
        cursor.execute(sql.create_stock_price)
        for stock_price_index in sql.create_stock_price_indexs:
            cursor.execute(stock_price_index)
finally:
    conn.close()

print("Done Create tables! [stock, stock_price]")