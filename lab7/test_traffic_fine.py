from hypothesis import given, strategies as st

from traffic_fine import parse_ticket_id, total_fines, speed_excess


# Fuzz tests: arbitrary strings and None must never crash the functions.
# Invalid input should be rejected with None, not an uncaught exception.

@given(st.text() | st.none())
def test_parse_ticket_id_no_crash(value):
    result = parse_ticket_id(value)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 3
        and isinstance(result[0], str)
        and isinstance(result[1], int)
        and isinstance(result[2], int)
    )


@given(st.text() | st.none())
def test_total_fines_no_crash(value):
    result = total_fines(value)
    assert result is None or (
        isinstance(result, int) and 0 <= result <= 10000
    )


@given(st.text() | st.none())
def test_speed_excess_no_crash(value):
    result = speed_excess(value)
    assert result is None or isinstance(result, int)


# Valid-input properties help ensure the functions still calculate correctly.

@given(
    prefix=st.text(
        alphabet=st.characters(min_codepoint=65, max_codepoint=90),
        min_size=1,
        max_size=5,
    ),
    year=st.integers(min_value=1000, max_value=9999),
    serial=st.integers(min_value=0, max_value=999999),
)
def test_parse_ticket_id_valid_inputs(prefix, year, serial):
    value = f"{prefix.lower()}-{year}-{serial}"
    assert parse_ticket_id(value) == (prefix, year, serial)


@given(st.lists(st.integers(min_value=0, max_value=20000), min_size=1, max_size=20))
def test_total_fines_valid_inputs(amounts):
    value = ",".join(map(str, amounts))
    assert total_fines(value) == min(sum(amounts), 10000)


@given(
    speed=st.integers(min_value=1, max_value=300),
    limit=st.integers(min_value=1, max_value=200),
)
def test_speed_excess_valid_inputs(speed, limit):
    value = f"{speed}/{limit}"
    assert speed_excess(value) == (speed - limit) * 100 // limit