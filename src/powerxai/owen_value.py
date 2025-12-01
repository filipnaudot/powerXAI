from math import factorial
from powerxai.shapley_value import shapley_weighted_coalitions
from powerxai.types import Callable, Any

def owen_value(player_index: int,
               players: list[Any],
               value_function: Callable[[list[Any], set[int]], float],
               ) -> float:
    """
    Compute the Owen value for a given player in a cooperative game with
    a priori unions (group structure).

    We assume:
        - `players` may be a partitioned list of groups list[Any] or list[list[Any]]),
        each group being a list of atomic players.
        - Atomic players are referred to by their index in the flattened list of players.
        - `player_index` is an index in [0, total_number_of_atomic_players - 1].
        - `value_function(flattened_players, S)` returns v(S), where S is a set of
          atomic player indices in the flattened list.

    Args:
        player_index (int): Index of the atomic player whose Owen value is computed
            in the flattened players list.
        players (list[Any]): List of players (each player may be a group of atomic players: list[list[Any]]).
        value_function (Callable[[list[Any], set[int]], float]): 
            A function that returns the value of any coalition (based on the player indices).

    Returns:
        float: The Owen value of the specified player.
    """
    partition_as_indices, num_atomic_players = _get_partition_as_indices(players)
    assert 0 <= player_index < num_atomic_players, (f"player_index out of range. Must be in [0, {num_atomic_players - 1}]")

    group_index_of_player = next(group_index for group_index, group in enumerate(partition_as_indices) if player_index in group)
    num_groups = len(partition_as_indices)
    player_group = set(partition_as_indices[group_index_of_player])
    group_indices = set(range(num_groups))

    total_value = 0.0
    # Form coalitions of groups, excluding the group containing the player of interest.
    for indices_outer_coalition, weight_outer_coalition in shapley_weighted_coalitions(group_index_of_player, group_indices):
        players_of_outer_coalition = {player for idx in indices_outer_coalition for player in partition_as_indices[idx]}

        # Form coalitions of players within the group containing the player of interest, excluding the player of interest.
        for inner_coalition, weight_inner_coalition in shapley_weighted_coalitions(player_index, player_group):
            weight = weight_outer_coalition * weight_inner_coalition
            base_coalition = players_of_outer_coalition | inner_coalition
            marginal_contribution = (
                value_function(players, base_coalition | {player_index}) -
                value_function(players, base_coalition)
            )
            total_value += weight * marginal_contribution

    return total_value


def _get_partition_as_indices(players: list[Any]) -> tuple[list[set[int]], int]:
    """
    Convert a partitioned list of player groups into index-based groups.

    Interprets `players` as a list of groups, where each group is an iterable
    of atomic players, and assigns consecutive integer indices to every
    atomic player in the order they appear.

    Args:
        players (list[Any]): A list of groups, where each group is a collection of atomic players.

    Returns:
        tuple[list[set[int]], int]: A pair (partition as indices, number of atomic players).
    """
    partition_as_indices: list[set[int]] = []
    current_index: int = 0
    for group in players:
        partition_as_indices.append(set(range(current_index, current_index := current_index + len(group))))
    return partition_as_indices, current_index