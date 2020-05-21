# -*- coding: utf-8 -*-
import pandas_datareader.data as web
import time

import db
import sql
import db_lib
conn = db.conn
counter = 1

try:
    with conn.cursor() as cursor:
        cursor.execute(sql.select_tousyou_stok_sql)
        for stock in cursor.fetchall():
            stock_code = stock[0]
            last_day_close_value = None
            previous_id = None
            stooq_result = web.DataReader(str(stock_code) + '.JP', 'stooq')
            max_index = len(stooq_result.index)

            for i in range(max_index):
                index = max_index - 1 - i
                value = stooq_result.values[index]
                close_value = value[3]
                vary_code = db_lib.convert_vary_code(last_day_close_value, close_value)
                insert_data = {
                    "previous_id": previous_id,
                    "code": int(stock_code),
                    "date": stooq_result.index[index].strftime("%Y-%m-%d"),
                    "start": int(value[0]),
                    "hight": int(value[1]),
                    "low": int(value[2]),
                    "close": int(close_value),
                    "vary_code": vary_code
                }
                cursor.execute(sql.insert_stock_price_sql, insert_data)
                conn.commit()
                previous_id = cursor.lastrowid
                last_day_close_value = close_value

            print("insert stock price [" + str(stock_code) + "]. ")
            if counter % 10 == 0:
                time.sleep(60)
except Exception as e:
    print(e)
    conn.rollback()
finally:
    conn.close()        
