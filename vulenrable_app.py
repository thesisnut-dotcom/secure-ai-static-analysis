import pandas as pd
import os

# 1. Define the path to your uploaded dataset
data_file = "_55b0420cd5644c0cbe89a84bf91f3c8b_demo_code_1.txt"

if os.path.exists(data_file):
# 2. Load the data
df = pd.read_txt(data_file)

# 3. Perform basic statistical analysis
print("--- Dataset Summary ---")
print(df.head()) # Shows the first 5 rows

print("\n--- Statistics ---")
print(df.describe()) # Shows mean, count, std dev, etc.

else:
print(f"Error: The file '{data_file}' was not found in the repository.")

