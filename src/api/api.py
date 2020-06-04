from flask import Flask, jsonify
import sql
import db

conn = db.conn
app = Flask(__name__)

@app.route('/stock_list')
def code_list():
    tmp = []

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql.stock_list_by_code)
            for stock in cursor.fetchall():
                tmp.append({'code': stock[0], 'name': stock[1]})
    finally:
        conn.close()

    return jsonify({
            'status': 'OK',
            'data': tmp
    })

if __name__ == "__main__":
    app.run(debug=True)