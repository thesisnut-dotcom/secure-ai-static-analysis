import subprocess
import hashlib

# VULNERABILITY 1: Weak MD5 hashing
password = input("Enter password: ")
hashed = hashlib.md5(password.encode()).hexdigest()

# VULNERABILITY 2: Command Injection via shell=True
filename = input("Enter filename to view: ")
subprocess.call("cat " + filename, shell=True)

print("Hash:", hashed)
