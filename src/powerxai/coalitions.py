from itertools import combinations


def coalitions(player_set: set[int], cardinality: int | None = None) -> list[set[int]]:
    """
    Enumerate all coalitions (all subsets) of the given set of players.

    Args:
        player_set (set[int]): Set of player indices.
        cardinality (int | None, optional): If provided, only enumerate coalitions of the specified size.

    Returns:
        list[set[int]]: A list of all subsets of player_set.
    """
    if cardinality is not None:
        assert 0 <= cardinality <= len(player_set), f"cardinality must be in [0, {len(player_set)}]"
        return [set(subset) for subset in combinations(player_set, cardinality)]

    return [set(subset) for subset_size in range(len(player_set) + 1)
            for subset in combinations(player_set, subset_size)]


def maximal_chains(player_set: set[int]) -> list[list[set[int]]]:
    """
    Enumerate all maximal chains in the subset lattice 2^X for the given players.

    Args:
        player_set (set[int]): Set of player indices.

    Returns:
        list[list[set[int]]]: A list of maximal chains. Each chain is a list of length n+1. There are n! chains.
    """
    from itertools import permutations
    X = tuple(player_set)
    return [[set(permutation[:i]) for i in range(len(X)+1)] for permutation in permutations(X)]
