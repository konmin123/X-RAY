from flask import render_template, request

from settings import app


@app.route("/", methods=["POST", "GET"])
def index():
    from model import Data

    if request.method == "POST":
        word = request.form["search_word"]
        data = Data.data_for_view(word)
    else:
        data = Data.data_for_view()
    return render_template("x-ray/index.html", data=data)
