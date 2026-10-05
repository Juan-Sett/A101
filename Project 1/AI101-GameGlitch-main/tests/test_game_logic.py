from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, _ = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, _ = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, _ = check_guess(40, 50)
    assert result == "Too Low"

def test_hint_messages_point_the_right_way():
    assert "LOWER" in check_guess(60, 50)[1]
    assert "HIGHER" in check_guess(40, 50)[1]


def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high > get_range_for_difficulty("Easy")[1]


def test_wrong_guess_always_costs_points():
    for attempt in (1, 2, 3, 4):
        assert update_score(50, "Too High", attempt) == 45
        assert update_score(50, "Too Low", attempt) == 45


def test_win_on_first_attempt_scores_100():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 2) == 90


def test_win_score_has_minimum_of_10():
    assert update_score(0, "Win", 20) == 10


def test_parse_guess_rejects_bad_input():
    assert parse_guess("")[0] is False
    assert parse_guess(None)[0] is False
    assert parse_guess("abc")[0] is False
    assert parse_guess("42") == (True, 42, None)


def test_check_guess_boundaries():
    assert check_guess(51, 50)[0] == "Too High"
    assert check_guess(49, 50)[0] == "Too Low"
    assert check_guess(1, 1)[0] == "Win"
    assert check_guess(100, 100)[0] == "Win"


def test_range_for_each_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)
    assert get_range_for_difficulty("Unknown") == (1, 100)


def test_parse_guess_numeric_forms():
    assert parse_guess("3.7") == (True, 3, None)
    assert parse_guess(" 5 ") == (True, 5, None)
    assert parse_guess("-4") == (True, -4, None)
    assert parse_guess("1e3")[0] is False


def test_score_unknown_outcome_unchanged():
    assert update_score(30, "Playing", 1) == 30


def test_score_can_go_negative():
    assert update_score(0, "Too Low", 1) == -5


# ---------------------------------------------------------------------------
# End-to-end tests that drive the Streamlit app headlessly
# ---------------------------------------------------------------------------

APP = str(Path(__file__).resolve().parent.parent / "app.py")


@pytest.fixture
def app():
    """A freshly loaded app whose secret is fixed to 50."""
    at = AppTest.from_file(APP, default_timeout=10).run()
    assert not at.exception
    at.session_state["secret"] = 50
    return at


def button(at, label):
    return next(b for b in at.button if label in b.label)


def guess(at, text):
    at.text_input[0].input(text)
    button(at, "Submit").click()
    return at.run()


def texts(elements):
    return " ".join(e.value for e in elements)


def test_app_loads_with_full_attempts(app):
    assert app.session_state["attempts"] == 0
    assert "Attempts left: 8" in app.info[0].value


def test_info_shows_range_for_difficulty(app):
    assert "between 1 and 50" in app.info[0].value
    app.sidebar.selectbox[0].select("Easy").run()
    assert "between 1 and 20" in app.info[0].value
    app.sidebar.selectbox[0].select("Hard").run()
    assert "between 1 and 100" in app.info[0].value


def test_too_high_guess_says_go_lower(app):
    guess(app, "60")
    assert "LOWER" in texts(app.warning)


def test_too_low_guess_says_go_higher(app):
    guess(app, "40")
    assert "HIGHER" in texts(app.warning)


def test_correct_guess_wins(app):
    guess(app, "50")
    assert app.session_state["status"] == "won"
    assert "You won" in texts(app.success)


def test_attempts_left_updates_immediately(app):
    guess(app, "60")
    assert "Attempts left: 7" in app.info[0].value


def test_invalid_guess_does_not_use_attempt(app):
    guess(app, "abc")
    assert app.session_state["attempts"] == 0
    assert "not a number" in texts(app.error)


def test_empty_guess_does_not_use_attempt(app):
    guess(app, "")
    assert app.session_state["attempts"] == 0


def test_game_allows_exactly_the_attempt_limit(app):
    for _ in range(7):
        guess(app, "60")
    assert app.session_state["status"] == "playing"
    guess(app, "60")
    assert app.session_state["status"] == "lost"
    assert "Out of attempts" in texts(app.error)


def test_wrong_guess_with_hints_off_still_gives_feedback(app):
    app.checkbox[0].uncheck().run()
    guess(app, "60")
    assert "Wrong guess" in texts(app.error)
    assert not app.warning


def test_new_game_resets_state_after_loss(app):
    for _ in range(8):
        guess(app, "60")
    assert app.session_state["status"] == "lost"
    button(app, "New Game").click()
    app.run()
    assert app.session_state["status"] == "playing"
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert "Attempts left: 8" in app.info[0].value


def test_new_game_clears_text_box(app):
    app.text_input[0].input("60").run()
    button(app, "New Game").click()
    app.run()
    assert app.text_input[0].value == ""


def test_changing_difficulty_rerolls_secret_in_range(app):
    app.sidebar.selectbox[0].select("Easy").run()
    assert 1 <= app.session_state["secret"] <= 20
    assert app.session_state["attempts"] == 0
    assert "Attempts left: 6" in app.info[0].value


def test_score_after_wrong_then_win(app):
    guess(app, "60")   # -5
    guess(app, "50")   # win on attempt 2 -> +90
    assert app.session_state["score"] == 85
