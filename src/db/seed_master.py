# -*- coding: utf-8 -*-
# Run example
# all data insert
#   python seed_master.py

import pandas as pd
import os

import db
import sql
import db_lib

def find_or_insert_master_id(conn, cursor, table_name, value):
    data = { "name": str(value)}
    cursor.execute(sql.select_master_id_by_name.format(str(table_name)), data)
    count = cursor.rowcount
    if count == 0:
        cursor.execute(sql.insert_only_name_master_sql.format(str(table_name)), data)  
        conn.commit()
        return cursor.lastrowid
    else:
        return cursor.fetchone()[0]     

    
conn = db.conn

# original data
#   その他統計資料 東証上場銘柄一
# 覧
#   https://www.jpx.co.jp/markets/statistics-equities/misc/01.html
stock_master_csv_path = os.getcwd() + "/db/seed/code_master.csv"

stock_master_data = pd.read_csv(stock_master_csv_path, encoding= "utf-8")
stock_codes = stock_master_data['code']
stock_names = stock_master_data['name']
stock_markets = stock_master_data['market']
stock_industry_types = stock_master_data['industry_type']
stock_sub_industry_types = stock_master_data['sub_industry_type']
stock_versions = stock_master_data['version']

try:
    with conn.cursor() as cursor:
        for n in range(len(stock_codes)):
            # find or create master tables
            market_id = find_or_insert_master_id(conn, cursor, "market", stock_markets[n].encode("utf-8"))
            industry_type_id = find_or_insert_master_id(conn, cursor, "industry_type", stock_industry_types[n].encode("utf-8"))
            sub_industry_type_id = find_or_insert_master_id(conn, cursor, "sub_industry_type", stock_sub_industry_types[n].encode("utf-8"))

            # create stock
            insert_data = {
                "code": int(stock_codes[n]),
                "name": stock_names[n].encode("utf-8"),
                "market_id": market_id,
                "industry_type_id": industry_type_id,
                "sub_industry_type_id": sub_industry_type_id,
                "version": str(stock_versions[n])
            }
            cursor.execute(sql.insert_stock_sql, insert_data)
            print("insert stock data[" + str(stock_codes[n]) + "]")
            conn.commit()
finally:
    conn.close()        

print("Done insert tables! [stock, market, industry_type, sub_industry_type]")