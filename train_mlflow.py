import os
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# MLflow SQLite Tracking URI
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("iris-classifier")

with mlflow.start_run(run_name="iris_rf_production"):
    # Load dataset
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # Train Random Forest
    n_estimators = 100
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)

    # Log parameters, metrics & model artifact
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("test_size", 0.2)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, name="model", serialization_format="cloudpickle")

    # Save model.pkl locally for FastAPI inference
    joblib.dump(model, "model.pkl")

    print(f"Logged to MLflow, accuracy: {round(acc, 3)}")
    print(f"Model saved as model.pkl")
