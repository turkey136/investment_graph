# -*- coding: utf-8 -*-
# Run example
# all data insert
#   python seed.py
# only code 001 abd 002 data insert
#   python seed.py 001,002

import pandas_datareader.data as web
import sys
import pandas as pd
import math
import datetime

import db
import sql

target_codes = []  
if len(sys.argv) > 2:
    target_codes = sys.argv[1].split(',')
limited_create = len(target_codes) != 0
conn = db.conn

stock_master_csv_path = "../seed/code_master.csv"

stock_master_data = pd.read_csv(stock_master_csv_path, encoding= "utf-8")
stock_codes = stock_master_data['code']
stock_names = stock_master_data['name']

try:
    with conn.cursor() as cursor:
        for n in range(len(stock_codes)):   
            if limited_create and str(stock_codes[n]) not in target_codes:
                continue

            # create stock
            insert_data = { "code": int(stock_codes[n]), "name": stock_names[n].encode("utf-8") }
            cursor.execute(sql.insert_stock_sql, insert_data)
            print("insert stock data[" +str(stock_codes[n]) + "]")

            # create stack_price
            last_day_close_value = None
            previous_id = None
            stooq_result = web.DataReader(str(stock_codes[n]) + '.JP', 'stooq')
            max_index = len(stooq_result.index)
            pearent_id = 0
            for i in range(max_index):
                index = max_index - 1 - i
                value = stooq_result.values[index]
                close_value = value[3]

                if last_day_close_value != None:
                    vary_percent = math.floor(close_value / last_day_close_value)
                    if close_value == last_day_close_value:
                      vary_code = 0
                    elif close_value > last_day_close_value:
                      vary_code = 1
                    else:
                      vary_code = -1
                else:
                    vary_percent = None
                    vary_code = None

                insert_data = {
                    "previous_id": previous_id,
                    "code": int(stock_codes[n]),
                    "date": stooq_result.index[index].strftime("%Y-%m-%d"),
                    "start": int(value[0]),
                    "hight": int(value[1]),
                    "low": int(value[2]),
                    "close": int(close_value),
                    "vary_percent": vary_percent,
                    "vary_code": vary_code
                }
                cursor.execute(sql.insert_stock_price_sql, insert_data)
                last_day_close_value = close_value
                conn.commit()
                previous_id = cursor.lastrowid
finally:
    conn.close()        

print("Done insert tables! [stock, stock_price]")