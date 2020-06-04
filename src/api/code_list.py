import sql

def search_all_stock_list(conn):
    tmp = []

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql.stock_list_by_code)
            for stock in cursor.fetchall():
                tmp.append({'code': stock[0], 'name': stock[1]})
    finally:
        conn.close()
        return tmp