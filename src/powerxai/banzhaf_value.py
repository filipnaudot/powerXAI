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