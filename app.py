from flask import Flask, render_template, request
import sqlite3

from service import Analizer
from model import DB

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    data = []
    if request.method == 'POST':
        word = request.form['search_word']
        expression_for_request =\
            f"SELECT * FROM statistic WHERE statistic.search_word = '{word}' ORDER BY id DESC LIMIT 4"
        cur.execute(expression_for_request)
        for i in cur:
            data.insert(0, i)
        if not data:
            print('слова нет в бд')
            DB.save_to_db(Analizer.create_table(word))
            cur.execute(expression_for_request)
    else:
        cur.execute('''SELECT * FROM statistic ORDER BY id DESC LIMIT 4''')
    for i in cur:
        data.insert(0, i)
    return render_template('x-ray/index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
