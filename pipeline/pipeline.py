import sys
import pandas as pd

print("arguments", sys.argv)

day = int(sys.argv[1])

print(f"Running pipeline for day {day}")

df = pd.DataFrame({"Name": ['Lemuel', 'Azarel'], "Age":[20, 10]})
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")