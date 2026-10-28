import pytest
from traffic_fine import speeding_fine, license_action, total_penalty


# --- Speeding Fine Decision & Boundary Tests ---

def test_speeding_exact_limit():
    """Boundary test: speed exactly at the posted speed limit (excess = 0)."""
    assert speeding_fine(50, 50, "school") == 0


def test_speeding_below_limit():
    """Condition test: speed below posted speed limit."""
    assert speeding_fine(40, 60, "city") == 0


def test_speeding_school_excess_over_40():
    """Decision test: school zone base (2000) with excess > 40 (multiplier x3)."""
    assert speeding_fine(85, 40, "school") == 6000  # excess = 45 > 40


def test_speeding_school_excess_boundary_40():
    """Boundary test: excess exactly 40 in school zone (excess > 20 branch, multiplier x2)."""
    assert speeding_fine(80, 40, "school") == 4000  # excess = 40 (not > 40, but > 20)


def test_speeding_school_excess_boundary_20():
    """Boundary test: excess exactly 20 in school zone (excess <= 20, multiplier x1)."""
    assert speeding_fine(60, 40, "school") == 2000  # excess = 20 (not > 20)


def test_speeding_highway_excess_over_40():
    """Decision test: highway zone base (1000) with excess > 40 (multiplier x3)."""
    assert speeding_fine(130, 80, "highway") == 3000  # excess = 50 > 40


def test_speeding_highway_excess_over_20():
    """Decision test: highway zone base (1000) with 20 < excess <= 40 (multiplier x2)."""
    assert speeding_fine(105, 80, "highway") == 2000  # excess = 25


def test_speeding_highway_excess_mild():
    """Decision test: highway zone base (1000) with excess <= 20 (multiplier x1)."""
    assert speeding_fine(95, 80, "highway") == 1000  # excess = 15


def test_speeding_default_zone_excess_over_40():
    """Decision test: default zone base (500) with excess > 40 (multiplier x3)."""
    assert speeding_fine(100, 50, "residential") == 1500  # excess = 50 > 40


def test_speeding_default_zone_excess_over_20():
    """Decision test: default zone base (500) with 20 < excess <= 40 (multiplier x2)."""
    assert speeding_fine(75, 50, "rural") == 1000  # excess = 25


def test_speeding_default_zone_excess_mild():
    """Decision test: default zone base (500) with excess <= 20 (multiplier x1)."""
    assert speeding_fine(60, 50, "other") == 500  # excess = 10


# --- License Action Decision & Boundary Tests ---

def test_license_points_12_commercial():
    """Boundary & decision test: points == 12, commercial driver -> revoke."""
    assert license_action(12, True, False) == "revoke"


def test_license_points_over_12_non_commercial():
    """Decision test: points > 12, non-commercial driver -> suspend."""
    assert license_action(15, False, True) == "suspend"


def test_license_points_11_repeat_offender():
    """Boundary & decision test: points == 11, repeat offender -> suspend."""
    assert license_action(11, False, True) == "suspend"


def test_license_points_8_first_time():
    """Boundary & decision test: points == 8, first-time offender -> warning."""
    assert license_action(8, True, False) == "warning"


def test_license_points_7_notice():
    """Boundary test: points == 7 -> notice."""
    assert license_action(7, False, False) == "notice"


def test_license_points_4_notice():
    """Boundary test: points == 4 -> notice."""
    assert license_action(4, True, True) == "notice"


def test_license_points_3_none():
    """Boundary test: points == 3 -> none."""
    assert license_action(3, False, False) == "none"


def test_license_clean_record_zero():
    """Boundary test: points == 0 -> none."""
    assert license_action(0, False, False) == "none"


# --- Total Penalty Decision & Exception Tests ---

def test_total_penalty_empty():
    """Loop boundary test: empty list of fines returns 0."""
    assert total_penalty([]) == 0


def test_total_penalty_normal_under_cap():
    """Decision test: sum of fines below 10000 cap."""
    assert total_penalty([1500, 2500, 1000]) == 5000


def test_total_penalty_exact_cap():
    """Boundary test: sum of fines exactly equal to 10000."""
    assert total_penalty([6000, 4000]) == 10000


def test_total_penalty_exceeds_cap():
    """Decision test: sum of fines exceeding 10000 cap is capped at 10000."""
    assert total_penalty([4000, 5000, 3000]) == 10000


def test_total_penalty_negative_fine_raises():
    """Exception branch test: negative fine raises ValueError."""
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([1000, -500, 2000])
