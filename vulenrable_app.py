import pickle
import os
import subprocess
import hashlib
import pandas as pd

# --- SECTION 1: AI SECURITY DEMO (Your current logic) ---
class MaliciousModel:
def __reduce__(self):
return (os.system, ('echo "Vulnerable"',))

with open('model.pkl', 'wb') as f:
pickle.dump(MaliciousModel(), f)

# VULNERABILITY 1: Insecure Deserialization (Pickle)
# Bandit/Semgrep WILL catch this.
with open('model.pkl', 'rb') as f:
model = pickle.load(f)

# --- SECTION 2: CLASSIC WEB/SYSTEM VULNERABILITIES ---
# Adding these ensures your "Security Pipeline" requirements are met!

# VULNERABILITY 2: Weak Cryptography (MD5)
# Bandit flags this as a High Severity risk.
password = "admin_password"
print("Hash:", hashlib.md5(password.encode()).hexdigest())

# VULNERABILITY 3: Command Injection (shell=True)
# Semgrep and Bandit both flag this.
user_input = "data.csv"
subprocess.call("ls " + user_input, shell=True)

# --- SECTION 3: DATA ANALYSIS ---
df = pd.read_csv("data.csv")
print(df.describe())
