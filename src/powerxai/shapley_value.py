from math import factorial
from powerxai.types import Callable, Any
from powerxai.coalitions import coalitions



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
    for coalition in coalitions(all_player_indices - {player_index}):
        weight = (factorial(len(coalition)) * factorial(num_players - len(coalition) - 1)) / factorial(num_players)
        marginal_contribution = value_function(players, coalition | {player_index}) - value_function(players, coalition)
        total_value += weight * marginal_contribution

    return total_value