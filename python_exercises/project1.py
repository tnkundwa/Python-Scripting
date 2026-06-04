import json
from pathlib import Path
import argparse
from datetime import datetime, date

filePath = input("Enter the file path please: ")
path = Path(filePath)


if not path.exists():
    print("Please enter a valid file")
else:
    with path.open("r") as file:
        total = 0
        errors = 0
        warnings = 0
        info = 0
        arr = {}
        for line in file:
            line = line.strip()
            total += 1
            if line.startswith("{"):
                log_data = json.loads(line)
                timestamp = log_data["timestamp"]
                message = log_data["message"]
                level = log_data["level"]
            else:
                log_data = line.split(" ", 3)
                timestamp = f"{log_data[0]} {log_data[1]}"
                message = log_data[3]
                level = log_data[2]

            match level:
                case "ERROR":
                    errors+=1
                case "WARNING":
                    warnings+=1
                case "INFO":
                    info+=1
            
            if message in arr:
                arr[message] += 1
            else:
                arr[message] = 1

        max_key = max(arr, key=arr.get)

        print(f"total logs {total}")
        print(f"errors: {errors}")
        print(f"warnings: {warnings}")
        print(f"info: {info}")
        print(f"most_common_error, {max_key}")