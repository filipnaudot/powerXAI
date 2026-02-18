import os
import numpy as np
import matplotlib.pyplot as plt

from powerxai import shapley_value, upsilon_value

os.makedirs("./plots", exist_ok=True)


PLAYERS = ["A", "B", "C"]

def game(players, coalition_indices):
    coalition = [PLAYERS[index] for index in coalition_indices]
    if set(coalition) == {PLAYERS[0], PLAYERS[1]}: return 1
    return 0


num_features = len(PLAYERS)
shapley_scores = np.array([shapley_value(i, PLAYERS, game) for i in range(num_features)])
upsilon_scores = np.array([upsilon_value(position, PLAYERS, game) for position in range(1, num_features + 1)])


coalition_size_labels = [f"size {i}" for i in range(1, num_features + 1)]
fig, (ax_shapley, ax_upsilon) = plt.subplots(1, 2, figsize=(10, 4))

# Shapley: contribution per player
shapley_colors = ["steelblue" if v >= 0 else "crimson" for v in shapley_scores]
ax_shapley.bar(range(num_features), shapley_scores, color=shapley_colors, edgecolor="white", linewidth=0.5)
ax_shapley.set_xticks(range(num_features))
ax_shapley.set_xticklabels(PLAYERS)
ax_shapley.set_ylabel("Avg. marginal contribution")
ax_shapley.set_xlabel("Player")
ax_shapley.set_title("Shapley value (per player)")
ax_shapley.axhline(0, color="black", linewidth=0.8)
ax_shapley.grid(axis="y", linestyle=":", alpha=0.4)

# Upsilon: contribution per cardinality
upsilon_colors = ["steelblue" if v >= 0 else "crimson" for v in upsilon_scores]
ax_upsilon.bar(range(num_features), upsilon_scores, color=upsilon_colors, edgecolor="white", linewidth=0.5)
ax_upsilon.set_xticks(range(num_features))
ax_upsilon.set_xticklabels(coalition_size_labels)
ax_upsilon.set_ylabel("Avg. marginal contribution")
ax_upsilon.set_xlabel("Coalition size")
ax_upsilon.set_title("Upsilon value (per cardinality)")
ax_upsilon.axhline(0, color="black", linewidth=0.8)
ax_upsilon.grid(axis="y", linestyle=":", alpha=0.4)

plt.tight_layout()
plt.savefig("./plots/shapley_vs_upsilon.png", dpi=300, bbox_inches="tight")
