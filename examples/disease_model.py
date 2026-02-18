import numpy as np

class DiseaseClassificationModel:
    """
    Mock ML model for multi-class disease classification based on symptoms.
    
    This model simulates a realistic diagnostic system with non-linear feature
    interactions, making it suitable for demonstrating power indices in ML.
    
    Attributes:
    -----------
    feature_names : list of str
        Names of the 6 symptom features
    class_names : list of str
        Names of the 4 disease classes
    n_features : int
        Number of features (6)
    n_classes : int
        Number of classes (4)
    """
    FEATURE_NAMES = ['fever', 'cough', 'headache', 'muscle_ache', 'sore_throat', 'fatigue']
    CLASS_NAMES = ['flu', 'cold', 'covid', 'healthy']
    NUM_FEATURES = len(FEATURE_NAMES)
    NUM_CLASSES = len(CLASS_NAMES)
    
    def __init__(self):
        """Initialize the model."""
        self.feature_names = self.FEATURE_NAMES
        self.class_names = self.CLASS_NAMES
        self.num_features = self.NUM_FEATURES
        self.num_classes = self.NUM_CLASSES
    

    def classify(self, symptoms, PRINT: bool = True):
        """
        Classify a symptom vector into disease probabilities.
        
        Parameters:
        -----------
        symptoms : array-like, shape (6,)
            Binary vector indicating presence (1) or absence (0) of symptoms:
            [fever, cough, headache, muscle_ache, sore_throat, fatigue]
        
        Returns:
        --------
        predicted_class : str
            Name of the class with the highest probability.
        predicted_prob : float
            Probability of the predicted class.
        class_names : list of str
            Names of the classes in a fixed order (see CLASS_NAMES above).
        probs : numpy array, shape (4,)
            Probability distribution over disease classes (sums to 1 and aligned w/ CLASS_NAMES).
        """
        symptoms = np.array(symptoms, dtype=float)
        if len(symptoms) != self.num_features:
            raise ValueError(f"Expected {self.num_features} features, got {len(symptoms)}")
        
        fever, cough, headache, muscle_ache, sore_throat, fatigue = symptoms
        flu_score = self._compute_flu_score(fever, cough, headache, muscle_ache, sore_throat, fatigue)
        cold_score = self._compute_cold_score(fever, cough, headache, muscle_ache, sore_throat, fatigue)
        covid_score = self._compute_covid_score(fever, cough, headache, muscle_ache, sore_throat, fatigue)
        healthy_score = self._compute_healthy_score(symptoms)
        scores = np.array([flu_score, cold_score, covid_score, healthy_score])
        probs = self._softmax(scores)
        max_index = np.argmax(probs)
        return self.class_names[max_index], probs[max_index], self.class_names, probs
    

    def print_prediction(self, symptoms, description=""):
        """
        Classify and pretty-print the prediction with optional description.
        
        Parameters:
        -----------
        symptoms : array-like, shape (6,)
            Binary symptom vector
        description : str, optional
            Description to print before prediction
        """
        prediction, prediction_prob, class_names, probs = self.classify(symptoms)
        if description: print(f"\n{description}")
        print(f"Symptoms: {symptoms}")
        active_symptoms = [self.feature_names[i] for i, s in enumerate(symptoms) if s == 1]
        print(f"Active: {', '.join(active_symptoms) if active_symptoms else 'none'}")
        print("\nPredictions:")
        for class_name, prob in zip(class_names, probs):
            bar = '█' * int(prob * 50)
            highlight = ' ← PREDICTED' if prob == max(probs) else ''
            print(f"  {class_name:8s}: {prob:.3f} {bar}{highlight}")
    

    def _softmax(self, scores):
        """Apply softmax to convert scores to probabilities."""
        exp_scores = np.exp(scores - np.max(scores))
        return exp_scores / np.sum(exp_scores)
    

    def _compute_flu_score(self, fever, cough, headache, muscle_ache, sore_throat, fatigue):
        """Compute raw score for flu diagnosis."""
        score = (
            2.0 * fever +
            1.5 * cough +
            0.5 * headache +
            1.0 * muscle_ache +
            0.3 * sore_throat +
            0.8 * fatigue +
            # Synergies
            3.0 * fever * cough +
            1.5 * fever * muscle_ache +
            1.0 * cough * fatigue +
            # Negative interaction (too many symptoms so maybe not flu)
            -1.2 * fever * cough * headache * sore_throat
        )
        return score
    

    def _compute_cold_score(self, fever, cough, headache, muscle_ache, sore_throat, fatigue):
        """Compute raw score for cold diagnosis."""
        score = (
            -0.5 * fever +
            1.0 * cough +
            0.8 * headache +
            0.3 * muscle_ache +
            2.0 * sore_throat +
            0.5 * fatigue +
            # Synergies
            2.0 * sore_throat * cough +
            1.0 * sore_throat * headache +
            -0.8 * fever * sore_throat
        )
        return score
    
    
    def _compute_covid_score(self, fever, cough, headache, muscle_ache, sore_throat, fatigue):
        """Compute raw score for COVID diagnosis."""
        n_symptoms = fever + cough + headache + muscle_ache + sore_throat + fatigue
        score = (
            1.8 * fever +
            1.2 * cough +
            1.0 * headache +
            1.2 * muscle_ache +
            0.8 * sore_throat +
            1.5 * fatigue +
            2.0 * fever * fatigue +
            1.5 * fever * muscle_ache +
            1.0 * cough * headache +
            0.5 * n_symptoms * (n_symptoms > 4)
        )
        return score
    

    def _compute_healthy_score(self, symptoms):
        """Compute raw score for healthy state."""
        n_symptoms = np.sum(symptoms)
        score = (
            5.0 +
            -3.0 * n_symptoms +
            -2.0 * n_symptoms**2
        )
        return score


if __name__ == "__main__":
    print("=== Disease Diagnosis Model Demo ===\n")

    model = DiseaseClassificationModel()
    test_cases = [
        ([0, 0, 0, 0, 0, 0], "No symptoms"),
        ([1, 1, 0, 0, 0, 0], "Fever + Cough"),
        ([1, 1, 1, 1, 0, 0], "Fever + Cough + Headache + Muscle ache"),
        ([0, 1, 0, 0, 1, 0], "Cough + Sore throat"),
        ([1, 0, 0, 1, 0, 1], "Fever + Muscle ache + Fatigue"),
        ([1, 1, 1, 1, 1, 1], "All symptoms"),
    ]
    
    for symptoms, description in test_cases:
        model.print_prediction(symptoms, description)

    def value_function(model, feature_indices, target_class=0):
        """
        Example value_function (a.k.a. 'the game') that just returns the prediction prob for a given class.
        
        :param feature_indices: List of indices representing the features to include
        :param target_class: Description
        """
        if isinstance(target_class, str):
            if target_class not in model.CLASS_NAMES: raise ValueError(f"Unknown class: {target_class}")
            target_class = model.CLASS_NAMES.index(target_class)
        symptoms = [0] * model.NUM_FEATURES
        for index in feature_indices:
            if index < 0 or index >= model.NUM_FEATURES: raise ValueError(f"Feature index {index} out of range [0, {model.NUM_FEATURES - 1}]")
            symptoms[index] = 1
        prediction, prediction_prob, class_names, probs = model.classify(symptoms)
        return probs[target_class]
    
    print("\n\n=== Value Function Examples (for Power Indices) ===\n")
    print(f"  {{fever, cough}}: {value_function(model, [0, 1]):.3f}")
    print(f"  {{fever}}: {value_function(model, [0]):.3f}")
    print(f"  {{cough}}: {value_function(model, [1]):.3f}")
    print(f"  {{fever, cough, headache}}: {value_function(model, [0, 1, 2]):.3f}")
    print(f"  All symptoms: {value_function(model, [0, 1, 2, 3, 4, 5]):.3f}")
    
    # Show synergy (set-based indices can capture this)
    print("\n\n=== Feature Synergy Example ===")
    value_fever = value_function(model, [0])
    value_cough = value_function(model, [1])
    value_both = value_function(model, [0, 1])
    print(f"v({{fever}}) = {value_fever:.3f}")
    print(f"v({{cough}}) = {value_cough:.3f}")
    print(f"v({{fever}}) + v({{cough}}) = {value_fever + value_cough:.3f}")
    print(f"v({{fever, cough}}) = {value_both:.3f}")
    print(f"Synergy: {value_both:.3f} > {value_fever + value_cough:.3f}")
