import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/CIC-IDS2017")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLES_PER_CLASS = 10000

# Files we need
files = {
    "DDoS": "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
    "PortScan": "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "DoS Hulk": "Wednesday-workingHours.pcap_ISCX.csv",
}

dataframes = []

# -----------------------------
# DDoS
# -----------------------------
file = DATA_DIR / files["DDoS"]

print("Loading DDoS...")
df = pd.read_csv(file)
df.columns = df.columns.str.strip()

ddos = df[df["Label"] == "DDoS"].sample(
    n=SAMPLES_PER_CLASS,
    random_state=42
)

dataframes.append(ddos)

# -----------------------------
# PortScan
# -----------------------------
file = DATA_DIR / files["PortScan"]

print("Loading PortScan...")
df = pd.read_csv(file)
df.columns = df.columns.str.strip()

portscan = df[df["Label"] == "PortScan"].sample(
    n=SAMPLES_PER_CLASS,
    random_state=42
)

dataframes.append(portscan)

# -----------------------------
# DoS Hulk
# -----------------------------
file = DATA_DIR / files["DoS Hulk"]

print("Loading DoS Hulk...")
df = pd.read_csv(file)
df.columns = df.columns.str.strip()

dos_hulk = df[df["Label"] == "DoS Hulk"].sample(
    n=SAMPLES_PER_CLASS,
    random_state=42
)

dataframes.append(dos_hulk)

# -----------------------------
# BENIGN
# -----------------------------
print("Loading BENIGN samples...")

benign_sources = [
    DATA_DIR / files["DDoS"],
    DATA_DIR / files["PortScan"],
    DATA_DIR / "Monday-WorkingHours.pcap_ISCX.csv",
]

benign_parts = []

for file in benign_sources:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    benign = df[df["Label"] == "BENIGN"]

    benign_parts.append(benign)

benign_df = pd.concat(benign_parts, ignore_index=True)

benign = benign_df.sample(
    n=SAMPLES_PER_CLASS,
    random_state=42
)

dataframes.append(benign)

# -----------------------------
# Combine
# -----------------------------
final_df = pd.concat(dataframes, ignore_index=True)

# Shuffle
final_df = final_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

output_file = OUTPUT_DIR / "training_data.csv"

final_df.to_csv(output_file, index=False)

print("\nDataset created successfully!")
print("Output:", output_file)
print("Shape:", final_df.shape)

print("\nClass distribution:")
print(final_df["Label"].value_counts())