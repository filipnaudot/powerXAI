"""
This file contains definitions of value functions that can be used for tests.
To use these value functions, label the players using capital letters A, B, C, ... , Z. 
Ensure that the value function supports the full set of players you define.
For instance, if your players are [A, B, C, D] but the value function is defined only for [A, B], 
you may encounter unexpected behavior.
"""


def C_is_valuable_value(players, coalition) -> float:
    """
    Value function that only values the player C.

    Args:
        players (List[Any]): List of players or elements in the reference set.
        coalition (Set[int]): Indices of players whose coalition value is computed.

    Returns:
        float: 1.0 if C is in the given coalition (defined by indices), 0.0 otherwise.
    """
    player_coalition = [players[index] for index in coalition]
    if "C" in player_coalition: return 1.0
    else:                       return 0.0


def A_and_C_is_valuable_value(players, coalition) -> float:
    """
    Value function that only values the players A and C.

    Args:
        players (List[Any]): List of players or elements in the reference set.
        coalition (Set[int]): Indices of players whose coalition value is computed.

    Returns:
        float: 1.0 if A or C is in the given coalition (defined by indices), 0.0 otherwise.
    """
    player_coalition = [players[index] for index in coalition]
    if   "A" in player_coalition: return 1.0
    elif "C" in player_coalition: return 1.0
    else:                         return 0.0


def weighted_ABC_value(players, coalition) -> float:
    """
    Value function that weights the players. The value is
    defined as the value of the sum of the individual players' weights.

    Args:
        players (List[Any]): List of players or elements in the reference set.
        coalition (Set[int]): Indices of players whose coalition value is computed.

    Returns:
        float: The sum of the individual players' weights.
    """
    weights = {"A": 1, "B": 2, "C": 3}
    return float(sum(weights[players[i]] for i in coalition))


def always_return_one_as_value(players, coalition) -> float:
    """
    Value function that always returns 1.0.

    Args:
        players (List[Any]): List of players or elements in the reference set.
        coalition (Set[int]): Indices of players whose coalition value is computed.

    Returns:
        float: 1.0.
    """
    return 1.0


def cardinality_value(players, coalition) -> float:
    """
    Value function that checks if the cardinality 
    of the coalition is one or not.

    Args:
        players (List[Any]): List of players or elements in the reference set.
        coalition (Set[int]): Indices of players whose coalition value is computed.

    Returns:
        float: 1.0 if the cardinality of the given set is 1, 0.0 otherwise.
    """
    if len(coalition) == 1: return 1.0
    return 0.0


def majority_value(players, coalition)  -> float:
    """
    Value function that checks if the majority
    of the the players are in the given coalition.

    Args:
        players (List[Any]): List of players or elements in the reference set.
        coalition (Set[int]): Indices of players whose coalition value is computed.

    Returns:
        float: 1.0 if the majority of the players are present.
    """
    return 1.0 if len(coalition) >= (len(players) // 2) else 0.0