# -*- coding: utf-8 -*-

# migrate
# stock
#   id INT
#   code INT : 株式コード
#   name VARCHAR : 名前
# stock_price
#   id INT
#   previous_id INT ： 親ID
#   start INT : 開始額
#   hight INT : 最高値
#   low INT : 最安値
#   close INT : 終値
#   vary_percent INT : 判定用増減率（小数値第1位切り捨て）
#   vary_code INT : 簡易判定用増減（-1: 減少, 0: 変化なし, +1: 増加 ）

create_stock_table = "CREATE TABLE IF NOT EXISTS stock(id INT PRIMARY KEY AUTO_INCREMENT, code INT, name VARCHAR(100));"
create_stock_indexs =[
    "CREATE UNIQUE INDEX IF NOT EXISTS code_index ON stock (code);"
]

create_stock_price = "CREATE TABLE IF NOT EXISTS stock_price(id INT PRIMARY KEY AUTO_INCREMENT, previous_id INT, code INT, date DATETIME(6), start INT, hight INT, low INT, close INT, vary_percent INT, vary_code INT);"
create_stock_price_indexs = [
    "CREATE INDEX IF NOT EXISTS code_index ON stock_price (code);",
    "CREATE INDEX IF NOT EXISTS previous_id_index ON stock_price (previous_id);",
    "CREATE INDEX IF NOT EXISTS vary_percent_index ON stock_price (vary_percent);",
    "CREATE INDEX IF NOT EXISTS vary_code_index ON stock_price (vary_code);"
]

# insert data
insert_stock_sql = "INSERT INTO stock (code, name) VALUES(%(code)s, %(name)s);"
insert_stock_price_sql = "INSERT INTO "\
                         "stock_price (previous_id, code, date, start, hight, low, close, vary_percent, vary_code) "\
                         "VALUES(%(previous_id)s, %(code)s, %(date)s, %(start)s, %(hight)s, %(low)s, %(close)s, %(vary_percent)s, %(vary_code)s);"

# drop data
drop_index = [
  "DROP INDEX code_index ON stock;",
  "DROP INDEX code_index ON stock_price;",
  "DROP INDEX vary_percent_index ON stock_price;",
  "DROP INDEX vary_code_index ON stock_price;",
  "DROP INDEX previous_id_index ON stock_price;"
]
drop_tables = [
  "DROP TABLE IF EXISTS stock;",
  "DROP TABLE IF EXISTS stock_price;"
]