from powerxai.banzhaf_value import banzhaf_value, cardinality_banzhaf_value
from .value_functions import (
    always_return_one_as_value,
    always_return_zero_as_value,
    cardinality_value,
    C_is_valuable_value,
    A_and_C_is_valuable_value,
    majority_value,
)


def test_banzhaf_single_non_null_player_raw():
    """
    Using C_is_valuable_value, C will have the
    power the swing 2^(N-1) coalitions.
    With N = 4, we get: 2^3 = 8.
    """
    players = ["A", "B", "C", "D"]
    expected = [0.0, 0.0, 8.0, 0.0]
    num_players = len(players)
    result = [
        banzhaf_value(player_index=i, players=players, value_function=C_is_valuable_value)
        for i in range(num_players)
    ]
    assert result == expected


def test_banzhaf_single_non_null_player_probabilistic():
    """
    Using C_is_valuable_value, C will have the
    power the swing 2^(N-1) coalitions.
    With N = 4, we get: 2^3 = 8. Since, we want the 
    probabilistic Banzhaf value we get 8 / (2^(N-1)) = 1 for C.
    """
    players = ["A", "B", "C", "D"]
    expected = [0.0, 0.0, 1.0, 0.0]
    result = [
        banzhaf_value(player_index=i, players=players, value_function=C_is_valuable_value, probabilistic=True)
        for i in range(len(players))
    ]
    assert result == expected



def test_banzhaf_two_non_null_player_raw():
    """
    Using A_and_C_is_valuable_value, A and C 
    will have the power the swing 2^(N-2) coalitions.
    With N = 4, we get: 2^2 = 4.
    """
    players = ["A", "B", "C", "D"]
    expected = [4.0, 0.0, 4.0, 0.0]
    result = [
        banzhaf_value(player_index=i, players=players, value_function=A_and_C_is_valuable_value)
        for i in range(len(players))
    ]
    assert result == expected


def test_majority_game_raw():
    """
    In a 4-player majority game (value=1 if coalition size >=2),
    each player is pivotal in exactly 3 coalitions.
    """
    players = ["A", "B", "C", "D"]
    expected = [3.0, 3.0, 3.0, 3.0]
    result = [
        banzhaf_value(i, players, majority_value)
        for i in range(len(players))
    ]
    assert result == expected


def test_majority_game_probabilistic():
    """
    Probabilistic Banzhaf = raw / 8 for N=4.
    """
    players = ["A", "B", "C", "D"]
    expected = [3/8, 3/8, 3/8, 3/8]

    result = [
        banzhaf_value(i, players, majority_value, probabilistic=True)
        for i in range(len(players))
    ]
    assert result == expected




####################
# CARDINALITY
####################
def test_cardinality_banzhaf_static_measure():
    players = ["A", "B", "C"]
    expected = [0.00, 0.00, 0.00]
    result = [
        cardinality_banzhaf_value(cardinality=i, players=players, value_function=always_return_zero_as_value)
        for i in range(1, len(players)+1)
    ]
    assert result == expected


def test_cardinality_banzhaf_cardinality_measure():
    players = ["A", "B", "C"]
    expected = [1.5, -1.5, 0.0]
    result = [
        cardinality_banzhaf_value(cardinality=i, players=players, value_function=cardinality_value)
        for i in range(1, len(players)+1)
    ]
    assert result == expected


def test_cardinality_banzhaf_single_player_with_cardinality_measure():
    """
    The cardinality definition gives zero weight to the grand coalition (grand coalition has size n): comb(n - 1, n) = 0.
    For a single-player game, the only coalition containing any players is the grand coalition,
    so all single-player games will have cardinality-Banzhaf value of 0 regardless of the value function.
    """
    players = ["A"]
    expected = [0.0]
    result = [
        cardinality_banzhaf_value(cardinality=i, players=players, value_function=cardinality_value)
        for i in range(1, len(players)+1)
    ]
    assert result == expected
