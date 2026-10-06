import pandas as pd
from pathlib import Path

data_folder = Path("data/CIC-IDS2017")

csv_files = list(data_folder.glob("*.csv"))

for file in csv_files:
    print("\n" + "=" * 70)
    print("FILE:", file.name)

    df = pd.read_csv(file)

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    print("\nLabels found:")

    print(df["Label"].value_counts())











































































































































# import pandas as pd
# from pathlib import Path

# data_folder = Path("data/CIC-IDS2017")

# csv_files = list(data_folder.glob("*.csv"))

# for file in csv_files:
#     print("\n" + "=" * 70)
#     print("FILE:", file.name)

#     # Read only the first row/header
#     df = pd.read_csv(file, nrows=1)

#     print("\nLAST 10 COLUMN NAMES:")
#     print(df.columns.tolist()[-10:])