# -*- coding: utf-8 -*-
import db
import sql
import db_lib

conn = db.conn
create_tables = [
            sql.create_market_table,
            sql.create_industry_type_table,
            sql.create_sub_industry_type_table,
            sql.create_stock_table,
            sql.create_stock_price,
            sql.create_stock_indexs,
            sql.create_stock_price_indexs,
            sql.create_view_sql
        ]

try:
    with conn.cursor() as cursor:   
        for query in db_lib.flatten(create_tables):
            print query
            cursor.execute(query)
finally:
    conn.close()

print("Done Create tables! [stock, stock_price]")