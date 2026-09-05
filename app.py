
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_test():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_test():
    return render_template("index.html")


@app.route("/restart", methods=["POST"])
def restart_test():

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
