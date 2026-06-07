import argparse
import json
from pathlib import Path

with open("health_checker.log", "r") as file:
    file_contents = file.read()
    content = json.loads(file_contents)
    print(type(content.get("servers")))