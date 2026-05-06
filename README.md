<div align="center">
  <img src="docs/_static/logo-powerxai.png" alt="powerXAI logo" width="180">
</div>
<div align="center">
  Power Indices for Explainable AI
</div>
<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue" alt="Supported Python versions: 3.10 to 3.14">
</div>



## Supported Indices

The library currently implements the following indices and attribution measures:

| Index / measure | Single player | Set of players | Cardinality |
|---|---:|---:|---:|
| Shapley value | Yes | Yes | No |
| Banzhaf value | Yes | Yes | No |
| Owen value | Yes | Yes | No |
| Upsilon value | No | No | Yes |
| Counterfactual value | Yes | Yes | No |
| Cardinality counterfactual value | No | No | Yes |

> [!NOTE]
> For sets of players, the library treats each set or group as one player. The returned values are defined at the level chosen by the user through the structure of `players`. `owen_value` is the special case where players are organized into explicit groups, and the user can choose whether to work at the level of the groups or at the level of the individual players inside them.

## Getting Started

Create and activate a virtual environment:

```bash
python -m venv env
```
```bash
source env/bin/activate
```

Install the project in editable mode:

```bash
pip install -e .
```

Try a minimal example:

```python
from powerxai import shapley_value

def weighted_ABC_value(players, coalition) -> float:
    weights = {"A": 1, "B": 2, "C": 3}
    return float(sum(weights.get(players[i], 0) for i in coalition))

players = ["A", "B", "C", "D"]
result = shapley_value(player_index=0, players=players, value_function=weighted_ABC_value)

print(f"The Shapley value for player 'A' is: {result}")
```

---
