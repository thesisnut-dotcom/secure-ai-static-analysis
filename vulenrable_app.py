import subprocess
iport hashlib

password = input("Enter password: ")

hashed = hashlib.md5(password.encode()).hexdigest()

filename = input("Enter filename: ")
subprocess.call("cat " + filename, shell=True)

print("Passoword hash:", hashed) 
