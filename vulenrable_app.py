import subprocess
iport os

# 1. Define the path to your uploaded dataset
data_file =  "data set.doc"

if os.path.exists(data_file):
# 2. Load the data
df = pd.read_doc(data_file)

# 3. Perform basic statistical analysis
print("--- Dataset Summary ---")
print(df.head()) # Shows the first 5 rows

print("\n--- Statistics ---")
print(df.describe()) # Shows mean, count, std dev, etc.

else:
print(f"Error: The file '{data_file}' was not found in the repository.")
