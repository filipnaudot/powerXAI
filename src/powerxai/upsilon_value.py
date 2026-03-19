from math import factorial
from powerxai.types import Callable, Any
from powerxai.coalitions import maximal_chains



def upsilon_value(cardinality: int,
                  players: list[Any],
                  value_function: Callable[[list[Any], set[int]], float]
                  ) -> float:
    """
    Compute the Y-value (upsilon value) for a given cardinality in a maximal chain of sets.

    The Y-value quantifies the average marginal contribution of set size c
    across all maximal chains in the lattice of subsets.
    Unlike the Shapley value, which assigns importance to individual players,
    the Y-value measures the influence of set cardinality or rank position in the chain.

    Args:
        cardinality (int): Cardinality indicating the position in the chain (1 ≤ c ≤ n).
        players (list[Any]): list of players or elements in the reference set.
        value_function (Callable[[list[Any], set[int]], float]):
            A function that returns the value of any coalition (based on the player indices).

    Returns:
        float: The Y-value corresponding to the specified cardinality.
    """
    num_players = len(players)
    assert 1 <= cardinality <= num_players, f"cardinality must be in [1, {len(players)}]"
    all_player_indices = set(range(num_players))
    total_value = 0.0
    for chain in maximal_chains(all_player_indices):
        total_value += value_function(players, chain[cardinality]) - value_function(players, chain[cardinality - 1])

    return (total_value / factorial(num_players))
