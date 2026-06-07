import json
from pathlib import Path
import argparse
from datetime import datetime, date
import csv

parser = argparse.ArgumentParser()

parser.add_argument("filePath", type=str)
parser.add_argument("level", type=str, nargs='?', default=None)
parser.add_argument("--from-date", dest="from_value", type=lambda d: datetime.strptime(d, "%Y-%m-%d %H:%M:%S"))
parser.add_argument("--to", type=lambda d: datetime.strptime(d, "%Y-%m-%d %H:%M:%S"))
parser.add_argument("--export", type=str)

args = parser.parse_args()

path = Path(args.filePath)


if not path.exists():
    print("Please enter a valid file")
else:
    with path.open("r") as file:
        total = 0
        errors = 0
        warnings = 0
        info = 0
        arr = {}
        failure_timestamps = []

        for line in file:
            line = line.strip()
            # total += 1
            if line.startswith("{"):
                log_data = json.loads(line)
                timestamp = log_data["timestamp"]
                dateTime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                message = log_data["message"]
                level = log_data["level"].upper()
            else:
                log_data = line.split(" ", 3)
                if len(log_data) < 4:
                    print(f"Skipping poorly formatted line: {line}")
                    continue
                timestamp = f"{log_data[0]} {log_data[1]}"
                dateTime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                message = log_data[3]
                level = log_data[2].upper()


            if args.from_value and dateTime < args.from_value:
                continue

            if args.to and dateTime > args.to:
                continue

            if args.level and level != args.level.upper():
                continue

            total += 1

            match level:
                case "ERROR":
                    errors += 1
                    failure_timestamps.append(timestamp)
                    if message in arr:
                        arr[message] += 1
                    else:
                        arr[message] = 1
                case "WARNING":
                    warnings+=1
                case "INFO":
                    info+=1

        if arr:
            max_key = max(arr, key=arr.get)
            print(f"most_common_error, {max_key}")
        else:
            print("No messages found matching the criteria.")

        print(f"total logs {total}")
        print(f"errors: {errors}")
        print(f"warnings: {warnings}")
        print(f"info: {info}")

        if args.export:
            most_common = max_key if arr else "N/A"
            
            try:
                with open(args.export, mode="w", newline="", encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    
                    writer.writerow(["metric", "value"])
                    
                    writer.writerow(["total_logs", total])
                    writer.writerow(["errors", errors])
                    writer.writerow(["warnings", warnings])
                    writer.writerow(["info", info])
                    writer.writerow(["most_common_error", most_common])
                    
                print(f"Summary successfully exported to {args.export}")
            except Exception as e:
                print(f"Error exporting CSV: {e}")