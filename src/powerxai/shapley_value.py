from math import factorial
from powerxai.types import Callable, Any
from powerxai.coalitions import coalitions



def shapley_weighted_coalitions(player_index: int,
                                player_indices: set[int],
                                ) -> list[tuple[set[int], float]]:
    """
    Creates all coalitions of players as a list of tuples 
    (coalition, weight) where `weight` is the Shapley weight for that coalition.

    Args:
        player_index (int): The index of the player whose Shapley value is computed.
        player_indices (set[int]): The set of indices for which to compute the coalitions.

    Returns:
        A list of pairs (coalition, weight), where `coalition` is a set of 
        player indices and `weight` is the corresponding Shapley weight for that coalition.
    """
    result: list[tuple[set[int], float]] = []
    num_players = len(player_indices)
    for coalition in coalitions(player_indices  - {player_index}):
        size_coalition = len(coalition)
        weight = factorial(size_coalition) * factorial(num_players - size_coalition - 1) / factorial(num_players)
        result.append((coalition, weight))
    return result


def shapley_value(player_index: int,
                  players: list[Any],
                  value_function: Callable[[list[Any], set[int]], float]
                  ) -> float:
    """
    Compute the Shapley value for a given player in a cooperative game.

    The Shapley value quantifies a player's average marginal contribution 
    across all possible coalitions.

    Args:
        player_index (int): The index of the player whose Shapley value is computed.
        players (list[Any]): list of players.
        value_function (Callable[[list[Any], set[int]], float]): 
            A function that returns the value of any coalition (based on the player indices).

    Returns:
        float: The Shapley value of the specified player.
    """
    num_players = len(players)
    assert player_index < num_players, f"player_index out of range. Must be in [0, {num_players - 1}]"
    all_player_indices = set(range(num_players))
    total_value = 0.0
    for coalition, weight in shapley_weighted_coalitions(player_index, all_player_indices):
        marginal_contribution = value_function(players, coalition | {player_index}) - value_function(players, coalition)
        total_value += weight * marginal_contribution

    return total_value