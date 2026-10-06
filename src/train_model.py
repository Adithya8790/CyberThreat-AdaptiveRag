import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


# --------------------------------
# 1. Load dataset
# --------------------------------

DATA_PATH = "data/processed/training_data.csv"

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# --------------------------------
# 2. Clean column names
# --------------------------------

df.columns = df.columns.str.strip()


# --------------------------------
# 3. Separate features and labels
# --------------------------------

X = df.drop(columns=["Label"])
y = df["Label"]


# --------------------------------
# 4. Convert feature values to numeric
# --------------------------------

X = X.apply(pd.to_numeric, errors="coerce")

# Replace infinity values
X = X.replace([float("inf"), float("-inf")], float("nan"))

# Replace missing values with 0
X = X.fillna(0)


# --------------------------------
# 5. Train/Test split
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------
# 6. Train Random Forest
# --------------------------------

print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# --------------------------------
# 7. Predictions
# --------------------------------

print("\nTesting model...")

y_pred = model.predict(X_test)


# --------------------------------
# 8. Evaluation
# --------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL RESULTS")
print("==============================")

print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# --------------------------------
# 9. Save model
# --------------------------------

model_path = "models/random_forest_ids.joblib"

joblib.dump(model, model_path)

print("\nModel saved to:")
print(model_path)