from functools import cache
from math import comb
from powerxai.types import Callable, Any
from powerxai.coalitions import coalitions



def banzhaf_value(player_index: int,
                  players: list[Any],
                  value_function: Callable[[list[Any], set[int]], float],
                  *,
                  probabilistic: bool = False,
                  ) -> float:
    """
    Compute the Banzhaf value for a given player in a cooperative game.

    If probabilistic is False (default), this returns the *raw* Banzhaf index, 
    i.e. the sum of the player's marginal contributions over all coalitions of the other players. 
    
    If probabilistic is True, this returns the *probabilistic* Banzhaf value, 
    i.e. the average marginal contribution over all 2^(n-1) coalitions of the other players.

    Args:
        player_index (int): The index of the player whose Banzhaf value is computed.
        players (list[Any]): list of players.
        value_function (Callable[[list[Any], set[int]], float]): 
            A function that returns the value of any coalition (based on the player indices).
        probabilistic (bool, optional):
            If False (default), return the raw Banzhaf value (sum of marginal contributions).
            If True, return the probabilistic Banzhaf value (average marginal contribution).


    Returns:
        float: The Banzhaf value of the specified player.
    """
    num_players = len(players)
    all_player_indices = set(range(num_players))
    total_marginal = 0.0
    for coalition in coalitions(all_player_indices - {player_index}):
        total_marginal += value_function(players, coalition | {player_index}) - value_function(players, coalition)
    
    if probabilistic: return total_marginal / (2**(num_players - 1))
    return total_marginal





#################
# CARDINALITY
#################

@cache
def _cardinality_banzhaf_weight(cardinality: int, num_players: int) -> float:
    return (1 / comb(num_players, cardinality) * num_players * comb(num_players - 1, cardinality) / 2**(num_players - 1))


def cardinality_banzhaf_value(cardinality: int,
                              players: list[Any],
                              value_function: Callable[[list[Any], set[int]], float]
                              ) -> float:
    """
    Compute the cardinality-based Banzhaf value for a given cardinality.

    The cardinality-based Banzhaf value compares the total value of coalitions
    with size c against coalitions with size c - 1, using the Banzhaf correction
    for each cardinality layer.

    Args:
        cardinality (int): Cardinality indicating the layer difference (1 <= c <= n).
        players (list[Any]): list of players or elements in the reference set.
        value_function (Callable[[list[Any], set[int]], float]):
            A function that returns the value of any coalition (based on the player indices).

    Returns:
        float: The cardinality-based Banzhaf value for the specified cardinality.
    """
    num_players = len(players)
    assert 1 <= cardinality <= num_players, f"cardinality must be in [1, {num_players}]"
    all_player_indices = set(range(num_players))

    total_value = 0.0
    for coalition in coalitions(all_player_indices, cardinality=cardinality):
        total_value += value_function(players, coalition) * _cardinality_banzhaf_weight(cardinality, num_players)
    for coalition in coalitions(all_player_indices, cardinality=cardinality - 1):
        total_value -= value_function(players, coalition) * _cardinality_banzhaf_weight(cardinality - 1, num_players)
    return total_value
