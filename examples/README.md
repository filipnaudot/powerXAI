# Medical Diagnosis Example
`disease_model.py` contains the disease classifier (mock ML model) used in the running example.
It simulates a real ML classifier by computing a score vector for each class and normalizing it with the softmax function.

## Properties of the model (by design):
- **Non-monotonic**: Adding more symptoms doesn't always increase flu probability
- **Feature synergies**: v({fever, cough}) > v({fever}) + v({cough})
- **Natural groupings**: Respiratory {fever, cough, sore_throat} vs. General {headache, muscle_ache, fatigue}
