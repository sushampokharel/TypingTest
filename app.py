
from flask import Flask, render_template
from logic import get_random_passage
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_test():
    passage = get_random_passage()

    return render_template(
        "index.html",
        passage=passage)


@app.route("/submit", methods=["POST"])
def submit_test():
    return render_template("index.html")


@app.route("/restart", methods=["POST"])
def restart_test():

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
