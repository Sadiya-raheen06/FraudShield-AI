```python
import numpy as np
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def train_fraud_model():

    np.random.seed(42)

    size = 5000

    data = pd.DataFrame({
        "amount": np.random.randint(100, 100000, size),
        "new_receiver": np.random.randint(0, 2, size),
        "unusual_activity": np.random.randint(0, 2, size),
        "night_transaction": np.random.randint(0, 2, size),
        "international": np.random.randint(0, 2, size),
        "failed_attempts": np.random.randint(0, 6, size)
    })

    risk = (
        (data["amount"] > 50000).astype(int) * 2 +
        data["new_receiver"] +
        data["unusual_activity"] * 2 +
        data["night_transaction"] +
        data["international"] * 2 +
        (data["failed_attempts"] >= 3).astype(int) * 2
    )

    data["fraud"] = (risk >= 5).astype(int)

    X = data.drop("fraud", axis=1)
    y = data["fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("FraudShield AI Model Training Complete")
    print("Model Accuracy:", round(accuracy * 100, 2), "%")

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    joblib.dump(model, "fraud_model.pkl")

    print("FraudShield AI model saved successfully!")

    return model


if __name__ == "__main__":
    model = train_fraud_model()
```
