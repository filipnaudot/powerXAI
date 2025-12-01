import pytest
from powerxai.shapley_value import shapley_weighted_coalitions


def test_single_player():
    result = shapley_weighted_coalitions(0, {0})
    expected = [(set(), 1.0)]
    assert result == expected


def test_order_invariant_player0():
    result_1 = shapley_weighted_coalitions(0, {0, 1, 2})
    result_2 = shapley_weighted_coalitions(0, {2, 1, 0})
    assert result_1 == result_2


def test_shapley_weighted_coalitions_three_players_player0():
    player_indices = {0, 1, 2}
    result = shapley_weighted_coalitions(0, player_indices)
    coalition_to_weight = {frozenset(coalition): weight for coalition, weight in result}
    expected = {
        frozenset():       1/3,
        frozenset({1}):    1/6,
        frozenset({2}):    1/6,
        frozenset({1, 2}): 1/3,
    }
    assert set(coalition_to_weight.keys()) == set(expected.keys())
    for coalition, expected_weight in expected.items():
        assert coalition_to_weight[coalition] == expected_weight


@pytest.mark.parametrize("num_players", [1, 2, 3, 4])
def test_shapley_weighted_coalitions_count(num_players):
    player_indices = set(range(num_players))
    for player_index in player_indices:
        result = shapley_weighted_coalitions(player_index, player_indices)
        assert len(result) == 2**(num_players - 1)


@pytest.mark.parametrize("num_players", [1, 2, 3, 4])
def test_shapley_weighted_coalitions_weights_sum_to_one(num_players):
    player_indices = set(range(num_players))
    for player_index in player_indices:
        result = shapley_weighted_coalitions(player_index, player_indices)
        total_weight = sum(weight for _, weight in result)
        assert total_weight == 1.0