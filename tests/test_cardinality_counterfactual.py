from powerxai.counterfactual import cardinality_counterfactual_value
from .value_functions import (
    weighted_ABC_value,
    always_return_one_as_value,
    cardinality_value,
)


def test_cardinality_counterfactual_asymmetric_contributions():
    players = ["A", "B", "C"]
    expected = [6.0, 4.0, 2.0, 0.0]
    result = [
        cardinality_counterfactual_value(cardinality=i, players=players, value_function=weighted_ABC_value)
        for i in range(len(players) + 1)
    ]
    assert result == expected


def test_cardinality_counterfactual_static_value_function():
    players = ["A", "B", "C"]
    expected = [0.0, 0.0, 0.0, 0.0]
    result = [
        cardinality_counterfactual_value(cardinality=i, players=players, value_function=always_return_one_as_value)
        for i in range(len(players) + 1)
    ]
    assert result == expected


def test_cardinality_counterfactual_cardinality_measure():
    players = ["A", "B", "C"]
    expected = [0.0, -1.0, 0.0, 0.0]
    result = [
        cardinality_counterfactual_value(cardinality=i, players=players, value_function=cardinality_value)
        for i in range(len(players) + 1)
    ]
    assert result == expected
