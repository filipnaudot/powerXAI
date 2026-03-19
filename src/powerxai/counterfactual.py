from math import comb
from powerxai.coalitions import coalitions
from powerxai.types import Callable, Any



def counterfactual_value(player_index: int,
                         players: list[Any],
                         value_function: Callable[[list[Any], set[int]], float]
                         ) -> float:
    """
    Compute the counterfactual value for a given player.

    The counterfactual value is defined as the value of the grand coalition
    minus the value of the grand coalition without the player of interest.

    Args:
        player_index (int): The index of the player whose counterfactual value is computed.
        players (list[Any]): list of players.
        value_function (Callable[[list[Any], set[int]], float]):
            A function that returns the value of any coalition (based on the player indices).

    Returns:
        float: The counterfactual value of the specified player.
    """
    num_players = len(players)
    assert player_index < num_players, f"player_index out of range. Must be in [0, {num_players - 1}]"
    all_player_indices = set(range(num_players))
    return value_function(players, all_player_indices) - value_function(players, all_player_indices - {player_index})




def cardinality_counterfactual_value(cardinality: int,
                                     players: list[Any],
                                     value_function: Callable[[list[Any], set[int]], float]
                                     ) -> float:
    """
    Compute the cardinality-based counterfactual value for a given cardinality.

    The cardinality-based counterfactual value is defined as the value of the
    grand coalition minus the average value of all coalitions with the given cardinality.

    Args:
        cardinality (int): The coalition cardinality c, where 0 <= c <= |N|.
        players (list[Any]): list of players.
        value_function (Callable[[list[Any], set[int]], float]):
            A function that returns the value of any coalition (based on the player indices).

    Returns:
        float: The cardinality-based counterfactual value for the specified cardinality.
    """
    num_players = len(players)
    assert 0 <= cardinality <= num_players, f"cardinality must be in [0, {num_players}]"
    all_player_indices = set(range(num_players))
    total_value = 0.0
    for coalition in coalitions(all_player_indices, cardinality=cardinality):
        total_value += value_function(players, coalition)

    return value_function(players, all_player_indices) - total_value / comb(num_players, cardinality)
