import json
from pathlib import Path

# filePath = input("Enter the file path please: ")
path = Path("./test.log")


if not path.exists():
    print("Please enter a valid file")
else:
    with path.open("r") as file:
        count = 0
        for line in file:
            if not line.startswith("{"):
                log_data = json.loads(line)
                # timestamp = log_data["timestamp"]
                # level = log_data["level"]
                # message = log_data["message"]
                # print(f"[{timestamp}] {level.upper()}: {message}")
                print(log_data)           
