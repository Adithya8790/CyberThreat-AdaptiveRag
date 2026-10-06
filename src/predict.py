# import pandas as pd
# import joblib

# # -----------------------------
# # Load model
# # -----------------------------

# MODEL_PATH = "models/random_forest_ids.joblib"
# DATA_PATH = "data/processed/training_data.csv"

# model = joblib.load(MODEL_PATH)

# print("Model loaded successfully.")


# # -----------------------------
# # Load test data
# # -----------------------------

# df = pd.read_csv(DATA_PATH)

# df.columns = df.columns.str.strip()

# X = df.drop(columns=["Label"])
# y = df["Label"]

# X = X.apply(pd.to_numeric, errors="coerce")

# X = X.replace(
#     [float("inf"), float("-inf")],
#     float("nan")
# )

# X = X.fillna(0)


# # -----------------------------
# # Select one network flow
# # -----------------------------

# # sample = X.iloc[[0]]

# # actual_label = y.iloc[0]

# # Choose an attack for demonstration
# attack_type = "PortScan"

# attack_indices = y[y == attack_type].index

# sample_index = attack_indices[0]

# sample = X.loc[[sample_index]]

# actual_label = y.loc[sample_index]


# # -----------------------------
# # Predict
# # -----------------------------

# prediction = model.predict(sample)[0]

# probabilities = model.predict_proba(sample)[0]

# confidence = probabilities.max() * 100


# # -----------------------------
# # Generate alert
# # -----------------------------

# print("\n==============================")
# print("        IDS ALERT")
# print("==============================")

# print("Actual Label    :", actual_label)
# print("Predicted Label :", prediction)
# print(f"Confidence      : {confidence:.2f}%")

# if prediction == "BENIGN":
#     print("Status          : NORMAL")
# else:
#     print("Status          : SUSPICIOUS")

#     print("\nThreat detected!")
#     print("Attack Type     :", prediction)













# import pandas as pd
# import joblib

# # -----------------------------
# # Load model
# # -----------------------------

# MODEL_PATH = "models/random_forest_ids.joblib"
# DATA_PATH = "data/processed/training_data.csv"

# model = joblib.load(MODEL_PATH)

# print("Model loaded successfully.")


# # -----------------------------
# # Load dataset
# # -----------------------------

# df = pd.read_csv(DATA_PATH)
# df.columns = df.columns.str.strip()

# X = df.drop(columns=["Label"])
# y = df["Label"]

# X = X.apply(pd.to_numeric, errors="coerce")

# X = X.replace(
#     [float("inf"), float("-inf")],
#     float("nan")
# )

# X = X.fillna(0)


# # -----------------------------
# # User selection
# # -----------------------------

# print("\nSelect traffic to test:")

# print("1. BENIGN")
# print("2. DDoS")
# print("3. DoS Hulk")
# print("4. PortScan")

# choice = input("\nEnter choice: ")


# # Map user choice to dataset label
# label_map = {
#     "1": "BENIGN",
#     "2": "DDoS",
#     "3": "DoS Hulk",
#     "4": "PortScan"
# }

# if choice not in label_map:
#     print("Invalid choice.")
#     exit()

# selected_label = label_map[choice]


# # -----------------------------
# # Select a sample
# # -----------------------------

# indices = y[y == selected_label].index

# sample_index = indices[0]

# sample = X.loc[[sample_index]]

# actual_label = y.loc[sample_index]


# # -----------------------------
# # Prediction
# # -----------------------------

# prediction = model.predict(sample)[0]

# probabilities = model.predict_proba(sample)[0]

# confidence = probabilities.max() * 100


# # -----------------------------
# # Generate alert
# # -----------------------------

# print("\n==============================")
# print("        IDS ALERT")
# print("==============================")

# print("Actual Label    :", actual_label)
# print("Predicted Label :", prediction)
# print(f"Confidence      : {confidence:.2f}%")


# if prediction == "BENIGN":

#     print("Status          : NORMAL")

# else:

#     print("Status          : SUSPICIOUS")

    # print("\nThreat detected!")
    # print("Attack Type     :", prediction)


import pandas as pd
import joblib
from neo4j import GraphDatabase

# ==============================
# CONFIGURATION
# ==============================

MODEL_PATH = "models/random_forest_ids.joblib"
DATA_PATH = "data/processed/training_data.csv"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "CyberThreatKG"


# ==============================
# LOAD ML MODEL
# ==============================

model = joblib.load(MODEL_PATH)
print("Model loaded successfully.")

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()

X = df.drop(columns=["Label"])
y = df["Label"]

X = X.apply(pd.to_numeric, errors="coerce")
X = X.replace([float("inf"), float("-inf")], float("nan"))
X = X.fillna(0)


# ==============================
# NEO4J CONNECTION
# ==============================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)


def get_attack_context(tx, attack_name):

    query = """
    MATCH (a:Attack {name: $attack_name})
          -[:MAPS_TO]->
          (t:Technique)

    OPTIONAL MATCH (t)-[:BELONGS_TO]->(tactic:Tactic)

    RETURN a.name AS attack,
           t.id AS technique_id,
           t.name AS technique,
           tactic.name AS tactic
    """

    result = tx.run(query, attack_name=attack_name)

    return [record.data() for record in result]


# ==============================
# SELECT TRAFFIC
# ==============================

print("\nSelect traffic to test:")
print("1. BENIGN")
print("2. DDoS")
print("3. DoS Hulk")
print("4. PortScan")

choice = input("\nEnter choice: ")

label_map = {
    "1": "BENIGN",
    "2": "DDoS",
    "3": "DoS Hulk",
    "4": "PortScan"
}

if choice not in label_map:
    print("Invalid choice.")
    driver.close()
    exit()

selected_label = label_map[choice]

indices = y[y == selected_label].index

sample_index = indices[0]

sample = X.loc[[sample_index]]

actual_label = y.loc[sample_index]


# ==============================
# ML PREDICTION
# ==============================

prediction = model.predict(sample)[0]

probabilities = model.predict_proba(sample)[0]

confidence = probabilities.max() * 100


print("\n==============================")
print("          IDS ALERT")
print("==============================")

print("Actual Label    :", actual_label)
print("Predicted Label :", prediction)
print(f"Confidence      : {confidence:.2f}%")


if prediction == "BENIGN":

    print("Status          : NORMAL")

else:

    print("Status          : SUSPICIOUS")

    print("\nThreat detected!")
    print("Attack Type     :", prediction)

    # ==============================
    # QUERY KNOWLEDGE GRAPH
    # ==============================

    print("\nRetrieving threat context from Neo4j...")

    with driver.session() as session:

        results = session.execute_read(
            get_attack_context,
            prediction
        )

    if results:

        print("\n==============================")
        print("      KNOWLEDGE GRAPH CONTEXT")
        print("==============================")

        for result in results:

            print("Attack       :", result["attack"])
            print("Technique ID :", result["technique_id"])
            print("Technique    :", result["technique"])
            print("Tactic       :", result["tactic"])

    else:

        print("\nNo threat context found in Knowledge Graph.")


# ==============================
# CLOSE CONNECTION
# ==============================

driver.close()