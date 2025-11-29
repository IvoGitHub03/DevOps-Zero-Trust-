import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def read_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r") as f:
        return json.load(f)

def write_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
