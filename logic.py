import random
import time

from pasaages import PASSAGES

_test_state = {
    "passage": None,
    "duration": None,
    "start_time": None, 
    "finished": False,
    "typed_text": "",
}

def get_random_passage():
    passage = random.choice(PASSAGES)
    _test_state["passage"] = passage
    return passage

def start_timer(duration):
    if duration not in (15, 30, 60):
        raise ValueError("Invalid Duration!")

    _test_state["duration"] = duration
    _test_state["start_time"] = time.time()
    _test_state["finished"] = False

    return _test_state

def remaining_seconds():
    if _test_state["start_time"] is None:
        return 0

    elapsed = time.time() - _test_state["start_time"]
    remaining =_test_state["duration"] - elapsed

    return max(0, int(remaining))

def is_test_finished():
    if _test_state["start_time"] is None:
        return False
    
    if remaining_seconds() <= 0:
        _test_state["finished"] = True
        return True

    return False

def validate_typed_text(submitted_text, passage):
    correct = 0

    for typed, expected in zip(submitted_text, passage):
        if typed == expected:
            correct += 1    

    total = len(sumbitted_text)
    incorrect = total - correct

    return{
        "correct_characters": correct,
        "incorrect_characters": incorrect,
        "total_characters": total,
    }

def calculate_wpm(correct_characters, elapsed_seconds):
    if elapsed_seconds <= 0:
        return 0 
    
    minutes = elapsed_seconds / 60
    return round((correct_characters / 5 ) / minutes)

def calculate_accuracy(correct_characters, total_characters):
    if total_characters <= 0:
        return 0

    return round((correct_characters / total_characters) * 100, 2)

def build_results():
    passage =  _test_state["passage"]

    if passage is None:
        return None

    elapsed_seconds = time.time() - _test_state["start_time"]

    character_results = validate_typed_text(
        submitted_text,
        passage
    )

    wpm = calculate_wpm(
        character_results["correct_characters"],
        elapsed_seconds
    )

    accuracy = calculate_accuracy(
        character_results["correct_characters"],
        character_results["total_characters"]
    )
    
    return {
        "wpm": wpm,
        "accuracy": accuracy,
        "correct_characters": character_results["correct_characters"],
        "incorrect_characters": character_results["incorrect_characters"],
        "total_characters": character_results["total_characters"],
        "elapsed_seconds": round(elapsed_seconds, 2),
    }


def reset_test():
    """Reset the current test."""

    _test_state["passage"] = None
    _test_state["duration"] = None
    _test_state["start_time"] = None
    _test_state["finished"] = False
    _test_state["typed_text"] = ""

    