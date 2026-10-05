# Change Log

Record of every change made to project files during the debugging session.

## 2026-10-05

### 1. Refactor game logic into `logic_utils.py`
- `logic_utils.py`: replaced the `NotImplementedError` stubs with the real implementations of `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score`, copied unchanged from `app.py`.
- `app.py`: removed those four function definitions and added `from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score`.
- `CHANGELOG.md`: created this file.
- Behavior is intentionally unchanged. Known bugs are still present and will be fixed in later steps.

### 2. Fix reported logic bugs
- `logic_utils.py` (`check_guess`): hints were reversed. A guess above the secret now returns "Go LOWER!" and a guess below returns "Go HIGHER!". Removed the `str` fallback branch that is no longer needed.
- `app.py`: removed the code that cast the secret to a string on even attempts, which made comparisons wrong. The integer secret is always used.
- `app.py`: attempts now start at 0 (was 1), so the game no longer ends one attempt early and "Attempts left" is correct.
- `app.py`: the guess input and submit button are now in an `st.form` with `st.form_submit_button`, so pressing Enter submits the guess.
- `app.py`: New Game now resets attempts, score, status and history, picks the secret from the current difficulty's range, and bumps a `game_id` used in widget keys so the text box clears. Shows a toast instead of a message that was lost on rerun.
- `app.py`: with hints off, a wrong guess now shows "❌ Wrong guess. Try again!".
- `tests/test_game_logic.py`: tests now unpack the `(outcome, message)` tuple that `check_guess` returns, and a new test checks the hint messages point the right way.
- Tests: 4 pass (`python -m pytest`).

### 3. Fix remaining logic bugs
- `app.py`: the info text now shows the real range (`low` to `high`) instead of a hardcoded "1 and 100".
- `logic_utils.py`: Hard range changed from 1-50 to 1-200 so it is harder than Normal.
- `app.py`: Hard attempt limit raised from 5 to 8 so the wider range is winnable (binary search on 200 needs 8).
- `logic_utils.py` (`update_score`): "Too High" no longer gives +5 on even attempts; both wrong-guess outcomes now cost 5 points. The win formula is now `100 - 10 * (attempt_number - 1)`, so a first-try win scores 100 (minimum stays 10).
- `app.py`: invalid input (empty or non-numeric) no longer uses up an attempt.
- `app.py`: added `reset_game()`, used for first load, New Game, and difficulty changes. Changing difficulty now starts a fresh game with a secret in the new range. New Game uses the same function instead of duplicating the reset code.
- `tests/test_game_logic.py`: added tests for the Hard range, wrong-guess scoring, win scoring and its minimum, and `parse_guess` rejecting bad input.

### 4. Fix stale "Attempts left" and debug panel
- `app.py`: the info box and Developer Debug Info expander were rendered before the guess was processed, so they lagged one guess behind. They now use `st.empty()` placeholders filled by a new `render_status()` function, called after guess handling (and before `st.stop()` when the game is over).

### 5. Expanded test suite
- `pytest.ini`: new file setting `pythonpath = .` and `testpaths = tests`, so plain `pytest` now works.
- `tests/test_game_logic.py`: end-to-end app tests (first written in a separate `tests/test_app.py`, then merged here at the user's request; that file was deleted). They using Streamlit's `AppTest`. They cover correct hint direction, winning, attempts left updating immediately, invalid and empty input not using attempts, the exact attempt limit, feedback with hints off, New Game resetting state and clearing the input, difficulty changes re-rolling the secret, and score after a wrong guess then a win.
- `tests/test_game_logic.py`: added tests for `check_guess` boundaries, ranges per difficulty, numeric parsing forms, unknown outcomes and negative scores.
- Note: the user changed the ranges in `logic_utils.py` to Easy 1-20, Normal 1-50, Hard 1-100. The tests were written to match.

### 6. Merge app tests into `test_game_logic.py`
- `tests/test_app.py`: deleted; its fixture, helpers and 14 tests now live at the bottom of `tests/test_game_logic.py`.
- Tests: 28 pass.
