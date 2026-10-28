import pytest
from traffic_fine import speeding_fine, license_action, total_penalty

# Baseline tests
def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0

def test_clean_record():
    assert license_action(2, False, False) == "none"

# Additional tests targeting statement/line coverage (>= 90%)
def test_speeding_school_zone_excessive():
    # excess = 50 > 40, school zone: exercises lines 4, 5-6, 11-12
    assert speeding_fine(90, 40, "school") == 6000

def test_speeding_highway_zone_moderate():
    # excess = 25 > 20, highway zone: exercises lines 7-8, 13-14
    assert speeding_fine(105, 80, "highway") == 2000

def test_speeding_other_zone_mild():
    # excess = 10 <= 20, other zone: exercises lines 9-10, 15
    assert speeding_fine(60, 50, "residential") == 500

def test_license_severe_commercial():
    # points = 14 >= 12, commercial = True: exercises lines 19, 20-21
    assert license_action(14, True, False) == "revoke"

def test_license_intermediate_repeat():
    # points = 9 >= 8, repeat = True: exercises lines 23, 24-25
    assert license_action(9, False, True) == "suspend"

def test_license_points_notice():
    # points = 5 >= 4: exercises lines 27-28
    assert license_action(5, False, False) == "notice"

def test_total_penalty_capped():
    # Loop exercises lines 33-35, 37; total > 10000 exercises lines 38-39, 40
    assert total_penalty([4000, 4000, 4000]) == 10000
