# -*- coding: utf-8 -*-

# migrate
# industry_type[master]
#   id INT : 33事業区分ID
#   name VARCHAR : 名前
# sub_industry_type[master]
#   id INT : 17事業区分ID
#   name VARCHAR : 名前
# market[master]
#   id INT : 市場ID
#   name VARCHAR : 名前
# stock[master]
#   id INT
#   code INT : 株式コード
#   name VARCHAR : 名前
#   market_id INT : 市場ID
#   industry_type_id INT : 33業種区分ID
#   sub_industry_type_id INT : 17業種区分ID
#   version VARCHAR : データバージョン
# stock_price
#   id INT
#   previous_id INT ： 親ID
#   start INT : 開始額
#   hight INT : 最高値
#   low INT : 最安値
#   close INT : 終値
#   vary_code INT : 判定用増減（-1: 減少, 0: 変化なし, +1: 増加 ）

create_market_table = "CREATE TABLE IF NOT EXISTS market(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100));"
create_industry_type_table = "CREATE TABLE IF NOT EXISTS industry_type(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100));"
create_sub_industry_type_table = "CREATE TABLE IF NOT EXISTS sub_industry_type(id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100));"

create_stock_table = "CREATE TABLE IF NOT EXISTS stock(id INT PRIMARY KEY AUTO_INCREMENT, code INT, name VARCHAR(100), market_id INT, industry_type_id INT, sub_industry_type_id INT, version VARCHAR(8));"
create_stock_indexs =[
    "CREATE UNIQUE INDEX IF NOT EXISTS code_index ON stock (code);"
]

create_stock_price = "CREATE TABLE IF NOT EXISTS stock_price(id INT PRIMARY KEY AUTO_INCREMENT, previous_id INT, code INT, date DATETIME(6), start INT, hight INT, low INT, close INT, vary_code INT);"
create_stock_price_indexs = [
    "CREATE INDEX IF NOT EXISTS code_index ON stock_price (code);",
    "CREATE INDEX IF NOT EXISTS previous_id_index ON stock_price (previous_id);",
    "CREATE INDEX IF NOT EXISTS vary_code_index ON stock_price (vary_code);"
]
create_view_sql = "CREATE VIEW search_vary_code AS "\
                  "select "\
                  "d1.code as stock_code, "\
                  "d1.id as older_id, d1.vary_code as older_vary, "\
                  "d2.id as d2_id, d2.vary_code as d2_varyd, "\
                  "d3.id as d3_id, d3.vary_code as d3_varyd, "\
                  "d4.id as d4_id, d4.vary_code as d4_varyd, "\
                  "d5.id as newest_id, d5.vary_code as newest_varyd "\
                  "from stock_price as d1 "\
                  "inner join stock_price as d2 on d2.previous_id = d1.id "\
                  "inner join stock_price as d3 on d3.previous_id = d2.id "\
                  "inner join stock_price as d4 on d4.previous_id = d3.id "\
                  "inner join stock_price as d5 on d5.previous_id = d4.id "\
                  "where d1.vary_code is not NULL;"

# insert master data
insert_stock_sql = "INSERT INTO "\
                   "stock (code, name, market_id, industry_type_id, sub_industry_type_id, version) "\
                   "VALUES(%(code)s, %(name)s, %(market_id)s, %(industry_type_id)s, %(sub_industry_type_id)s, %(version)s);"
insert_only_name_master_sql = "INSERT INTO {0} (name) VALUES(%(name)s);"
select_master_id_by_name = "select id from {0} where name = %(name)s;"

# insert stock_price data
select_tousyou_stok_sql = "select code, name, market.name as market_name from stock inner join market on market.id = stock.market_id where market.name like '市場%' and market.name like '%（内国株）%';"
insert_stock_price_sql = "INSERT INTO "\
                         "stock_price (previous_id, code, date, start, hight, low, close, vary_code) "\
                         "VALUES(%(previous_id)s, %(code)s, %(date)s, %(start)s, %(hight)s, %(low)s, %(close)s, %(vary_code)s);"

# drop data
drop_index = [
  "DROP INDEX code_index ON stock;",
  "DROP INDEX code_index ON stock_price;",
  "DROP INDEX vary_code_index ON stock_price;",
  "DROP INDEX previous_id_index ON stock_price;"
]
drop_tables = [
  "DROP TABLE IF EXISTS stock;",
  "DROP TABLE IF EXISTS stock_price;",
  "DROP TABLE IF EXISTS market;",
  "DROP TABLE IF EXISTS industry_type;",
  "DROP TABLE IF EXISTS sub_industry_type;"
]

# search same data
