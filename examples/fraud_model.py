from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ClassificationResult:
    predicted_class: str
    predicted_prob: float
    class_names: list[str]
    probabilities: np.ndarray

    def probability_of(self, class_name: str) -> float:
        if class_name not in self.class_names:
            raise ValueError(f"Unknown class: {class_name}")
        return float(self.probabilities[self.class_names.index(class_name)])

    @property
    def probability_by_class(self) -> dict[str, float]:
        return {class_name: float(probability)
                for class_name, probability in zip(self.class_names, self.probabilities)}


class FraudDetectionModel:
    """
    Mock ML model for transaction fraud classification.

    The model uses six binary risk indicators organized into two evidence channels:
    device/network signals and transaction-behavior signals.

    This keeps the public API aligned with the disease example while providing
    a setting where grouped attribution methods are easier to motivate.
    """

    FEATURE_NAMES = [
        "Location",
        "Foreign IP",
        "VPN Detected",
        "High Amount",
        "Velocity Spike",
        "Odd Hour",
    ]
    CLASS_NAMES = ["Legitimate", "Review", "Fraud", "Account Takeover"]
    NUM_FEATURES = len(FEATURE_NAMES)
    NUM_CLASSES = len(CLASS_NAMES)

    def __init__(self):
        self.feature_names = self.FEATURE_NAMES
        self.class_names = self.CLASS_NAMES
        self.num_features = self.NUM_FEATURES
        self.num_classes = self.NUM_CLASSES

    def classify(self, indicators, PRINT: bool = True):
        """
        Classify a transaction into fraud-related outcome probabilities.

        Parameters
        ----------
        indicators : array-like, shape (6,)
            Binary vector indicating whether a risk signal is present:
            [location, foreign_ip, vpn_detected, high_amount, velocity_spike, odd_hour]

        Returns
        -------
        ClassificationResult
            Structured prediction result with named fields and helper accessors.
        """
        indicators = np.array(indicators, dtype=float)
        if len(indicators) != self.num_features:
            raise ValueError(f"Expected {self.num_features} features, got {len(indicators)}")

        location, foreign_ip, vpn_detected, high_amount, velocity_spike, odd_hour = indicators

        device_risk = location + foreign_ip + vpn_detected
        transaction_risk = high_amount + velocity_spike + odd_hour
        total_risk = device_risk + transaction_risk

        legitimate_score = self._compute_legitimate_score(total_risk, device_risk, transaction_risk)
        review_score = self._compute_review_score(
            device_risk=device_risk,
            transaction_risk=transaction_risk,
            total_risk=total_risk,
            high_amount=high_amount,
            velocity_spike=velocity_spike,
            odd_hour=odd_hour,
        )
        fraud_score = self._compute_fraud_score(
            device_risk=device_risk,
            transaction_risk=transaction_risk,
            total_risk=total_risk,
            high_amount=high_amount,
            velocity_spike=velocity_spike,
            odd_hour=odd_hour,
        )
        account_takeover_score = self._compute_account_takeover_score(
            device_risk=device_risk,
            transaction_risk=transaction_risk,
            total_risk=total_risk,
            location=location,
            foreign_ip=foreign_ip,
            vpn_detected=vpn_detected,
        )

        scores = np.array([
            legitimate_score,
            review_score,
            fraud_score,
            account_takeover_score,
        ])
        probabilities = self._softmax(scores)
        max_index = np.argmax(probabilities)
        return ClassificationResult(
            predicted_class=self.class_names[max_index],
            predicted_prob=float(probabilities[max_index]),
            class_names=self.class_names,
            probabilities=probabilities,
        )

    def print_prediction(self, indicators, description=""):
        """Classify and pretty-print a transaction risk prediction."""
        result = self.classify(indicators)
        if description:
            print(f"\n{description}")
        print(f"Indicators: {indicators}")
        active_indicators = [self.feature_names[i] for i, x in enumerate(indicators) if x == 1]
        print(f"Active: {', '.join(active_indicators) if active_indicators else 'none'}")
        print("\nPredictions:")
        for class_name, probability in zip(result.class_names, result.probabilities):
            bar = "█" * int(probability * 50)
            highlight = " ← PREDICTED" if class_name == result.predicted_class else ""
            print(f"  {class_name:16s}: {probability:.3f} {bar}{highlight}")

    def _softmax(self, scores):
        exp_scores = np.exp(scores - np.max(scores))
        return exp_scores / np.sum(exp_scores)

    def _compute_legitimate_score(self, total_risk, device_risk, transaction_risk):
        return 5.5 - 2.8 * total_risk - 0.7 * device_risk * transaction_risk

    def _compute_review_score(self, device_risk, transaction_risk, total_risk, high_amount, velocity_spike, odd_hour):
        return (
            -0.5
            + 0.9 * total_risk
            + 0.8 * (device_risk > 0) * (transaction_risk > 0)
            + 0.6 * high_amount * odd_hour
            + 0.6 * velocity_spike * odd_hour
            - 0.8 * (total_risk > 4)
        )

    def _compute_fraud_score(self, device_risk, transaction_risk, total_risk, high_amount, velocity_spike, odd_hour):
        return (
            -1.2
            + 0.7 * device_risk
            + 1.1 * transaction_risk
            + 1.8 * (device_risk > 0) * (transaction_risk > 0)
            + 1.4 * high_amount * velocity_spike
            + 1.0 * high_amount * odd_hour
            + 1.0 * velocity_spike * odd_hour
            + 0.8 * (total_risk > 4)
        )

    def _compute_account_takeover_score(self, device_risk, transaction_risk, total_risk, location, foreign_ip, vpn_detected):
        # Treat the three device/network indicators as a nearly symmetric
        # "credential compromise" channel. This makes account takeover a good
        # target for group-aware attribution examples without changing the public API.
        return (
            -2.0
            + 0.35 * device_risk
            + 0.15 * transaction_risk
            + 0.25 * (device_risk > 0)
            + 0.55 * (device_risk > 1)
            + 5.0 * location * foreign_ip * vpn_detected
            + 0.35 * (total_risk > 3)
        )


if __name__ == "__main__":
    print("=== Fraud Detection Model Demo ===\n")

    model = FraudDetectionModel()
    test_cases = [
        ([0, 0, 0, 0, 0, 0], "Normal checkout"),
        ([1, 0, 0, 0, 0, 0], "Known customer from a new location"),
        ([0, 0, 0, 1, 1, 0], "Large fast-spiking purchase"),
        ([1, 1, 1, 0, 0, 0], "Suspicious login environment"),
        ([1, 0, 1, 1, 1, 0], "Device risk plus aggressive transaction pattern"),
        ([1, 1, 1, 1, 1, 1], "All signals active"),
    ]

    for indicators, description in test_cases:
        model.print_prediction(indicators, description)

    def value_function(model, feature_indices, target_class=2):
        """
        Example value function that returns the predicted probability for a class.

        Parameters
        ----------
        feature_indices : list[int]
            Indices of active fraud signals.
        target_class : int | str
            Class index or class name.
        """
        if isinstance(target_class, str):
            if target_class not in model.CLASS_NAMES:
                raise ValueError(f"Unknown class: {target_class}")
            target_class = model.CLASS_NAMES.index(target_class)

        indicators = [0] * model.NUM_FEATURES
        for index in feature_indices:
            if index < 0 or index >= model.NUM_FEATURES:
                raise ValueError(f"Feature index {index} out of range [0, {model.NUM_FEATURES - 1}]")
            indicators[index] = 1

        result = model.classify(indicators)
        return float(result.probabilities[target_class])

    print("\n\n=== Value Function Examples (for Power Indices) ===\n")
    print(f"  {{location}} -> Account Takeover: {value_function(model, [0], 'Account Takeover'):.3f}")
    print(f"  {{location, Foreign IP}} -> Account Takeover: {value_function(model, [0, 1], 'Account Takeover'):.3f}")
    print(f"  {{location, Foreign IP, vpn_detected}} -> Account Takeover: {value_function(model, [0, 1, 2], 'Account Takeover'):.3f}")
    print(f"  {{high_amount, Velocity Spike}} -> Fraud: {value_function(model, [3, 4], 'Fraud'):.3f}")
