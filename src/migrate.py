# -*- coding: utf-8 -*-
import db
conn = db.conn

# stock
#   id INT
#   code INT : 株式コード
#   name VARCHAR : 名前
# stock_price
#   id INT
#   start INT : 開始額
#   hight INT : 最高値
#   low INT : 最安値
#   close INT : 終値
#   vary_percent INT : 判定用増減率（小数値第1位切り捨て）
create_stock_table = "CREATE TABLE IF NOT EXISTS stock(id INT PRIMARY KEY AUTO_INCREMENT, code INT, name VARCHAR(100));"
create_stock_indexs =[
    "CREATE UNIQUE INDEX IF NOT EXISTS code_index ON stock (code);"
]                    
create_stock_price = "CREATE TABLE IF NOT EXISTS stock_price(id INT PRIMARY KEY AUTO_INCREMENT, code INT, date DATETIME(6), start INT, high INT, low INT, close INT, vary_percent INT);"
create_stock_price_indexs = [
    "CREATE INDEX IF NOT EXISTS code_index ON stock_price (code);",
    "CREATE INDEX IF NOT EXISTS vary_percent_index ON stock_price (vary_percent);"
]

try:
    with conn.cursor() as cursor:
        cursor.execute(create_stock_table)
        for stock_index in create_stock_indexs:
            cursor.execute(stock_index)
        cursor.execute(create_stock_price)
        for stock_price_index in create_stock_price_indexs:
            cursor.execute(stock_price_index)
finally:
    conn.close()

print("Done Create tables! [stock, stock_price]")