from powerxai.counterfactual import counterfactual_value
from .value_functions import (
    C_is_valuable_value,
    weighted_ABC_value,
    always_return_one_as_value,
)


def test_counterfactual_single_non_null_player():
    players = ["A", "B", "C", "D"]
    expected = [0.0, 0.0, 1.0, 0.0]
    num_players = len(players)
    result = [
        counterfactual_value(player_index=i, players=players, value_function=C_is_valuable_value)
        for i in range(num_players)
    ]
    assert result == expected


def test_counterfactual_asymmetric_contributions():
    players = ["A", "B", "C"]
    expected = [1.0, 2.0, 3.0]
    num_players = len(players)
    result = [
        counterfactual_value(player_index=i, players=players, value_function=weighted_ABC_value)
        for i in range(num_players)
    ]
    assert result == expected


def test_counterfactual_static_value_function():
    players = ["A", "B", "C"]
    expected = [0.0, 0.0, 0.0]
    num_players = len(players)
    result = [
        counterfactual_value(player_index=i, players=players, value_function=always_return_one_as_value)
        for i in range(num_players)
    ]
    assert result == expected
