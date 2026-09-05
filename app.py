"""TypeTest -- a typing speed test built with Flask.

This file is the Flask skeleton only. The complete frontend is rendered from
``templates/index.html`` and styled by ``static/css/style.css``; there is no
JavaScript in this project, so every behaviour listed in the TODOs below has to
be implemented in Python.

Run it with::

    python3 app.py

then open http://127.0.0.1:5000/

The domain logic lives in ``logic.py`` and ``passages.py`` -- both are stubs.
"""

from flask import Flask, render_template

app = Flask(__name__)

# TODO: Load configuration (secret key, default test duration, ...)
# TODO: Set up server-side test state / session storage for the running test
# TODO: Import the stub modules ``logic`` and ``passages`` once they are filled in


@app.route("/", methods=["GET"])
def index():
    """Serve the typing test UI."""
    # TODO: Fetch a random typing passage
    # TODO: Read the selected test duration (15 / 30 / 60 seconds)
    # TODO: Calculate the remaining time on the timer
    # TODO: Calculate WPM
    # TODO: Calculate accuracy
    # TODO: Count typed characters (correct / incorrect / total)
    # TODO: Handle test results
    # TODO: Pass all of the above to the template as context values
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_test():
    """Start a new test run."""
    # TODO: Validate the submitted duration and passage
    # TODO: Initialize the test state
    # TODO: Start the timer
    # TODO: Render the running test
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_test():
    """Receive the text typed by the user."""
    # TODO: Read the submitted text from the form
    # TODO: Run typing validation against the passage
    # TODO: Count correct, incorrect and total characters
    # TODO: Update WPM, accuracy and the timer
    # TODO: End the test when the time is up and handle the results
    return render_template("index.html")


@app.route("/restart", methods=["POST"])
def restart_test():
    """Discard the current run and prepare a fresh one."""
    # TODO: Reset the test state and the timer
    # TODO: Clear the previous results
    # TODO: Select a new random passage
    return render_template("index.html")


if __name__ == "__main__":
    # TODO: Disable the reloader/debug mode for anything other than local work
    app.run(debug=True)
