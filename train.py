from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load data
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print(f"Accuracy: {round(acc, 3)}")

# Save serialized model artifact
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")
