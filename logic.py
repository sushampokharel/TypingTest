"""Typing test domain logic.

The frontend has no JavaScript, so every calculation -- timer, WPM, accuracy,
character counting and validation -- happens here on the server.

The test state lives in the module level ``_test_state`` dictionary. That is
deliberately simple: it tracks one test at a time for one local user.
"""

import random
import time

from passages import PASSAGES

VALID_DURATIONS = (15, 30, 60)
DEFAULT_DURATION = 60

_test_state = {
    "passage": None,
    "passage_number": None,
    "duration": None,
    "start_time": None,
    "finished": False,
    "typed_text": "",
}


def get_random_passage():
    """Pick a passage at random and remember it as the current target."""
    if not PASSAGES:
        return None

    index = random.randrange(len(PASSAGES))
    _test_state["passage_number"] = index + 1
    _test_state["passage"] = PASSAGES[index]

    return _test_state["passage"]


def start_timer(duration):
    """Start the countdown for the given duration in seconds."""
    try:
        duration = int(duration)
    except (TypeError, ValueError):
        duration = DEFAULT_DURATION

    if duration not in VALID_DURATIONS:
        duration = DEFAULT_DURATION

    _test_state["duration"] = duration
    _test_state["start_time"] = time.time()
    _test_state["finished"] = False
    _test_state["typed_text"] = ""

    return _test_state


def has_test_started():
    """Return whether a test has been started and not yet reset."""
    return _test_state["start_time"] is not None


def remaining_seconds():
    """Return the seconds left on the clock, or None before a test starts."""
    if not has_test_started():
        return None

    elapsed = time.time() - _test_state["start_time"]
    remaining = _test_state["duration"] - elapsed

    return max(0, int(remaining))


def is_test_finished():
    """Return whether the selected duration has run out."""
    if not has_test_started():
        return False

    if remaining_seconds() <= 0:
        _test_state["finished"] = True
        return True

    return _test_state["finished"]


def elapsed_seconds():
    """Return how long the user has been typing, capped at the duration."""
    if not has_test_started():
        return 0

    elapsed = time.time() - _test_state["start_time"]
    duration = _test_state["duration"]

    return min(elapsed, duration) if duration else elapsed


def current_passage():
    return _test_state["passage"]


def current_passage_number():
    return _test_state["passage_number"]


def current_duration():
    return _test_state["duration"]


def current_typed_text():
    return _test_state["typed_text"]


def validate_typed_text(submitted_text, passage):
    """Compare the submitted text against the passage character by character."""
    correct = 0

    for typed, expected in zip(submitted_text, passage):
        if typed == expected:
            correct += 1

    total = len(submitted_text)

    return {
        "correct_characters": correct,
        # Characters typed past the end of the passage cannot be correct.
        "incorrect_characters": total - correct,
        "total_characters": total,
    }


def calculate_wpm(correct_characters, elapsed):
    """Return words per minute: five correct characters count as one word."""
    if elapsed <= 0:
        return 0

    minutes = elapsed / 60

    return round((correct_characters / 5) / minutes)


def calculate_accuracy(correct_characters, total_characters):
    """Return the share of typed characters that were correct, in percent."""
    if total_characters <= 0:
        return 0

    return round((correct_characters / total_characters) * 100, 2)


def build_results(submitted_text):
    """Score the run and return every value the results section needs."""
    passage = _test_state["passage"]

    if passage is None or not has_test_started():
        return None

    _test_state["typed_text"] = submitted_text
    _test_state["finished"] = True

    elapsed = elapsed_seconds()
    character_results = validate_typed_text(submitted_text, passage)

    wpm = calculate_wpm(character_results["correct_characters"], elapsed)
    accuracy = calculate_accuracy(
        character_results["correct_characters"],
        character_results["total_characters"],
    )

    return {
        "wpm": wpm,
        "accuracy": accuracy,
        "correct_characters": character_results["correct_characters"],
        "incorrect_characters": character_results["incorrect_characters"],
        "total_characters": character_results["total_characters"],
        "elapsed_seconds": round(elapsed, 2),
    }


def reset_test():
    """Clear the current run so a new test can begin."""
    _test_state["passage"] = None
    _test_state["passage_number"] = None
    _test_state["duration"] = None
    _test_state["start_time"] = None
    _test_state["finished"] = False
    _test_state["typed_text"] = ""
