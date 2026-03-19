from powerxai.coalitions import coalitions


def test_empty_set():
    result = coalitions(set())
    assert result == [set()], "Empty input should return a list with only the empty set"


def test_single_element():
    result = coalitions({1})
    expected = [set(), {1}]
    assert result == expected


def test_two_elements():
    result = coalitions({1, 2})
    expected = [set(), {1}, {2}, {1, 2}]
    assert all(coalition in result for coalition in expected)
    assert len(result) == len(expected)


def test_three_elements():
    result = coalitions({1, 2, 3})
    expected = [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]
    assert all(coalition in result for coalition in expected)
    assert len(result) == len(expected)


def test_order_invariant():
    assert coalitions({1, 2, 3}) == coalitions({3, 2, 1})


def test_cardinality_zero():
    result = coalitions({1, 2, 3}, cardinality=0)
    assert result == [set()]


def test_cardinality_one():
    result = coalitions({1, 2, 3}, cardinality=1)
    expected = [{1}, {2}, {3}]
    assert all(coalition in result for coalition in expected)
    assert len(result) == len(expected)


def test_cardinality_two():
    result = coalitions({1, 2, 3}, cardinality=2)
    expected = [{1, 2}, {1, 3}, {2, 3}]
    assert all(coalition in result for coalition in expected)
    assert len(result) == len(expected)


def test_cardinality_full_set():
    result = coalitions({1, 2, 3}, cardinality=3)
    assert result == [{1, 2, 3}]
