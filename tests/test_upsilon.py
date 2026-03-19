from powerxai.upsilon_value import upsilon_value
from .value_functions import (
    cardinality_value,
    C_is_valuable_value,
    always_return_one_as_value,
)


def test_cardinality_measure():    
    players = ["A", "B", "C"]
    expected = [1.0, -1.0, 0.0]
    result = [
        upsilon_value(cardinality=i, players=players, value_function=cardinality_value)
        for i in range(1, len(players)+1)
    ]
    assert result == expected


def test_static_measure():
    players = ["A", "B", "C"]
    expected = [0.0, 0.0, 0.0]
    result = [
        upsilon_value(cardinality=i, players=players, value_function=always_return_one_as_value)
        for i in range(1, len(players)+1)
    ]
    assert result == expected


def test_single_valuable_player():    
    players = ["A", "B", "C", "D"]
    expected = [0.25, 0.25, 0.25, 0.25]
    result = [
        upsilon_value(cardinality=i, players=players, value_function=C_is_valuable_value)
        for i in range(1, len(players)+1)
    ]
    assert result == expected
