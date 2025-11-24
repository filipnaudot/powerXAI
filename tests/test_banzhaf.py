from powerxai.banzhaf_value import banzhaf_value
from .value_functions import (
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