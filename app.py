"""TypeTest -- a typing speed test built with Flask.

The frontend contains no JavaScript: every interaction is a plain HTML form
submission, and the timer, WPM, accuracy and character counts are all produced
by Python (see ``logic.py``).

Run it with::

    python3 app.py

then open http://127.0.0.1:5001/
"""

from flask import Flask, redirect, render_template, request, url_for

from logic import (
    build_results,
    current_duration,
    current_passage,
    current_passage_number,
    current_typed_text,
    get_random_passage,
    has_test_started,
    remaining_seconds,
    reset_test,
    start_timer,
)

app = Flask(__name__)


def render_test(test_status, **overrides):
    """Render the page with the values that always come from the test state."""
    context = {
        "passage": current_passage(),
        "passage_number": current_passage_number(),
        "duration": current_duration(),
        "typed_text": current_typed_text(),
        "time_remaining": remaining_seconds(),
        "test_status": test_status,
    }
    context.update(overrides)

    return render_template("index.html", **context)


@app.route("/")
def index():
    """Show a fresh test, or the running one if the page is reloaded."""
    if not has_test_started():
        return render_test("Not started")

    return render_test("Running")


@app.route("/start", methods=["POST"])
def start_test():
    """Start a new run: pick a passage and begin the countdown."""
    reset_test()

    passage = get_random_passage()
    start_timer(request.form.get("duration"))

    return render_test("Running", passage=passage)


@app.route("/submit", methods=["POST"])
def submit_test():
    """Score what the user typed and show the results."""
    if not has_test_started():
        return redirect(url_for("index"))

    results = build_results(request.form.get("typed_text", ""))

    if results is None:
        return redirect(url_for("index"))

    return render_test(
        "Finished",
        time_remaining=0,
        wpm=results["wpm"],
        accuracy=results["accuracy"],
        characters_typed=results["total_characters"],
        final_wpm=results["wpm"],
        final_accuracy=results["accuracy"],
        correct_characters=results["correct_characters"],
        incorrect_characters=results["incorrect_characters"],
        total_characters=results["total_characters"],
    )


@app.route("/restart", methods=["POST"])
def restart_test():
    """Discard the current run and go back to the idle screen."""
    reset_test()

    return render_test("Not started")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
