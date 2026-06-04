import os
import subprocess

# all = os.listdir()

# for item in all:
#     if item.endswith(".log") or item.endswith(".tmp"):
#         os.remove(item)

website = input ("What is the website: ")
output = subprocess.run(["ping", "-c",  "3", website])

if output.returncode == 0:
    print("sucess!")
else:
    print("Error!")