import os
import numpy as np
import matplotlib.pyplot as plt

from disease_model import DiseaseClassificationModel
from powerxai import shapley_value, owen_value

os.makedirs("./plots", exist_ok=True)


model = DiseaseClassificationModel()
feature_names = model.FEATURE_NAMES
TARGET_CLASS = "covid"
TARGET_CLASS_INDEX = model.CLASS_NAMES.index(TARGET_CLASS)
PROBABILITIES_INDEX = 3

owen_groups = [["fever", "cough", "headache"], ["muscle_ache", "sore_throat", "fatigue"]]


def probability_of_cold(players, coalition_indices):
    symptom_vector = [1 if i in coalition_indices else 0 for i in range(len(feature_names))]
    probabilities = model.classify(symptom_vector, PRINT=False)[PROBABILITIES_INDEX]
    return probabilities[TARGET_CLASS_INDEX]


### Compute influence scores
num_features = len(feature_names)
shapley_scores = np.array([shapley_value(i, feature_names, probability_of_cold) for i in range(num_features)])
owen_scores = np.array([owen_value(i, owen_groups, probability_of_cold) for i in range(num_features)])
print(shapley_scores)
print(owen_scores)
shapley_ranking = np.argsort(np.abs(shapley_scores))[::-1]
owen_ranking = np.argsort(np.abs(owen_scores))[::-1]

# Map each feature to its 1-based rank position
shapley_rank_of = np.empty(num_features, dtype=int)
owen_rank_of = np.empty(num_features, dtype=int)
shapley_rank_of[shapley_ranking] = np.arange(1, num_features + 1)
owen_rank_of[owen_ranking] = np.arange(1, num_features + 1)

### Bump chart
fig, ax = plt.subplots(figsize=(5, 4))
for i in range(num_features):
    rank_changed = shapley_rank_of[i] != owen_rank_of[i]
    color = "crimson" if rank_changed else "steelblue"
    alpha = 1.0 if rank_changed else 0.4
    ax.plot([0, 1], [shapley_rank_of[i], owen_rank_of[i]], "o-", color=color, alpha=alpha, linewidth=2, markersize=7)
    ax.text(-0.08, shapley_rank_of[i], feature_names[i], ha="right", va="center", fontsize=9)
    ax.text(1.08, owen_rank_of[i], feature_names[i], ha="left", va="center", fontsize=9)

ax.set_xticks([0, 1])
ax.set_xticklabels(["Shapley", "Owen"], fontsize=11, fontweight="bold")
ax.set_xlim(-0.45, 1.45)
ax.invert_yaxis()
ax.set_yticks(range(1, num_features + 1))
ax.set_ylabel("Rank")
ax.set_title(f"Ranking shift: Shapley vs Owen. Target Disease: {TARGET_CLASS}")
ax.grid(axis="y", linestyle=":", alpha=0.4)
plt.tight_layout()
plt.savefig("./plots/shapley_vs_owen_bump_cold.png", dpi=300, bbox_inches="tight")
