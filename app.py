from flask import Flask, render_template, request

from model import DB

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        word = request.form['search_word']
        data = DB.data_for_view(word)
    else:
        data = DB.data_for_view()
    return render_template('x-ray/index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
