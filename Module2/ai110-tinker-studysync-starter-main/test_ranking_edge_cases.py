"""
Edge cases for score_study_spot() aimed at weight bias.

Current weights: noise = 1, distance = 4, seats = 1.
These tests document what the weights do, not what they "should" do.
"""

from itertools import product

from ranking import NOISE_ORDER, load_study_spots, rank_study_spots, score_study_spot

QUIET_PROFILE = {"max_noise": "quiet", "max_distance": 1.0, "min_seats": 4}


def spot(noise="quiet", dist=0.5, seats=10):
    return {"noise_level": noise, "distance_miles": dist, "seats_available": seats}


def score(profile, s):
    return score_study_spot(profile, s)[0]


# --- Does distance dominate? -------------------------------------------------

def test_loud_close_beats_quiet_far_for_a_student_who_asked_for_quiet():
    loud_close = score(QUIET_PROFILE, spot(noise="loud", dist=0.2))
    quiet_far = score(QUIET_PROFILE, spot(noise="quiet", dist=1.2))
    assert loud_close > quiet_far


def test_loud_close_with_no_seats_still_beats_perfect_quiet_far_spot():
    loud_close_no_seats = score(QUIET_PROFILE, spot(noise="loud", dist=0.2, seats=0))
    quiet_far_roomy = score(QUIET_PROFILE, spot(noise="quiet", dist=1.2, seats=50))
    assert loud_close_no_seats > quiet_far_roomy


def test_noise_and_seats_together_can_never_outweigh_distance():
    """Exhaustive: any in-range spot outranks any out-of-range spot."""
    noises = list(NOISE_ORDER)
    for max_noise, in_n, in_s, out_n, out_s in product(noises, noises, (0, 50), noises, (0, 50)):
        profile = {"max_noise": max_noise, "max_distance": 1.0, "min_seats": 4}
        in_range = score(profile, spot(noise=in_n, dist=1.0, seats=in_s))
        out_range = score(profile, spot(noise=out_n, dist=1.01, seats=out_s))
        assert in_range > out_range


# --- Cliffs and flat penalties -----------------------------------------------

def test_distance_cliff_one_hundredth_of_a_mile_costs_four_points():
    assert score(QUIET_PROFILE, spot(dist=1.0)) - score(QUIET_PROFILE, spot(dist=1.01)) == 4.0


def test_far_is_far_no_matter_how_far():
    assert score(QUIET_PROFILE, spot(dist=1.01)) == score(QUIET_PROFILE, spot(dist=50.0))


def test_noise_penalty_is_flat_one_step_or_two_steps_over():
    profile = {"max_noise": "quiet", "max_distance": 1.0, "min_seats": 4}
    assert score(profile, spot(noise="moderate")) == score(profile, spot(noise="loud"))


def test_noise_and_seats_are_worth_the_same_so_they_are_interchangeable():
    noisy_roomy = score(QUIET_PROFILE, spot(noise="loud", seats=50))
    quiet_empty = score(QUIET_PROFILE, spot(noise="quiet", seats=0))
    assert noisy_roomy == quiet_empty


# --- Boundaries --------------------------------------------------------------

def test_exact_boundaries_count_as_matches():
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    s, reasons = score_study_spot(profile, spot(noise="moderate", dist=1.0, seats=4))
    assert s == 6.0
    assert reasons == ["quiet enough", "close enough", "enough seats"]


def test_zero_max_distance_matches_nothing_real():
    profile = {"max_noise": "loud", "max_distance": 0.0, "min_seats": 1}
    assert score(profile, spot(dist=0.1)) == 2.0  # only noise + seats


def test_everything_misses_scores_zero_with_all_three_reasons():
    profile = {"max_noise": "quiet", "max_distance": 0.1, "min_seats": 100}
    s, reasons = score_study_spot(profile, spot(noise="loud", dist=5.0, seats=1))
    assert s == 0.0
    assert reasons == ["too noisy", "too far", "not enough seats"]


# --- Real CSV: who gets buried? ----------------------------------------------

def test_loud_spots_outrank_quiet_far_spots_for_a_quiet_student():
    spots = load_study_spots("data/study_spots.csv")
    ranked = [s["name"] for s, _, _ in rank_study_spots(QUIET_PROFILE, spots, k=len(spots))]
    for loud in ("Courtyard Cafe", "Student Union Tables"):
        for quiet_far in ("North Stacks Nook", "24-Hour Annex"):
            assert ranked.index(loud) < ranked.index(quiet_far)


def test_quiet_far_spots_are_buried_below_every_close_spot():
    spots = load_study_spots("data/study_spots.csv")
    ranked = rank_study_spots(QUIET_PROFILE, spots, k=len(spots))
    far_names = {s["name"] for s in spots if s["distance_miles"] > 1.0}
    last_names = {s["name"] for s, _, _ in ranked[-len(far_names):]}
    assert last_names == far_names
